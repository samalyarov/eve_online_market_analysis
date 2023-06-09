# EVE API parser
Directory containing the EVE API parser scrips. Additional info on EVE market API calls can be found [here](https://wiki.eveuniversity.org/API_access_to_market_data).

| File | Description | Libraries and tools used |
| :--------------------: | :---------------------: |:---------------------------:|
| [1.Database creation](https://github.com/samalyarov/eve_online_market_analysis/tree/main/postgresql_db)| Stage 1 includes creating a database (developing a proper schema, creating tables and setting up connections in order to fill it an export data later on. I've used a Docker Container in order to host the database and sqlalchemy + DBeaver to set it up and edit. | *postgresql, dbeaver, sqlalchemy, docker* |
