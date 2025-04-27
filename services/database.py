from config.db_config import get_db_connection
from config.dayorder_tracker import get_dayorder


import pandas as pd
import numpy as np


def insert_options_data(df, day_order):


    df = df.replace({np.nan: None, pd.NA: None})


    conn = get_db_connection()
    cursor = conn.cursor()

    # 处理 NaN
    df = df.where(pd.notnull(df), None)

    # 加上固定的 DayOrder
    df['DayOrder'] = day_order

    sql = """
            INSERT INTO stock_options (
                contract_name,
                last_trade_date,
                strike,
                last_price,
                bid,
                ask,
                change_amount,
                percent_change,
                volume,
                open_interest,
                implied_volatility,
                optiontype,
                querytime,
                stockcode,
                DayOrder
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    data = [tuple(row) for row in df.values]

    cursor.executemany(sql, data)
    conn.commit()

    inserted_count = cursor.rowcount

    cursor.close()
    conn.close()

    print(f"✅ 数据插入完成，共{inserted_count}条，DayOrder={day_order}")