import os
from email.message import EmailMessage
from smtplib import SMTP
import requests
from bs4 import BeautifulSoup

def get_top_100_movies():
    movies_list = [movie.text for movie in BeautifulSoup(requests.get('https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/').text, 'html.parser').select('h3')][::-1]
    with open("movies.txt", "w", encoding='utf-8') as file:
        file.write("\n".join(movies_list))

def send_email():
    message = EmailMessage()
    message["Subject"] = "Top 100 Movies"
    message["From"] = os.environ['SENDER_MAIL']
    message["To"] = os.environ["RECEIVER_MAIL"]
    message.set_content("This is the list of top 100 movies all time.")
    message.add_attachment(open("movies.txt").read(), filename="Top_100_movies.txt")

    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=os.environ['SENDER_MAIL'], password=os.environ['PASSWORD'])
        connection.send_message(message)

get_top_100_movies()
send_email()