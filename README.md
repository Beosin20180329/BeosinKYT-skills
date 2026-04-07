---
name: beosin-kyt-risk-assessment
description: Beosin KYT/KYA 区块链风险评估 Skill。当用户需要评估区块链地址或交易的风险等级时触发，包括地址风险评估、交易风险评估（存款/提款）等场景。使用此 Skill 帮助用户进行区块链合规和反洗钱风险分析。
---

# Beosin KYT/KYA 区块链风险评估 Skill

## 快速开始

⚡️ **最简调用方式（一行命令完成）**：

```bash
# 地址风险评估 (Tron 链)
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET address-v4 79 TNpK4NKPQTQsvMj4aDGR5nxabvFKWJ3m2E

# 存款交易风险评估
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET deposit-v4 1 0x...

# 提款交易风险评估
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET withdraw-v4 1 0x...
```

**完整流程（3 步）：**
1. 获取 API 密钥（向用户请求 APPID 和 APP-SECRET）
2. 一行命令调用脚本
3. 解析 JSON 结果并生成风险评估报告

## 概述

此 Skill 用于调用 Beosin KYT (Know Your Transaction) 和 KYA (Know Your Address) API，对区块链地址和交易进行风险评估。

## 触发场景

当用户提及以下内容时，应使用此 Skill：
- "评估这个地址的风险"
- "检查这个交易是否有风险"
- "KYT"、"KYA"
- "Beosin 风险评估"
- "区块链合规"、"AML"
- "交易风险"、"地址风险"

## 使用流程

### 步骤 1：获取 API 密钥

首次使用时，直接提示用户输入 API 密钥：

```
请提供您的 Beosin API 密钥：
- APPID: [请在此输入您的 APPID]
- APP-SECRET: [请在此输入您的 APP-SECRET]
```

⚠️ **重要：API 密钥通过 HTTP Header 传递，不是 URL 参数！**

### 步骤 2：调用 Python 脚本（唯一推荐方式）

**必须使用 `scripts/beosin_api.py` 脚本调用 API！** 不允许手动使用 curl 或创建临时脚本。

调用示例：

```bash
# 脚本路径：/Users/edy/Downloads/Skill/.trae/skills/beosin-kyt-risk-assessment/scripts/beosin_api.py

# 地址风险评估
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET address-v4 79 地址

# 存款交易评估
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET deposit-v4 1 交易哈希

# 提款交易评估
python scripts/beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET withdraw-v4 1 交易哈希
```

### 步骤 3：调用 API 并生成报告（严格参考“输出格式要求”章节）

脚本执行后会直接输出格式化的风险评估结果，格式参考“输出格式要求”章节。：


⚠️ **重要：必须使用 `scripts/beosin_api.py` 脚本调用 API！禁止使用 curl 命令或创建临时脚本！**

根据用户提供的参数类型，自动选择合适的 API 端点：
- 提供 `address` → 调用地址风险评估 (KYA)
- 提供交易 `hash` 且用户提及"存款"/"入金" → 调用存款交易风险评估 (KYT Deposit)
- 提供交易 `hash` 且用户提及"提款"/"出金" → 调用提款交易风险评估 (KYT Withdraw)

优先使用 V4 版本以获取更详细的实体信息和跳数数据。

#### API 端点参考（仅供查阅，脚本已封装）

**地址风险评估 (KYA V4)**: `GET https://api.beosin.com/api/v4/kyt/address/risk`

**存款交易风险评估 (KYT V4)**: `GET https://api.beosin.com/api/v4/kyt/tx/deposit`

**提款交易风险评估 (KYT V4)**: `GET https://api.beosin.com/api/v4/kyt/tx/withdraw`

## 支持的区块链网络

Beosin API 支持以下区块链：

| Chain ID | 区块链 | 支持类型 |
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
| aptos | Aptos | Full Query |
| 8217 | Kaia | Full Query |
| 4200 | Merlin | Basic Query |
| solana | Solana | Full Query |
| 888 | Neo | Basic Query |
| ton | TON | Full Query |
| 1030 | Conflux (eSpace) | Basic Query |
| xrp | XRP | Full Query |
| 324 | Zksync | Full Query |
| 4689 | IoTeX | Full Query |
| 810180 | Zklink | Basic Query |
| 534352 | Scroll | Basic Query |
| 2020 | Ronin | Basic Query |
| 59144 | Linea | Basic Query |
| 80084 | Berachain | Basic Query |
| monad | Monad | Basic Query |
| 592 | Astar | Basic Query |
| 167000 | Taiko | Basic Query |
| 200901 | Bitlayer | Basic Query |
| 54176 | Over | Basic Query |
| aleo | Aleo | Basic Query |
| avail | Avail | Basic Query |
| kaska | Kaska | Basic Query |
| movement | Movement | Basic Query |
| sui | Sui | Basic Query |
| 255 | Kroma | Basic Query |
| 8453 | Base | Basic Query |
| tao | Tao | Basic Query |
| 48900 | ZRC | Basic Query |
| tia |TIA | Basic Query |
| peaq | Peaq | Basic Query |
| 6 | Supra | Basic Query |
| arweave | Arweave | Basic Query |
| 1329 | Sei | Basic Query |
| 1111 | Wemix | Basic Query |
| 17777 | Eos | Basic Query |
| 994873017 | Lumia | Basic Query |
| 177 | Hsk | Basic Query |
| 88 | Viction | Basic Query |
| ao | AO | Basic Query |
| 1514 | Story | Basic Query |
| autonomys | Autonomys | Basic Query |
| 146 | Sonic | Basic Query |
| nillion | Nillion | Basic Query |
| babylon | Babylon | Basic Query |
| 321 | KCC | Basic Query |
| initiainitia | Initia | Basic Query |
| 4352 | Memecore | Basic Query |
| 16661 | 0G | Basic Query |
| 9745 | Plasma | Basic Query |

**说明**：
- Full Query：支持完整的风险评估数据查询
- Basic Query：仅支持地址标签查询

## 风险等级说明

所有风险评估结果统一使用以下风险等级：

| 等级 | 说明 |
|------|------|
| Severe | 严重风险 |
| High | 高风险 |
| Medium | 中风险 |
| Low | 低风险 |

## 响应字段说明

### 地址风险评估响应字段

| 字段 | 说明 |
|------|------|
| score | 地址总分 (0-100) |
| riskLevel | 风险等级 |
| incomingScore | 入金风险评分 |
| incomingLevel | 入金风险等级 |
| outgoingScore | 出金风险评分 |
| outgoingLevel | 出金风险等级 |
| incomingDetail | 入金命中风险详情 |
| outgoingDetail | 出金命中风险详情 |
| entityDetails | 实体详情（V4新增） |
| hops | 跳数（V4新增） |

## 注意事项

1. **API 密钥传递方式**：必须通过 HTTP Header 传递（`-H "APPID: xxx" -H "APP-SECRET: xxx"`），不是 URL 参数！
2. **API 密钥安全**：不要在日志或公开场合暴露用户的 API 密钥
3. **参数验证**：在调用 API 前验证地址格式和 chainId
4. **错误处理**：遇到错误码时向用户解释原因并提供解决方案
5. **响应时间**：风险评估接口响应时间可能较长（<30s），请告知用户耐心等待
6. **V4 特性**：优先使用 V4 版本以获取更详细的实体信息和跳数数据

## 错误码处理

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 40001 | 参数错误 | 检查请求参数是否正确 |
| 40002 | Empty appId | API 密钥未正确传递，请确认使用 HTTP Header 方式传递 APPID 和 APP-SECRET |
| 40021 | 平台不支持 | 确认 chainId 是否在支持列表中 |
| 40022 | 地址错误 | 检查地址格式是否正确 |
| 40023 | 交易哈希错误 | 检查交易哈希格式 |
| 41023 | 交易哈希不存在 | 确认交易是否已上链 |
| 41024 | 不支持非 ERC-20 交易 | 确认代币类型 |
| 41035 | 代币不在篮子中 | 该代币暂不支持 |
| 41038 | 任务执行中 | 稍后重试 |

### 交易风险评估响应字段

| 字段 | 说明 |
|------|------|
| score | 评分 |
| riskLevel | 风险等级 |
| risks | 命中风险列表 |
| riskStrategy | 风险策略名称 |
| exposure | 暴露类型 (Direct/Indirect) |
| entityDetails | 实体详情 |

## 风险分析解读框架

您是一个反洗钱合规官助手，需要根据本次评估的结果（kyt_result、risk_level、risk_score）对生成的风险分析结果进行解读。

### 每次回复必须包含的内容

#### 1. 免责声明（必须声明）
```
以下内容由AI提供，仅供参考。
```

#### 2. 风险概述
简要总结最值得关注的风险即可，如果存在风险标签（riskTagLevel/riskTagDetails），那么表明该地址即为风险实体，优先级最高。

#### 3. 风险缓解建议
结合监管要求，提供给合规官合理的处置建议。

### 输出格式要求（强制）

⚠️ **必须严格按照以下模板输出，禁止自由发挥或省略任何章节！**

1. **重点信息用颜色区分**以增加可读性（使用 emoji 或 Markdown 格式）
2. **规范标题等级的字体大小和段落间距**以增加可读性
3. 使用清晰的层级结构：
   - `#` 主标题
   - `##` 二级标题  
   - `###` 三级标题
   - `-` 或 `*` 列表项
4. **主要风险不同类型不要挤在同一行**，每种风险类型单独一行展示

### 输出格式模板（地址风险评估）

```markdown
# 区块链地址风险评估报告

---

**以下内容由AI提供，仅供参考。**

## 🏷️ 风险标签

> ⚠️ 该地址已被标记为风险实体！

| 标签类型 | 说明 |
|----------|------|
| [风险标签1] | [说明] |
| [风险标签2] | [说明] |

## 📋 评估概览

| 项目 | 信息 |
|------|------|
| 地址 | 0x... |
| 链 | Ethereum |
| 代币类型 | 原生代币 (ETH) / ERC-20 代币 / 其他 |
| 风险评分 | XX |
| 风险等级 | 🔴 Severe / 🟠 High / 🟡 Medium / 🟢 Low |

## ⚠️ 风险概述
### 风险实体详情
- 风险评分: XX
- 风险等级: [等级]
- 风险标签：XX

### 入金风险详情
- 风险评分: XX
- 风险等级: [等级]
- 命中策略:
  - [策略1]: 比例 XX%, 金额 $XX, 跳数 X
  - [策略2]: 比例 XX%, 金额 $XX, 跳数 X

### 出金风险详情
- 风险评分: XX
- 风险等级: [等级]
- 命中策略:
  - [策略1]: 比例 XX%, 金额 $XX, 跳数 X
  - [策略2]: 比例 XX%, 金额 $XX, 跳数 X

## 💡 风险缓解建议

1. [建议1]
2. [建议2]
3. [建议3]

---
*报告生成时间: YYYY-MM-DD HH:mm:ss*
```

### 输出格式模板（交易风险评估）

```markdown
# 区块链交易风险评估报告

---

**以下内容由AI提供，仅供参考。**

## 📋 评估概览

| 项目 | 信息 |
|------|------|
| 交易哈希 | 0x... |
| 链 | Ethereum |
| 交易方向 | 存款 / 提款 |
| 代币类型 | 原生代币 (ETH) / ERC-20 代币 / 其他 |
| 风险评分 | XX |
| 风险等级 | 🔴 Severe / 🟠 High / 🟡 Medium / 🟢 Low |

## ⚠️ 风险详情

### 命中风险列表

| 风险策略 | 风险等级 | 跳数 | 暴露类型 | 比例 | 金额 |
|----------|----------|------|----------|------|------|
| [策略1] | [等级] | X | Direct/Indirect | XX% | $XX |
| [策略2] | [等级] | X | Direct/Indirect | XX% | $XX |

### 实体详情

- [实体名称]: 跳数 X, 清洗金额 $XX, 清洗比例 XX%

## 💡 风险缓解建议

1. [建议1]
2. [建议2]
3. [建议3]

---
*报告生成时间: YYYY-MM-DD HH:mm:ss*
```

## Windows 兼容性

此 Skill 使用 Python 脚本进行 API 调用，已处理跨平台兼容性，Windows 用户无需额外配置。

脚本会自动检测并适配 Windows/macOS/Linux 系统。
