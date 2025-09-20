# Dockerfile

# Dockerfile

# --- Stage 1: Builder ---
# 將 python:3.10-slim-bullseye 改為 python:3.12-slim-bullseye
FROM python:3.12-slim-bullseye AS builder

# ... (builder 階段的其他內容保持不變) ...

# --- Stage 2: Runtime ---
# 同樣，將這裡的 python:3.10-slim-bullseye 也改為 python:3.12-slim-bullseye
FROM python:3.12-slim-bullseye


# 設定環境變數，避免互動式提示
ENV DEBIAN_FRONTEND=noninteractive

# 安裝建置 TA-Lib 所需的系統套件
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    wget && \
    rm -rf /var/lib/apt/lists/*

# 下載 TA-Lib 原始碼並編譯安裝
WORKDIR /tmp
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install

# --- Stage 2: Runtime ---
# 使用一個乾淨的 Python 映像檔作為最終的執行環境
FROM python:3.10-slim-bullseye

# 從 builder 階段複製編譯好的 TA-Lib 函式庫
COPY --from=builder /usr/lib/libta_lib.so.0 /usr/lib/libta_lib.so.0
COPY --from=builder /usr/lib/libta_lib.so.0.0.0 /usr/lib/libta_lib.so.0.0.0

# 設定環境變數
ENV DEBIAN_FRONTEND=noninteractive

# 設定應用程式的工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝 Python 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有應用程式程式碼
COPY . .

# 暴露服務運行的端口 (Zeabur 會自動偵測並映射)
EXPOSE 8080

# 啟動應用程式的命令
# 使用 0.0.0.0 讓服務可以從容器外部被訪問
# Zeabur 會透過 $PORT 環境變數指定端口，如果沒有則使用 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT:-8080}"]