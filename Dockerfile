FROM python:3.11-slim

# 安裝系統必要套件 (包含 TA-Lib 需要的依賴)
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    wget \
    curl \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# 安裝 TA-Lib C library
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && make && make install && \
    cd .. && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# 建立工作目錄
WORKDIR /app

# 複製 requirements
COPY requirements.txt .

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# 啟動 Flask
CMD ["python", "app.py"]
