import sys
import os
import ast
from datetime import datetime
import requests
from secret import *
from common import *
import pytz
# current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(current_dir, '..', '..'))
# from spot.volume.common import symbols, sned_alerts_to_dc, configure_logger


logger = configure_logger('bian-premium_info-alert-crontab.log')

def send_long_message_in_parts(logger, content, channel_id):
    max_length = 2000
    parts = []
    current_part = ""

    # 第一部分是独立的标题
    if content.startswith("**"):
        header, content = content.split('\n', 1)
        parts.append(header + "\n")
    
    for line in content.split('\n'):
        if len(current_part) + len(line) + 1 > max_length - 6:  # 减去代码块标记的长度:
            parts.append(current_part)
            current_part = line + "\n"
        else:
            current_part += line + "\n"

    if current_part:
        parts.append(current_part)

    for i, part in enumerate(parts):
        if i == 0 and part.startswith("**"):
            send_alerts_to_dc(logger, part.strip(), channel_id)
        else:
            part_with_code_block = "```\n" + part.strip() + "\n```"
            send_alerts_to_dc(logger, part_with_code_block, channel_id)


def get_funding_rate(symbols):
    # 查询资金费率历史（U本位合约）
    url = 'https://fapi.binance.com/fapi/v1/fundingRate'
    response = requests.get(url)

    if response.status_code == 200:
        datas = response.json()
    else:
        logger.error(f"请求 fundingInfo 失败，状态码: {response.status_code}, 返回信息: {response.text}")
        return

    results = []
    symbols = set(ast.literal_eval(symbols))
    for item in datas:
        if item['symbol'] in symbols:
            funding_rate_percent = float(item['fundingRate']) * 100  # 转换为百分比
            # 如果资金费率为负或者大于0.03%，进行收集
            if funding_rate_percent < 0 or funding_rate_percent > 0.03:
                results.append([item['symbol'], item['markPrice'], funding_rate_percent, datetime.fromtimestamp(item['fundingTime']/1000)])

    if len(results) != 0:
        content = f"**Get Funding Rate History** | {str(datetime.now())[5:16]}\n"
        content += "  Symbol      MarkPrice      FundingRate(%)   FundingTime\n"
        content += "----------------------------------------------------------------\n"

        for symbol, markPrice, fundingRate, fundingTime in results:
            formatted_rate = ('%.6f' % fundingRate).rstrip('0').rstrip('.')  # 去除尾随零和小数点
            content += f"{symbol:<10}  {markPrice:>12}      {formatted_rate:>8}%      {fundingTime.strftime('%Y-%m-%d %H:%M')}\n"

        send_long_message_in_parts(logger, content, 1247100925609246752)

def get_premium_info(symbols):
    # 查询最新标记价格和资金费率（U本位合约）
    url = 'https://fapi.binance.com/fapi/v1/premiumIndex'
    response = requests.get(url)

    if response.status_code == 200:
        datas = response.json()
    else:
        logger.error(f"请求 fundingInfo 失败，状态码: {response.status_code}, 返回信息: {response.text}")
        return

    results = []
    symbols = set(ast.literal_eval(symbols))
    for item in datas:
        if item['symbol'] in symbols:
            funding_rate_percent = float(item['lastFundingRate']) * 100  # 转换为百分比
            # 如果资金费率为负或者大于0.02%，进行收集
            if funding_rate_percent < min_funding_rate_percent_hreshold or funding_rate_percent >= max_funding_rate_percent_hreshold:
                results.append(
                    [item['symbol'],         # 交易对
                    item['markPrice'],       # 标记价格
                    item['indexPrice'],      # 指数价格
                    funding_rate_percent,    # 最近更新的资金费率
                    datetime.fromtimestamp(item['time']/1000), # 下次资金费时间
                    datetime.fromtimestamp(item['nextFundingTime']/1000), # 更新时间
                    item['estimatedSettlePrice'],      # 预估结算价,仅在交割开始前最后一小时有意义
                    ])

    if len(results) != 0:
        # 按照资金费率降序排列
        results_sorted = sorted(results, key=lambda x: x[3], reverse=True)
        shanghai_tz = pytz.timezone('Asia/Shanghai')
        content = f"**Get Funding Rate History** | {str(datetime.now(shanghai_tz))[5:16]}\n"
        # content += " Symbol             MarkPrice        IndexPrice      FundingRate   NextFundingTime \n"
        # content += "---------------------------------------------------------------------------------\n"
        content += " Symbol             MarkPrice        IndexPrice      FundingRate \n"
        content += "---------------------------------------------------------------\n"

        for symbol, markPrice, indexPrice, fundingRate, fundingTime, nextFundingTime, _ in results_sorted:
            formatted_rate = ('%.6f' % fundingRate).rstrip('0').rstrip('.')  # 去除尾随零和小数点
            # content += f"{symbol:<13}  {markPrice.rstrip('0').rstrip('.'):>14}    {indexPrice.rstrip('0').rstrip('.'):>14}    {formatted_rate:>10}%      {nextFundingTime.strftime('%m-%d %H:%M')}\n"
            content += f"{symbol:<13}  {markPrice.rstrip('0').rstrip('.'):>14}    {indexPrice.rstrip('0').rstrip('.'):>14}    {formatted_rate:>10}%\n"
        
        send_long_message_in_parts(logger, content, channel_id)


def get_funding_info(symbols):
    # 币本位，历史资金费率
    url = 'https://fapi.binance.com/fapi/v1/fundingInfo'
    response = requests.get(url)

    if response.status_code == 200:
        datas = response.json()
    else:
        logger.error(f"请求 fundingInfo 失败，状态码: {response.status_code}, 返回信息: {response.text}")
        return

    results = []
    symbols = set(ast.literal_eval(symbols))
    for item in datas:
        if item['symbol'] in symbols:
            results.append(item)

    # 分组
    group_4_hours = [item for item in results if item['fundingIntervalHours'] == 4]
    group_8_hours = [item for item in results if item['fundingIntervalHours'] == 8]

    # 打印4小时组
    content_4_hours = "4 Hours Interval Data:\n" + "\n".join(
        [f"Symbol: {item['symbol']}, Adjusted Funding Rate Cap: {float(item['adjustedFundingRateCap']):.4f}, Adjusted Funding Rate Floor: {float(item['adjustedFundingRateFloor']):.4f}" for item in group_4_hours])
    
    # 打印8小时组
    content_8_hours = "\n8 Hours Interval Data:\n" + "\n".join(
        [f"Symbol: {item['symbol']}, Adjusted Funding Rate Cap: {float(item['adjustedFundingRateCap']):.4f}, Adjusted Funding Rate Floor: {float(item['adjustedFundingRateFloor']):.4f}" for item in group_8_hours])

    content = "Get Funding Rate History\n" + content_4_hours + f"\n{'-'*100}\n" + content_8_hours

    send_long_message_in_parts(logger, content, 1247100925609246752)

if __name__ == '__main__':
    get_premium_info(symbols)