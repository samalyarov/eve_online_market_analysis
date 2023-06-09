# EVE API parser
Directory containing the EVE API parser scrips. Additional info on EVE market API calls can be found [here](https://wiki.eveuniversity.org/API_access_to_market_data).

**File 1: [*eve_async_market_scraper.py*](https://github.com/samalyarov/eve_online_market_analysis/blob/main/api_parser/eve_async_market_scraper.py).**
- The current version of the script automated with the use of Windows Task Scheduler to run every hour. 
- Script uses the aiohttp library (similar to requests but allows for interaction with asyncio and asynchronous programming in general. 
- The script connects to a local database using sqlalchemy (can be switched to connect to external one by changing key parameters in db_config.ini), gets market data for 6 key in-game trading hubs through API calls. These market calls are done asynchronously (all 6 at the same time)
- EVE online only allows for 200 items per request, so the whole list (~45 thousand items) is divided into lists 200 items each to be used in API calls (1 such list per call). This is also a part of asynchronous process and is executed for all trade hubs at once. 
- Such design allows for near infinite scaling (the only limiting factor is the DB size), but the requirements of current research are adequately met with analysing 6 main trade hubs (as smaller ones are likely to turn less of a profit per hour spent working at them due to smaller scale of operations).

Libraries used: *pandas, configparser, asyncio, aiohttp, warnings, datetime, tqdm, sqlalchemy* |
