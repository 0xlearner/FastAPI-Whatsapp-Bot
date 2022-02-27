from twilio.twiml.messaging_response import MessagingResponse
from fastapi import Response

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from sqlalchemy import or_


from models.cake import Cake
from models.customer import Customer

from models.order import CakeOrder
from db.models.user import User, Status
from db.models.order import Order
from services.get_cake import get_menu, get_price

cake_dict = {}
customer_data = {}
cake_price = {}


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

    async def fetch_user(self, number: str, email: str):
        user = await self.db_session.execute(
            select(User).filter(or_(User.email == email, User.phone == number))
        )
        return user.scalar_one_or_none()

    async def record_order(self, u: Customer, c: Cake, price: float):
        user = await self.fetch_user(u.number, u.email)

        order = Order(
            **c.dict(),
            price=price,
            user_id=user.id,
        )
        self.db_session.add(order)
        await self.db_session.flush()

        return order

    async def process_flavour_mode(
        self, message, user: User, response: MessagingResponse
    ):
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
            cake_dict["flavour"] = selected_flavour

            response.message(
                f"You can select one of the following cake sizes to order: \n\n1️⃣ Small  \n2️⃣ Medium \n3️⃣ Large \n Type 'B' to go one step back  \n0️⃣ Go Back to Main"
            )

            user.status = Status.size_mode

            return cake_dict["flavour"]
        else:
            response.message("Please enter a valid response.")

    async def process_size_mode(self, message, user: User, response: MessagingResponse):
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
            cake_dict["size"] = selected_size

            cake = await get_menu()
            frosting = cake["frosting"]

            response.message(
                f"What frosting do you want to pair with it? We have: \n\n1️⃣ {frosting[0].title()}  \n2️⃣ {frosting[1].title()} \n3️⃣ {frosting[2].title()}\n4️⃣ {frosting[3].title()}  \n0️⃣ Go Back \n Type 'B' to go one step back"
            )

            user.status = Status.frosting_mode

            return cake_dict["size"]
        else:
            response.message("Please enter a valid response.")

    async def process_frosting_mode(
        self, message, user: User, response: MessagingResponse
    ):
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
            cake_dict["frosting"] = selected_frosting

            response.message(
                f"Finally, let's pick a topping : \n\n1️⃣ {topping[0].title()}  \n2️⃣ {topping[1].title()} \n3️⃣ {topping[2].title()}\n4️⃣ {topping[3].title()}  \n0️⃣ Go Back \n Type 'B' to go one step back"
            )

            user.status = Status.topping_mode

            return cake_dict["frosting"]
        else:
            response.message("Please enter a valid response.")

    async def process_topping_mode(
        self, message, user: User, response: MessagingResponse
    ):
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
            cake_dict["topping"] = selected_topping

            response.message(f"Tap  1️⃣ to confirm.\n0️⃣ Go Back")

            user.status = Status.price_mode

            return cake_dict["topping"]
        else:
            response.message("Please enter a valid response.")

    async def confirm_price(
        self,
        message,
        size,
        flavour,
        frosting,
        topping,
        user: User,
        response: MessagingResponse,
    ):
        options = self.helper_process(message, response)

        if options == 0:
            user.status = Status.main_mode
            response.message(
                "You can choose from one of the options below: "
                "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                "To get our *address*"
            )

        elif message != str(0):

            price = await get_price(size, flavour, frosting, topping)
            cake_price["price"] = price

            response.message(
                f"Your *{size}* *{flavour}* cake with *{frosting}* frosting and *{topping}* topping will cost *{price}$* \n\n\n Enter details to check out.\n\n\n0️⃣ Go Back"
            )

            response.message("Please provide your name.")
            # print(user.status, type(user.status))
            user.status = Status.get_name_mode
            # print(user.status, type(user.status))

            return cake_price["price"]

    async def process_name_mode(self, message, user: User, response: MessagingResponse):
        # options = self.helper_process(message, response)

        if message == str(0):
            user.status = Status.main_mode
            response.message(
                "You can choose from one of the options below: "
                "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                "To get our *address*"
            )

        else:
            customer_data["name"] = message
            user.name = customer_data["name"].title()
            response.message("Please provide your email address.")
            user.status = Status.get_email_mode
            return customer_data["name"]

    async def process_email_mode(
        self, message, user: User, response: MessagingResponse
    ):
        customer_data["email"] = ""

        if message == str(0):
            user.status = Status.main_mode
            response.message(
                "You can choose from one of the options below: "
                "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                "To get our *address*"
            )

        elif "@" not in message:
            response.message("Please enter a valid email address.")

        else:
            customer_data["email"] = message
            user.email = customer_data["email"]
            user.status = Status.order_review

            return customer_data["email"]

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

            await self.process_flavour_mode(message, user, response)

        elif user.status == Status.size_mode:

            if message.lower() == "b":
                user.status = Status.ordering_mode
                menu = await get_menu()
                response.message(
                    f"You can select one of the following cakes to order: \n\n1️⃣ {menu['flavour'][0].title()}  \n2️⃣ {menu['flavour'][1].title()} \n3️⃣ {menu['flavour'][2].title()}"
                    f"\n4️⃣ {menu['flavour'][3].title()} \n5️⃣ {menu['flavour'][4].title()} \n0️⃣ Go Back"
                )
            else:

                await self.process_size_mode(message, user, response)

        elif user.status == Status.frosting_mode:
            if message.lower() == "b":
                user.status = Status.size_mode
                response.message(
                    f"You can select one of the following cake sizes to order: \n\n1️⃣ Small  \n2️⃣ Medium \n3️⃣ Large \n Type 'B' to go one step back  \n0️⃣ Go Back to Main"
                )
            else:

                await self.process_frosting_mode(message, user, response)

        elif user.status == Status.topping_mode:
            if message.lower() == "b":
                user.status = Status.frosting_mode
                cake = await get_menu()
                frosting = cake["frosting"]

                response.message(
                    f"What frosting do you want to pair with it? We have: \n\n1️⃣ {frosting[0].title()}  \n2️⃣ {frosting[1].title()} \n3️⃣ {frosting[2].title()}\n4️⃣ {frosting[3].title()}  \n0️⃣ Go Back"
                )

            else:

                await self.process_topping_mode(message, user, response)

        elif user.status == Status.price_mode:

            if message.lower() == "b":
                user.status = Status.topping_mode
                cake = await get_menu()
                topping = cake["topping"]
                response.message(
                    f"Finally, let's pick a topping : \n\n1️⃣ {topping[0].title()}  \n2️⃣ {topping[1].title()} \n3️⃣ {topping[2].title()}\n4️⃣ {topping[3].title()}  \n0️⃣ Go Back"
                )
            else:

                cake_flavour = cake_dict["flavour"]
                cake_size = cake_dict["size"]
                cake_frosting = cake_dict["frosting"]
                cake_topping = cake_dict["topping"]

                await self.confirm_price(
                    message,
                    cake_size,
                    cake_flavour,
                    cake_frosting,
                    cake_topping,
                    user,
                    response,
                )

        elif user.status == Status.get_name_mode:

            await self.process_name_mode(message, user, response)

        elif user.status == Status.get_email_mode:
            await self.process_email_mode(message, user, response)

            cake_flavour = cake_dict["flavour"]
            cake_size = cake_dict["size"]
            cake_frosting = cake_dict["frosting"]
            cake_topping = cake_dict["topping"]
            price = cake_price["price"]
            email = customer_data["email"]
            name = customer_data["name"]
            customer_data["number"] = number

            if email:
                response.message(
                    f"*Review your order and Details:* \n\n\nName: {name} \nEmail: {email} \nPhone: {number} \n\n\n*Cake* \nFlavour: {cake_flavour}\nSize: {cake_size}\nFrosting: {cake_frosting}\nTopping: {cake_topping}\nPrice: {price}$ \n\n\n Tap  *[Y]* to confirm. \n\n Tap  *[N]* to cancel."
                )

        elif user.status == Status.order_review:

            if message.lower() != "y":
                user.status = Status.main_mode
                response.message(
                    "*Order cancelled successfully.*You can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*"
                )
            else:

                data = {
                    "customer": customer_data,
                    "cake": cake_dict,
                    "price": cake_price["price"],
                }
                print(data)
                print("Done!")

                cake_order = CakeOrder(**data)
                db_order = await self.record_order(
                    cake_order.customer, cake_order.cake, cake_order.price
                )
                response.message(
                    f"Thank you for your order!\n\n Your order_id is \n*{db_order.id}*"
                )
                user.status = Status.ordered

        elif user.status == Status.ordered:
            response.message(
                f"Hi, *{user.name}* thanks for contacting *The Red Velvet* again\nYou can choose from one of the options below: "
                "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                "To get our *address*"
            )
            user.status = Status.main_mode

        return Response(content=str(response), media_type="application/xml")
