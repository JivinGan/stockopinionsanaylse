import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from config.db_config import get_db_connection

plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文字体
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

def fetch_open_interest_summary(stockcode, old_dayorder, new_dayorder):
    conn = get_db_connection()
    sql = """
    SELECT 
        new.optiontype,
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
        new.stockcode = %s
        AND old.stockcode = %s
        AND new.DayOrder = %s
        AND old.DayOrder = %s
    GROUP BY 
        new.optiontype
    """
    df = pd.read_sql(sql, conn, params=(stockcode, stockcode, new_dayorder, old_dayorder))
    conn.close()
    return df


def plot_open_interest_summary(df, stockcode, old_dayorder, new_dayorder):
    fig, ax = plt.subplots(figsize=(8,6))
    bar_width = 0.35
    index = range(len(df))

    ax.bar(index, df['total_increase'], width=bar_width, label='Increase (增仓)', color='skyblue')
    ax.bar([i + bar_width for i in index], df['total_decrease'], width=bar_width, label='Decrease (减仓)', color='salmon')

    ax.set_xlabel('Option Type')
    ax.set_ylabel('Open Interest Change')
    ax.set_title(f'{stockcode} Open Interest Change (今日期权变化差异)')
    ax.set_xticks([i + bar_width/2 for i in index])
    ax.set_xticklabels(df['optiontype'])
    ax.legend()

    plt.tight_layout()

    # 保存文件到 report/yyyyMMdd 目录下
    today_str = datetime.now().strftime('%Y%m%d')
    output_dir = os.path.join('report', today_str)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{stockcode}_今日期权变化差异.png")
    plt.savefig(output_path)
    print(f"\U0001F4E6 图表已保存至：{output_path}")

    plt.close()

def batch_process_stocks(stock_list, old_dayorder, new_dayorder):
    for stockcode in stock_list:
        try:
            df = fetch_open_interest_summary(stockcode, old_dayorder, new_dayorder)
            if df.empty:
                print(f"⚠️ {stockcode} 无数据，跳过。")
                continue
            plot_open_interest_summary(df, stockcode, old_dayorder, new_dayorder)
        except Exception as e:
            print(f"❌ 处理 {stockcode} 出错：{e}")

if __name__ == "__main__":
    # 要处理的股票列表
    stocks = ['QQQ']
    old_dayorder = 8
    new_dayorder = 9

    batch_process_stocks(stocks, old_dayorder, new_dayorder)

    print("✅ 全部处理完成。")
