from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Service is running!"

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    # Zeabur 會把流量導向 container 的 5000 port
    app.run(host="0.0.0.0", port=5000)
