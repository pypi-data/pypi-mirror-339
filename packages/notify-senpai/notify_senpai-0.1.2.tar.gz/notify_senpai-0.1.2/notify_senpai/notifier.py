import subprocess
import importlib.resources as pkg_resources
from pathlib import Path
import time
import traceback
import io
from contextlib import redirect_stdout
# def notify(message=""):
#     """Send a desktop notification using notify.sh."""

#     # Get the correct path of notify.sh inside the installed package
#     with pkg_resources.path("notify", "notify.sh") as script_path:
#         subprocess.run([str(script_path), message], shell=False)

# # Example usage
# if __name__ == "__main__":
#     notify("Hello from Python package! 🎉")

# import subprocess
# import importlib.resources as pkg
# import smtplib
# from email.message import EmailMessage
import requests


# def send_email_notification(subject, body, recipients, smtp_config):
#     if not recipients or not smtp_config:
#         return

#     msg = EmailMessage()
#     msg.set_content(body)
#     msg['Subject'] = subject
#     msg['From'] = smtp_config['from_email']
#     msg['To'] = ', '.join(recipients)

#     try:
#         with smtplib.SMTP_SSL(smtp_config['server'], smtp_config['port']) as server:
#             server.login(smtp_config['login'], smtp_config['password'])
#             server.send_message(msg)
#             print("Email sent!")
#     except Exception as e:
#         print(f"Failed to send email: {e}")


def send_slack_notification(message, webhook_url):
    if not webhook_url:
        return
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("Slack message sent!")
        else:
            print(f"Slack notification failed: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Slack notification exception: {e}")


def notify_on_completion(slack_webhook_url=None, email_recipients=None, smtp_config=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            stdout_buffer = io.StringIO()
            try:
                with redirect_stdout(stdout_buffer):
                    result = func(*args, **kwargs)
                success = True
            except Exception:
                result = traceback.format_exc()
                success = False

            printed_output = stdout_buffer.getvalue()
            elapsed_time = time.time() - start_time
            status = "✅ Success" if success else "❌ Error"
            message = (
                f"{status}: {func.__name__} completed in {elapsed_time:.2f} seconds.\n\n"
                f"Printed Output:\n{printed_output}\n"
                f"Returned Output:\n{result if success else ''}\n"
                f"Error (if any):\n{'' if success else result}"
            )
            if slack_webhook_url:
                send_slack_notification(message, slack_webhook_url)
            with pkg_resources.path("notify_senpai", "notify.sh") as script_path:
                subprocess.run([str(script_path), message], shell=False)
            # send_email_notification(
            #     subject="Jupyter Cell Execution Completed",
            #     body=message,
            #     recipients=email_recipients,
            #     smtp_config=smtp_config
            # )
            return result
        return wrapper
    return decorator

def just_notify(message='', slack_webhook_url=None):
    """Send a desktop notification using notify.sh."""
    # Get the correct path of notify.sh inside the installed package
    with pkg_resources.path("notify_senpai", "notify.sh") as script_path:
        subprocess.run([str(script_path), message], shell=False)
    slack_message = message
    if slack_message == '':
        slack_message = 'execution done 🫡'
    if slack_webhook_url:
        send_slack_notification(slack_message, slack_webhook_url)