FROM python:3.11-slim

WORKDIR /app

# 安裝 git（必要，因為要從 GitHub 拉 pandas-ta）
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
