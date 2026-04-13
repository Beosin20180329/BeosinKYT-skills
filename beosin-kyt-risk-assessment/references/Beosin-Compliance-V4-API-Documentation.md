# Beosin API Documentation - Compliance-V4 Compliance Interface

## Overview

Compliance-V4 is a Beosin API service series specifically developed for compliance scenarios. Compared to the previous version, V4 returns more information:

- **Entity Details**: Entity names, risk amounts, and ratios under hit risk types
- **Hop Count Display**: Shows the shortest hop count between risk types or entities and the query target

**Base URL**: `https://api.beosin.com`

**Common Request Headers**: `Content-Type: application/json`

**Authentication**: SIGN (signature authentication)

---

## Table of Contents

1. [KYA V4 - EOA Address Risk Assessment](#1-kyav4---eoa-address-risk-assessment)
2. [KYT V4 - Deposit Transaction Assessment](#2-kytv4---deposit-transaction-assessment)
3. [KYT V4 - Withdraw Transaction Assessment](#3-kytv4---withdraw-transaction-assessment)

---

## 1. KYA V4 - EOA Address Risk Assessment

Beosin-KYT analyzes the target address's transactions based on the specified asset type and risk strategy, examining fund inflow and outflow.

**New Response Content**:
1. Added entity details under hit risk types, including entity name, risk amount, and ratio
2. Added hop count display, showing the shortest hop count between risk types or entities and the query target

**Applicable Scenarios**:
- When receiving funds: Assess the risk of the source address
- When sending funds: Assess the risk of the destination address

### Request

**Endpoint**: `GET /api/v4/kyt/address/risk`

### Request Parameters

| Parameter | Type | Required | Description |
|------|------|------|------|
| appId | String | Y | Unique identity APPID assigned by KYT system |
| appSecret | String | Y | Unique identity APP-SECRET assigned by KYT system |
| chainId | String | Y | Chain ID |
| address | String | Y | Address hash |
| token | String | N | Token address, defaults to native token if not specified |

### Response

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

### Response Field Description

| Field | Type | Description |
|------|------|------|
| score | Double | Total address score |
| riskLevel | String | Address risk level: Severe, High, Medium, Low |
| incomingScore | Double | Incoming risk score |
| incomingLevel | String | Incoming risk level |
| incomingDetail | Array | Incoming risk hit details |
| incomingDetail[].strategyName | String | Strategy name |
| incomingDetail[].exposure | String | Exposure type: Direct or Indirect |
| incomingDetail[].riskLevel | String | Risk level of incoming hit strategy |
| incomingDetail[].hops | Integer | Hop count for incoming risk type |
| incomingDetail[].rate | Double | Ratio of risk funds to total incoming funds |
| incomingDetail[].amount | BigDecimal | Risk fund amount for incoming direction |
| incomingDetail[].entityDetails | Array | Entity details for incoming risk type |
| incomingDetail[].entityDetails[].entityName | String | Entity name |
| incomingDetail[].entityDetails[].hops | Integer | Entity hop count |
| incomingDetail[].entityDetails[].purificationAmountU | BigDecimal | Entity risk fund amount |
| incomingDetail[].entityDetails[].purificationRate | Double | Entity risk fund ratio |
| outgoingScore | Double | Outgoing risk score |
| outgoingLevel | String | Outgoing risk level |
| outgoingDetail | Array | Outgoing risk hit details (same structure as incomingDetail) |
| riskTagScore | Double | Risk tag score |
| riskTagLevel | String | Risk tag level |
| riskTagDetails | Array | Risk tag type list |

### Example Request

```
https://api.beosin.com/api/v4/kyt/address/risk?address=0xc0e80a623c9593b3c3911682d2084c4e93bea4a7&chainId=1&token=0xdac17f958d2ee523A2206206994597c13d831EC7
```

---

## 2. KYT V4 - Deposit Transaction Assessment

This interface is used to assess the risk of funds when a user transfers funds to your platform's designated wallet address.

**New Response Content**:
1. Added entity details under hit risk types, including entity name, risk amount, and ratio
2. Added hop count display, showing the shortest hop count between risk types or entities and the query target

### Request

**Endpoint**: `GET /api/v4/kyt/tx/deposit`

### Request Parameters

| Parameter | Type | Required | Description |
|------|------|------|------|
| appId | String | Y | Unique identity APPID assigned by KYT system |
| appSecret | String | Y | Unique identity APP-SECRET assigned by KYT system |
| chainId | String | Y | Chain ID |
| hash | String | Y | Transaction hash |
| token | String | N | Token address (ERC-20 token address, native tokens like ETH, BTC, Sol use token name) |

### Response

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

### Response Field Description

| Field | Type | Description |
|------|------|------|
| score | BigDecimal | Address score |
| riskLevel | String | Risk level: Severe, High, Medium, Low |
| risks | Array | Hit risk list |
| risks[].riskStrategy | String | Risk strategy name |
| risks[].exposure | String | Exposure type: Direct or Indirect |
| risks[].riskLevel | String | Risk level |
| risks[].hops | Integer | Hop count between risk entity and query target |
| risks[].rate | BigDecimal | Fund ratio (4 significant digits) |
| risks[].amount | BigDecimal | Amount |
| risks[].entityDetails | Array | Entity details list |
| risks[].entityDetails[].entityName | String | Entity name |
| risks[].entityDetails[].hops | Integer | Hop count between entity and query target |
| risks[].entityDetails[].purificationRate | BigDecimal | Fund ratio |
| risks[].entityDetails[].purificationAmountU | BigDecimal | Amount |

### Example Request

```
https://api.beosin.com/api/v4/kyt/tx/deposit?chainId=137&hash=0xa7381d43259250e004478478df0715fcb85a95d6345a3dd097a18dbeebe40173&token=0x8f3cf7ad23cd3cadbd9735aff958023239c6a063
```

### Error Codes

| Error Code | Description |
|--------|------|
| 40001 | Parameter error |
| 40021 | Platform not supported |
| 40023 | Transaction hash error |
| 41023 | Transaction hash does not exist |
| 41024 | Non ERC-20 transaction assessment not supported |
| 41035 | Transaction involves tokens not in token basket |
| 41038 | Task is executing, please retry later |

---

## 3. KYT V4 - Withdraw Transaction Assessment

When there is a withdrawal transaction, risk assessment of the fund destination is required.

**New Response Content**:
1. Added entity details under hit risk types, including entity name, risk amount, and ratio
2. Added hop count display, showing the shortest hop count between risk types or entities and the query target

### Request

**Endpoint**: `GET /api/v4/kyt/tx/withdraw`

### Request Parameters

| Parameter | Type | Required | Description |
|------|------|------|------|
| appId | String | Y | Unique identity APPID assigned by KYT system |
| appSecret | String | Y | Unique identity APP-SECRET assigned by KYT system |
| chainId | String | Y | Chain ID |
| hash | String | Y | Transaction hash |
| token | String | N | Token address (ERC-20 token address, native tokens like ETH, BTC, Sol use token name) |

### Response

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

### Response Field Description

Same structure as Deposit Transaction Assessment (KYT V4 - Deposit).

### Example Request

```
https://api.beosin.com/api/v4/kyt/tx/withdraw?chainId=43114&hash=0x1e6c99bb4d1e8b0858d84b8c24a62f23fcc327701469755955352e7ba9e7bc22&token=0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e
```

### Error Codes

| Error Code | Description |
|--------|------|
| 40001 | Parameter error |
| 40021 | Platform not supported |
| 40023 | Transaction hash error |
| 41023 | Transaction hash does not exist |
| 41024 | Non ERC-20 transaction assessment not supported |
| 41035 | Transaction involves tokens not in token basket |
| 41038 | Task is executing, please retry later |

---

## V4 vs V2/V3 Comparison

| Feature | V2/V3 | V4 |
|------|-------|-----|
| Basic score and risk level | ✅ | ✅ |
| Risk strategy details | ✅ | ✅ |
| Entity details (name, amount, ratio) | ❌ | ✅ |
| Hop count display | ❌ | ✅ |
| Exposure type (Direct/Indirect) | ❌ | ✅ |

**Note**: V4 request parameter format is the same as V2/V3, for quick integration.

---

## Response Time

- All V4 interfaces: < 30 seconds

---

## Document Information

- **Source**: [Beosin API Documentation](https://beosinofficials-organization.gitbook.io/beosin-api-documentation/api-endpoints/compliance-v4)
- **Last Updated**: 2024