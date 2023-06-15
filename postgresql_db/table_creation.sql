CREATE TABLE sell_orders (
	record_id SERIAL PRIMARY KEY,
	record_date TIMESTAMP,
	item_id INT8,
	item_region INT8,
	item_system INT8,
	min_quantity INT8,
	volume INT8,
	p_weighted_average FLOAT,
	p_average FLOAT,
	p_variance FLOAT,
	p_stddev FLOAT,
	p_median FLOAT,
	p_fivepercent FLOAT,
	p_max FLOAT,
	p_min FLOAT
	);
