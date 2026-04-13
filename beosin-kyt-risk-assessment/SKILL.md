---
name: beosin-kyt-risk-assessment
description: Beosin KYT/KYA Blockchain Risk Assessment Skill. Triggered when users need to assess the risk level of blockchain addresses or tokens (such as SHIB, USDT, USDC), including address risk assessment, transaction risk assessment (deposit/withdraw), token risk query and other scenarios. Use this Skill to help users with blockchain compliance and anti-money laundering risk analysis. If the user only provides the token name without an address, you must first look up the token contract address from currency_basket_output.json before calling the API.
---

# Beosin KYT/KYA Blockchain Risk Assessment Skill

## Quick Start

⚡️ **Minimal usage (one-liner)**:

```bash
# Address risk assessment (Tron chain)
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET address-v4 79 TNpK4NKPQTQsvMj4aDGR5nxabvFKWJ3m2E

# Deposit transaction risk assessment
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET deposit-v4 1 0x...

# Withdraw transaction risk assessment
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET withdraw-v4 1 0x...
```

**Full workflow (3 steps)**:
1. Get API keys (request APPID and APP-SECRET from user)
2. Call script with one command
3. Parse JSON results and generate risk assessment report

## Overview

This Skill is used to call Beosin KYT (Know Your Transaction) and KYA (Know Your Address) API to perform risk assessment on blockchain addresses and transactions.

## Trigger Scenarios

Use this Skill when users mention:
- "Assess the risk of this address"
- "Check if this transaction is risky"
- "KYT", "KYA"
- "Beosin risk assessment"
- "Blockchain compliance", "AML"
- "Transaction risk", "Address risk"
- "Assess SHIB risk", "Check USDT address risk" (need to look up token address first)

## Token Address Lookup

When users ask about risk assessment for a token (such as SHIB, USDT, USDC, etc.), you must first look up the token contract address from the token address mapping file.

### Step 1: Look up token address

Call `scripts/txt` script or use the following Python command to look up token address:

```bash
# Method 1: Using script
python scripts/txt get_address <chain> <token_symbol>

# Examples
python scripts/txt get_address ETH SHIB
python scripts/txt get_address BSC USDT
python scripts/txt get_address SOLANA BONK
```

Or directly read `scripts/currency_basket_output.json` file to look up token address.

### Step 2: Confirm chain ID

Based on the found token address format, confirm the chain and get the corresponding chainId:

| Chain Name | Chain ID | Token Address Pattern |
|------|----------|--------------|
| ETH | 1 | Starts with 0x, 42 chars |
| BSC | 56 | Starts with 0x, 42 chars |
| TRON | 79 | Starts with T, 34 chars |
| POLYGON | 137 | Starts with 0x, 42 chars |
| ARBITRUM | 42161 | Starts with 0x, 42 chars |
| OPTIMISM | 10 | Starts with 0x, 42 chars |
| SOLANA | solana | base58 encoded |
| TON | ton | Starts with EQ |

### Step 3: Call risk assessment API

After finding the token address and chainId, use the above API calling workflow for risk assessment.

⚠️ **Important**:
- If the user only provides token name (e.g., "SHIB") without address, you must first look up the token address
- If the user asks about different chains (e.g., USDT on BSC vs USDT on ETH), clarify which chain
- If the token doesn't exist on the current chain, inform the user and suggest other chains

## Usage Workflow

### Step 1: Get API keys

On first use, prompt the user for API keys:

```
Please provide your Beosin API keys:
- APPID: [Enter your APPID here]
- APP-SECRET: [Enter your APP-SECRET here]
```

⚠️ **Important: API keys are passed via HTTP Header, not URL parameters!**

### Step 2: Call Python script (the only recommended method)

**You must use `scripts/beosin_api.py` script to call the API!** Using curl or creating temporary scripts is not allowed.

Examples:

```bash
# Script path: /Users/edy/Downloads/Skill/.trae/skills/beosin-kyt-risk-assessment/scripts/beosin_api.py

# Address risk assessment
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET address-v4 79 address

# Deposit transaction assessment
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET deposit-v4 1 tx_hash

# Withdraw transaction assessment
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET withdraw-v4 1 tx_hash
```

### Step 3: Call API and generate report (strictly follow "Output Format Requirements" section)

The script will directly output formatted risk assessment results after execution, format follows the "Output Format Requirements" section:

⚠️ **Important: You must use `scripts/beosin_api.py` script to call the API! Using curl commands or creating temporary scripts is prohibited!**

Based on the parameter type provided by the user, automatically select the appropriate API endpoint:
- Provide `address` → Call address risk assessment (KYA)
- Provide transaction `hash` and user mentions "deposit"/"deposit funds" → Call deposit transaction risk assessment (KYT Deposit)
- Provide transaction `hash` and user mentions "withdraw"/"withdraw funds" → Call withdraw transaction risk assessment (KYT Withdraw)

Use V4 version preferentially to get more detailed entity information and hop count data.

#### API Endpoint Reference (for reference only, script already encapsulates)

**Address Risk Assessment (KYA V4)**: `GET https://api.beosin.com/api/v4/kyt/address/risk`

**Deposit Transaction Risk Assessment (KYT V4)**: `GET https://api.beosin.com/api/v4/kyt/tx/deposit`

**Withdraw Transaction Risk Assessment (KYT V4)**: `GET https://api.beosin.com/api/v4/kyt/tx/withdraw`

## Supported Blockchain Networks

Beosin API supports the following blockchains:

| Chain ID | Blockchain | Support Type |
|----------|--------|----------|
| 0 | BTC | Full Query |
| 1 | ETH | Full Query |
| 56 | BSC | Full Query |
| 79 | Tron | Full Query |
| 137 | Polygon | Full Query |
| 43114 | Avalanche | Full Query |
| 42161 | Arbitrum | Full Query |
| 10 | Optimism | Full Query |
| 227 | LTC | Full Query |
| Aptos | Aptos | Full Query |
| 8217 | Kaia | Full Query |
| 4200 | Merlin | Basic Query |
| Solana | Solana | Full Query |
| 888 | Neo | Basic Query |
| TON | TON | Full Query |
| 1030 | Conflux (eSpace) | Basic Query |
| XRP | XRP | Full Query |
| 324 | Zksync | Full Query |
| 4689 | IoTeX | Full Query |
| 810180 | Zklink | Basic Query |
| 534352 | Scroll | Basic Query |
| 2020 | Ronin | Basic Query |
| 59144 | Linea | Basic Query |
| 80084 | Berachain | Basic Query |
| Monad | Monad | Basic Query |
| 592 | Astar | Basic Query |
| 167000 | Taiko | Basic Query |
| 200901 | Bitlayer | Basic Query |
| 54176 | Over | Basic Query |
| Aleo | Aleo | Basic Query |
| Avail | Avail | Basic Query |
| Kaska | Kaska | Basic Query |
| Movement | Movement | Basic Query |
| Sui | Sui | Basic Query |
| 255 | Kroma | Basic Query |
| 8453 | Base | Basic Query |
| Tao | Tao | Basic Query |
| 48900 | ZRC | Basic Query |
| TIA | TIA | Basic Query |
| Peaq | Peaq | Basic Query |
| 6 | Supra | Basic Query |
| Arweave | Arweave | Basic Query |
| 1329 | Sei | Basic Query |
| 1111 | Wemix | Basic Query |
| 17777 | Eos | Basic Query |
| 994873017 | Lumia | Basic Query |
| 177 | Hsk | Basic Query |
| 88 | Viction | Basic Query |
| AO | AO | Basic Query |
| 1514 | Story | Basic Query |
| Autonomys | Autonomys | Basic Query |
| 146 | Sonic | Basic Query |
| Nillion | Nillion | Basic Query |
| Babylon | Babylon | Basic Query |
| 321 | KCC | Basic Query |
| Initia | Initia | Basic Query |
| 4352 | Memecore | Basic Query |
| 16661 | 0G | Basic Query |
| 9745 | Plasma | Basic Query |

**Note**:
- Full Query: Supports complete risk assessment data query
- Basic Query: Only supports address tag query

## Risk Level Description

All risk assessment results use the following unified risk levels:

| Level | Description |
|------|------|
| Severe | Severe risk |
| High | High risk |
| Medium | Medium risk |
| Low | Low risk |

## Response Field Description

### Address Risk Assessment Response Fields

| Field | Description |
|------|------|
| score | Total address score (0-100) |
| riskLevel | Risk level |
| incomingScore | Incoming risk score |
| incomingLevel | Incoming risk level |
| outgoingScore | Outgoing risk score |
| outgoingLevel | Outgoing risk level |
| incomingDetail | Incoming risk hit details |
| outgoingDetail | Outgoing risk hit details |
| entityDetails | Entity details (V4 new) |
| hops | Hop count (V4 new) |

## Important Notes

1. **API key transmission**: Must be passed via HTTP Header (`-H "APPID: xxx" -H "APP-SECRET: xxx"`), not URL parameters!
2. **API key security**: Do not expose user's API keys in logs or public places
3. **Parameter validation**: Validate address format and chainId before calling API
4. **Error handling**: Explain reasons to users and provide solutions when encountering error codes
5. **Response time**: Risk assessment API response time may be long (<30s), please inform user to wait patiently
6. **V4 features**: Use V4 version preferentially to get more detailed entity information and hop count data

## Error Code Handling

| Error Code | Description | Handling |
|--------|------|----------|
| 40001 | Parameter error | Check if request parameters are correct |
| 40002 | Empty appId | API key not passed correctly, confirm using HTTP Header method to pass APPID and APP-SECRET |
| 40021 | Platform not supported | Confirm if chainId is in supported list |
| 40022 | Address error | Check if address format is correct |
| 40023 | Transaction hash error | Check transaction hash format |
| 41023 | Transaction hash does not exist | Confirm if transaction is on-chain |
| 41024 | Non ERC-20 transaction not supported | Confirm token type |
| 41035 | Token not in basket | Token not currently supported |
| 41038 | Task executing | Retry later |

### Transaction Risk Assessment Response Fields

| Field | Description |
|------|------|
| score | Score |
| riskLevel | Risk level |
| risks | Hit risk list |
| riskStrategy | Risk strategy name |
| exposure | Exposure type (Direct/Indirect) |
| entityDetails | Entity details |

## Risk Analysis Interpretation Framework

You are an Anti-Money Laundering Compliance Officer assistant. You need to interpret the risk analysis results based on the assessment results (kyt_result, risk_level, risk_score).

### Required Content in Each Response

#### 1. Disclaimer (must state)
```
The following content is provided by AI for reference only.
```

#### 2. Risk Overview

Briefly summarize the most notable risks. If there are risk tags (riskTagLevel/riskTagDetails), then the address is a risk entity, highest priority.

#### 3. Risk Mitigation Suggestions

Combine regulatory requirements to provide compliance officers with reasonable handling suggestions.

### Output Format Requirements (Mandatory)

⚠️ **Must strictly follow the template below, no free formatting or omitting any sections!**

1. **Use colors for key information** for readability (use emoji or Markdown formatting)
2. **Standardize title hierarchy font size and paragraph spacing** for readability
3. Use clear hierarchical structure:
   - `#` Main title
   - `##` Secondary title  
   - `###` Tertiary title
   - `-` or `*` List items
4. **Don't squeeze different risk types on the same line**, display each risk type on a separate line

### Output Format Template (Address Risk Assessment)

```markdown
# Blockchain Address Risk Assessment Report

---

**The following content is provided by AI for reference only.**

## 🏷️ Risk Tags

> ⚠️ This address has been tagged as a risk entity!

| Tag Type | Description |
|----------|------|
| [Risk Tag 1] | [Description] |
| [Risk Tag 2] | [Description] |

## 📋 Assessment Overview

| Item | Information |
|------|------|
| Address | 0x... |
| Chain | Ethereum |
| Token Type | Native Token (ETH) / ERC-20 Token / Other |
| Risk Score | XX |
| Risk Level | 🔴 Severe / 🟠 High / 🟡 Medium / 🟢 Low |

## ⚠️ Risk Overview
### Risk Entity Details
- Risk Score: XX
- Risk Level: [Level]
- Risk Tags: XX

### Incoming Risk Details
- Risk Score: XX
- Risk Level: [Level]
- Hit Strategies:
  - [Strategy 1]: Ratio XX%, Amount $XX, Hops X
  - [Strategy 2]: Ratio XX%, Amount $XX, Hops X

### Outgoing Risk Details
- Risk Score: XX
- Risk Level: [Level]
- Hit Strategies:
  - [Strategy 1]: Ratio XX%, Amount $XX, Hops X
  - [Strategy 2]: Ratio XX%, Amount $XX, Hops X

## 💡 Risk Mitigation Suggestions

1. [Suggestion 1]
2. [Suggestion 2]
3. [Suggestion 3]

---
*Report generated at: YYYY-MM-DD HH:mm:ss*
```

### Output Format Template (Transaction Risk Assessment)

```markdown
# Blockchain Transaction Risk Assessment Report

---

**The following content is provided by AI for reference only.**

## 📋 Assessment Overview

| Item | Information |
|------|------|
| Transaction Hash | 0x... |
| Chain | Ethereum |
| Transaction Direction | Deposit / Withdraw |
| Token Type | Native Token (ETH) / ERC-20 Token / Other |
| Risk Score | XX |
| Risk Level | 🔴 Severe / 🟠 High / 🟡 Medium / 🟢 Low |

## ⚠️ Risk Details

### Hit Risk List

| Risk Strategy | Risk Level | Hops | Exposure Type | Ratio | Amount |
|----------|----------|------|----------|------|------|
| [Strategy 1] | [Level] | X | Direct/Indirect | XX% | $XX |
| [Strategy 2] | [Level] | X | Direct/Indirect | XX% | $XX |

### Entity Details

- [Entity Name]: Hops X, Wash Amount $XX, Wash Ratio XX%

## 💡 Risk Mitigation Suggestions

1. [Suggestion 1]
2. [Suggestion 2]
3. [Suggestion 3]

---
*Report generated at: YYYY-MM-DD HH:mm:ss*
```

## Windows Compatibility

This Skill uses Python scripts for API calls, cross-platform compatibility has been handled. Windows users don't need additional configuration.

The script will automatically detect and adapt to Windows/macOS/Linux systems.