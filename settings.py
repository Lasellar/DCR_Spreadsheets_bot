import os
import ast

from aiogoogle.auth.creds import ServiceAccountCreds
from dotenv import load_dotenv

CREDENTIALS_FILE = 'google_credentials.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
load_dotenv()
TEMPLATE_URL_SECOND = os.environ.get('TEMPLATE_URL_SECOND')
TEMPLATE_URL_THIRD = os.environ.get('TEMPLATE_URL_THIRD')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
ME = os.environ.get('ME')
creds = ast.literal_eval(os.environ.get('CREDS'))
cred = ServiceAccountCreds(scopes=SCOPES, **creds)

VALUES_1SH_3ROW = (
    'Браслет', 'Цена', 'Было', 'Остаток', 'Прошло',
    'Итого(стат.)', 'Итого(факт.)', 'Расхождение'
)


def rgb_num(red: int, green: int, blue: int, alpha: int =1) -> dict:
    return {'red': red/255, 'green': green/255, 'blue': blue/255, 'alpha': alpha}


COLORS = {
    'l-g-1': rgb_num(217, 217, 217), # светло-серый (1)
    'l-g-2': rgb_num(239, 239, 239), # светло-серый (2)
    'l-y-3': rgb_num(255, 242, 204), # светло-желтый (3) А
    'l-y-2': rgb_num(255, 229, 153), # светло-желтый (2) А
    'l-v-3': rgb_num(217, 210, 233), # светло-фиолетовый (3) В, TAB
    'l-v-2': rgb_num(180, 167, 214), # светло-фиолетовый (2) В
    'l-p-3': rgb_num(234, 209, 220), # светло-пурпурный (3) С
    'l-p-1': rgb_num(194, 123, 160), # светло-пурпурный (1) С
    'l-b-1': rgb_num(111, 168, 220), # светло-синий (1) E
    'l-r-1': rgb_num(224, 102, 102), # светло-красный (1) R
    'l-r-2': rgb_num(234, 153, 153), # светло-красный (2)
    'l-gr-3': rgb_num(217, 234, 211), # светло-зеленый (3)
    'l-gr-2': rgb_num(182, 215, 168), # светло-зеленый (2)
    'g': rgb_num(0, 255, 0), # зеленый Полный итог
    'r': rgb_num(255, 0, 0), # красный TAB
    'o': rgb_num(255, 140, 0), # оранжевый TAB,
    'v': rgb_num(123, 104, 238), # фиолетовый TAB,
    'p': rgb_num(255, 0, 255), # пурпурный Все гости
    'b': rgb_num(0, 0, 0), # черный
    'w': rgb_num(255, 255, 255) # белый
}
