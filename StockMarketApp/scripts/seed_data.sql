-- Use MySQL LOAD DATA INFILE Command to load CSV data into the table
-- Ensure the CSV file is accessible by the MySQL server
-- Adjust the file path as necessary
LOAD DATA INFILE '/full/path/to/project_root/scripts/nifty_bank_bulk_data.csv'
INTO TABLE bank_nifty_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS -- Skip header row
(symbol, series, trade_date, prev_close, open_price, high_price, low_price, last_price, close_price, average_price, total_traded_quantity, turnover_in_rs, number_of_trades, deliverable_qty, percent_dly_qty_to_traded);   
-- Note: Ensure the MySQL server has permission to read the file at the specified path.