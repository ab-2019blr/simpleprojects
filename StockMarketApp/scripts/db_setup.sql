-- Initial DB Setup & Data Loading Script for Stock Market App
-- To be run in MySQL environment
-- mysql -u username -p
-- source path/to/db_setup.sql;
-- Or use a MySQL client to execute
-- mysql -u username -p < /full/path/to/project_root/scripts/db_setup.sql
-- Create database if not exists
CREATE DATABASE IF NOT EXISTS stock_market_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE stock_market_db;

-- Create tables
CREATE TABLE IF NOT EXISTS bank_nifty_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    series VARCHAR(10) NOT NULL,
    trade_date DATE NOT NULL,
    prev_close FLOAT,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    last_price FLOAT,
    close_price FLOAT,
    average_price FLOAT,
    total_traded_quantity BIGINT,
    turnover_in_rs DOUBLE,
    number_of_trades INT,
    deliverable_qty BIGINT,
    percent_dly_qty_to_traded FLOAT,
    UNIQUE KEY unique_symbol_date (symbol, trade_date)
);

-- Insert startup data (example)
INSERT INTO bank_nifty_data (symbol, series, trade_date, prev_close) VALUES
('CANBK', 'EQ', '2025-09-12', 112.07),
('PNB', 'EQ', '2025-09-12', 107.76);
