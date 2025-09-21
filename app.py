from flask import Flask, request, jsonify
import pandas as pd
import pandas_ta as ta

app = Flask(__name__)

@app.route("/indicators", methods=["POST"])
def indicators():
    data = request.json
    df = pd.DataFrame(data)

    if "close" not in df.columns:
        return jsonify({"error": "需要提供 close 價格欄位"}), 400

    # 計算技術指標
    df["MA5"] = ta.sma(df["close"], length=5)
    df["MA20"] = ta.sma(df["close"], length=20)
    macd = ta.macd(df["close"])
    rsi = ta.rsi(df["close"], length=14)

    # 合併結果
    df = pd.concat([df, macd, rsi], axis=1)

    return df.to_json(orient="records")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
