import os
import sys
import pandas as pd
import mysql.connector
from datetime import datetime
from email.message import EmailMessage
import smtplib

# Step 1: Fetch data from MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Pratu@0125',
    'database': 'report_db'
}

# 2. Create report file path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
media_dir = os.path.join(project_root, 'media', 'reports')
os.makedirs(media_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = os.path.join(media_dir, f"Report_{timestamp}.xlsx")

try:
    conn = mysql.connector.connect(**db_config)
    query = "SELECT * FROM transactions"
    df = pd.read_sql(query, conn)
    conn.close()

    df.to_excel(output_file, index=False)
    print(f"[SUCCESS] Report saved to {output_file}")

except mysql.connector.Error as err:
    print(f"[DATABASE ERROR] {err}")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Something went wrong: {e}")
    sys.exit(1)

# Step 3: Email the report
EMAIL_ADDRESS = 'pratikshadanavale@gmail.com'
EMAIL_PASSWORD = 'vdjgwohbswnveqfn'  # App password
TO_EMAIL = 'prsdshingne1@gmail.com'

msg = EmailMessage()
msg['Subject'] = 'Automated Transaction Report'
msg['From'] = EMAIL_ADDRESS
msg['To'] = TO_EMAIL
msg.set_content('Hi,\n\nPlease find the attached transaction report.\n\nRegards,\nAutomation Script')

# Attach the Excel report
with open(output_file, 'rb') as f:
    file_data = f.read()
    file_name = os.path.basename(output_file)
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("[SUCCESS] Email sent successfully!")
except Exception as e:
    print(f"[ERROR] Failed to send email: {e}")

# Step 4: Log the report in Django database
try:
    # Setup Django environment
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(project_root)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import django
    django.setup()

    from report_portal.reports.models import ReportLog

    ReportLog.objects.create(
        title=f"Automation Report - {timestamp}",
        report_file=f"reports/Report_{timestamp}.xlsx",
        status="Success"
    )
    print("✅ Report entry saved to Django database.")

except Exception as e:
    print(f"[ERROR] Failed to log report in Django: {e}")


import requests
import json

def send_log_to_django(job_name, status, build_no, log_output):
    url = 'http://127.0.0.1:8000/api/logs/'
    data = {
        "job_name": job_name,
        "status": status,
        "build_no": build_no,
        "log_output": log_output
    }

    try:
        res = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        print(f"[LOG API] Status: {res.status_code} | Response: {res.text}")
    except Exception as e:
        print(f"[LOG API ERROR] Failed to send log: {e}")


send_log_to_django("jenkins-email-report", "SUCCESS", 101, "Excel report generated and email sent.")
