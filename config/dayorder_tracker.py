import os
import json
from datetime import datetime

# 保存DayOrder的文件
DAYORDER_FILE = os.path.join(os.path.dirname(__file__), 'dayorder.json')


def load_dayorder():
    if not os.path.exists(DAYORDER_FILE):
        return {"date": current_date(), "stocks": {}}

    with open(DAYORDER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_dayorder(data):
    with open(DAYORDER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def current_date():
    return datetime.now().strftime('%Y%m%d')  # 格式：20250427


def get_dayorder(stockcode):
    data = load_dayorder()
    today = current_date()

    # 如果日期不同，重置
    if data.get("date") != today:
        data = {"date": today, "stocks": {}}

    # 更新次数
    stocks = data.setdefault("stocks", {})
    stocks[stockcode] = stocks.get(stockcode, 0) + 1

    save_dayorder(data)

    return stocks[stockcode]
