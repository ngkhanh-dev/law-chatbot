import requests
from bs4 import BeautifulSoup
import time
import random

def crawl_page(url):
    """
    Crawl text content from a given English webpage with anti-bot tricks.
    
    Args:
        url (str): The URL of the English webpage.
    
    Returns:
        list[dict]: Extracted text content from the page.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)
    time.sleep(random.uniform(2, 3))  
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = soup.find_all('div', class_='box-item-content')
    articles_data = []

    for _, article in enumerate(articles, start=1):
        # Collect author + time
        question_info = article.find('div', class_='box-item-top')
        name = question_info.find('span', class_='author').get_text(strip=True)
        time_info = question_info.find('span', class_='time').get_text(strip=True)

        # Collect question
        question_element = article.find('a', class_='question-title')
        question = question_element.get_text(strip=True)

        # Collect detail link
        detail_link = article.find('a', class_='box-viewmore')['href']
        detail_url = f"https://chinhsachonline.chinhphu.vn{detail_link}"

        # Request detail page (with delay)
        detail_response = requests.get(detail_url, headers=headers)
        time.sleep(random.uniform(2, 5)) 
        detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

        # Collect context
        context_div = detail_soup.find('div', class_='detail__cquestion')
        context = context_div.get_text(strip=True) if context_div else 'No context available'

        # Collect answer
        answer_div = detail_soup.find('div', class_='detail__rcontent')
        answer = answer_div.get_text(strip=True) if answer_div else 'No answer available'

        # Save data
        articles_data.append({
            'Name': name,
            'Time': time_info,
            'Question': question,
            'Situation': context,
            'Answer': answer,
        })

    return articles_data
