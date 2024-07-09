from selenium import webdriver
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(vacant_seats, class_number):
    email = 'PRIMARY EMAIL'#EMAIL WILL SENT FROM THIS ADDRESS
    password = 'ENTER YOUR APP PASSWORD' #APP PASSWORD FOR THE ABOVE EMAIL
    send_to_email = 'ENTER YOUR EMAIL' #INFO ABOUT SEATS WILL BE SENT TO THIS EMAIL ADDRESS. (Both email addresses can be same).
    subject = 'Class Vacancy Notification'
    message = f"Vacant seats for class {class_number}: {vacant_seats}"

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()

    print("Email sent")


def check_class_availability(class_number):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    url = f'https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=C&honors=F&keywords={class_number}&promod=F&searchType=all&term=2247'
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    class_div = soup.find('div', class_='class-results-cell seats')

    if class_div:
        seats_info = class_div.find('div', class_='text-nowrap').text.strip()
        vacant_seats = seats_info.split()[0]
        print(vacant_seats)
    else:
        vacant_seats = '0'

    driver.quit()

    return vacant_seats


class_number = 78544 #Class number which you want to find seats for.
previous_vacant_seats = None

while True:
    vacant_seats = check_class_availability(class_number)
    print('sent')
    if previous_vacant_seats is None:
        previous_vacant_seats = vacant_seats

    if vacant_seats != previous_vacant_seats:
        send_email(vacant_seats, class_number)
        previous_vacant_seats = vacant_seats
    send_email(vacant_seats, class_number)
    time.sleep(60)  # Check every 1 minutes, you can change it according to your comfort.
