import os
import pandas as pd
from config.db_config import get_db_connection

def export_latest_to_data_folder(stock_code):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 找最新querytime
    cursor.execute("""
        SELECT MAX(querytime) AS max_querytime
        FROM stock_options
        WHERE stockcode = %s
    """, (stock_code,))
    max_querytime = cursor.fetchone()[0]

    if not max_querytime:
        print(f"⚠️ 没有找到 {stock_code} 的数据，跳过导出。")
        cursor.close()
        conn.close()
        return

    # 查询这一批数据
    cursor.execute("""
        SELECT strike, last_price, bid, ask, change_amount, percent_change,
               volume, open_interest, implied_volatility, optiontype, querytime, stockcode
        FROM stock_options
        WHERE stockcode = %s
          AND querytime = %s
        ORDER BY strike ASC
    """, (stock_code, max_querytime))

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    if not rows:
        print(f"⚠️ {stock_code} 最新数据为空，跳过生成CSV。")
        return

    df = pd.DataFrame(rows, columns=columns)

    # 你的固定绝对路径
    output_dir = r"C:\Users\jivin\OneDrive\Desktop\data"

    # 格式化querytime
    time_str = max_querytime.replace('/', '').replace(' ', '_').replace(':', '')

    # 生成绝对路径的文件名
    filename = os.path.join(output_dir, f"{stock_code}_{time_str}.csv")

    # 确保目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 保存csv
    df.to_csv(filename, index=False, encoding='utf-8-sig')


    print(f"📦 成功导出 {filename}")
