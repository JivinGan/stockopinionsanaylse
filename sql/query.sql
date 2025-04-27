SELECT *
FROM stock_options
WHERE stockcode = 'QQQ'
ORDER BY strike ASC;







--增减方向
SELECT
    new.contract_name,
    new.optiontype,
    old.open_interest AS old_open_interest,
    new.open_interest AS new_open_interest,
    (new.open_interest - old.open_interest) AS open_interest_change,
    CASE
        WHEN new.open_interest > old.open_interest THEN 'Increase'
        WHEN new.open_interest < old.open_interest THEN 'Decrease'
        ELSE 'No Change'
    END AS change_direction
FROM
    stock_options new
JOIN
    stock_options old
ON
    new.contract_name = old.contract_name
    AND new.stockcode = old.stockcode
    AND new.optiontype = old.optiontype
WHERE
    new.stockcode = 'QQQ'
    AND old.stockcode = 'QQQ'
    AND new.DayOrder = 9
    AND old.DayOrder = 8
ORDER BY
    ABS(new.open_interest - old.open_interest) DESC;


--第二步：新增一版 汇总统计（call/put整体变化）
--直接用下面这条SQL：

SELECT
    optiontype,
    SUM(CASE WHEN new.open_interest > old.open_interest THEN (new.open_interest - old.open_interest) ELSE 0 END) AS total_increase,
    SUM(CASE WHEN new.open_interest < old.open_interest THEN (old.open_interest - new.open_interest) ELSE 0 END) AS total_decrease
FROM
    stock_options new
JOIN
    stock_options old
ON
    new.contract_name = old.contract_name
    AND new.stockcode = old.stockcode
    AND new.optiontype = old.optiontype
WHERE
    new.stockcode = 'QQQ'
    AND old.stockcode = 'QQQ'
    AND new.DayOrder = 9
    AND old.DayOrder = 8
GROUP BY
    optiontype;