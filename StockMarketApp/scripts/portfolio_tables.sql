-- This script creates the portfolio_transactions table if it doesn't exist
-- ================================================
-- Portfolio Tables Setup Script
-- ================================================

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS stock_market_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE stock_market_db;

-- Drop existing tables (optional - only if you want to start fresh)
-- DROP TABLE IF EXISTS transactions;
-- DROP TABLE IF EXISTS current_prices;

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INT NOT NULL AUTO_INCREMENT,
    stock_symbol VARCHAR(20) NOT NULL,
    stock_name VARCHAR(100) NOT NULL,
    transaction_date DATE NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    transaction_type ENUM('BUY', 'SELL') DEFAULT 'BUY',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_stock_symbol (stock_symbol),
    INDEX idx_transaction_date (transaction_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create current_prices table
CREATE TABLE IF NOT EXISTS current_prices (
    stock_symbol VARCHAR(20) NOT NULL,
    stock_name VARCHAR(100) NOT NULL,
    current_price DECIMAL(10, 2) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (stock_symbol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert popular Indian stocks with sample prices
INSERT INTO current_prices (stock_symbol, stock_name, current_price) VALUES
('TCS', 'Tata Consultancy Services', 3850.00),
('RELIANCE', 'Reliance Industries', 2450.00),
('INFY', 'Infosys', 1650.00),
('HDFCBANK', 'HDFC Bank', 1580.00),
('ICICIBANK', 'ICICI Bank', 1120.00),
('HINDUNILVR', 'Hindustan Unilever', 2380.00),
('ITC', 'ITC Limited', 450.00),
('SBIN', 'State Bank of India', 785.00),
('BHARTIARTL', 'Bharti Airtel', 1520.00),
('KOTAKBANK', 'Kotak Mahindra Bank', 1750.00)
ON DUPLICATE KEY UPDATE 
    stock_name = VALUES(stock_name),
    current_price = VALUES(current_price);

-- Verify tables created
SHOW TABLES;

-- Display table structures
DESCRIBE transactions;
DESCRIBE current_prices;

-- Display data
SELECT * FROM current_prices;

-- Success message
SELECT 'Database setup completed successfully!' AS Status;
