CREATE TABLE buy_orders (
	record_id SERIAL PRIMARY KEY,
	record_date TIMESTAMP,
	item_id INT,
	item_region INT,
	item_system INT,
	min_quantity INT,
	volume INT,
	p_weighted_average FLOAT,
	p_average FLOAT,
	p_variance FLOAT,
	p_stddev FLOAT,
	p_median FLOAT,
	p_fivepercent FLOAT,
	p_max FLOAT,
	p_min FLOAT,
	);
