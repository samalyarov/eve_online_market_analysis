# EVE API parser
Directory containing the EVE API parser scrips. Additional info on EVE market API calls can be found [here](https://wiki.eveuniversity.org/API_access_to_market_data).

| File | Description | Libraries and tools used |
| :--------------------: | :---------------------: |:---------------------------:|
| [1.eve_async_market_scraper.py](https://github.com/samalyarov/eve_online_market_analysis/tree/main/postgresql_db)| The current version of the script automated with the use of Windows Task Scheduler to run every hour. Script uses the aiohttp library (similar to requests but allows for interaction with asyncio and asynchronous programming in general. 

The script connects to a local database using sqlalchemy (can be switched to connect to external one by changing key parameters in db_config.ini), gets market data for 6 key in-game trading hubs through API calls. 

EVE online only allows for 200 items per request, so the whole list (~45 thousand items) is divided into lists 200 items each to be used in API calls (1 such list per call) | *postgresql, dbeaver, sqlalchemy, docker* |
