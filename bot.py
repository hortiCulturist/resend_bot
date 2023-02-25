import asyncio
import os
import uuid
from datetime import datetime
import datetime

from pyrogram import Client, filters, enums
from pyrogram.types import Message
import config

app = Client(name='resend',
             api_id=config.api_id,
             api_hash=config.api_hash)
print('bot started')


async def post(chat, start_time):
    from_chat = int(chat)
    t_now_date = datetime.datetime.now().date()
    t_start = datetime.datetime.strptime(start_time, '%Y %m %d')
    last_date_of_message, incrementor_date = 0, 0
    history = app.get_chat_history(chat_id=from_chat)

    messages_list = []
    async for message in history:
        if message.service or message.date <= t_start:
            continue
        messages_list.append(message)

    for message_from_list in messages_list[::-1]:
        if message_from_list.date.day != last_date_of_message:
            last_date_of_message = message_from_list.date.day
            incrementor_date += 1
        date_to_schedule = t_now_date + datetime.timedelta(days=incrementor_date)
        await app.copy_message(chat_id=from_chat,
                               from_chat_id=from_chat,
                               message_id=message_from_list.id,
                               schedule_date=message_from_list.date.replace(year=date_to_schedule.year,
                                                                            day=date_to_schedule.day,
                                                                            month=date_to_schedule.month))
        print(f"Время в сообщении - {message_from_list.date}\n"
              f"Дата постинга - {date_to_schedule}")


@app.on_message(filters.regex('^add'))  # add *id* *2022.12.12*
async def new_pattern(_, message: Message):
    text = message.text
    text = text.split('_')
    print(text)
    await app.send_message(message.from_user.id, 'Start')
    await post(text[1], text[2])
    await app.send_message(message.from_user.id, 'Done')


if __name__ == '__main__':
    app.run()
