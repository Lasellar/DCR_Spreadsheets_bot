import asyncio
from pprint import pprint

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from utils.create_spreadsheet import create_spreadsheet
from settings import (
    BOT_TOKEN, API_HASH, API_ID
)

import markups


bot = Client('bot', bot_token=BOT_TOKEN, api_hash=API_HASH, api_id=API_ID)
users_states = dict()


@bot.on_message(filters.command('start') & ~filters.group & ~filters.service)
async def start_command(_, message: Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text='Для создания документа отправь команду /create',
        reply_to_message_id=None
    )


@bot.on_message(filters.private)
async def handle_messages(_, message: Message):
    user_dict = users_states.get(message.chat.id)
    if user_dict is None:
        users_states[message.chat.id] = {}
    user_state = users_states[message.chat.id].get('state')
    if message.text.lower() == '/create':
        users_states[message.chat.id]['state'] = 'waiting for date'
        await bot.send_message(
            chat_id=message.chat.id,
            text='Напиши дату ивента или нажми на одну из предложенных снизу',
            reply_markup=markups.m_date
        )
    elif message.text == '/drop':
        users_states[message.chat.id] = {'state': None}
        await bot.send_message(
            chat_id=message.chat.id, text='Все состояния сброшены',
            reply_markup=None
        )
    elif message.text == '/permanent_list':
        await bot.send_message(
            chat_id=message.chat.id, text='Сейчас постоянный список выглядит так:',
            reply_markup=None
        )
        await asyncio.sleep(1)
        users_states[message.chat.id]['state'] = 'waiting for permanent_list'
        with open('permanent_list.txt', 'r', encoding='utf-8') as file:
            permanent_list = file.read()
            await bot.send_message(
                chat_id=message.chat.id, text=permanent_list, reply_markup=None
            )
            await asyncio.sleep(1)
            await bot.send_message(
                chat_id=message.chat.id,
                text='- Скопируй текущий постоянный список\n'
                     '- Отправь измененный вариант обратно мне\n'
                     'Обязательно нужно соблюдать структуру. Все три '
                     'ячейки должны быть написаны через запятую: имя, '
                     'количество плюсов,внесено от. Если нужно оставить какую-то ячейку '
                     'пустой, нужно просто ничего не вписывать, но запятая обязательно '
                     'должна остаться, например строка "Игорь,," создаст строку только '
                     'с именем, без плюсов и "внесено от". После каждого человека обязательно'
                     'делать перенос строки',

            )
    elif user_state == 'waiting for permanent_list':
        new_permanent_list = message.text
        try:
            with open('permanent_list.txt', 'w', encoding='utf-8') as file:
                file.write(new_permanent_list)
            await bot.send_message(
                chat_id=message.chat.id,
                text='Постоянный список успешно обновлен'
            )
            users_states[message.chat.id]['state'] = None
        except Exception as e:
            await bot.send_message(
                chat_id=message.chat.id,
                text=f'Произошла ошибка при записи файла: {str(e)}'
            )
    elif user_state == 'waiting for date':
        users_states[message.chat.id]['date'] = message.text
        users_states[message.chat.id]['state'] = 'waiting for event title'
        await bot.send_message(
            chat_id=message.chat.id, text='Напиши название ивента'
        )
    elif user_state == 'waiting for event title':
        users_states[message.chat.id]['event_title'] = message.text
        users_states[message.chat.id]['state'] = 'waiting for time start'
        await bot.send_message(
            chat_id=message.chat.id, text='Напиши время открытия дверей',
            reply_markup=markups.m_time_start
        )
    elif user_state == 'waiting for time start':
        users_states[message.chat.id]['time_start'] = message.text
        users_states[message.chat.id]['state'] = 'waiting for time end'
        await bot.send_message(
            chat_id=message.chat.id, text='Напиши время закрытия входа',
            reply_markup=markups.m_time_end
        )
    elif user_state == 'waiting for time end':
        users_states[message.chat.id]['time_end'] = message.text
        users_states[message.chat.id]['state'] = 'waiting for presale init'
        await bot.send_message(
            chat_id=message.chat.id, text='Напиши кол-во браслетов А(пресейл)',
            reply_markup=markups.m_presale_init
        )
    elif user_state == 'waiting for presale init':
        users_states[message.chat.id]['presale_init'] = message.text
        users_states[message.chat.id]['state'] = 'waiting for cash init'
        await bot.send_message(
            chat_id=message.chat.id, text='Напиши кол-во браслетов B(нал)',
            reply_markup=markups.m_cash_init
        )
    elif user_state == 'waiting for cash init':
        users_states[message.chat.id]['cash_init'] = message.text
        users_states[message.chat.id]['state'] = 'waiting for card init'
        await bot.send_message(
            chat_id=message.chat.id, text='Напиши кол-во браслетов С(карты)',
            reply_markup=markups.m_card_init
        )
    elif user_state == 'waiting for card init':
        users_states[message.chat.id]['card_init'] = message.text
        users_states[message.chat.id]['state'] = 'waiting for price on doors'
        await bot.send_message(
            chat_id=message.chat.id, text='Напиши цену на входе(0 если пока неизветно)',
            reply_markup=markups.m_price_on_doors
        )
    elif user_state == 'waiting for price on doors':
        users_states[message.chat.id]['price_on_doors'] = message.text
        users_states[message.chat.id]['state'] = 'waiting for guest init'
        await bot.send_message(
            chat_id=message.chat.id, text='Напиши кол-во браслетов F(списки)',
            reply_markup=markups.m_guest_init
        )
    elif user_state == 'waiting for guest init':
        users_states[message.chat.id]['guest_init'] = message.text
        users_states[message.chat.id]['state'] = 'waiting for artist init'
        await bot.send_message(
            chat_id=message.chat.id, text='Напиши кол-во браслетов S(артисты)',
            reply_markup=markups.m_artist_init
        )
    elif user_state == 'waiting for artist init':
        users_states[message.chat.id]['artist_init'] = message.text
        users_states[message.chat.id]['state'] = 'waiting for staff init'
        await bot.send_message(
            chat_id=message.chat.id, text='Напиши кол-во браслетов T(стафф)',
            reply_markup=markups.m_staff_init
        )
    elif user_state == 'waiting for staff init':
        users_states[message.chat.id]['staff_init'] = message.text
        users_states[message.chat.id]['state'] = 'waiting for is rega'
        await bot.send_message(
            chat_id=message.chat.id, text='Будет рега? Да/Нет',
                reply_markup=markups.m_yes_no
        )
    elif user_state == 'waiting for is rega':
        answer = message.text.lower()
        if answer == 'нет':
            users_states[message.chat.id]['is_rega'] = False
            users_states[message.chat.id]['state'] = 'waiting for is rest'
            await bot.send_message(
                chat_id=message.chat.id, text='Будет ресторан? Да/Нет',
                reply_markup=markups.m_yes_no
            )
        elif answer == 'да':
            users_states[message.chat.id]['is_rega'] = True
            users_states[message.chat.id]['state'] = 'waiting for rega init'
            await bot.send_message(
                chat_id=message.chat.id, text='Напиши кол-во браслетов E(рега)',
                reply_markup=markups.m_rega_init
            )
    elif user_state == 'waiting for rega init':
        users_states[message.chat.id]['rega_init'] = message.text
        users_states[message.chat.id]['state'] = 'waiting for is rest'
        await bot.send_message(
            chat_id=message.chat.id, text='Будет ресторан? Да/Нет',
            reply_markup=markups.m_yes_no
        )
    elif user_state == 'waiting for is rest':
        answer = message.text.lower()
        if answer == 'нет':
            users_states[message.chat.id]['is_rest'] = False
            pprint(users_states)
            await create_and_send_spreadsheet(message.chat.id)
        elif answer == 'да':
            users_states[message.chat.id]['is_rest'] = True
            users_states[message.chat.id]['state'] = 'waiting for rest init'
            await bot.send_message(
                chat_id=message.chat.id, text='Напиши кол-во браслетов R(ресторан)',
                reply_markup=markups.m_rest_init
            )
    elif user_state == 'waiting for rest init':
        users_states[message.chat.id]['rest_init'] = message.text
        pprint(users_states)
        await create_and_send_spreadsheet(message.chat.id)


async def create_and_send_spreadsheet(chat_id):
    """Создает таблицу и отправляет ссылку пользователю"""
    msg: Message = await bot.send_message(
        chat_id=chat_id, text='Создаю таблицу'
    )
    animation_task = asyncio.create_task(animate_creation(msg))
    try:
        user_data = users_states[chat_id]
        spreadsheet_link = await create_spreadsheet(
            date=user_data.get('date'),
            event_title=user_data.get('event_title'),
            start_time=user_data.get('time_start'),
            end_time=user_data.get('time_end'),
            presale_init=user_data.get('presale_init'),
            cash_init=user_data.get('cash_init'),
            card_init=user_data.get('card_init'),
            guest_init=user_data.get('guest_init'),
            artist_init=user_data.get('artist_init'),
            staff_init=user_data.get('staff_init'),
            price_on_doors=user_data.get('price_on_doors'),
            rega_init=user_data.get('rega_init', '0'),
            rest_init=user_data.get('rest_init', '0'),
            is_rega=user_data.get('is_rega', False),
            is_rest=user_data.get('is_rest', False)
        )
        animation_task.cancel()
        await asyncio.sleep(0.5)
        final_text = (
            f"**{user_data.get('date')} {user_data.get('event_title')}**\n\n"
            f"[Открыть таблицу]({spreadsheet_link})"
        )
        print(spreadsheet_link)
        await msg.edit(final_text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        animation_task.cancel()
        await msg.edit(f"Произошла ошибка при создании таблицы: {str(e)}")
    users_states[chat_id] = {'state': None}


async def animate_creation(msg: Message):
    """Анимация многоточия в сообщении"""
    dots = 0
    base_text = "Создаю таблицу."
    try:
        while True:
            dots = (dots + 1) % 3
            text = base_text + "." * dots
            await msg.edit(text, reply_markup=None)
            await asyncio.sleep(0.3)
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    print('Бот запущен')
    bot.run()
