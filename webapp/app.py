from flask import Flask, render_template, request, redirect
import motor_control
from servo_control import open_all_servos, close_all_servos
import atexit
import io
import sys
from contextlib import redirect_stdout, redirect_stderr


atexit.register(motor_control.cleanup)

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
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer), redirect_stderr(buffer):
            print("$ python3 robot_controller.py")
            print("Traceback (most recent call last):", file=sys.stderr)
            1 / 0  # Intentional error
    except Exception as e:
        with redirect_stderr(buffer):
            print(f"{type(e).__name__}: {e}")
    
    # Format captured output
    raw_output = buffer.getvalue()
    highlighted = (
        raw_output.replace("Traceback", "<span class='error-text'>Traceback</span>")
                  .replace("ZeroDivisionError", "<span class='error-text'>ZeroDivisionError</span>")
                  .replace("File", "<span class='error-text'>File</span>")
                  .replace("line", "<span class='error-text'>line</span>")
    )
    return render_template("error.html", error_output=highlighted)

@app.route("/supplies")
def supplies():
    return render_template("supplies.html")

# Tracks whether the group is open or closed
all_open = False

@app.route("/toggle_all_servos", methods=["POST"])
def toggle_all_servos():
    global all_open
    try:
        channels = [0, 1, 2, 3]  # List of servo channels
        if all_open:
            close_all_servos(channels)
        else:
            open_all_servos(channels)
        all_open = not all_open
        return "Opened" if all_open else "Closed", 200
    except Exception as e:
        return str(e), 400

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

# Optional manual cleanup
'''
@app.teardown_appcontext
def cleanup(exception=None):
    motor_control.cleanup()
'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
