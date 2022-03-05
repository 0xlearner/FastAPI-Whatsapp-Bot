import base64
import uuid
import sendgrid
import os
from pathlib import Path
from dotenv import load_dotenv
import html2text
import jinja2
import pdfkit

from db.models.order import Order

env_path = Path.home() / "wa-bot" / ".env"
load_dotenv(dotenv_path=env_path)


def send_order_receipt(order: Order):
    client = sendgrid.SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))

    from_email = sendgrid.From("aun.abbas@cr-pl.com", "CRPL")
    to_email = sendgrid.To(order.users.email, order.users.name)
    subject = sendgrid.Subject("Your order receipt from cloud city cakes.")
    html = build_html("email/receipt.html", {"order": order})
    text = html2text.html2text(html)

    invoice_html = build_html("email/invoice.html", {"order": order})
    pdf = build_pdf(invoice_html)

    attachment = sendgrid.Attachment()
    attachment.file_content = pdf
    attachment.disposition = "attachment"
    attachment.file_type = "application/pdf"
    attachment.file_name = f"cloud-city-invoice-{order.id}.pdf"

    message = sendgrid.Mail(from_email, to_email, subject, text, html)
    message.add_attachment(attachment)

    response = client.send(message)

    if response.status_code not in {200, 201, 202}:
        raise Exception(f"Error sending email: {response.status_code}")

    print(
        f"Sent email successfully: Order {order.id} to {order.users.name} at {order.users.email}"
    )


def build_pdf(html: str) -> str:
    # Requires install from https://wkhtmltopdf.org/ in addition to pdfkit.
    temp_file = Path(__file__).parent.parent / (str(uuid.uuid4()) + ".pdf")

    pdfkit.from_string(html, str(temp_file))
    pdf_bytes = temp_file.read_bytes()

    encoded_pdf = base64.b64encode(pdf_bytes).decode("ascii")
    return encoded_pdf


def build_html(template_file: str, data: dict) -> str:
    template_folder = str(Path(__file__).parent.parent / "templates")
    loader = jinja2.FileSystemLoader(template_folder)
    env = jinja2.Environment(loader=loader)

    template: jinja2.Template = loader.load(env, template_file, None)
    html = template.render(**data)

    return html
