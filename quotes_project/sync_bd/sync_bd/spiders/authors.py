import scrapy


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {'FEED_FORMAT': 'json', 'FEED_URI': 'authors.json'}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response, **kwargs):
        for quote in response.xpath('/html//div[@class=\'quote\']'):
            yield response.follow(self.start_urls[0] + quote.xpath('span/a/@href').get(), self.about)
        next_link = response.xpath('//li[@class="next"]/a/@href').get()
        if next_link:
            yield scrapy.Request(self.start_urls[0] + next_link)

    @staticmethod
    def about(response, **kwargs):
        yield {
            'fullname': response.xpath('//h3/text()').get(),
            'born_date': response.xpath('//span[@class="author-born-date"]/text()').get(),
            'born_location': response.xpath('//span[@class="author-born-location"]/text()').get(),
            'description': response.xpath('//div[@class="author-description"]/text()').get().strip()
        }
