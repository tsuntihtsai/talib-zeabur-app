from flask import Flask, request, jsonify
import pandas as pd
import pandas_ta as ta

app = Flask(__name__)

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        data = request.json.get("data", [])
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # 假設傳入格式為：
        # data = [
        #   {"date": "2024-09-02", "open": 100, "high": 105, "low": 98, "close": 102, "volume": 10000},
        #   {"date": "2024-09-03", "open": 103, "high": 106, "low": 100, "close": 105, "volume": 12000},
        # ]

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])

        # 技術指標計算
        df["MA5"] = ta.sma(df["close"], length=5)
        df["MA20"] = ta.sma(df["close"], length=20)

        macd = ta.macd(df["close"], fast=12, slow=26, signal=9)
        df["MACD"] = macd["MACD_12_26_9"]
        df["MACD_signal"] = macd["MACDs_12_26_9"]
        df["MACD_hist"] = macd["MACDh_12_26_9"]

        df["RSI"] = ta.rsi(df["close"], length=14)

        # 輸出只回傳必要欄位
        output = df[["date", "close", "MA5", "MA20", "MACD", "MACD_signal", "MACD_hist", "RSI"]].dropna().to_dict(orient="records")

        return jsonify({"result": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "TA Indicator Service is running!"
