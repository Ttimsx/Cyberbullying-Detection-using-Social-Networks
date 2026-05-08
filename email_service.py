import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_ADDRESS = "genemail421@gmail.com"
EMAIL_PASSWORD = "lpkjailbtoawixqg"


# ---------------- BASIC EMAIL ----------------

def send_email(to_email, subject, message):

    try:

        msg = MIMEText(message)

        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_ADDRESS,
            to_email,
            msg.as_string()
        )

        server.quit()

        print("✅ Email Sent")

        return True

    except Exception as e:

        print("❌ Email Error:", e)

        return False


# ---------------- REPORT EMAIL ----------------

def send_report_email(
        parent_email,
        parent_name,
        child_name,
        text,
        prediction,
        date
):

    try:

        message = f"""
Hello {parent_name},

📄 CYBERSHIELD REPORT

Child Name : {child_name}

Analyzed Message:
"{text}"

Prediction:
{prediction}

Date:
{date}

Regards,
CyberShield System
"""

        send_email(
            parent_email,
            "📄 CyberShield Report",
            message
        )

        return True

    except Exception as e:

        print("❌ Report Email Error:", e)

        return False