from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/nifty-oi")
def get_oi():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)
    response = session.get(url, headers=headers)
    data = response.json()

    spot = data["records"]["underlyingValue"]
    strikes = data["records"]["strikePrices"]

    nearest = min(strikes, key=lambda x: abs(x - spot))
    idx = strikes.index(nearest)
    selected = strikes[max(0, idx - 2):idx + 3]

    result = []
    for d in data["records"]["data"]:
        if d["strikePrice"] in selected:
            ce = d.get("CE", {})
            pe = d.get("PE", {})
            result.append({
                "strike": d["strikePrice"],
                "ce_oi": ce.get("openInterest", 0),
                "ce_chg": ce.get("changeinOpenInterest", 0),
                "pe_oi": pe.get("openInterest", 0),
                "pe_chg": pe.get("changeinOpenInterest", 0),
            })

    return jsonify({
        "spot": spot,
        "data": result
    })
