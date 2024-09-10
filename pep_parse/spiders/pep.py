import re
import scrapy

from constants import GET_NUMBER_PEP
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps_href = response.css(
            'a.pep.reference.internal::attr(href)'
        ).getall()
        for pep_href in sorted(set(all_peps_href)):
            if re.fullmatch(r'^pep\-\d+\/$', pep_href) is None:
                continue
            yield response.follow(pep_href, callback=self.parse_pep)

    def parse_pep(self, response):
        data = {
            'number': re.search(
                r'\d+', response.css('h1.page-title::text').get()
            )[GET_NUMBER_PEP],
            'name': response.css('h1.page-title::text').get(),
            'status': response.css('abbr::text').get(),
        }
        yield PepParseItem(data)
