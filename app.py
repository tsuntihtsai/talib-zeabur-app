from flask import Flask, request, jsonify
import pandas as pd
import pandas_ta as ta

app = Flask(__name__)

@app.route("/indicators", methods=["POST"])
def indicators():
    data = request.json

    # 從 HTTP Header 或額外傳入 stock
    stock_code = request.args.get("stock") or request.json.get("stock")

    # 處理單一物件輸入
    if isinstance(data, dict):
        data = [data]

    df = pd.DataFrame(data)

    if "close" not in df.columns or "date" not in df.columns:
        return jsonify({"error": "請求中需要包含 'date' 與 'close' 欄位"}), 400

    if len(df) < 20:
        return jsonify({"error": f"資料筆數不足以計算技術指標。至少需要 20 筆，但只收到 {len(df)} 筆。"}), 400

    # 轉換日期欄位並排序
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df.set_index("date", inplace=True)

    # 日線指標
    df["MA5"] = ta.sma(df["close"], length=5)
    df["MA20"] = ta.sma(df["close"], length=20)
    macd = ta.macd(df["close"])
    rsi = ta.rsi(df["close"], length=14)
    df = pd.concat([df, macd, rsi], axis=1)

    # 加股票代碼
    df["stock"] = stock_code

    # 週線資料
    if not isinstance(df.index, pd.DatetimeIndex):
        return jsonify({"error": "日期欄位轉換失敗，無法計算週線"}), 500

    df_week = df.resample("W-FRI").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum" if "volume" in df.columns else "first"
    }).dropna()

    if len(df_week) >= 20:
        df_week["W_MA5"] = ta.sma(df_week["close"], length=5)
        df_week["W_MA20"] = ta.sma(df_week["close"], length=20)
        w_macd = ta.macd(df_week["close"])
        w_rsi = ta.rsi(df_week["close"], length=14)
        df_week = pd.concat([df_week, w_macd, w_rsi], axis=1)

        # 週線也加股票代碼
        df_week["stock"] = stock_code

    result = {
        "daily": df.reset_index().to_dict(orient="records"),
        "weekly": df_week.reset_index().to_dict(orient="records")
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
