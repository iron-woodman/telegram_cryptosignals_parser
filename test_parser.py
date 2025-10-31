
import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient
from tlgparser import Signal

# Загрузка переменных окружения
load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
bot_token = os.getenv('bot_token')
destination_channel_id = int(os.getenv('destination_channel_id'))

# Создание тестового сигнала
test_signal_text = "BTC/USDT\nLONG\n65000.0"

async def main():
    # Инициализация клиента Telegram
    client = TelegramClient('bot_session', api_id, api_hash)
    await client.start(bot_token=bot_token)
    print("Клиент Telegram запущен...")

    try:
        # Создание и обработка сигнала
        signal = Signal(test_signal_text)
        signal.parse_signal()

        if signal.is_valid:
            new_signal_message = signal.form_new_signal()
            print("Сформировано тестовое сообщение:")
            print(new_signal_message)

            # Отправка сообщения
            await client.send_message(destination_channel_id, new_signal_message)
            print(f"Тестовое сообщение успешно отправлено в канал {destination_channel_id}")
        else:
            print("Не удалось обработать тестовый сигнал.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Отключение клиента
        await client.disconnect()
        print("Клиент Telegram остановлен.")

if __name__ == "__main__":
    asyncio.run(main())
