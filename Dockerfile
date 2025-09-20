# 使用 Python 3.11 slim 版本
FROM python:3.11-slim

# 安裝必要套件
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製需求檔並安裝套件
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# 開放 Flask 預設埠
EXPOSE 5000

# 啟動 Flask
CMD ["python", "app.py"]
