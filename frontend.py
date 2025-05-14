from flask import Flask, render_template, request, jsonify
from medivance_backend import load_model, generate_response

app = Flask(__name__)
user_profile = {}

# Load the model once at startup
load_model("merged_tinyllama")

@app.route("/")
def profile():
    return render_template("profile.html")

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route("/set_profile", methods=["POST"])
def set_profile():
    data = request.get_json()
    print("📥 Received profile data:", data)  # 🔍 Debug here
    user_profile["name"] = data["name"]
    user_profile["age"] = data["age"]
    user_profile["gender"] = data["gender"]
    user_profile["conditions"] = data["conditions"]
    return jsonify({"message": "Profile set successfully."})

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    print("💬 Received user message:", user_input)  # 🔍 Debug here
    response = generate_response(user_input, user_profile)
    print("🤖 Response from backend:", response)    # 🔍 Debug here
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
