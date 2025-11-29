import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MASTER_ADMIN_ID = int(os.getenv("ADMIN_ID", ""))
GROUP_LINK = os.getenv("GROUP_LINK", "")
SITE_LINK = os.getenv("SITE_LINK", "")
WEBAPP_URL = os.getenv("WEBAPP_URL", "")
COACH_SUPPORT_CHANNEL = os.getenv("COACH_SUPPORT_CHANNEL", "")  # Set your private group ID
ADMIN_PANEL_PASSWORD = os.getenv("ADMIN_PANEL_PASSWORD", "crown2025")

PAYMENT_ACCOUNTS = {
    "Nigeria (Opay)": "Account: 6110749592\nBank: Opay\nName: Chike Eluem Olanrewaju",
    "Nigeria (Zenith)": "Account: 2267515466\nBank: Zenith Bank\nName: Chike Eluem Olanrewaju",
}

HELP_TOPICS = {
    "how_to_pay": {"label": "How to Pay", "type": "text", "text": "Video coming soon"},
    "register": {"label": "Registration Process", "type": "text", "text": "Step by step guide..."},
    "apply_coach": {"label": "Become a Coach", "type": "callback", "callback": "apply_coach"},
    "faq": {"label": "FAQs", "type": "faq"},
}
