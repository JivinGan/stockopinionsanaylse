import pandas as pd

def process_csv(file_path, stock_code, opiniontype, querytime):
    df = pd.read_csv(file_path)

    # 加字段
    df['opiniontype'] = opiniontype
    df['querytime'] = querytime
    df['stockcode'] = stock_code

    # 保留需要的列，改列名
    required_columns = [
        'contractSymbol',
        'lastTradeDate',
        'strike',
        'lastPrice',
        'bid',
        'ask',
        'change',
        'percentChange',
        'volume',
        'openInterest',
        'impliedVolatility',
        'opiniontype',
        'querytime',
        'stockcode'
    ]

    df = df[required_columns]
    df = df.rename(columns={
        'contractSymbol': 'contract_name',
        'lastTradeDate': 'last_trade_date',
        'change': 'change_amount',
        'percentChange': 'percent_change'
    })

    return df
