from tkinter.messagebox import NO
from twilio.twiml.messaging_response import MessagingResponse
from fastapi import Response

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from db.models.user import User, Status
from db.models.order import Order
from services.get_cake import get_menu, get_price

cake = {}


class Bot_DAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def helper_process(self, message, response: MessagingResponse):
        try:
            option = int(message)
            return option
        except:
            response.message("Please enter a valid response.")
            return Response(content=str(response), media_type="application/xml")

    async def fetch_user_by_phone(self, number: str):
        user = await self.db_session.execute(select(User).filter(User.phone == number))
        return user.scalar_one_or_none()

    async def process_flavour_mode(self, message, number, response: MessagingResponse):
        user = await self.fetch_user_by_phone(number)
        options = self.helper_process(message, response)

        if options == 0:
            user.status = Status.main_mode
            response.message(
                "You can choose from one of the options below: "
                "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                "To get our *address*"
            )

        elif 1 <= options <= 5:
            cake_details = await get_menu()
            cakes = cake_details["flavour"]
            selected_flavour = cakes[options - 1].title()

            response.message(
                f"You can select one of the following cake sizes to order: \n\n1️⃣ Small  \n2️⃣ Medium \n3️⃣ Large  \n0️⃣ Go Back"
            )

            user.status = Status.size_mode

            return selected_flavour

    async def process_size_mode(self, message, number, response: MessagingResponse):
        user = await self.fetch_user_by_phone(number)
        options = self.helper_process(message, response)

        if options == 0:
            user.status = Status.main_mode
            response.message(
                "You can choose from one of the options below: "
                "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                "To get our *address*"
            )

        elif 1 <= options <= 3:
            size_dict = {"1": "small", "2": "medium", "3": "large"}
            selected_size = size_dict[str(options)]

            cake = await get_menu()
            frosting = cake["frosting"]

            response.message(
                f"What frosting do you want to pair with it? We have: \n\n1️⃣ {frosting[0].title()}  \n2️⃣ {frosting[1].title()} \n3️⃣ {frosting[2].title()}\n4️⃣ {frosting[3].title()}  \n0️⃣ Go Back"
            )

            user.status = Status.frosting_mode

            return selected_size

    async def process_frosting_mode(self, message, number, response: MessagingResponse):
        user = await self.fetch_user_by_phone(number)
        options = self.helper_process(message, response)

        if options == 0:
            user.status = Status.main_mode
            response.message(
                "You can choose from one of the options below: "
                "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                "To get our *address*"
            )

        if 1 <= options <= 4:
            cake = await get_menu()
            frosting = cake["frosting"]
            selected_frosting = frosting[options - 1]
            topping = cake["topping"]

            response.message(
                f"Finally, let's pick a topping : \n\n1️⃣ {topping[0].title()}  \n2️⃣ {topping[1].title()} \n3️⃣ {topping[2].title()}\n4️⃣ {topping[3].title()}  \n0️⃣ Go Back"
            )

            user.status = Status.topping_mode

            return selected_frosting

    async def process_topping_mode(self, message, number, response: MessagingResponse):
        user = await self.fetch_user_by_phone(number)
        options = self.helper_process(message, response)

        if options == 0:
            user.status = Status.main_mode
            response.message(
                "You can choose from one of the options below: "
                "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                "To get our *address*"
            )

        if 1 <= options <= 4:
            cake = await get_menu()
            topping = cake["topping"]
            selected_topping = topping[options - 1]

            response.message(f"Tap  1️⃣ to confirm.\n0️⃣ Go Back")

            user.status = Status.price_mode

            return selected_topping

    async def confirm_price(
        self,
        message,
        number,
        size,
        flavour,
        frosting,
        topping,
        response: MessagingResponse,
    ):
        user = await self.fetch_user_by_phone(number)
        options = self.helper_process(message, response)

        if options == 0:
            user.status = Status.main_mode
            response.message(
                "You can choose from one of the options below: "
                "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                "To get our *address*"
            )
        elif options == 1:

            price = await get_price(size, flavour, frosting, topping)

            response.message(
                f"Your *{size}* *{flavour}* cake with *{frosting}* frosting and *{topping}* topping will cost *{price}$* \n 1️⃣ To check out.\n0️⃣ Go Back"
            )

            user.status = Status.get_name_mode

            return price

    async def process_name_mode(self, message, number, response: MessagingResponse):
        user = await self.fetch_user_by_phone(number)
        print(user)
        response.message("Please provide your name.")

        customer = message

        user.status = Status.get_email_mode

        return customer

    async def process_email_mode(self, message, number, response: MessagingResponse):
        user = await self.fetch_user_by_phone(number)
        response.message("Please provide your email address.")

        customer_email = message

        user.status = Status.ordered_mode

        return customer_email

    async def process_main_mode(self, message, number, response: MessagingResponse):
        user = await self.fetch_user_by_phone(number)

        if bool(user) == False:
            response.message(
                "Hi, thanks for contacting *The Red Velvet*.\nYou can choose from one of the options below: "
                "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                "To get our *address*"
            )

            customer = User(phone=number, status=Status.main_mode)
            self.db_session.add(customer)
            await self.db_session.flush()

        elif user.status == Status.main_mode:
            try:
                option = int(message)
            except:
                response.message("Please enter a valid response.")
                return Response(content=str(response), media_type="application/xml")

            if option == 1:
                response.message(
                    "You can contact us through phone or e-mail.\n\n*Phone*: 991234 56789 \n*E-mail* : contact@theredvelvet.io"
                )

            elif option == 2:
                response.message("You have entered *ordering mode*.")
                user.status = Status.ordering_mode

                menu = await get_menu()
                response.message(
                    f"You can select one of the following cakes to order: \n\n1️⃣ {menu['flavour'][0].title()}  \n2️⃣ {menu['flavour'][1].title()} \n3️⃣ {menu['flavour'][2].title()}"
                    f"\n4️⃣ {menu['flavour'][3].title()} \n5️⃣ {menu['flavour'][4].title()} \n0️⃣ Go Back"
                )

            elif option == 3:
                response.message("We work from *9 a.m. to 5 p.m*.")

            elif option == 4:
                response.message(
                    "We have multiple stores across the city. Our main center is at *4/54, Baker street*"
                )

            else:
                response.message("Please enter a valid response.")
        elif user.status == Status.ordering_mode:

            cake["flavour"] = await self.process_flavour_mode(message, number, response)
            print(cake, cake["flavour"])

        elif user.status == Status.size_mode:

            cake["size"] = await self.process_size_mode(message, number, response)
            print(cake, cake["size"])

        elif user.status == Status.frosting_mode:

            cake["frosting"] = await self.process_frosting_mode(
                message, number, response
            )
            print(cake, cake["frosting"])

        elif user.status == Status.topping_mode:

            cake["topping"] = await self.process_topping_mode(message, number, response)
            print(cake, cake["topping"])

        elif user.status == Status.price_mode:

            cake_flavour = cake["flavour"]
            cake_size = cake["size"]
            cake_frosting = cake["frosting"]
            cake_topping = cake["topping"]

            cake["price"] = await self.confirm_price(
                message,
                number,
                cake_size,
                cake_flavour,
                cake_frosting,
                cake_topping,
                response,
            )
            print(cake, cake["price"])

        elif user.status == Status.get_name_mode:
            name = await self.process_name_mode(number, message, response)
            print(name)

        elif user.status == Status.get_email_mode:
            email = await self.process_email_mode(number, message, response)
            print(email)

        return Response(content=str(response), media_type="application/xml")
