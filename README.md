# Beosin KYT/KYA Blockchain Risk Assessment

A blockchain risk assessment tool using Beosin KYT (Know Your Transaction) and KYA (Know Your Address) APIs. This tool helps users perform blockchain compliance and anti-money laundering (AML) risk analysis.

## Features

- **Address Risk Assessment (KYA)**: Evaluate the risk level of blockchain addresses
- **Transaction Risk Assessment (KYT)**: Assess deposit and withdrawal transaction risks
- **Token Risk Lookup**: Query risk information for tokens like SHIB, USDT, USDC
- **Multi-chain Support**: Support for 50+ blockchain networks including Ethereum, BSC, Tron, Polygon, Solana, and more

## Quick Start

### Minimal Usage (One-liner)

```bash
# Address risk assessment (Tron chain)
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET address-v4 79 TNpK4NKPQTQsvMj4aDGR5nxabvFKWJ3m2E

# Deposit transaction risk assessment
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET deposit-v4 1 0x...

# Withdraw transaction risk assessment
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET withdraw-v4 1 0x...
```

## Prerequisites

- Python 3.7+
- Beosin API credentials (APPID and APP-SECRET)

### Get API Credentials

1. Sign up at [Beosin](https://www.beosin.com/)
2. Obtain your APPID and APP-SECRET
3. Pass credentials via HTTP Header (not URL parameters)

## Project Structure

```
beosin-kyt-risk-assessment/
├── SKILL.md                         # Skill definition and documentation
├── README.md                        # This file
├── scripts/
│   ├── beosin_api.py               # Main API call script
│   ├── txt                         # Token address lookup tool
│   └── currency_basket_output.json # Token address mappings
└── references/
    └── Beosin-Compliance-V4-API-Documentation.md  # API documentation
```

## Usage

### 1. Token Address Lookup

When users ask about token risk (e.g., SHIB, USDT), first look up the token contract address:

```bash
# Look up token address
python scripts/txt get_address ETH SHIB
python scripts/txt get_address BSC USDT
python scripts/txt get_address SOLANA BONK

# List all tokens on a chain
python scripts/txt list_tokens ETH

# List supported chains
python scripts/txt list_chains
```

### 2. Address Risk Assessment

```bash
# Address risk assessment (KYA)
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET address-v4 79 0x...
```

### 3. Transaction Risk Assessment

```bash
# Deposit transaction risk assessment (KYT)
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET deposit-v4 1 0x...

# Withdraw transaction risk assessment (KYT)
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET withdraw-v4 1 0x...
```

## Supported Blockchains

| Chain ID | Blockchain | Support Type |
|----------|------------|--------------|
| 0 | BTC | Full Query |
| 1 | ETH | Full Query |
| 56 | BSC | Full Query |
| 79 | Tron | Full Query |
| 137 | Polygon | Full Query |
| 43114 | Avalanche | Full Query |
| 42161 | Arbitrum | Full Query |
| 10 | Optimism | Full Query |
| solana | Solana | Full Query |
| ton | TON | Full Query |
| 324 | Zksync | Full Query |
| 8453 | Base | Full Query |
| ... | And 40+ more | Basic/Full Query |

**Note**: 
- Full Query: Complete risk assessment data
- Basic Query: Address tag query only

## Risk Levels

| Level | Description |
|-------|-------------|
| 🔴 Severe | Severe risk - immediate action required |
| 🟠 High | High risk - careful consideration needed |
| 🟡 Medium | Medium risk - monitor closely |
| 🟢 Low | Low risk - normal transaction |

## Error Handling

| Error Code | Description | Solution |
|------------|-------------|----------|
| 40001 | Parameter error | Check request parameters |
| 40002 | Empty appId | Use HTTP Header to pass APPID/SECRET |
| 40021 | Platform not supported | Verify chainId is supported |
| 40022 | Address error | Check address format |
| 40023 | Transaction hash error | Verify transaction hash format |
| 41023 | Transaction not on-chain | Confirm transaction is confirmed |
| 41035 | Token not in basket | Token not currently supported |

## Output Format

The script outputs formatted risk assessment results with:

- Risk score (0-100)
- Risk level (Severe/High/Medium/Low)
- Risk details including:
  - Strategy name
  - Hop count
  - Exposure type (Direct/Indirect)
  - Fund ratio
  - Entity details

## Windows Compatibility

This tool uses Python scripts with cross-platform compatibility. Windows users don't need additional configuration. The script automatically detects and adapts to Windows/macOS/Linux systems.

## License

This project is for educational and compliance purposes. Use responsibly.

## References

- [Beosin Official Website](https://www.beosin.com/)
- [Beosin API Documentation](https://beosinofficials-organization.gitbook.io/beosin-api-documentation/)
