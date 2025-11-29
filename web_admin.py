from flask import Flask, request, render_template_string, session, url_for, redirect
from config.settings import ADMIN_PANEL_PASSWORD, MASTER_ADMIN_ID
from database.connection import cursor

app = Flask(__name__)
app.secret_key = "crown2025"

HTML = """
<!DOCTYPE html>
<html><head><title>FortuneX Admin Panel</title>
<style>body{font-family:Arial;background:#0e0e0e;color:#0f0;text-align:center;padding:50px;}
input,button{padding:12px;margin:10px;border-radius:8px;}</style></head>
<body>
<h1>FortuneX ADMIN PANEL</h1>
{% if not session.logged_in %}
<form method=post>
<input type=password name=pass placeholder="Enter Admin Password" style="width:300px;font-size:18px;">
<button type=submit style="background:#0f0;color:black;font-weight:bold;">LOGIN</button>
</form>
{% else %}
<h2>Coaches</h2><pre>{{ coaches }}</pre>
<h2>Recent Payments</h2><pre>{{ payments }}</pre>
<a href="/logout"><button style="background:#f00;color:white;">LOGOUT</button></a>
{% endif %}
</body></html>
"""

@app.route("/", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form.get("pass") == ADMIN_PANEL_PASSWORD:
            session["logged_in"] = True
        else:
            return "<h2>Wrong password!</h2>"

    if not session.get("logged_in"):
        return render_template_string(HTML)

    # Logged in — show data
    cursor.execute("SELECT chat_id, earnings, total_referrals FROM coaches ORDER BY earnings DESC LIMIT 20")
    coaches = cursor.fetchall()
    cursor.execute("SELECT chat_id, amount, package, status, timestamp FROM payments ORDER BY timestamp DESC LIMIT 30")
    payments = cursor.fetchall()

    return render_template_string(HTML, coaches=coaches, payments=payments)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
