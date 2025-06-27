import mysql.connector
import pandas as pd

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Pratu@0125',  # Replace this with your actual password
    'database': 'report_db'
}

# Connect to MySQL and fetch data
try:
    conn = mysql.connector.connect(**db_config)
    query = "SELECT * FROM transactions"
    df = pd.read_sql(query, conn)
    conn.close()

    # Show data (optional)
    print(df)
# Export to Excel
    output_file = "C:/Users/pratiksha/OneDrive/Desktop/automation/report.xlsx"
    df.to_excel(output_file, index=False)
    print(f"[SUCCESS] Report saved to {output_file}")

except mysql.connector.Error as err:
    print(f"[DATABASE ERROR] {err}")
except Exception as e:
    print(f"[ERROR] Something went wrong: {e}")

import smtplib
from email.message import EmailMessage
import os

# Email configuration
EMAIL_ADDRESS = 'pratikshadanavale@gmail.com'       #  Replace with your email
EMAIL_PASSWORD = "vdjgwohbswnveqfn"  # Use app password if Gmail
TO_EMAIL = "prsdshingne1@gmail.com"            #  Replace with recipient email

# Create email message
msg = EmailMessage()
msg['Subject'] = 'Automated Transaction Report'
msg['From'] = EMAIL_ADDRESS
msg['To'] = TO_EMAIL
msg.set_content('Hi,\n\nPlease find the attached transaction report.\n\nRegards,\nAutomation Script')

# Attach Excel file
with open(output_file, 'rb') as f:
    file_data = f.read()
    file_name = os.path.basename(output_file)

msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

# Send the email using SMTP
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:  # For Gmail
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("[SUCCESS] Email sent successfully!")
except Exception as e:
    print(f"[ERROR] Failed to send email: {e}")
