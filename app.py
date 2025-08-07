from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Change to a secure key in production
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_response(user_input):
    user_input = user_input.lower()
    state = session.get("state", None)

    # Handle follow-up for reset password
    if state == "awaiting_reset_confirmation":
        if user_input in ["yes", "y", "yeah", "yep", "sure"]:
            session.pop("state", None)
            return ("🔒 To reset your password:<br>"
                    "Press <strong>Ctrl + Alt + Delete</strong>, then select <strong>‘Change a password’</strong>.")
        else:
            session.pop("state", None)
            return ("Okay! Please pick an option from my menu — I'm still learning and will be able to help with more issues soon! 😊")

    # Handle follow-up for soundbar
    if state == "awaiting_soundbar_confirmation":
        if user_input in ["yes", "y", "yeah", "yep", "sure"]:
            session.pop("state", None)
            return ("🔊 For soundbar issues:<br>"
                    "1️⃣ Make sure the soundbar is switched on.<br>"
                    "2️⃣ Check if it’s flashing green — that means it’s trying to connect.<br>"
                    "3️⃣ Ensure it’s paired with the correct device.")
        else:
            session.pop("state", None)
            return ("No problem! Please choose from the menu — I’m learning more every day! 😊")

    # Handle user saying thanks
    if any(phrase in user_input for phrase in ["thank you", "thanks", "thx", "ty"]):
        session["state"] = "awaiting_further_help"
        return ("You're very welcome! 😊 Do you need any more help? (yes/no)")

    # Handle if user says yes or no after thanks
    if state == "awaiting_further_help":
        if user_input in ["yes", "y", "yeah", "yep", "sure"]:
            session.pop("state", None)
            return ("Great! How can I assist you further?")
        else:
            session.pop("state", None)
            return ("No worries! Have a wonderful day! 🌟😊")

    # No active state, detect keywords and ask confirmation if needed
    if "reset" in user_input or "password" in user_input:
        session["state"] = "awaiting_reset_confirmation"
        return "Do you need help with resetting your password? (yes/no)"

    if "soundbar" in user_input:
        session["state"] = "awaiting_soundbar_confirmation"
        return "Are you having issues with your soundbar? (yes/no)"

    # Other common responses
    if "wifi" in user_input or "internet" in user_input:
        return ("📶 For Wi-Fi issues:<br>"
                "1️⃣ Forget the school Wi-Fi network.<br>"
                "2️⃣ Reconnect using your school username and password.<br>"
                "3️⃣ When asked for a CA Certificate, choose <strong>‘Do Not Validate’</strong>.<br>"
                "✅ You should now be connected!")

    if "printer" in user_input:
        return ("🖨️ For printer problems:<br>"
                "- Ensure the printer has paper and toner.<br>"
                "- Confirm you’re on the correct school Wi-Fi.<br>"
                "- Try restarting the printer.")

    if "email" in user_input:
        return ("📧 For email issues:<br>"
                "- Visit <a href='https://outlook.office.com' target='_blank'>Outlook Web</a>.<br>"
                "- Use your school login credentials.<br>"
                "- If forgotten, reset your password.")

    # Default fallback - super friendly
    return ("🤖 I'm sorry, I’m not quite sure about that. But no worries! You can always log a ticket by emailing <a href='mailto:helpdesk@dgc.co.za'>helpdesk@dgc.co.za</a>.<br>"
            "We're here to help you as best we can! Feel free to ask about resetting passwords, Wi-Fi, printers, soundbars, or email access. 😊")

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/get", methods=["POST"])
def chat():
    user_input = request.form["msg"]
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

