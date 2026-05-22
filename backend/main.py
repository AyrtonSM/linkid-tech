from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from dotenv import load_dotenv
import os
from email.message import EmailMessage

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    email: str
    message: str

@app.post("/send-email")
async def send_email(data: EmailRequest):
    
    print(f"Email: {data.email}, Message: {data.message}")
    msg = EmailMessage()

    msg["Subject"] = "Contato do site Linkid Tech"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER
    msg["Reply-To"] = data.email
    msg.set_content("HTML email not supported. Please view this email in an HTML compatible email viewer.")
    msg.add_alternative(get_html(data), subtype="html")

    

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:

        server.starttls()

        server.login(
            EMAIL_USER,
            EMAIL_PASSWORD
        )

        server.send_message(msg)

   
    return {"status": "sent"}


@app.get("/api/hello")
async def hello():
    return {
        "message": "Hello from FastAPI"
    }

def get_html(data):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">

    <style>

        body {{
            background-color: #f4f7fb;
            font-family: Arial, Helvetica, sans-serif;
            padding: 40px;
            margin: 0;
        }}

        .container {{
            max-width: 700px;
            margin: auto;
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }}

        .header {{
            background: linear-gradient(135deg, #2563eb, #1e40af);
            padding: 40px;
            color: white;
            text-align: center;
        }}

        .header h1 {{
            margin: 0;
            font-size: 32px;
        }}

        .header p {{
            margin-top: 10px;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .card {{
            background: #f8fafc;
            border-radius: 12px;
            padding: 24px;
            margin-top: 24px;
            border-left: 5px solid #2563eb;
        }}

        .label {{
            font-size: 13px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }}

        .value {{
            font-size: 17px;
            color: #0f172a;
            word-break: break-word;
        }}

        .message {{
            margin-top: 16px;
            line-height: 1.7;
            white-space: pre-wrap;
        }}

        .footer {{
            text-align: center;
            padding: 24px;
            font-size: 13px;
            color: #94a3b8;
            border-top: 1px solid #e2e8f0;
        }}

        .button {{
            display: inline-block;
            margin-top: 30px;
            padding: 14px 24px;
            background: #2563eb;
            color: white !important;
            text-decoration: none;
            border-radius: 10px;
            font-weight: bold;
        }}

    </style>
</head>

<body>

    <div class="container">

        <div class="header">
            <h1>📩 New Contact Message</h1>
            <p>Your website received a new message</p>
        </div>

        <div class="content">

            <div class="card">
                <div class="label">Visitor Email</div>
                <div class="value">
                    {data.email}
                </div>
            </div>

            <div class="card">
                <div class="label">Message</div>

                <div class="value message">
                    {data.message}
                </div>
            </div>

            <a
                href="mailto:{data.email}"
                class="button"
            >
                Reply to Visitor
            </a>

        </div>

        <div class="footer">
            Sent automatically from your website contact form
        </div>

    </div>

</body>
</html>
    """