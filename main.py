from flask import Flask, request, render_template
import pywhatkit
import os
from openai import OpenAI
from flask import jsonify

#website link: http://127.0.0.1:5000/ !!!!!!!!

client = OpenAI(
  api_key="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"
)

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )

        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/individual", methods=["GET", "POST"])
def individual():
    if request.method == "POST":
        phone = request.form["phone"]
        message = request.form["message"]
        hour = int(request.form["hour"])
        minute = int(request.form["minute"])

        try:
            pywhatkit.sendwhatmsg(phone, message, hour, minute)
            return f"Message scheduled to {phone} at {hour}:{minute}."
        except Exception as e:
            return f"An error occurred while sending individual message: {e}"

    return render_template("individual.html")

@app.route("/group", methods=["GET", "POST"])
def group():
    if request.method == "POST":
        group_id = request.form["group_id"]
        message = request.form["message"]
        hour = int(request.form["hour"])
        minute = int(request.form["minute"])

        try:
            pywhatkit.sendwhatmsg_to_group(group_id, message, hour, minute)
            return f"Group message scheduled to {group_id} at {hour}:{minute}."
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template("group.html")

@app.route("/picture", methods=["GET", "POST"])
def picture():
    if request.method == "POST":
        phone = request.form["phone"]
        caption = request.form.get("caption", "")
        hour = int(request.form["hour"])
        minute = int(request.form["minute"])

        image_file = request.files["image"]
        image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(image_path)

        try:
            pywhatkit.sendwhats_image(
                receiver=phone,
                img_path=image_path,
                caption=caption,
                wait_time=15,
                tab_close=True,
                close_time=3
            )
            return f"Image scheduled to {phone} at {hour}:{minute}."
        except Exception as e:
            return f"An error occurred while sending image: {e}"

    return render_template("picture.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
