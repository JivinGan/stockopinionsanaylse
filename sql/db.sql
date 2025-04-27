-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS stock_option_data DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE stock_option_data;

-- 创建表
CREATE TABLE IF NOT EXISTS stock_options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contract_name VARCHAR(100),
    last_trade_date DATETIME,
    strike DECIMAL(10,2),
    last_price DECIMAL(10,2),
    bid DECIMAL(10,2),
    ask DECIMAL(10,2),
    change_amount DECIMAL(10,2),
    percent_change DECIMAL(10,2),
    volume INT,
    open_interest INT,
    implied_volatility DECIMAL(10,2),
    optiontype ENUM('call', 'put'),
    querytime VARCHAR(20),
    stockcode VARCHAR(20),
    KEY idx_querytime (querytime),
    KEY idx_stockcode (stockcode)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


SELECT *
FROM stock_options
WHERE stockcode = 'QQQ'
  AND optiontype = 'put'
ORDER BY strike ASC;

USE stock_option_data;

ALTER TABLE stock_options
ADD COLUMN DayOrder INT COMMENT '查询批次顺序',
ADD INDEX idx_DayOrder (DayOrder);