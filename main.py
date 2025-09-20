FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# 安裝必要工具並編譯 TA-Lib C library
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential wget curl autoconf automake libtool pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
 && tar -xzf ta-lib-0.4.0-src.tar.gz \
 && cd ta-lib \
 && ./configure --prefix=/usr \
 && make \
 && make install \
 && cd .. \
 && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENV PORT 8080
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:$PORT --workers 1"]
