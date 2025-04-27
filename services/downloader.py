import yfinance as yf
import pandas as pd

def download_options_csv(stock_code):
    ticker = yf.Ticker(stock_code)
    expiration_dates = ticker.options

    if not expiration_dates:
        raise Exception(f"{stock_code} 没有找到任何期权到期日")

    exp_date = expiration_dates[0]  # 默认取第一个到期日

    opt_chain = ticker.option_chain(exp_date)

    # 分开处理calls和puts
    df_calls = opt_chain.calls
    df_puts = opt_chain.puts

    call_path = f"{stock_code}_calls.csv"
    put_path = f"{stock_code}_puts.csv"

    df_calls.to_csv(call_path, index=False)
    df_puts.to_csv(put_path, index=False)

    return call_path, put_path
