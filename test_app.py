from flask import Flask, jsonify, request

app = Flask(__name__)

password = "admin123"   # Hardcoded credential (Security issue)

@app.route("/")
def home():
    unused_variable = 100  # Code smell (unused variable)
    return jsonify({"message": "Flask SonarQube Integration Working!"})

@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    a = data.get("a", 0)
    b = data.get("b", 0)
    return jsonify({"result": a + b})

@app.route("/divide")
def divide():
    a = 10
    b = 0
    return jsonify({"result": a / b})  # Division by zero (Bug)

@app.route("/danger")
def danger():
    user_input = request.args.get("code")
    eval(user_input)   # Security vulnerability (Use of eval)
    return "Executed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)