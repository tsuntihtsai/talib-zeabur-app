import os
from flask import Flask, request, jsonify
import pandas as pd
import talib

app = Flask(__name__)

@app.route("/")
def hello():
    return "TA-Lib service running"

@app.route("/indicators", methods=["POST"])
def indicators():
    payload = request.get_json(force=True)
    data = payload.get("data", [])
    cols = ["date","volume","amount","open","high","low","close","diff","trades"]
    df = pd.DataFrame(data, columns=cols)

    # 數字欄位清理
    for c in ["open","high","low","close","amount"]:
        df[c] = df[c].astype(str).str.replace(",", "").astype(float)
    df["volume"] = df["volume"].astype(str).str.replace(",", "").astype(float)

    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values

    # 常見指標計算
    df["SMA5"] = talib.SMA(close, timeperiod=5)
    df["SMA20"] = talib.SMA(close, timeperiod=20)
    df["RSI14"] = talib.RSI(close, timeperiod=14)
    macd, macd_signal, macd_hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    df["MACD"] = macd
    df["MACD_SIGNAL"] = macd_signal
    df["MACD_HIST"] = macd_hist
    upper, middle, lower = talib.BBANDS(close, timeperiod=20)
    df["BB_UPPER"] = upper
    df["BB_MIDDLE"] = middle
    df["BB_LOWER"] = lower
    df["ATR14"] = talib.ATR(high, low, close, timeperiod=14)
    df["OBV"] = talib.OBV(close, volume)

    return jsonify(df.tail(30).to_dict(orient="records"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
