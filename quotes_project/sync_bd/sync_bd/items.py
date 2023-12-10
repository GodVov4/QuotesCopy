# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from quotes_project.quotes_app.models import Authors, Quotes, Tags


class Author(DjangoItem):
    django_model = Authors


class Quote(DjangoItem):
    django_model = Quotes


class Tag(DjangoItem):
    django_model = Tags
