# Парсер торговых сигналов для Telegram

Этот проект представляет собой Telegram-бота, написанного на Python с использованием библиотеки Telethon. Бот предназначен для автоматического мониторинга одного Telegram-канала (источника), извлечения из него торговых сигналов по криптовалюте, их модификации и последующей пересылки в другой Telegram-канал (назначения).

## Основной функционал

- **Мониторинг канала:** Бот в реальном времени отслеживает появление новых сообщений в указанном канале-источнике.
- **Парсинг сигналов:** При появлении нового сообщения, бот анализирует его текст, чтобы определить, является ли оно торговым сигналом. Он извлекает ключевые данные:
    - **Торговая пара:** Например, `BTC/USDT`.
    - **Тип сигнала:** `LONG` (покупка) или `SHORT` (продажа).
    - **Точка входа:** Цена, по которой рекомендуется открывать сделку.
- **Модификация сигнала:** После успешного парсинга, бот генерирует новое сообщение, изменяя исходные данные:
    - **Расчет новых целей (Take Profit):** Автоматически рассчитываются 5 новых целей для фиксации прибыли.
    - **Расчет нового Stop Loss:** Рассчитывается новый уровень стоп-лосса для ограничения убытков.
    - **Форматирование:** Сообщение оформляется с добавлением эмодзи и дополнительной информации о размере лота.
- **Ретрансляция:** Сформированное новое сообщение отправляется в канал-назначение.

## Инструкция по развертыванию на VPS (Ubuntu)

### 1. Подготовка

Убедитесь, что на вашем VPS установлены `python3`, `pip` и `git`.

```bash
sudo apt update
sudo apt install python3 python3-pip git python3-venv -y
```

### 2. Клонирование репозитория

Склонируйте репозиторий в удобную для вас директорию. Например, `/opt/telegram_parser`.

```bash
sudo git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ> /opt/telegram_parser
cd /opt/telegram_parser
```

### 3. Создание виртуального окружения и установка зависимостей

```bash
sudo python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Скопируйте файл `.env_example` в `.env`:

```bash
cp .env_example .env
```

Откройте файл `.env` и замените тестовые значения на ваши реальные:

```bash
sudo nano .env
```

Пример содержимого файла `.env`:

```ini
api_id=ВАШ_API_ID
api_hash=ВАШ_API_HASH
bot_token=ВАШ_БОТ_ТОКЕН
source_channel_id=ID_КАНАЛА_ИСТОЧНИКА
destination_channel_id=ID_КАНАЛА_НАЗНАЧЕНИЯ
```

- `api_id` и `api_hash`: Получите на [my.telegram.org](https://my.telegram.org).
- `bot_token`: Создайте бота и получите токен у [@BotFather](https://t.me/BotFather).
- `source_channel_id` и `destination_channel_id`: ID ваших каналов. Чтобы их узнать, можно добавить в канал бота [@userinfobot](https://t.me/userinfobot).

### 5. Настройка сервиса systemd для автозапуска

Мы будем использовать `systemd` для того, чтобы бот работал в фоновом режиме и автоматически перезапускался.

Создайте и откройте файл сервиса:

```bash
sudo nano /etc/systemd/system/tlg_parser.service
```

Вставьте в него следующее содержимое. **Обязательно** измените `WorkingDirectory` и `ExecStart` на ваши реальные пути, если вы клонировали репозиторий в другую директорию.

```ini
[Unit]
Description=Telegram Signals Parser Bot
After=network.target

[Service]
Type=simple
User=root
# Путь к директории вашего проекта
WorkingDirectory=/opt/telegram_parser
# Путь к python внутри вашего виртуального окружения и к главному файлу
ExecStart=/opt/telegram_parser/venv/bin/python3 /opt/telegram_parser/main.py
RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target
```

### 6. Запуск бота

После сохранения файла сервиса, выполните следующие команды:

```bash
# Перезагрузить конфигурацию systemd
sudo systemctl daemon-reload

# Запустить сервис
sudo systemctl start tlg_parser.service

# Добавить сервис в автозагрузку
sudo systemctl enable tlg_parser.service
```

### 7. Проверка статуса

Вы можете проверить, что бот работает, с помощью команды:

```bash
sudo systemctl status tlg_parser.service
```

Если все настроено правильно, вы увидите статус `active (running)`.

## Контакты для сотрудничества

Если у вас есть предложения по сотрудничеству или вопросы, вы можете связаться со мной:

- **Telegram (профиль):** [Мой_профиль_Telegram](https://t.me/alexandro_st)
- **Telegram (группа по разработке ботов):** [Telegram Bot | Разработка](https://t.me/avtomatizator30)
- **Электронная почта:** skobarev.aa@gmail.com
