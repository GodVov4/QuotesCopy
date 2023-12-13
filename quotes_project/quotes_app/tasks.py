import requests
from bs4 import BeautifulSoup
from celery import shared_task

from .models import Authors, Quotes, Tags


class Spider:
    start_url = 'https://quotes.toscrape.com'

    @staticmethod
    def get_page(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content

    def parse(self, url=None):
        print(url)
        if not url:
            url = self.start_url
        soup = BeautifulSoup(self.get_page(url), 'html.parser')
        for quote in soup.select('div.quote'):
            author_url = self.start_url + quote.select_one('span a')['href']
            author_data = self.get_data(author_url)
            author_obj, create_author = Authors.objects.get_or_create(fullname=author_data['fullname'],
                                                                      defaults=author_data)
            quote_text = quote.select_one('span.text').get_text(strip=True)
            quote_data = {
                'author': author_obj,
                'quote': quote_text
            }
            quote_obj, create_quote = Quotes.objects.get_or_create(quote=quote_data['quote'], defaults=quote_data)
            tags = quote.select('div.tags a')
            for tag in tags:
                tag_name = tag.get_text(strip=True)
                tag_obj, create_tag = Tags.objects.get_or_create(name=tag_name)
                quote_obj.tags.add(tag_obj)
        next_link = soup.select_one('li.next a')['href'] if soup.select_one('li.next a') else None
        if next_link:
            return self.parse(self.start_url + next_link)

    def get_data(self, url):
        soup = BeautifulSoup(self.get_page(url), 'html.parser')
        data = {
            'fullname': soup.select_one('h3').text.strip(),
            'born_date': soup.select_one('span.author-born-date').get_text(strip=True),
            'born_location': soup.select_one('span.author-born-location').get_text(strip=True),
            'description': soup.select_one('div.author-description').get_text(strip=True)
        }
        return data


@shared_task
def task():
    print('------------ work_process -----------')
    sync_authors = Spider()
    sync_authors.parse()
    print('---------------- done ---------------')
