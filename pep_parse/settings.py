from constants import ORDER_PEP_PARSE_PIPELINE

BOT_NAME = 'pep_parse'

SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'

ROBOTSTXT_OBEY = True

FEEDS = {
    'results/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True
    },
}

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': ORDER_PEP_PARSE_PIPELINE,
}

NAME_SPIDER = 'pep'

ALLOWED_DOMAINS = ['peps.python.org']
START_URLS = ['https://peps.python.org/']
