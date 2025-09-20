# 使用輕量級 Python 基底映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製需求檔並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# 啟動 Flask
CMD ["python", "app.py"]
