from flask import Flask, request, jsonify
import pandas as pd
import pandas_ta as ta

app = Flask(__name__)

@app.route("/indicators", methods=["POST"])
def indicators():
    data = request.json
    df = pd.DataFrame(data)

    if "close" not in df.columns or "date" not in df.columns:
        return jsonify({"error": "需要提供 date 與 close 欄位"}), 400

    # 轉換日期欄位
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df.set_index("date", inplace=True)

    # ========== 日線指標 ==========
    df["MA5"] = ta.sma(df["close"], length=5)
    df["MA20"] = ta.sma(df["close"], length=20)
    macd = ta.macd(df["close"])
    rsi = ta.rsi(df["close"], length=14)
    df = pd.concat([df, macd, rsi], axis=1)

    # ========== 週線資料 ==========
    df_week = df.resample("W").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum" if "volume" in df.columns else "first"
    }).dropna()

    # 週線指標
    df_week["W_MA5"] = ta.sma(df_week["close"], length=5)
    df_week["W_MA20"] = ta.sma(df_week["close"], length=20)
    w_macd = ta.macd(df_week["close"])
    w_rsi = ta.rsi(df_week["close"], length=14)
    df_week = pd.concat([df_week, w_macd, w_rsi], axis=1)

    # 輸出 JSON（把日線與週線分開）
    result = {
        "daily": df.reset_index().to_dict(orient="records"),
        "weekly": df_week.reset_index().to_dict(orient="records")
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
