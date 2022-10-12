import requests
import smtplib
import os


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# You will need your own API keys saved in environment variables for this to work
STOCK_API_KEY = os.environ['STOCK_API_KEY']
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "datatype": "json",
    "apikey": STOCK_API_KEY
}

NEWS_API_KEY = os.environ['NEWS_API_KEY']
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY
}

MY_EMAIL = "test@yahoo.com"


def get_news():

    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)

    news_data = news_response.json()
    articles = news_data["articles"]
    three_articles = articles[:3]
    formatted_articles = [f"{STOCK} is {up_down} {abs(rounded_difference)}% \nHeadline: {article['title']}. \n" \
                          f"Summary: {article['description']}" for article in three_articles]
    print(formatted_articles)
    for article_number in range(0, 2):
        try:
            news_titles = news_data["articles"][article_number]["title"]
            news_descriptions = news_data["articles"][article_number]["description"]
            print(news_titles)
            print(news_descriptions)
            return news_descriptions
        except IndexError:
            pass


def send_email(news_descriptions):

    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password="testpassword")
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject: Stock alert\n\nThe stock price changed by {rounded_difference}. "
                f"Here are some news articles that might say why:\n{news_descriptions}")


stocks_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)

stock_data = stocks_response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]
today_stock_data = stock_data_list[0]
yesterday_stock_data = stock_data_list[1]

difference_in_stock = ((float(today_stock_data["4. close"]) - float(yesterday_stock_data["4. close"])) / float(today_stock_data["4. close"])) * 100
rounded_difference = (round(difference_in_stock, 2))
up_down = None

if rounded_difference > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"

# This will send the email with the news articles of the difference in stock prices is > 5%
if abs(rounded_difference) > 1:
    get_news()
    send_email(get_news())


