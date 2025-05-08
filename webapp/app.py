from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/control")
def control():
    return render_template("control.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/supplies")
def supplies():
    return render_template("supplies.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)