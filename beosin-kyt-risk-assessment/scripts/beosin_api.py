#!/usr/bin/env python3
"""
Beosin KYT/KYA API Call Script
For blockchain address and transaction risk assessment

Supported versions: V2, V3, V4
Authentication: V2/V3 uses Header auth, V4 requires SIGN auth
"""

import requests
import json
import sys
import argparse
from typing import Optional, Dict, Any, Tuple

BASE_URL = "https://api.beosin.com"

CHAIN_ID_MAP = {
    "btc": "0",
    "eth": "1",
    "bsc": "56",
    "tron": "79",
    "polygon": "137",
    "avalanche": "43114",
    "arbitrum": "42161",
    "optimism": "10",
    "ltc": "227",
    "aptos": "aptos",
    "kaia": "8217",
    "merlin": "4200",
    "solana": "solana",
    "neo": "888",
    "ton": "ton",
    "conflux": "1030",
    "xrp": "xrp",
    "zksync": "324",
    "iotex": "4689",
    "zklink": "810180",
    "scroll": "534352",
    "ronin": "2020",
    "linea": "59144",
    "berachain": "80084",
    "monad": "monad",
    "astar": "592",
    "taiko": "167000",
    "bitlayer": "200901",
    "over": "54176",
    "aleo": "aleo",
    "avail": "avail",
    "kaska": "kaska",
    "movement": "movement",
    "sui": "sui",
    "kroma": "255",
    "base": "8453",
    "tao": "tao",
    "zrc": "48900",
    "tia": "tia",
    "peaq": "peaq",
    "supra": "6",
    "arweave": "arweave",
    "sei": "1329",
    "wemix": "1111",
    "eos": "17777",
    "lumia": "994873017",
    "hsk": "177",
    "viction": "88",
    "ao": "ao",
    "story": "1514",
    "autonomys": "autonomys",
    "sonic": "146",
    "nillion": "nillion",
    "babylon": "babylon",
    "kcc": "321",
    "initia": "initiainitia",
    "memecore": "4352",
    "0g": "16661",
    "plasma": "9745",
}

CHAIN_NAME_MAP = {v: k for k, v in CHAIN_ID_MAP.items()}


def get_chain_id(chain: str) -> str:
    chain_lower = str(chain).lower()
    if chain_lower in CHAIN_ID_MAP:
        return CHAIN_ID_MAP[chain_lower]
    return str(chain)


def get_chain_name(chain_id: str) -> str:
    return CHAIN_NAME_MAP.get(str(chain_id), f"Unknown ({chain_id})")


def call_api(
    endpoint: str,
    params: Dict[str, Any],
    app_id: str,
    app_secret: str,
    api_version: str = "v3"
) -> Tuple[Dict[str, Any], str]:
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "APPID": app_id,
        "APP-SECRET": app_secret
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json(), api_version
    except requests.exceptions.Timeout:
        return {"code": -1, "msg": "Request timeout"}, api_version
    except requests.exceptions.RequestException as e:
        return {"code": -1, "msg": str(e)}, api_version


def address_risk_assessment_v3(
    app_id: str,
    app_secret: str,
    chain_id: str,
    address: str,
    token: Optional[str] = None
) -> Dict[str, Any]:
    params = {
        "chainId": chain_id,
        "address": address
    }
    if token:
        params["token"] = token
    else:
        params["token"] = ""
    return call_api("/api/v3/kyt/address/risk", params, app_id, app_secret, "v3")[0]


def address_risk_assessment_v4(
    app_id: str,
    app_secret: str,
    chain_id: str,
    address: str,
    token: Optional[str] = None
) -> Dict[str, Any]:
    params = {
        "chainId": chain_id,
        "address": address
    }
    if token:
        params["token"] = token
    result, _ = call_api("/api/v4/kyt/address/risk", params, app_id, app_secret, "v4")
    return result


def deposit_transaction_assessment_v3(
    app_id: str,
    app_secret: str,
    chain_id: str,
    tx_hash: str,
    token: Optional[str] = None
) -> Dict[str, Any]:
    params = {
        "chainId": chain_id,
        "hash": tx_hash
    }
    if token:
        params["token"] = token
    return call_api("/api/v3/kyt/tx/deposit", params, app_id, app_secret, "v3")[0]


def withdraw_transaction_assessment_v3(
    app_id: str,
    app_secret: str,
    chain_id: str,
    tx_hash: str,
    token: Optional[str] = None
) -> Dict[str, Any]:
    params = {
        "chainId": chain_id,
        "hash": tx_hash
    }
    if token:
        params["token"] = token
    return call_api("/api/v3/kyt/tx/withdraw", params, app_id, app_secret, "v3")[0]


def deposit_transaction_assessment_v4(
    app_id: str,
    app_secret: str,
    chain_id: str,
    tx_hash: str,
    token: Optional[str] = None
) -> Dict[str, Any]:
    params = {
        "chainId": chain_id,
        "hash": tx_hash
    }
    if token:
        params["token"] = token
    return call_api("/api/v4/kyt/tx/deposit", params, app_id, app_secret, "v4")[0]


def withdraw_transaction_assessment_v4(
    app_id: str,
    app_secret: str,
    chain_id: str,
    tx_hash: str,
    token: Optional[str] = None
) -> Dict[str, Any]:
    params = {
        "chainId": chain_id,
        "hash": tx_hash
    }
    if token:
        params["token"] = token
    return call_api("/api/v4/kyt/tx/withdraw", params, app_id, app_secret, "v4")[0]


def format_risk_result(result: Dict[str, Any], assessment_type: str = "address", api_version: str = "v3") -> str:
    if result.get("code") != 200:
        msg = result.get("msg", "Unknown error")
        if "Empty" in msg:
            return f"❌ API call failed: {msg}\n💡 Tip: Make sure to pass APPID and APP-SECRET via HTTP Header"
        return f"❌ API call failed: {msg}"

    data = result.get("data", {})
    output = []

    if assessment_type == "address":
        score = data.get("score", 0)
        risk_level = data.get("riskLevel", "Unknown")
        level_emoji = {"Severe": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(risk_level, "⚪")

        output.append(f"📊 Address Risk Assessment Result (API {api_version})")
        output.append(f"Risk Score: {score}")
        output.append(f"Risk Level: {level_emoji} {risk_level}")

        incoming_score = data.get("incomingScore")
        incoming_level = data.get("incomingLevel")
        if incoming_score is not None:
            output.append(f"\n📥 Incoming Risk:")
            output.append(f"  Score: {incoming_score}, Level: {incoming_level}")

        incoming = data.get("incomingDetail", [])
        if incoming:
            for item in incoming:
                strategy = item.get("strategyName", "Unknown")
                hops = item.get("hops", "N/A")
                exposure = item.get("exposure", "N/A")
                rate = item.get("rate", 0)
                amount = item.get("amount", 0)

                risk_details = item.get("riskDetails", [])
                if risk_details and api_version in ["v2", "v3"]:
                    for rd in risk_details:
                        rd_name = rd.get("riskName", "Unknown")
                        rd_rate = rd.get("rate", rate)
                        rd_amount = rd.get("amount", amount)
                        output.append(f"  - {strategy} ({rd_name}) | Hops: {hops} | Exposure: {exposure} | Ratio: {rd_rate*100:.2f}% | Amount: {rd_amount}")
                else:
                    output.append(f"  - {strategy} | Hops: {hops} | Exposure: {exposure} | Ratio: {rate*100:.2f}% | Amount: {amount}")

                entity_details = item.get("entityDetails", [])
                if entity_details:
                    output.append(f"    Entity Details:")
                    for entity in entity_details:
                        entity_name = entity.get("entityName", "Unknown")
                        entity_hops = entity.get("hops", "N/A")
                        purification_amount = entity.get("purificationAmountU", 0)
                        purification_rate = entity.get("purificationRate", 0)
                        output.append(f"      - {entity_name} (Hops: {entity_hops}, Amount: {purification_amount}, Ratio: {purification_rate*100:.4f}%)")

        outgoing_score = data.get("outgoingScore")
        outgoing_level = data.get("outgoingLevel")
        if outgoing_score is not None:
            output.append(f"\n📤 Outgoing Risk:")
            output.append(f"  Score: {outgoing_score}, Level: {outgoing_level}")

        outgoing = data.get("outgoingDetail", [])
        if outgoing:
            for item in outgoing:
                strategy = item.get("strategyName", "Unknown")
                hops = item.get("hops", "N/A")
                exposure = item.get("exposure", "N/A")
                rate = item.get("rate", 0)
                amount = item.get("amount", 0)

                risk_details = item.get("riskDetails", [])
                if risk_details and api_version in ["v2", "v3"]:
                    for rd in risk_details:
                        rd_name = rd.get("riskName", "Unknown")
                        rd_rate = rd.get("rate", rate)
                        rd_amount = rd.get("amount", amount)
                        output.append(f"  - {strategy} ({rd_name}) | Hops: {hops} | Exposure: {exposure} | Ratio: {rd_rate*100:.2f}% | Amount: {rd_amount}")
                else:
                    output.append(f"  - {strategy} | Hops: {hops} | Exposure: {exposure} | Ratio: {rate*100:.2f}% | Amount: {amount}")

                entity_details = item.get("entityDetails", [])
                if entity_details:
                    output.append(f"    Entity Details:")
                    for entity in entity_details:
                        entity_name = entity.get("entityName", "Unknown")
                        entity_hops = entity.get("hops", "N/A")
                        purification_amount = entity.get("purificationAmountU", 0)
                        purification_rate = entity.get("purificationRate", 0)
                        output.append(f"      - {entity_name} (Hops: {entity_hops}, Amount: {purification_amount}, Ratio: {purification_rate*100:.4f}%)")

        risk_tag_level = data.get("riskTagLevel")
        if risk_tag_level:
            output.append(f"\n🏷️ Risk Tag Level: {risk_tag_level}")
            risk_tag_details = data.get("riskTagDetails", [])
            if risk_tag_details:
                output.append(f"  Tags: {', '.join(risk_tag_details)}")

    elif assessment_type in ["deposit", "withdraw"]:
        score = data.get("score", 0)
        risk_level = data.get("riskLevel", "Unknown")
        level_emoji = {"Severe": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(risk_level, "⚪")

        direction = "📥 Deposit" if assessment_type == "deposit" else "📤 Withdraw"
        output.append(f"{direction} Transaction Risk Assessment Result (API {api_version})")
        output.append(f"Risk Score: {score}")
        output.append(f"Risk Level: {level_emoji} {risk_level}")

        risks = data.get("risks", [])
        if risks:
            output.append("\nHit Risks:")
            for risk in risks:
                strategy = risk.get("riskStrategy", "Unknown")
                risk_lvl = risk.get("riskLevel", "Unknown")
                hops = risk.get("hops", "N/A")
                exposure = risk.get("exposure", "N/A")
                rate = risk.get("rate", 0)
                amount = risk.get("amount", 0)
                output.append(f"  - {strategy} | Level: {risk_lvl} | Hops: {hops} | Exposure: {exposure} | Ratio: {rate*100:.2f}% | Amount: {amount}")

                entity_details = risk.get("entityDetails", [])
                if entity_details:
                    output.append(f"    Entity Details:")
                    for entity in entity_details:
                        entity_name = entity.get("entityName", "Unknown")
                        entity_hops = entity.get("hops", "N/A")
                        purification_amount = entity.get("purificationAmountU", 0)
                        purification_rate = entity.get("purificationRate", 0)
                        output.append(f"      - {entity_name} (Hops: {entity_hops}, Amount: {purification_amount}, Ratio: {purification_rate*100:.4f}%)")

    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Beosin KYT/KYA API Call Tool")
    parser.add_argument("--appid", "-i", help="Beosin API APPID")
    parser.add_argument("--secret", "-s", help="Beosin API APP-SECRET")
    parser.add_argument("command", nargs="?", help="Command: address-v3, address-v4, deposit-v3, deposit-v4, withdraw-v3, withdraw-v4")
    parser.add_argument("param1", nargs="?", help="chain_id or tx_hash")
    parser.add_argument("param2", nargs="?", help="address or token")
    parser.add_argument("param3", nargs="?", help="token (optional)")
    
    args = parser.parse_args()
    
    if not args.command:
        print("Usage: python beosin_api.py --appid <APPID> --secret <APP-SECRET> <command> <param1> [param2] [param3]")
        print("\nCommands:")
        print("  python beosin_api.py --appid xxx --secret xxx address-v4 79 0x...")
        print("  python beosin_api.py --appid xxx --secret xxx deposit-v4 1 0x...")
        print("  python beosin_api.py --appid xxx --secret xxx withdraw-v4 1 0x...")
        sys.exit(1)
    
    app_id = args.appid
    app_secret = args.secret
    
    if not app_id or not app_secret:
        print("Error: Please provide API keys via --appid and --secret parameters")
        print("Example: python beosin_api.py --appid YOUR_APPID --secret YOUR_SECRET address-v4 79 0x...")
        sys.exit(1)

    command = args.command

    if command == "address-v3" and args.param1 and args.param2:
        chain_id = args.param1
        address = args.param2
        token = args.param3 if args.param3 else None
        result = address_risk_assessment_v3(app_id, app_secret, chain_id, address, token)
        print(format_risk_result(result, "address", "v3"))

    elif command == "address-v4" and args.param1 and args.param2:
        chain_id = args.param1
        address = args.param2
        token = args.param3 if args.param3 else None
        result = address_risk_assessment_v4(app_id, app_secret, chain_id, address, token)
        print(format_risk_result(result, "address", "v4"))

    elif command == "deposit-v3" and args.param1 and args.param2:
        chain_id = args.param1
        tx_hash = args.param2
        token = args.param3 if args.param3 else None
        result = deposit_transaction_assessment_v3(app_id, app_secret, chain_id, tx_hash, token)
        print(format_risk_result(result, "deposit", "v3"))

    elif command == "deposit-v4" and args.param1 and args.param2:
        chain_id = args.param1
        tx_hash = args.param2
        token = args.param3 if args.param3 else None
        result = deposit_transaction_assessment_v4(app_id, app_secret, chain_id, tx_hash, token)
        print(format_risk_result(result, "deposit", "v4"))

    elif command == "withdraw-v3" and args.param1 and args.param2:
        chain_id = args.param1
        tx_hash = args.param2
        token = args.param3 if args.param3 else None
        result = withdraw_transaction_assessment_v3(app_id, app_secret, chain_id, tx_hash, token)
        print(format_risk_result(result, "withdraw", "v3"))

    elif command == "withdraw-v4" and args.param1 and args.param2:
        chain_id = args.param1
        tx_hash = args.param2
        token = args.param3 if args.param3 else None
        result = withdraw_transaction_assessment_v4(app_id, app_secret, chain_id, tx_hash, token)
        print(format_risk_result(result, "withdraw", "v4"))

    else:
        print("Invalid command or arguments")
        sys.exit(1)