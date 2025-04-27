import os
import re
from services.downloader import download_options_csv
from services.export_latest_to_data_folder import export_latest_to_data_folder
from services.processor import process_csv
from services.database import insert_options_data
from utils.helpers import get_current_time, is_valid_stock_code

from config.dayorder_tracker import get_dayorder


def main():
    while True:
        stocks_input = input("请输入要查询的股票代码（多个股票用逗号分隔，例如 NVDA,AAPL,QQQ），输入exit退出：").strip()

        if stocks_input.lower() == "exit":
            print("退出程序。")
            break

        stock_codes = [code.strip().upper() for code in stocks_input.split(",")]

        for stock_code in stock_codes:
            try:
                print(f"正在处理股票：{stock_code}")

                # 👇 第一次拉取固定DayOrder
                day_order = get_dayorder(stock_code)

                # 统一生成查询时间
                batch_query_time = get_current_time()

                # 下载 call/put
                call_path, put_path = download_options_csv(stock_code)

                # 处理 call 数据
                df_call = process_csv(call_path, stock_code, 'call', batch_query_time)
                insert_options_data(df_call, day_order)
                os.remove(call_path)

                # 处理 put 数据
                df_put = process_csv(put_path, stock_code, 'put', batch_query_time)
                insert_options_data(df_put, day_order)
                os.remove(put_path)

                print(f"✅ {stock_code} 期权数据处理完成！")
                export_latest_to_data_folder(stock_code)

            except Exception as e:
                print(f"❌ {stock_code} 出错了：{e}")


if __name__ == "__main__":
    main()
