# Beosin API 文档 - Compliance-V4 合规接口

## 概述

Compliance-V4 是 Beosin 专为合规场景开发的 API 服务系列。相比上一版本，V4 版本在返回数据中增加了更多信息：

- **实体详情**：命中的风险类型下包含的实体名称、风险金额和比例
- **跳数显示**：显示风险类型或实体与查询目标之间的最短跳数

**Base URL**: `https://api.beosin.com`

**通用请求头**: `Content-Type: application/json`

**验证方式**: SIGN（签名认证）

---

## 目录

1. [KYA V4 - EOA 地址风险评估](#1-kya-v4---eoa-地址风险评估)
2. [KYT V4 - 存款交易评估](#2-kyt-v4---存款交易评估)
3. [KYT V4 - 提款交易评估](#3-kyt-v4---提款交易评估)

---

## 1. KYA V4 - EOA 地址风险评估

Beosin-KYT 会根据您指定的资产类型和风险策略，穿透目标地址的交易，分析资金流入和流出情况。

**新增返回内容**：
1. 增加了命中的风险类型下的实体详情，如实体名称、风险金额和比例
2. 增加了跳数显示，展示风险类型或实体与查询目标之间的最短跳数

**适用场景**：
- 收到资金时：评估来源地址的风险
- 资金转出时：评估目标地址的风险

### 请求

**Endpoint**: `GET /api/v4/kyt/address/risk`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appId | String | Y | KYT 系统分配的唯一身份认证 APPID |
| appSecret | String | Y | KYT 系统分配的唯一身份认证 APP-SECRET |
| chainId | String | Y | 链 ID |
| address | String | Y | 地址哈希 |
| token | String | N | 代币地址，不填默认为原生代币 |

### 响应

```json
{
    "code": 200,
    "msg": "success",
    "data": {
        "score": 90,
        "riskLevel": "Low",
        "incomingScore": null,
        "incomingLevel": null,
        "incomingDetail": [],
        "outgoingScore": 90,
        "outgoingLevel": "Low",
        "outgoingDetail": [
            {
                "strategyName": "Official Freeze",
                "riskLevel": "Low",
                "hops": 4,
                "exposure": "Indirect",
                "rate": 0.000062,
                "amount": 0.00392723338777528420843893,
                "entityDetails": [
                    {
                        "entityName": "unnamed entity",
                        "hops": 4,
                        "purificationAmountU": 0.00392723338,
                        "purificationRate": 0.000062
                    }
                ]
            }
        ],
        "riskTagScore": null,
        "riskTagLevel": null,
        "riskTagDetails": []
    }
}
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| score | Double | 地址总分 |
| riskLevel | String | 地址风险等级：Severe, High, Medium, Low |
| incomingScore | Double | 入金风险评分 |
| incomingLevel | String | 入金风险等级 |
| incomingDetail | Array | 入金命中风险详情 |
| incomingDetail[].strategyName | String | 策略名称 |
| incomingDetail[].exposure | String | 暴露类型：Direct（直接）或 Indirect（间接） |
| incomingDetail[].riskLevel | String | 入金方向命中策略的风险等级 |
| incomingDetail[].hops | Integer | 入金方向命中此风险类型的跳数 |
| incomingDetail[].rate | Double | 入金方向此风险类型对应的风险资金占总入金的比例 |
| incomingDetail[].amount | BigDecimal | 入金方向此风险类型对应的风险资金金额 |
| incomingDetail[].entityDetails | Array | 入金方向此风险类型对应的实体详情 |
| incomingDetail[].entityDetails[].entityName | String | 实体名称 |
| incomingDetail[].entityDetails[].hops | Integer | 实体跳数 |
| incomingDetail[].entityDetails[].purificationAmountU | BigDecimal | 实体风险资金金额 |
| incomingDetail[].entityDetails[].purificationRate | Double | 实体风险资金比例 |
| outgoingScore | Double | 出金风险评分 |
| outgoingLevel | String | 出金风险等级 |
| outgoingDetail | Array | 出金命中风险详情（同 incomingDetail 结构） |
| riskTagScore | Double | 风险标签评分 |
| riskTagLevel | String | 风险标签等级 |
| riskTagDetails | Array | 风险标签类型列表 |

### 示例请求

```
https://api.beosin.com/api/v4/kyt/address/risk?address=0xc0e80a623c9593b3c3911682d2084c4e93bea4a7&chainId=1&token=0xdac17f958d2ee523A2206206994597c13d831EC7
```

---

## 2. KYT V4 - 存款交易评估

当用户向您平台的指定钱包地址转入资金时，此接口用于评估资金来源的风险。

**新增返回内容**：
1. 增加了命中的风险类型下的实体详情，如实体名称、风险金额和比例
2. 增加了跳数显示，展示风险类型或实体与查询目标之间的最短跳数

### 请求

**Endpoint**: `GET /api/v4/kyt/tx/deposit`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appId | String | Y | KYT 系统分配的唯一身份认证 APPID |
| appSecret | String | Y | KYT 系统分配的唯一身份认证 APP-SECRET |
| chainId | String | Y | 链 ID |
| hash | String | Y | 交易哈希 |
| token | String | N | 代币地址（ERC-20 代币填地址，原生代币如 ETH、BTC、Sol 填代币名称） |

### 响应

```json
{
    "code": 200,
    "data": {
        "riskLevel": "Low",
        "risks": [
            {
                "amount": 0.00000371,
                "entityDetails": [
                    {
                        "entityName": "unnamed entity",
                        "hops": 3,
                        "purificationAmountU": 0.00000371,
                        "purificationRate": 0.000001
                    }
                ],
                "exposure": "Indirect",
                "hops": 3,
                "rate": 0.000001,
                "riskLevel": "Low",
                "riskStrategy": "Phishing"
            }
        ],
        "score": 90
    },
    "msg": "success"
}
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| score | BigDecimal | 地址评分 |
| riskLevel | String | 风险等级：Severe, High, Medium, Low |
| risks | Array | 命中风险列表 |
| risks[].riskStrategy | String | 风险策略名称 |
| risks[].exposure | String | 暴露类型：Direct 或 Indirect |
| risks[].riskLevel | String | 风险等级 |
| risks[].hops | Integer | 风险实体与查询目标之间的跳数 |
| risks[].rate | BigDecimal | 资金比例（保留4位有效数字） |
| risks[].amount | BigDecimal | 金额 |
| risks[].entityDetails | Array | 实体详情列表 |
| risks[].entityDetails[].entityName | String | 实体名称 |
| risks[].entityDetails[].hops | Integer | 实体与查询目标的跳数 |
| risks[].entityDetails[].purificationRate | BigDecimal | 资金比例 |
| risks[].entityDetails[].purificationAmountU | BigDecimal | 金额 |

### 示例请求

```
https://api.beosin.com/api/v4/kyt/tx/deposit?chainId=137&hash=0xa7381d43259250e004478478df0715fcb85a95d6345a3dd097a18dbeebe40173&token=0x8f3cf7ad23cd3cadbd9735aff958023239c6a063
```

### 错误码

| 错误码 | 说明 |
|--------|------|
| 40001 | 参数错误 |
| 40021 | 平台不支持 |
| 40023 | 交易哈希错误 |
| 41023 | 交易哈希不存在 |
| 41024 | 不支持非 ERC-20 交易评估 |
| 41035 | 交易涉及不在代币篮子中的代币 |
| 41038 | 任务正在执行中，请稍后重试 |

---

## 3. KYT V4 - 提款交易评估

当有出金交易时，需要对资金目的地进行风险评估。

**新增返回内容**：
1. 增加了命中的风险类型下的实体详情，如实体名称、风险金额和比例
2. 增加了跳数显示，展示风险类型或实体与查询目标之间的最短跳数

### 请求

**Endpoint**: `GET /api/v4/kyt/tx/withdraw`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appId | String | Y | KYT 系统分配的唯一身份认证 APPID |
| appSecret | String | Y | KYT 系统分配的唯一身份认证 APP-SECRET |
| chainId | String | Y | 链 ID |
| hash | String | Y | 交易哈希 |
| token | String | N | 代币地址（ERC-20 代币填地址，原生代币如 ETH、BTC、Sol 填代币名称） |

### 响应

```json
{
    "code": 200,
    "data": {
        "riskLevel": "Medium",
        "risks": [
            {
                "amount": 3e-7,
                "entityDetails": [
                    {
                        "entityName": "unnamed entity",
                        "hops": 5,
                        "purificationAmountU": 3e-7,
                        "purificationRate": 0.000001
                    }
                ],
                "exposure": "Indirect",
                "hops": 5,
                "rate": 0.000001,
                "riskLevel": "Low",
                "riskStrategy": "Hacker"
            },
            {
                "amount": 0.00001334,
                "entityDetails": [
                    {
                        "entityName": "unnamed entity",
                        "hops": 3,
                        "purificationAmountU": 0.00001334,
                        "purificationRate": 0.000002
                    }
                ],
                "exposure": "Indirect",
                "hops": 3,
                "rate": 0.000002,
                "riskLevel": "Low",
                "riskStrategy": "Phishing"
            },
            {
                "amount": 0.00004989,
                "entityDetails": [
                    {
                        "entityName": "KyberSwap",
                        "hops": 4,
                        "purificationAmountU": 0.00004989,
                        "purificationRate": 0.000005
                    }
                ],
                "exposure": "Indirect",
                "hops": 4,
                "rate": 0.000005,
                "riskLevel": "Low",
                "riskStrategy": "Grey List - FATF"
            },
            {
                "amount": 10.23194027014,
                "entityDetails": [
                    {
                        "entityName": "Betfury",
                        "hops": 1,
                        "purificationAmountU": 10.23194027014,
                        "purificationRate": 0.995045
                    }
                ],
                "exposure": "Direct",
                "hops": 1,
                "rate": 0.995,
                "riskLevel": "Medium",
                "riskStrategy": "Gambling"
            }
        ],
        "score": 60
    },
    "msg": "success"
}
```

### 响应字段说明

与存款交易评估（KYT V4 - Deposit）结构相同。

### 示例请求

```
https://api.beosin.com/api/v4/kyt/tx/withdraw?chainId=43114&hash=0x1e6c99bb4d1e8b0858d84b8c24a62f23fcc327701469755955352e7ba9e7bc22&token=0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e
```

### 错误码

| 错误码 | 说明 |
|--------|------|
| 40001 | 参数错误 |
| 40021 | 平台不支持 |
| 40023 | 交易哈希错误 |
| 41023 | 交易哈希不存在 |
| 41024 | 不支持非 ERC-20 交易评估 |
| 41035 | 交易涉及不在代币篮子中的代币 |
| 41038 | 任务正在执行中，请稍后重试 |

---

## V4 版本与 V2/V3 版本对比

| 特性 | V2/V3 | V4 |
|------|-------|-----|
| 基本评分和风险等级 | ✅ | ✅ |
| 风险策略详情 | ✅ | ✅ |
| 实体详情（名称、金额、比例） | ❌ | ✅ |
| 跳数显示 | ❌ | ✅ |
| 暴露类型（Direct/Indirect） | ❌ | ✅ |

**注意**：V4 版本的请求参数格式与 V2/V3 版本相同，可快速接入。

---

## 响应时间

- 所有 V4 接口：< 30秒

---

## 文档信息

- **来源**: [Beosin API Documentation](https://beosinofficials-organization.gitbook.io/beosin-api-documentation/api-endpoints/compliance-v4)
- **更新时间**: 2024年
