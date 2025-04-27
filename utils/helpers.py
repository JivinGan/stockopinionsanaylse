from datetime import datetime

def get_current_time():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

import re

def is_valid_stock_code(code):
    pattern = r'^[A-Z0-9]{1,4}(\.[A-Z])?$'
    return re.match(pattern, code) is not None

# 校验股票代码是否合法
def is_valid_stock_code(code):
    pattern = r'^[A-Z0-9]{1,4}(\.[A-Z])?$'
    return re.match(pattern, code) is not None