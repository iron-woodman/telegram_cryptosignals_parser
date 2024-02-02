from telethon import TelegramClient, events
import logging
import os
from dotenv import load_dotenv
from tlgparser import Signal


# load environment variables
load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
bot_token = os.getenv('bot_token')
source_channel_id = int(os.getenv('source_channel_id'))
destination_channel_id = int(os.getenv('destination_channel_id'))
# # test
# source_channel_id=-1002003304823
# destination_channel_id=-1001931294008


logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s:%(message)s')
# Создание экземпляра TelegramClient с использованием токена бота
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

async def send_mess(message):
    try:
        await client.send_message(entity=destination_channel_id, message=message)
        logging.info(f"New signal sent to tlg")
    except Exception as e:
        subject = getattr(e, 'message', '')
        print("send_mess exception:", subject)
        logging.error(f"send_mess exception: {subject}")

 # Определение обработчика событий для входящих сообщений из исходного канала
@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    # print(event.text)
    print('New message')
    signal = Signal(event.text)
    signal.parse_signal()
    if signal.is_valid:
        # print(json.dumps(signal.to_json(), indent=4))
        new_signal = signal.form_new_signal()
        print('New signal detected')
        await send_mess(message=new_signal)

# Запуск клиента
client.run_until_disconnected()
