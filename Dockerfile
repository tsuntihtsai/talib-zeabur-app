# Dockerfile (最終修正版)

# --- Stage 1: Builder ---
# 使用一個包含建置工具的基礎映像檔來編譯 TA-Lib
FROM python:3.12-slim-bullseye AS builder

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
    # 移除 --prefix=/usr 讓其安裝到預設位置 (通常是 /usr/local)
    ./configure && \
    make && \
    make install

# --- Stage 2: Runtime ---
# 使用一個乾淨的 Python 映像檔作為最終的執行環境
FROM python:3.12-slim-bullseye

# 從 builder 階段複製編譯好的 TA-Lib 函式庫
# 注意：來源路徑已改為 /usr/local/lib，這是最關鍵的修正
COPY --from=builder /usr/local/lib/libta_lib.so.0 /usr/local/lib/libta_lib.so.0
COPY --from=builder /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta_lib.so.0.0.0

# 執行 ldconfig 讓系統能正確找到函式庫，這一步也很重要
RUN ldconfig

# 設定環境變數
ENV DEBIAN_FRONTEND=noninteractive

# 設定應用程式的工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝 Python 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有應用程式程式碼
COPY . .

# 暴露服務運行的端口
EXPOSE 8080

# 啟動應用程式的命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT:-8080}"]