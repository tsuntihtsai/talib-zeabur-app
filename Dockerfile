# 使用 Python 3.12 slim
FROM python:3.12-slim

# 安裝必要套件
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安裝 TA-Lib C library
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && make && make install && \
    cd .. && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# 設定工作目錄
WORKDIR /app

# 複製需求檔並安裝 Python 套件
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# 開放 Flask 預設埠
EXPOSE 5000

# 啟動 Flask
CMD ["python", "app.py"]
