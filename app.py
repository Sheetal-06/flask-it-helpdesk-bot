from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_response(user_input):
    user_input = user_input.lower().strip()

    # Greeting
    if any(greet in user_input for greet in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]):
        return "Hello! 👋 How can I assist you with IT today?"

    # Polite thanks
    if any(phrase in user_input for phrase in ["thank you", "thanks", "thx", "ty"]):
        return "You're very welcome! 😊 Do you need any more help today?"

    # Separate follow-ups for reset password and soundbar
    if "reset" in user_input or "reset password" in user_input:
        return "Okay, do you need help with resetting your password? Please reply 'yes' or 'no'."

    if "soundbar" in user_input:
        return "Okay, do you need help with soundbar issues? Please reply 'yes' or 'no'."

    # Follow-up yes/no answer after reset or soundbar question
    if user_input in ["yes", "yeah", "yep", "sure", "of course"]:
        return ("Great! Here’s what to do:<br>"
                "- For resetting password: Press Ctrl + Alt + Del, then choose 'Change Password' and follow the prompts.<br>"
                "- For soundbar issues: Make sure the soundbar is switched on and the connection light is flashing green.")

    if user_input in ["no", "nah", "nope"]:
        return ("Okay, please pick an option from my menu — I'm still learning new issues and will assist more soon! 😊")

    # Projector help
    if "projector" in user_input:
        response = ("To fix projector display issues:<br>"
                    "1️⃣ Press Windows + P and select 'Duplicate' to mirror your screen.<br>"
                    "2️⃣ Make sure the projector is switched ON.<br>"
                    "3️⃣ Check if the projector has a power light.<br>"
                    "If there is NO light on the projector, it’s likely a power issue — please arrange for it to be checked.<br>"
                    "If none of these help, please <a href='https://mail.google.com/mail/?view=cm&fs=1&to=helpdesk@dgc.co.za' target='_blank'>email the helpdesk</a> and they’ll assist you further.")
        return response

    # Printing help
    if "print" in user_input or "printing" in user_input:
        return (
            "If you can’t print, have you checked your printing credits?<br>"
            "If you need credits, please "
            "<a href='https://mail.google.com/mail/?view=cm&fs=1&to=helpdesk@dgc.co.za&su=Request%20for%20Printing%20Credits&body=Hi,%0APlease%20may%20I%20have%20printing%20credits.%0AThank%20you!' target='_blank'>"
            "email the helpdesk via Gmail</a>."
        )

    # Common responses
    if "wifi" in user_input or "internet" in user_input:
        return ("For Wi-Fi issues:<br>"
                "1️⃣ Forget the network and reconnect.<br>"
                "2️⃣ Enter your username and password.<br>"
                "3️⃣ For CA certificate, select 'Don't validate'.<br>"
                "You should now be connected.")

    if "printer" in user_input:
        return ("For printer problems:<br>"
                "- Check that the printer has paper and toner.<br>"
                "- Make sure you’re connected to the school Wi-Fi.<br>"
                "- Restart the printer if needed.")

    if "email" in user_input:
        return ("For email help:<br>"
                "- Visit <a href='https://mail.google.com' target='_blank'>Gmail Webmail</a>.<br>"
                "- Log in with your school email and password.<br>"
                "- Reset your password if you forgot it.")

    # Friendly fallback for unknown queries
    return (
        "🤔 Hmm... I don't know that yet!<br>"
        "But no worries! 💡 Try picking something from my menu or asking about:<br>"
        "🖥️ Projectors<br>"
        "🖨️ Printing<br>"
        "🔒 Password resets<br>"
        "🔊 Soundbar help<br>"
        "📧 Or you can just send an email to the helpdesk right here:<br>"
        "<a href='https://mail.google.com/mail/?view=cm&fs=1&to=helpdesk@dgc.co.za' target='_blank'>📬 Click to email Helpdesk</a><br><br>"
        "I’m learning more every day! 🐣✨"
    )


@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/get", methods=["POST"])
def chat():
    user_input = request.form["msg"]
    response = get_response(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Use environment port if available, else 5000
    app.run(host="0.0.0.0", port=port, debug=True)

