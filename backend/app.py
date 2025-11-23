from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route("/stats")
def get_stats():
    data = {
        "cpu": psutil.cpu_percent(interval=0.5),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "net": {
            "sent": psutil.net_io_counters().bytes_sent,
            "recv": psutil.net_io_counters().bytes_recv
        }
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5040)

