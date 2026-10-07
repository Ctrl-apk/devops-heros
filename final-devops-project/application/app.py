from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Config from environment variables (ConfigMap / Secret)
APP_ENV = os.getenv("APP_ENV", "development")
PORT = int(os.getenv("PORT", 5000))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to Final DevOps End-to-End Application!",
        "status": "online",
        "environment": APP_ENV
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "database": "connected" if DATABASE_URL else "disconnected"
    }), 200

@app.route("/api/v1/data", methods=["GET"])
def get_data():
    return jsonify({
        "service": "DevOps Final Project API",
        "items": [
            {"id": 1, "name": "CI/CD Pipeline", "status": "Passed"},
            {"id": 2, "name": "DevSecOps Gates", "status": "Enforced"},
            {"id": 3, "name": "Kubernetes Cluster", "status": "Running"},
            {"id": 4, "name": "GitOps ArgoCD", "status": "Synced"}
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
