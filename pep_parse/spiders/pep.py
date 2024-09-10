import scrapy

from pep_parse.items import PepParseItem
from pep_parse.settings import ALLOWED_DOMAINS, NAME_SPIDER, START_URLS


class PepSpider(scrapy.Spider):
    name = NAME_SPIDER
    allowed_domains = ALLOWED_DOMAINS
    start_urls = START_URLS

    def parse(self, response):
        all_peps_href = response.css(
            'a.pep.reference.internal::attr(href)'
        ).getall()
        for pep_href in all_peps_href:
            if pep_href.startswith('pep-') and pep_href.endswith('/'):
                yield response.follow(pep_href, callback=self.parse_pep)

    def parse_pep(self, response):
        pep_number = int(response.css('h1.page-title::text').re_first(r'\d+'))
        data = {
            'number': pep_number,
            'name': response.css('h1.page-title::text').get(),
            'status': response.css('abbr::text').get(),
        }
        yield PepParseItem(data)
