from pyrogram.types import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove
)

from datetime import date, timedelta

m_date = ReplyKeyboardMarkup(
    keyboard=[
        [
            f'{(date.today()).strftime("%d.%m.%Y")}',
            f'{(date.today() + timedelta(days=1)).strftime("%d.%m.%Y")}',
            f'{(date.today() + timedelta(days=2)).strftime("%d.%m.%Y")}',
            f'{(date.today() + timedelta(days=3)).strftime("%d.%m.%Y")}',
        ]
    ],
    resize_keyboard=True
)

m_time_start = ReplyKeyboardMarkup(
    keyboard=[
        ['16:00', '17:00', '18:00', '19:00'],
        ['20:00', '21:00', '22:00', '23:00']
    ],
    resize_keyboard=True
)

m_time_end = ReplyKeyboardMarkup(
    keyboard=[
        ['02:00', '03:00', '04:00', '05:00'],
        ['02:30', '03:30', '04:30', '05:30']
    ],
    resize_keyboard=True
)

m_presale_init = ReplyKeyboardMarkup(keyboard=[['300', '400', '500', '600']],
    resize_keyboard=True)
m_cash_init = ReplyKeyboardMarkup(keyboard=[['50', '100', '200', '300']],
    resize_keyboard=True)
m_card_init = ReplyKeyboardMarkup(keyboard=[['50', '100', '200', '300']],
    resize_keyboard=True)
m_guest_init = ReplyKeyboardMarkup(keyboard=[['200', '300', '400', '500']],
    resize_keyboard=True)
m_artist_init = ReplyKeyboardMarkup(keyboard=[['100', '200', '300', '400']],
    resize_keyboard=True)
m_staff_init = ReplyKeyboardMarkup(keyboard=[['50', '100', '200', '300']],
    resize_keyboard=True)
m_yes_no = ReplyKeyboardMarkup(keyboard=[['Да', 'Нет']],
    resize_keyboard=True)
m_rega_init = ReplyKeyboardMarkup(keyboard=[['500', '600', '700', '800']],
    resize_keyboard=True)
m_rest_init = ReplyKeyboardMarkup(keyboard=[['500', '600', '700', '800']],
    resize_keyboard=True)
m_price_on_doors = ReplyKeyboardMarkup(keyboard=[['0']],
    resize_keyboard=True)
m_remove = ReplyKeyboardRemove()
