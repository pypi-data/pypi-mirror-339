import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import asyncio
from typing import Dict, List
import aiohttp
import pandas as pd
import datetime
import nest_asyncio
from loguru import logger


async def fetch_single_page(
        session: aiohttp.ClientSession, url: str, params: Dict
) -> Dict:
    """异步获取单页数据"""
    async with session.get(url, params=params, ssl=False) as response:
        return await response.json()


async def fetch_all_pages_async(url: str, base_params: Dict) -> List[Dict]:
    """异步获取所有页面数据"""
    # 首先获取总数以计算页数
    first_page_params = base_params.copy()
    first_page_params["pn"] = "1"

    async with aiohttp.ClientSession() as session:
        first_page_data = await fetch_single_page(session, url, first_page_params)

        # 检查是否成功获取数据
        if first_page_data.get("rc") != 0 or not first_page_data.get("data"):
            return [first_page_data]  # 返回错误信息

        total = first_page_data["data"]["total"]
        page_size = int(base_params["pz"])
        total_pages = (total + page_size - 1) // page_size

        # 限制页数，避免过大请求
        total_pages = min(total_pages, 100)

        # 创建所有页面的任务
        tasks = []
        for page in range(1, total_pages + 1):
            page_params = base_params.copy()
            page_params["pn"] = str(page)
            tasks.append(fetch_single_page(session, url, page_params))

        # 并发执行所有任务
        results = await asyncio.gather(*tasks)
        return results


def process_data(page_results: List[Dict]) -> pd.DataFrame:
    """处理获取到的数据，转换为DataFrame"""
    all_data = []

    # 保存每个页面的结果和页码
    page_number = 1
    items_per_page = 100  # 假设每页100条

    for result in page_results:
        if result.get("rc") == 0 and result.get("data") and result["data"].get("diff"):
            page_data = result["data"]["diff"]

            # 添加页面信息以便后续计算序号
            for item in page_data:
                item["page_number"] = page_number
                item["page_index"] = page_data.index(item)

            all_data.extend(page_data)
            page_number += 1

    if not all_data:
        return pd.DataFrame()

    df = pd.DataFrame(all_data)

    # 删除临时列
    df.drop(columns=["page_number", "page_index"], inplace=True, errors="ignore")

    df = df.rename(columns={
        "f2": "now_price",
        "f3": "chg",
        "f5": "volume",
        "f6": "amount",
        "f8": "exchange",
        "f10": "quantity_ratio",
        "f22": "up_speed",
        "f11": "up_speed_05",
        "f12": "symbol",
        "f14": "name",
        "f15": "high",
        "f16": "low",
        "f17": "open",
        "f18": "yesterday_price",
        "f20": "total_mv",
        "f21": "flow_mv",
        "f26": "list_date",
        "f33": "wei_bi",
        "f34": "outer_disk",
        "f35": "inner_disk",
        "f62": "today_main_net_inflow",
        "f66": "super_large_order_net_inflow",
        "f69": "super_large_order_net_inflow_ratio",
        "f72": "large_order_net_inflow",
        # "f78": "medium_order_net_inflow",
        # "f84": "small_order_net_inflow",
        "f100": "industry",
        # "f103": "concept",
        "f184": "today_main_net_inflow_ratio",
        "f352": "average_price",
        "f211": "buy_1_num",
        "f212": "sell_1_num"
    })

    # 选择需要的列并确保所有需要的列都存在
    desired_columns = [
        'symbol',
        "now_price",
        "chg",
        "volume",
        "amount",
        "exchange",
        "quantity_ratio",
        "up_speed",
        "up_speed_05",
        "high",
        "low",
        "open",
        "yesterday_price",
        "total_mv",
        "flow_mv",
        "wei_bi",
        "outer_disk",
        "inner_disk",
        "today_main_net_inflow",
        "super_large_order_net_inflow",
        "super_large_order_net_inflow_ratio",
        "large_order_net_inflow",
        "today_main_net_inflow_ratio",
        "average_price",
        "buy_1_num",
        "sell_1_num",
    ]

    # 过滤出存在的列
    available_columns = [col for col in desired_columns if col in df.columns]
    df = df[available_columns]

    # 转换数值类型
    numeric_columns = [
        "now_price",
        "chg",
        "volume",
        "amount",
        "exchange",
        "quantity_ratio",
        "up_speed",
        "up_speed_05",
        "high",
        "low",
        "open",
        "yesterday_price",
        "total_mv",
        "flow_mv",
        "wei_bi",
        "outer_disk",
        "inner_disk",
        "today_main_net_inflow",
        "super_large_order_net_inflow",
        "super_large_order_net_inflow_ratio",
        "large_order_net_inflow",
        "today_main_net_inflow_ratio",
        "average_price",
        "buy_1_num",
        "sell_1_num",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df.loc[df[col] == '-', col] = 0
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 大单比例
    df['large_order_net_inflow_ratio'] = round((df['large_order_net_inflow'] / df['amount']) * 100, 2)

    # 外盘是内盘倍数
    df['disk_ratio'] = round((df['outer_disk'] - df['inner_disk']) / df['inner_disk'], 2)
    # 只有外盘没有内盘
    df.loc[df["inner_disk"] == 0, ['disk_ratio']] = 1688
    # 按涨跌幅降序排序
    df.sort_values(by="chg", ascending=False, inplace=True)

    return df


async def stock_zh_a_spot_em_async() -> pd.DataFrame:
    fields = "f352,f2,f3,f5,f6,f8,f10,f11,f22,f12,f15,f16,f17,f18,f20,f21,f33,f34,f35,f62,f66,f69,f72,f184,f211,f212",
    # 获取当前日期和时间
    current_time = datetime.datetime.now()

    # 将当前时间转换为时间戳（以毫秒为单位）
    current_timestamp_ms = int(current_time.timestamp() * 1000)
    """
    异步获取东方财富网-沪深京 A 股-实时行情
    https://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    url = "https://82.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f12",
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048",
        "fields": fields,
        "_": current_timestamp_ms
    }

    results = await fetch_all_pages_async(url, params)
    return process_data(results)


def stock_real_quotes() -> pd.DataFrame:
    """
    东方财富网-沪深京 A 股-实时行情 (同步接口)
    https://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    try:
        nest_asyncio.apply()
        return asyncio.run(stock_zh_a_spot_em_async())
    except Exception as e:
        logger.error("同步实时行情出现异常:{}", e)


if __name__ == "__main__":
    while True:
        stock_zh_a_spot_em_df = stock_real_quotes()
        logger.info(1)
