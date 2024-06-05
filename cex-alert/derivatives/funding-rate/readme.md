# Binance API 接口访问

## 资金费率历史
官方文档：https://developers.binance.com/docs/zh-CN/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History
### 接口说明
GET https://fapi.binance.com/fapi/v1/fundingRate

此接口返回资金费率历史数据。资金费率是用来确保期货市场价格与现货市场价格保持一致的机制。正资金费率表示多头支付空头，负资金费率表示空头支付多头。

请求参数

	•	symbol (字符串, 必填): 交易对，例如 BTCUSDT
	•	startTime (整数, 选填): 起始时间戳
	•	endTime (整数, 选填): 结束时间戳
	•	limit (整数, 选填): 返回的记录数量，默认值 100, 最大值 1000


## 最新标记价格和资金费率
官方文档：https://developers.binance.com/docs/zh-CN/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price

### 接口说明
GET https://fapi.binance.com/fapi/v1/premiumIndex

此接口返回最新的标记价格和资金费率。标记价格是用来避免市场操纵和过度波动的指标价，资金费率是用来确保期货市场价格与现货市场价格保持一致的机制。

请求参数

	symbol (字符串, 选填): 交易对，例如 BTCUSDT

响应:
```json
{
    "symbol": "BTCUSDT",                // 交易对
    "markPrice": "11793.63104562",      // 标记价格
    "indexPrice": "11781.80495970",     // 指数价格
    "estimatedSettlePrice": "11781.16138815",  // 预估结算价,仅在交割开始前最后一小时有意义
    "lastFundingRate": "0.00038246",    // 最近更新的资金费率
    "nextFundingTime": 1597392000000,   // 下次资金费时间
    "interestRate": "0.00010000",       // 标的资产基础利率
    "time": 1597370495002               // 更新时间
}
```
当不指定symbol时相应
```json
[
    {
        "symbol": "BTCUSDT",            // 交易对
        "markPrice": "11793.63104562",  // 标记价格
        "indexPrice": "11781.80495970", // 指数价格
        "estimatedSettlePrice": "11781.16138815",  // 预估结算价,仅在交割开始前最后一小时有意义
        "lastFundingRate": "0.00038246",    // 最近更新的资金费率
        "nextFundingTime": 1597392000000,   // 下次资金费时间
        "interestRate": "0.00010000",       // 标的资产基础利率
        "time": 1597370495002               // 更新时间
    }
]
```