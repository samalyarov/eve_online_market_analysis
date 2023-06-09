# Eve Online Market analysis
Repository currently WIP. The status of the project is reflected in this README file and will be updated as the analysis progresses

| Stage | Description | Libraries and tools used |
| :--------------------: | :---------------------: |:---------------------------:|
| [1.Database creation](https://github.com/samalyarov/eve_online_market_analysis/blob/main/postgresql_db/readme.md)| Stage 1 includes creating a database (developing a proper schema, creating tables and setting up connections in order to fill it an export data later on. I've used a Docker Container in order to host the database and sqlalchemy + DBeaver to set it up and edit. | *postgresql, dbeaver, sqlalchemy, docker* |
| [2.API parsing tool](link_here) | Stage 2 includes creating a Python script to constantly parse the official Eve API for market data. Since analysis requires data from several different systems, alongside API limits of 200 items per request the task is done asynchronously. Automation is done via the Windows Task Scheduler and the results are offloaded every hour into a local PostgreSQLdatabase | *pandas, configparser, asyncio, aiohttp, warnings, datetime, tqdm, sqlalchemy* |
