import datetime as dt
from pathlib import Path

'''Константы для загрузок'''
BASE_DIR = Path(__file__).parent
RESULTS = 'results'
PEP_STATUS = 'pep_status.csv'
DATE_TIME = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

'''Константы для функций'''
GET_NUMBER_PEP = 0
ORDER_PEP_PARSE_PIPELINE = 300
