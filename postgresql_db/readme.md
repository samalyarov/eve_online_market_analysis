# PostgreSQL Database
Stage 1 includes creating a database (developing a proper schema, creating tables and setting up connections in order to fill it an export data later on. I've used a Docker Container in order to host the database and sqlalchemy + DBeaver to set it up and edit.

Database features a simple schema:

![image](https://github.com/samalyarov/eve_online_market_analysis/assets/107198574/e75d24d8-3996-4db7-b8f0-5989d0f8b1a3)

Data collected is divided into two core categories - buy and sale orders (representative of both Eve and real world stock market). These are to be analyzed separately.

**Table 1: 'item_ids'. Columns:**
- *PRIMARY KEY + FOREIGN KEY* item_id (int8): item_id in eve online database. Used for making API calls and decreasing the DB complexity (to write ids instead of names in other tables). 
- item_name (varchar): item name in game (as shown to players). Useful to understand what item are we talking about and to display in graphs|analysis.
- 
Directory also contains a 'typeids.csv' file loaded from Fuzzworks containings names and ids of all entities in the game. Useful for creating the type IDs table in the DB. Item source: https://www.fuzzwork.co.uk/resources/typeids.csv


**Table 2: buy_orders'. Columns:**
- *PRIMARY KEY* record_id (serial4): iterable primary key creating upon entering a row into database.
- *FOREIGN KEY* item_id (int8): item_id in eve online database
- item_region (int8): region of the entry (game world is divided into different regions)
- item_system (int8): system of the entry (game world is divided into different systems). I am analysing 5 of those systems (key trade hubs).
- volume (int8): amount of items in buy orders on the market
- p_weighted_average (float8): weighted average purchase price per item
- p_average (float8): average purchase price per item
- p_variance (float8): item price variance
- p_stddev (float8): item price standard deviation
- p_median (float8): item median price per item 
- p_fivepercent (float8): average price per unit among top 5% (by price) buy orders
- p_max (float8): maximum purchase price per unit
- p_min (float8): minimum purchase price per unit

**Table 3: sell_orders'. Columns:**
- *PRIMARY KEY* record_id (serial4): iterable primary key creating upon entering a row into database.
- *FOREIGN KEY* item_id (int8): item_id in eve online database
- item_region (int8): region of the entry (game world is divided into different regions)
- item_system (int8): system of the entry (game world is divided into different systems). I am analysing 5 of those systems (key trade hubs).
- volume (int8): amount of items in sell orders on the market
- p_weighted_average (float8): weighted average sell price per item
- p_average (float8): average sell price per item
- p_variance (float8): item price variance
- p_stddev (float8): item price standard deviation
- p_median (float8): item median price per item 
- p_fivepercent (float8): average price per unit among bottom 5% (by price) sell orders
- p_max (float8): maximum selling price per unit
- p_min (float8): minimum selling price per unit
