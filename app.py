from flask import Flask, request, jsonify
import pandas as pd
import pandas_ta as ta

app = Flask(__name__)

@app.route("/indicators", methods=["POST"])
def indicators():
    try:
        # 取得 JSON 資料
        data = request.get_json()
        if not data:
            return jsonify({"error": "請提供 JSON 資料"}), 400

        df = pd.DataFrame(data)

        # 確認有 close 欄位
        if "close" not in df.columns:
            return jsonify({"error": "資料中必須包含 'close' 欄位"}), 400

        # 計算技術指標
        df["MA5"] = ta.sma(df["close"], length=5)
        df["MA20"] = ta.sma(df["close"], length=20)
        
        # MACD
        macd = ta.macd(df["close"])
        df = pd.concat([df, macd], axis=1)

        # RSI
        df["RSI"] = ta.rsi(df["close"], length=14)

        # 回傳 JSON
        return df.to_json(orient="records")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        print("Flask啟動錯誤:", e)
