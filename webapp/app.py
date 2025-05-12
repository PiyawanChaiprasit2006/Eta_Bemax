from flask import Flask, render_template, request
import motor_control

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

# Motor movement endpoint
@app.route("/move", methods=["POST"])
def move():
    direction = request.form.get("direction")
    try:
        if direction == "forward":
            motor_control.move_forward()
            return "Moving forward"
        elif direction == "backward":
            motor_control.move_backward()
            return "Moving backward"
        elif direction == "left":
            motor_control.turn_left()
            return "Turning left"
        elif direction == "right":
            motor_control.turn_right()
            return "Turning right"
        elif direction == "stop":
            motor_control.stop_motors()
            return "Motors stopped"
        else:
            return "Invalid direction", 400
    except Exception as e:
        return str(e), 500

# Clean up GPIO on shutdown
@app.teardown_appcontext
def cleanup(exception=None):
    motor_control.cleanup()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
