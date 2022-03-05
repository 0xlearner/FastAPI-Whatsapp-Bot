import os
from pathlib import Path
from dotenv import load_dotenv
from twilio.rest import Client


from db.models.order import Order

env_path = Path.home() / "wa-bot" / ".env"
load_dotenv(dotenv_path=env_path)


def send_cake_ready(order: Order):
    client = Client(
        username=os.getenv("TWILIO_SID"), password=os.getenv("TWILIO_API_KEY")
    )

    from_number = "whatsapp:+14155238886"
    to_number = order.users.phone
    message_body = f"You cake order's status code is READY FOR PICKUP"

    resp = client.messages.create(to=to_number, from_=from_number, body=message_body)
    if resp.error_message:
        raise Exception(f"Cannot send whatsapp message: {resp.error_message}.")
