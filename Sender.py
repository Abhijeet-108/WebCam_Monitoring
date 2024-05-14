import smtplib
from email.message import EmailMessage
from PIL import Image
from io import BytesIO

PASSWORD = "buvj oepp cmvv advx"
SENDER = "abhijeetkr889@gmail.com"
RECEIVER = "abhijeetkr889@gmail.com"

def get_image_type(image_bytes):
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            return img.format.lower()
    except Exception as e:
        print(f"Error determining image type: {e}")
        return None

def send_email(imagepath):
    email_message = EmailMessage()
    email_message["Subject"] = "New Person on Cam"
    email_message.set_content("Hey, we just saw a person on camera..")

    with open(imagepath, "rb") as file:
        content = file.read()

    image_type = get_image_type(content)
    if image_type:
        email_message.add_attachment(content, maintype="image", subtype=image_type)
    else:
        print("Failed to determine image type.")

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()

if __name__ == "__main__":
    send_email(imagepath="images/52.png")