print('Parsing script initiated!')

# Importing libraries
import pandas as pd
import configparser
import asyncio
import aiohttp
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

from datetime import datetime
from tqdm.asyncio import tqdm
from sqlalchemy import create_engine 
print('Library import complete')

# Setting up the database connection
## Reading the config file with connection data
config = configparser.ConfigParser()
config.read("db_config.ini")

## Credentials for DB connection:
user_name = config['Database']['user_name']
password = config['Database']['password']

## Connection settings
db_host = config['Database']['host']
db_port = config['Database']['port']
db_name = config['Database']['database']

## Starting connection
connection_string = f'postgresql://{user_name}:{password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_string)
print('Database connection established')

# Acquiring data
## Reading the file with ID types:
ids = pd.read_excel('typeids.xlsx')['object_id']

# Get current time
current_time = datetime.now().replace(second=0, microsecond=0)
current_time = current_time.strftime("%d/%m/%Y, %H:%M:%S")

# Identifying systems for data collection (rolling with 5 biggest trade hubs in the game):
systems = {30000142: 'Jita', #Jita IV - Moon 4 - Caldari Navy Assembly Plant (Caldari)
           30002187: 'Amarr', # Amarr VIII (Oris) - Emperor Family Academy (Amarr)
           30002510: 'Rens', # Rens VI - Moon 8 - Brutor Tribe Treasury (Minmatar)
           30002659: 'Dodixie', # Dodixie IX - Moon 20 - Federation Navy Assembly Plant (Gallente)
           30002053: 'Hek', # Hek VIII - Moon 12 - Boundless Creation Factory (Minmatar #2)
           30000144: 'Perimeter' # Tranquility Trading Tower
           }

async def gather_data(session, link):
    async with session.get(link) as response:
        return await response.json()

async def main(system):
    '''
    A function for getting all the data on the system market from EVE API.
    Built for concurrent API calls to get data on all the systems at once (much faster, but more taxing on CPU)
    '''

    async with aiohttp.ClientSession() as session:
        # Create a DataFrame to house the data:
        data = pd.DataFrame(columns=['buy.forQuery.bid', 
                                    'buy.forQuery.types', 
                                    'buy.forQuery.regions',
                                    'buy.forQuery.systems', 
                                    'buy.forQuery.hours', 
                                    'buy.forQuery.minq',
                                    'buy.volume', 
                                    'buy.wavg', 
                                    'buy.avg', 
                                    'buy.variance', 
                                    'buy.stdDev',
                                    'buy.median', 
                                    'buy.fivePercent', 
                                    'buy.max', 
                                    'buy.min', 
                                    'buy.highToLow',
                                    'buy.generated'
                                    'sell.forQuery.bid', 
                                    'sell.forQuery.types',
                                    'sell.forQuery.regions', 
                                    'sell.forQuery.systems', 
                                    'sell.forQuery.hours',
                                    'sell.forQuery.minq', 
                                    'sell.volume', 
                                    'sell.wavg', 
                                    'sell.avg',
                                    'sell.variance', 
                                    'sell.stdDev', 
                                    'sell.median', 
                                    'sell.fivePercent',
                                    'sell.max', 
                                    'sell.min', 
                                    'sell.highToLow'
                                    'sell.generated'
                                    ]
                                    )
                                    
        # Getting 200 IDs at once (current EVE API limit)
        for i in tqdm(range(0, len(ids) + 1, 200), desc=f'Loading {systems[system]} data:'):
            # Create an empty API call string
            ids_string = ''

            # Get a list of IDs to call
            ids_to_analyze = ids[i:i+200]

            # Add IDs to string for an API call
            for k in ids_to_analyze:
                ids_string = ids_string + f',{k}'
                
            ids_string = ids_string[1:] # Remove the first comma

            link = f'https://api.evemarketer.com/ec/marketstat/json?typeid={ids_string}&usesystem={system}'

            # Acquire data
            curr_market_data = await gather_data(session, link)
            curr_market_data = pd.json_normalize(curr_market_data)

            # Append the data to the dataframe:
            data = pd.concat([data, curr_market_data])

        # Transforming the DataFrame:
        ## Deleting the unnecessary columns
        data = data.drop(columns=['buy.forQuery.bid',
                                'buy.forQuery.hours',
                                'buy.forQuery.minq',
                                'buy.highToLow',
                                'buy.generated'
                                'sell.forQuery.bid',
                                'sell.forQuery.hours',
                                'sell.forQuery.minq',
                                'sell.highToLow'
                                'sell.generated'
                                ])

        # Editing the columns with lists instead of values:
        lists_to_ints = ['buy.forQuery.types',
                        'buy.forQuery.regions',
                        'buy.forQuery.systems',
                        'sell.forQuery.types',
                        'sell.forQuery.regions',
                        'sell.forQuery.systems'
                        ]

        # Since the lists are all 1 element long - just take the first one
        for column in lists_to_ints:
            try:
                data[column] = data[column].apply(lambda x: x[0])
            except Exception:
                pass # To still allow various interrupts

        # Converting the 'volume' columns to integers:
        strings_to_ints = ['buy.volume',
                        'sell.volume',
                        ]

        for column in strings_to_ints:
            try:
                data[column] = data[column].astype(int)
            except Exception:
                pass # To still allow various interrupts

        # Changing the column types:
        data['buy.volume'] = data['buy.volume'].astype('int64')
        data['sell.volume'] = data['sell.volume'].astype('int64')

        # Insert timestamp as a separate column:
        data['timestamp'] = current_time

        # Only get records with volume (and thus, with data in them)
        data = data[(data['buy.volume'] != 0) | (data['sell.volume'] !=0)] # Using "OR" operator - as certain items may have one type of orders (buy or sell) but not the other

        # Getting two dataframes for tables:
        tables_columns=['record_date',
                        'item_id',
                        'item_region',
                        'item_system',
                        'volume',
                        'p_weighted_average',
                        'p_average',
                        'p_variance',
                        'p_stddev',
                        'p_median',
                        'p_fivepercent',
                        'p_max',
                        'p_min'
                        ]

        buy_orders = data[['timestamp', 
                        'buy.forQuery.types', 
                        'buy.forQuery.regions', 
                        'buy.forQuery.systems', 
                        'buy.volume',
                        'buy.wavg',
                        'buy.avg',
                        'buy.variance',
                        'buy.stdDev',
                        'buy.median',
                        'buy.fivePercent',
                        'buy.max',
                        'buy.min'
                        ]]

        sell_orders = data[['timestamp', 
                        'sell.forQuery.types', 
                        'sell.forQuery.regions', 
                        'sell.forQuery.systems', 
                        'sell.volume',
                        'sell.wavg',
                        'sell.avg',
                        'sell.variance',
                        'sell.stdDev',
                        'sell.median',
                        'sell.fivePercent',
                        'sell.max',
                        'sell.min'
                        ]]

        # Setting the columns (not necessary, but handy for testing|bugfixes)
        buy_orders.columns = tables_columns
        sell_orders.columns = tables_columns

        # Uploading data
        buy_orders.to_sql('buy_orders',
                        engine.connect(),
                        if_exists='append',
                        index=False,
                        )

        sell_orders.to_sql('sell_orders',
                        engine.connect(),
                        if_exists='append',
                        index=False,
                        )

# Executing the asyncio script
loop = asyncio.get_event_loop()
tasks = []
for system_id in systems.keys():
    tasks.append(loop.create_task(main(system_id)))

loop.run_until_complete(asyncio.wait(tasks))

print('Data parsing and upload complete!')
