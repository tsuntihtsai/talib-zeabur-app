from flask import Flask, request, jsonify
import pandas as pd
import pandas_ta as ta

app = Flask(__name__)

@app.route("/indicators", methods=["POST"])
def indicators():
    payload = request.json

    # 支援多檔股票：payload 可以是 list 或 dict
    stocks = []
    if isinstance(payload, dict):
        # 單一股票
        stocks.append(payload)
    elif isinstance(payload, list):
        # 多檔股票
        stocks = payload
    else:
        return jsonify({"error": "無效的 JSON 結構"}), 400

    results = []

    for stock_item in stocks:
        # 取得股票代碼與交易資料
        stock_code = stock_item.get("stock")
        data = stock_item.get("data")

        if not data or len(data) < 20:
            # 至少需要 20 筆資料計算 MA20
            results.append({
                "stock": stock_code,
                "error": f"資料筆數不足以計算技術指標，收到 {len(data) if data else 0} 筆"
            })
            continue

        df = pd.DataFrame(data)

        if "close" not in df.columns or "date" not in df.columns:
            results.append({
                "stock": stock_code,
                "error": "資料缺少 'date' 或 'close' 欄位"
            })
            continue

        # 轉換日期
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        df.set_index("date", inplace=True)

        # 日線技術指標
        df["MA5"] = ta.sma(df["close"], length=5)
        df["MA20"] = ta.sma(df["close"], length=20)
        df = pd.concat([df, ta.macd(df["close"]), ta.rsi(df["close"], length=14)], axis=1)

        # 加股票代碼
        df["stock"] = stock_code

        # 週線資料
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
            df_week = pd.concat([df_week, ta.macd(df_week["close"]), ta.rsi(df_week["close"], length=14)], axis=1)

        df_week["stock"] = stock_code

        # 將結果加入 results
        results.append({
            "stock": stock_code,
            "daily": df.reset_index().to_dict(orient="records"),
            "weekly": df_week.reset_index().to_dict(orient="records")
        })

    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
