#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Jarvis - Telegram Bot для управления компьютером
Автор: AI Assistant
Версия: 2.0
"""

# =============================================================================
# ИМПОРТЫ
# =============================================================================

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from data import botToken
import os
import asyncio
import subprocess
import platform
import psutil
import time
from PIL import ImageGrab
import io
import logging

# =============================================================================
# КОНФИГУРАЦИЯ И КОНСТАНТЫ
# =============================================================================

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=botToken)
dp = Dispatcher(bot)

# Callback data для инлайн кнопок
volume_callback = CallbackData("volume", "action")

# Эмодзи для красивого интерфейса
EMOJIS = {
    'robot': '🤖',
    'computer': '💻',
    'volume': '🔊',
    'music': '🎵',
    'screenshot': '📸',
    'info': '📊',
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'play': '▶️',
    'pause': '⏸️',
    'next': '⏭️',
    'prev': '⏮️',
    'mute': '🔇',
    'unmute': '🔊',
    'up': '🔊',
    'down': '🔉',
    'system': '🖥️',
    'memory': '💾',
    'cpu': '⚡',
    'disk': '💿',
    'network': '🌐'
}

# =============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =============================================================================

def format_bytes(bytes_value):
    """Конвертирует байты в читаемый формат"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def get_system_uptime():
    """Получает время работы системы"""
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    return f"{hours}ч {minutes}м"

async def execute_command(command, success_msg, error_msg):
    """Выполняет системную команду с обработкой ошибок"""
    try:
        subprocess.run(command, check=True)
        return success_msg
    except subprocess.CalledProcessError:
        return error_msg

# =============================================================================
# ОСНОВНЫЕ КОМАНДЫ
# =============================================================================

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    """Команда приветствия и главное меню"""
    welcome_text = f"""
{EMOJIS['robot']} <b>Добро пожаловать, {message.from_user.first_name}!</b>

{EMOJIS['computer']} <b>Jarvis Bot</b> - ваш персональный помощник для управления компьютером

<b>🎯 Основные возможности:</b>
• {EMOJIS['volume']} Управление звуком и музыкой
• {EMOJIS['screenshot']} Создание скриншотов
• {EMOJIS['info']} Мониторинг системы
• {EMOJIS['system']} Управление питанием

<b>📋 Быстрые команды:</b>
/volume - {EMOJIS['volume']} Управление звуком и музыкой
/screenshot - {EMOJIS['screenshot']} Создать скриншот
/screenshot_test - {EMOJIS['info']} Проверить скриншоты
/info - {EMOJIS['info']} Информация о системе
/help - 📖 Полная справка

<b>⚡ Готов к работе!</b>
"""
    await message.answer(welcome_text, parse_mode="HTML")

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    """Команда помощи с полным списком функций"""
    help_text = f"""
{EMOJIS['robot']} <b>Справка по командам Jarvis Bot</b>

<b>🎯 Основные команды:</b>
/start - {EMOJIS['robot']} Главное меню
/help - 📖 Эта справка
/reboot - 🔄 Перезагрузить компьютер
/shutdown - ⏹️ Выключить компьютер

<b>{EMOJIS['volume']} Управление звуком и музыкой:</b>
/volume - {EMOJIS['volume']} Интерактивное управление звуком и музыкой
/volume50 - {EMOJIS['volume']} Установить громкость 50%
/volume100 - {EMOJIS['volume']} Установить громкость 100%
/music_pause - {EMOJIS['pause']} Приостановить музыку
/music_play - {EMOJIS['play']} Возобновить музыку
/music_next - {EMOJIS['next']} Следующая композиция
/music_prev - {EMOJIS['prev']} Предыдущая композиция
/music_info - {EMOJIS['music']} Информация о музыке

<b>{EMOJIS['screenshot']} Другие команды:</b>
/screenshot - {EMOJIS['screenshot']} Создать скриншот экрана
/screenshot_test - {EMOJIS['info']} Проверить доступность скриншотов
/info - {EMOJIS['info']} Подробная информация о системе

<b>💡 Совет:</b> Используйте команду /volume для удобного управления звуком через кнопки!
"""
    await message.answer(help_text, parse_mode="HTML")

# =============================================================================
# КОМАНДЫ УПРАВЛЕНИЯ СИСТЕМОЙ
# =============================================================================

@dp.message_handler(commands=["reboot"])
async def reboot(message: types.Message):
    """Перезагрузка компьютера"""
    await message.answer(f"{EMOJIS['warning']} <b>Перезагрузка компьютера...</b>\n\n{EMOJIS['system']} Система будет перезагружена через несколько секунд", parse_mode="HTML")
    os.system("reboot")

@dp.message_handler(commands=["shutdown"])
async def shutdown(message: types.Message):
    """Выключение компьютера"""
    await message.answer(f"{EMOJIS['warning']} <b>Выключение компьютера...</b>\n\n{EMOJIS['system']} Система будет выключена через несколько секунд", parse_mode="HTML")
    os.system("shutdown")

# =============================================================================
# УПРАВЛЕНИЕ ЗВУКОМ И МУЗЫКОЙ
# =============================================================================

@dp.message_handler(commands=["volume"])
async def volume(message: types.Message):
    """Главная команда управления звуком и музыкой с инлайн кнопками"""
    keyboard = InlineKeyboardMarkup(row_width=3)

    # Быстрые команды громкости
    keyboard.add(
        InlineKeyboardButton(f"{EMOJIS['volume']} 50%", callback_data=volume_callback.new(action="set_50")),
        InlineKeyboardButton(f"{EMOJIS['info']} Info", callback_data=volume_callback.new(action="info")),
        InlineKeyboardButton(f"{EMOJIS['volume']} 100%", callback_data=volume_callback.new(action="set_100"))
    )

    # Точная настройка громкости
    keyboard.add(
        InlineKeyboardButton(f"{EMOJIS['up']} +10%", callback_data=volume_callback.new(action="up_10")),
        InlineKeyboardButton(f"{EMOJIS['up']} +5%", callback_data=volume_callback.new(action="up_5")),
        InlineKeyboardButton(f"{EMOJIS['up']} +1%", callback_data=volume_callback.new(action="up_1"))
    )
    keyboard.add(
        InlineKeyboardButton(f"{EMOJIS['mute']} Mute", callback_data=volume_callback.new(action="mute")),
        InlineKeyboardButton(f"{EMOJIS['unmute']} Unmute", callback_data=volume_callback.new(action="unmute"))
    )
    keyboard.add(
        InlineKeyboardButton(f"{EMOJIS['down']} -1%", callback_data=volume_callback.new(action="down_1")),
        InlineKeyboardButton(f"{EMOJIS['down']} -5%", callback_data=volume_callback.new(action="down_5")),
        InlineKeyboardButton(f"{EMOJIS['down']} -10%", callback_data=volume_callback.new(action="down_10"))
    )

    # Управление музыкой
    keyboard.add(
        InlineKeyboardButton(f"{EMOJIS['pause']} Пауза", callback_data=volume_callback.new(action="music_pause")),
        InlineKeyboardButton(f"{EMOJIS['play']} Воспроизведение", callback_data=volume_callback.new(action="music_play"))
    )
    keyboard.add(
        InlineKeyboardButton(f"{EMOJIS['prev']} Предыдущая", callback_data=volume_callback.new(action="music_prev")),
        InlineKeyboardButton(f"{EMOJIS['music']} Музыка Info", callback_data=volume_callback.new(action="music_info")),
        InlineKeyboardButton(f"{EMOJIS['next']} Следующая", callback_data=volume_callback.new(action="music_next"))
    )

    await message.answer(
        f"{EMOJIS['volume']} <b>Центр управления звуком и музыкой</b>\n\n"
        f"{EMOJIS['success']} Выберите действие из меню ниже:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.callback_query_handler(volume_callback.filter())
async def volume_callback_handler(callback: CallbackQuery, callback_data: dict):
    """Обработчик инлайн кнопок управления звуком и музыкой"""
    action = callback_data["action"]

    try:
        # Команды управления громкостью
        if action == "set_50":
            subprocess.run(["amixer", "set", "Master", "50%"], check=True)
            await callback.answer(f"{EMOJIS['volume']} Громкость установлена на 50%")

        elif action == "set_100":
            subprocess.run(["amixer", "set", "Master", "100%"], check=True)
            await callback.answer(f"{EMOJIS['volume']} Громкость установлена на 100%")

        elif action == "up_10":
            subprocess.run(["amixer", "set", "Master", "10%+"], check=True)
            await callback.answer(f"{EMOJIS['up']} Громкость увеличена на 10%")

        elif action == "up_5":
            subprocess.run(["amixer", "set", "Master", "5%+"], check=True)
            await callback.answer(f"{EMOJIS['up']} Громкость увеличена на 5%")

        elif action == "up_1":
            subprocess.run(["amixer", "set", "Master", "1%+"], check=True)
            await callback.answer(f"{EMOJIS['up']} Громкость увеличена на 1%")

        elif action == "down_10":
            subprocess.run(["amixer", "set", "Master", "10%-"], check=True)
            await callback.answer(f"{EMOJIS['down']} Громкость уменьшена на 10%")

        elif action == "down_5":
            subprocess.run(["amixer", "set", "Master", "5%-"], check=True)
            await callback.answer(f"{EMOJIS['down']} Громкость уменьшена на 5%")

        elif action == "down_1":
            subprocess.run(["amixer", "set", "Master", "1%-"], check=True)
            await callback.answer(f"{EMOJIS['down']} Громкость уменьшена на 1%")

        elif action == "mute":
            subprocess.run(["amixer", "set", "Master", "mute"], check=True)
            await callback.answer(f"{EMOJIS['mute']} Звук отключен")

        elif action == "unmute":
            subprocess.run(["amixer", "set", "Master", "unmute"], check=True)
            await callback.answer(f"{EMOJIS['unmute']} Звук включен")

        elif action == "info":
            result = subprocess.run(["amixer", "get", "Master"], capture_output=True, text=True)
            volume_info = result.stdout.split('\n')[4]
            await callback.answer(f"{EMOJIS['info']} {volume_info}")

        # Команды управления музыкой
        elif action == "music_pause":
            subprocess.run(["playerctl", "pause"], check=True)
            await callback.answer(f"{EMOJIS['pause']} Музыка приостановлена")

        elif action == "music_play":
            subprocess.run(["playerctl", "play"], check=True)
            await callback.answer(f"{EMOJIS['play']} Музыка возобновлена")

        elif action == "music_next":
            subprocess.run(["playerctl", "next"], check=True)
            await callback.answer(f"{EMOJIS['next']} Следующая композиция")

        elif action == "music_prev":
            subprocess.run(["playerctl", "previous"], check=True)
            await callback.answer(f"{EMOJIS['prev']} Предыдущая композиция")

        elif action == "music_info":
            result = subprocess.run(["playerctl", "metadata", "--format", "{{artist}} - {{title}}"],
                                  capture_output=True, text=True)
            if result.stdout.strip():
                await callback.answer(f"{EMOJIS['music']} {result.stdout.strip()}")
            else:
                await callback.answer(f"{EMOJIS['music']} Музыка не воспроизводится")

    except subprocess.CalledProcessError:
        await callback.answer(f"{EMOJIS['error']} Ошибка при управлении звуком/музыкой")

# =============================================================================
# БЫСТРЫЕ КОМАНДЫ ГРОМКОСТИ
# =============================================================================

@dp.message_handler(commands=["volume50"])
async def volume50(message: types.Message):
    """Быстрая установка громкости на 50%"""
    try:
        subprocess.run(["amixer", "set", "Master", "50%"], check=True)
        await message.answer(f"{EMOJIS['volume']} <b>Громкость установлена на 50%</b>", parse_mode="HTML")
    except subprocess.CalledProcessError:
        await message.answer(f"{EMOJIS['error']} Ошибка при изменении громкости")

@dp.message_handler(commands=["volume100"])
async def volume100(message: types.Message):
    """Быстрая установка громкости на 100%"""
    try:
        subprocess.run(["amixer", "set", "Master", "100%"], check=True)
        await message.answer(f"{EMOJIS['volume']} <b>Громкость установлена на 100%</b>", parse_mode="HTML")
    except subprocess.CalledProcessError:
        await message.answer(f"{EMOJIS['error']} Ошибка при изменении громкости")

# =============================================================================
# КОМАНДЫ УПРАВЛЕНИЯ МУЗЫКОЙ
# =============================================================================

@dp.message_handler(commands=["music_pause"])
async def music_pause(message: types.Message):
    """Приостановка музыки"""
    try:
        subprocess.run(["playerctl", "pause"], check=True)
        await message.answer(f"{EMOJIS['pause']} <b>Музыка приостановлена</b>", parse_mode="HTML")
    except subprocess.CalledProcessError:
        await message.answer(f"{EMOJIS['error']} Ошибка при приостановке музыки")

@dp.message_handler(commands=["music_play"])
async def music_play(message: types.Message):
    """Возобновление музыки"""
    try:
        subprocess.run(["playerctl", "play"], check=True)
        await message.answer(f"{EMOJIS['play']} <b>Музыка возобновлена</b>", parse_mode="HTML")
    except subprocess.CalledProcessError:
        await message.answer(f"{EMOJIS['error']} Ошибка при возобновлении музыки")

@dp.message_handler(commands=["music_next"])
async def music_next(message: types.Message):
    """Следующая композиция"""
    try:
        subprocess.run(["playerctl", "next"], check=True)
        await message.answer(f"{EMOJIS['next']} <b>Следующая композиция</b>", parse_mode="HTML")
    except subprocess.CalledProcessError:
        await message.answer(f"{EMOJIS['error']} Ошибка при переключении на следующую композицию")

@dp.message_handler(commands=["music_prev"])
async def music_prev(message: types.Message):
    """Предыдущая композиция"""
    try:
        subprocess.run(["playerctl", "previous"], check=True)
        await message.answer(f"{EMOJIS['prev']} <b>Предыдущая композиция</b>", parse_mode="HTML")
    except subprocess.CalledProcessError:
        await message.answer(f"{EMOJIS['error']} Ошибка при переключении на предыдущую композицию")

@dp.message_handler(commands=["music_info"])
async def music_info(message: types.Message):
    """Информация о текущей композиции"""
    try:
        result = subprocess.run(["playerctl", "metadata", "--format", "{{artist}} - {{title}}"],
                              capture_output=True, text=True)
        if result.stdout.strip():
            await message.answer(f"{EMOJIS['music']} <b>Сейчас играет:</b>\n{result.stdout.strip()}", parse_mode="HTML")
        else:
            await message.answer(f"{EMOJIS['music']} <b>Музыка не воспроизводится</b>", parse_mode="HTML")
    except subprocess.CalledProcessError:
        await message.answer(f"{EMOJIS['error']} Ошибка при получении информации о музыке")

# =============================================================================
# КОМАНДЫ СИСТЕМНОЙ ИНФОРМАЦИИ
# =============================================================================

@dp.message_handler(commands=["screenshot"])
async def screenshot(message: types.Message):
    """Создание скриншота экрана"""
    try:
        await message.answer(f"{EMOJIS['screenshot']} <b>Создаю скриншот...</b>", parse_mode="HTML")

        # Проверяем доступность дисплея
        display = os.environ.get('DISPLAY')
        if not display:
            await message.answer(f"{EMOJIS['error']} <b>Ошибка:</b> Дисплей недоступен. Убедитесь, что бот запущен в графической среде.", parse_mode="HTML")
            return

        # Пробуем разные методы создания скриншота
        screenshot_img = None

        # Метод 1: PIL ImageGrab (основной)
        try:
            screenshot_img = ImageGrab.grab()
        except Exception as e:
            logger.warning(f"PIL ImageGrab failed: {e}")

            # Метод 2: scrot (если установлен)
            try:
                subprocess.run(["scrot", "/tmp/screenshot.png"], check=True)
                screenshot_img = ImageGrab.open("/tmp/screenshot.png")
                os.remove("/tmp/screenshot.png")  # Удаляем временный файл
            except Exception as e2:
                logger.warning(f"scrot method failed: {e2}")

                # Метод 3: gnome-screenshot (для GNOME)
                try:
                    subprocess.run(["gnome-screenshot", "-f", "/tmp/screenshot.png"], check=True)
                    screenshot_img = ImageGrab.open("/tmp/screenshot.png")
                    os.remove("/tmp/screenshot.png")
                except Exception as e3:
                    logger.warning(f"gnome-screenshot method failed: {e3}")

                    # Метод 4: import (ImageMagick)
                    try:
                        subprocess.run(["import", "-window", "root", "/tmp/screenshot.png"], check=True)
                        screenshot_img = ImageGrab.open("/tmp/screenshot.png")
                        os.remove("/tmp/screenshot.png")
                    except Exception as e4:
                        logger.error(f"All screenshot methods failed: {e4}")
                        raise Exception("Все методы создания скриншота недоступны")

        if screenshot_img is None:
            raise Exception("Не удалось создать скриншот")

        # Конвертируем в байты
        img_byte_arr = io.BytesIO()
        screenshot_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Отправляем скриншот
        await message.answer_photo(
            photo=img_byte_arr,
            caption=f"{EMOJIS['screenshot']} <b>Скриншот экрана</b>\n\n{EMOJIS['success']} Создан успешно!",
            parse_mode="HTML"
        )

    except Exception as e:
        error_msg = f"{EMOJIS['error']} <b>Ошибка при создании скриншота:</b>\n\n"

        if "X" in str(e) or "display" in str(e).lower():
            error_msg += f"• Дисплей недоступен\n"
            error_msg += f"• Убедитесь, что бот запущен в графической среде\n"
            error_msg += f"• Проверьте переменную DISPLAY\n\n"
            error_msg += f"<b>💡 Решения:</b>\n"
            error_msg += f"• Запустите бота в терминале с графическим интерфейсом\n"
            error_msg += f"• Установите: <code>sudo apt install scrot</code>\n"
            error_msg += f"• Или: <code>sudo apt install imagemagick</code>"
        else:
            error_msg += f"• {str(e)}\n\n"
            error_msg += f"<b>💡 Попробуйте:</b>\n"
            error_msg += f"• Установить scrot: <code>sudo apt install scrot</code>\n"
            error_msg += f"• Установить ImageMagick: <code>sudo apt install imagemagick</code>\n"
            error_msg += f"• Перезапустить бота"

        await message.answer(error_msg, parse_mode="HTML")

@dp.message_handler(commands=["screenshot_test"])
async def screenshot_test(message: types.Message):
    """Проверка доступности методов создания скриншота"""
    try:
        test_results = f"{EMOJIS['info']} <b>Проверка методов создания скриншота</b>\n\n"

        # Проверяем переменную DISPLAY
        display = os.environ.get('DISPLAY')
        if display:
            test_results += f"{EMOJIS['success']} DISPLAY: {display}\n"
        else:
            test_results += f"{EMOJIS['error']} DISPLAY: не установлена\n"

        # Проверяем доступность PIL ImageGrab
        try:
            ImageGrab.grab()
            test_results += f"{EMOJIS['success']} PIL ImageGrab: доступен\n"
        except Exception as e:
            test_results += f"{EMOJIS['error']} PIL ImageGrab: {str(e)[:50]}...\n"

        # Проверяем scrot
        try:
            subprocess.run(["scrot", "--version"], check=True, capture_output=True)
            test_results += f"{EMOJIS['success']} scrot: установлен\n"
        except:
            test_results += f"{EMOJIS['error']} scrot: не установлен\n"

        # Проверяем gnome-screenshot
        try:
            subprocess.run(["gnome-screenshot", "--version"], check=True, capture_output=True)
            test_results += f"{EMOJIS['success']} gnome-screenshot: доступен\n"
        except:
            test_results += f"{EMOJIS['error']} gnome-screenshot: недоступен\n"

        # Проверяем ImageMagick import
        try:
            subprocess.run(["import", "-version"], check=True, capture_output=True)
            test_results += f"{EMOJIS['success']} ImageMagick: установлен\n"
        except:
            test_results += f"{EMOJIS['error']} ImageMagick: не установлен\n"

        test_results += f"\n<b>💡 Для установки недостающих пакетов:</b>\n"
        test_results += f"• <code>sudo apt install scrot</code>\n"
        test_results += f"• <code>sudo apt install imagemagick</code>"

        await message.answer(test_results, parse_mode="HTML")

    except Exception as e:
        await message.answer(f"{EMOJIS['error']} Ошибка при проверке: {str(e)}")

@dp.message_handler(commands=["info"])
async def info(message: types.Message):
    """Подробная информация о системе"""
    try:
        # Получаем информацию о системе
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        system_info = f"""
{EMOJIS['system']} <b>Информация о компьютере</b>

<b>{EMOJIS['system']} Операционная система:</b>
• Система: {platform.system()}
• Версия: {platform.release()}
• Архитектура: {platform.machine()}
• Процессор: {platform.processor()}

<b>{EMOJIS['memory']} Память (RAM):</b>
• Общая память: {format_bytes(memory.total)}
• Используется: {format_bytes(memory.used)}
• Свободно: {format_bytes(memory.available)}
• Процент использования: {memory.percent}%

<b>{EMOJIS['disk']} Диск:</b>
• Общий объем: {format_bytes(disk.total)}
• Используется: {format_bytes(disk.used)}
• Свободно: {format_bytes(disk.free)}
• Процент использования: {round((disk.used / disk.total) * 100, 2)}%

<b>{EMOJIS['cpu']} Процессор:</b>
• Загрузка CPU: {psutil.cpu_percent(interval=1)}%
• Количество ядер: {psutil.cpu_count(logical=False)}
• Логических процессоров: {psutil.cpu_count(logical=True)}

<b>{EMOJIS['network']} Система:</b>
• Время работы: {get_system_uptime()}
        """

        await message.answer(system_info, parse_mode="HTML")

    except Exception as e:
        await message.answer(f"{EMOJIS['error']} Ошибка при получении информации о системе: {str(e)}")

# =============================================================================
# ЗАПУСК БОТА
# =============================================================================

async def cli_loop():
    """Асинхронный цикл для ввода команд в консоли"""
    loop = asyncio.get_event_loop()
    print(f"\n{EMOJIS['robot']} Интерактивный режим активен. Введите 'exit' для выхода или любую команду ОС.\n")
    
    while True:
        try:
            # Используем run_in_executor для неблокирующего ввода
            command = await loop.run_in_executor(None, input, "Jarvis > ")
            
            if not command.strip():
                continue
                
            if command.lower() in ['exit', 'quit', 'stop']:
                print(f"{EMOJIS['warning']} Завершение работы...")
                os._exit(0) # Жесткий выход для завершения всего процесса
                
            # Выполняем команду
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if stdout:
                print(stdout.decode().strip())
            if stderr:
                print(f"{EMOJIS['error']} Error: {stderr.decode().strip()}")
                
        except EOFError:
            break
        except Exception as e:
            print(f"{EMOJIS['error']} Ошибка CLI: {e}")

async def on_startup(dp):
    """Функция запуска бота"""
    logger.info(f"{EMOJIS['robot']} Jarvis Bot запущен и готов к работе!")
    print(f"{EMOJIS['robot']} Jarvis Bot запущен и готов к работе!")
    
    # Запускаем CLI цикл в фоне
    asyncio.create_task(cli_loop())

if __name__ == "__main__":
    print(f"{EMOJIS['robot']} Запуск Jarvis Bot...")
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)