# EVE API parser
Directory containing the EVE API parser scrips. Additional info on EVE market API calls can be found [here](https://wiki.eveuniversity.org/API_access_to_market_data).

**File 1: [*eve_async_market_scraper.py*](https://github.com/samalyarov/eve_online_market_analysis/blob/main/api_parser/eve_async_market_scraper.py).**
- The current version of the script. Locally automated with the use of Windows Task Scheduler to run every hour, a good alternative for easy use would be a remote machine with crontab.
- Script uses the aiohttp library (similar to requests but allows for interaction with asyncio and asynchronous programming in general. 
- SwaggerAPI only allows for 200 items per request, so the whole list (~45 thousand items) is divided into lists 200 items each to be used in API calls (1 such list per call). This is also a part of asynchronous process and is executed for all trade hubs at once. 
- The script connects to a local database using sqlalchemy (can be switched to connect to external one by changing key parameters in db_config.ini), gets market data for 6 key in-game trading hubs through API calls. These market calls are done asynchronously (all 6 at the same time)
- Such design allows for easy scaling (the only limiting factor is the DB size), but the requirements of current research are adequately met with analysing 6 main trade hubs (as smaller ones are likely to turn less of a profit per hour spent working at them due to smaller scale of operations).

Libraries used: *pandas, configparser, asyncio, aiohttp, warnings, datetime, tqdm, sqlalchemy* |

**File 2: [*eve_market_scraper.py*](https://github.com/samalyarov/eve_online_market_analysis/blob/main/api_parser/eve_market_scraper.py).**
- Non-asynchronous version of the script that uses the requests library to achieve similar results within a simple loop (for each system => for each 200 item ids). However, that variation is significantly slower, as only one system is processed at a time.
- First version of the script developed, as analysis was initially planned to be limited to a single system (Jita, game main trade hub). 
- Conducted EDA confirmed profitability of inter-hub trading, which required comparative analysis of different markets within eve. As a result, that version of the script was created, but a simple loop architecture made the time needed for the script to complete increase linearly with each new system, which proved to be detrimental even with 6 hubs - not to mention potential expansion opportunities.
- The script uses *requests* library to make API calls.

Libraries used: *pandas, configparser, requests, datetime, tqdm, sqlalchemy* |

**File 3: [*db_config.ini*](https://github.com/samalyarov/eve_online_market_analysis/blob/main/api_parser/db_config.ini).**
- A simple config file for storing connection data. Easy to change.
