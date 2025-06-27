# Jenkins Email Report Automation

This project automates the generation and delivery of an Excel report using:
- Python
- MySQL
- Pandas
- SMTP email
- Jenkins (CI/CD automation)

### Features:
- Fetches data from MySQL database
- Converts it into an Excel report
- Emails it automatically via Gmail
- Scheduled daily using Jenkins

### Setup Instructions:
1. Update MySQL credentials and Gmail App password in `send_report.py`
2. Install dependencies using:


pip install -r requirements.txt

