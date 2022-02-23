from fastapi import Request, Response, APIRouter
from twilio.twiml.messaging_response import MessagingResponse
from fastapi import Depends

from db.models.user import User
from db.models.order import Order

from web_hook.process import Bot_DAL
from depends import get_bot_db


router = APIRouter()


@router.post("/webhook")
async def web_hook(request: Request, data: Bot_DAL = Depends(get_bot_db)):

    incoming_msg = await request.form()
    message = incoming_msg.get("Body").strip().lower()
    number = incoming_msg.get("From").replace("whatsapp:", "")
    response = MessagingResponse()

    bot_response = await data.process_main_mode(message, number, response)
    return bot_response
