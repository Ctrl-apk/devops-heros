from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Hello World from Python CI Pipeline!",
        "status": "ok"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return jsonify({"result": a + b})


@app.route("/subtract/<int:a>/<int:b>")
def subtract(a, b):
    return jsonify({"result": a - b})


@app.route("/multiply/<int:a>/<int:b>")
def multiply(a, b):
    return jsonify({"result": a * b})


@app.route("/divide/<int:a>/<int:b>")
def divide(a, b):
    if b == 0:
        return jsonify({"error": "Cannot divide by zero"}), 400
    return jsonify({"result": a / b})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
