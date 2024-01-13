
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from pyrogram import filters
from pyrogram import filters, types
from pyrogram.errors.exceptions import ChannelInvalid
import datetime
import asyncpg
import pyrogram
from pyrogram import enums
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pyrogram import Client, filters
from pyrogram.types import Message

# -*- coding: utf-8 -*-
  

api_id = 23780487
api_hash = "8e756a529aa577d1ae33859476ca4bf5"
bot_token = "6951286086:AAGEk-g7fAN1d4IqYEh2XFe_Zfy-itdeR2s"

app = Client(
    "tag_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)



def save_call_info(chat_id, user_id, time):
    try:
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)
    except (json.JSONDecodeError, FileNotFoundError):
        # Випадки, коли файл порожній або виникає помилка JSON
        config_data = {}

    if chat_id not in config_data:
        config_data[chat_id] = {}

    # Використовуйте ваш власний серіалізатор для datetime
    config_data[chat_id][user_id] = {"time": time.isoformat()}

    with open("config.json", "w") as config_file:
        json.dump(config_data, config_file)


        
@app.on_message(filters.command("check"))
async def check_group_type(bot, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat_member = await bot.get_chat_member(chat_id, user_id)
    
    
    
    if chat_member.status is enums.ChatMemberStatus.OWNER:
        await message.reply("Группа является админом.")
    

@app.on_message(filters.command("start"))
async def start_command(bot, message):

        await message.reply("Вітаю! Я бот, який допоможе проінформувати всіх учасників групи про важливу подію! . Я працюю лише у групах і маю поки лише одну команду /call. Пропиши її у чат, і я поясню, як нею користуватися. Також варто дати мені права адміністратора, щоб я міг писати.")

@app.on_message(filters.command("check"))
async def start_command(bot, message):
    await check_group_type(bot, message)

@app.on_message(filters.command("get_user"))
async def get_user_command(client, message):
    # Розбираємо параметри команди
    command_parts = message.text.split(" ", 1)
    if len(command_parts) != 2:
        await message.reply("Usage: /get_user <user_id>")
        return

    # Отримуємо айді користувача
    user_id_str = command_parts[1]
    try:
        user_id = int(user_id_str)
    except ValueError:
        await message.reply("Invalid user_id. Please provide a valid numeric user_id.")
        return

    # Отримуємо інформацію про користувача
    chat_id = message.chat.id
    try:
        user_info = await app.get_chat(user_id)
        await message.reply(f"User info for user with ID {user_id}:\n\n{user_info}")
    except Exception as e:
        await message.reply(f"Failed to get user info: {str(e)}") 
@app.on_message(filters.command("call"))
async def call_users(bot, message):
    try:
        text = message.text.split(" ", maxsplit=4)

        if len(text) < 5:
            await message.reply("Потрібно вказати текст для згадування та кількість користувачів, наприклад: /call ТЕКСТ 20 (посилання) (текст після згадування)")
            return

        mention_text = text[1]

        try:
            chunk_size = int(text[2])
        except ValueError:
            await message.reply("Некоректна кількість користувачів. Введіть число.")
            return

        button_link = text[3] if len(text) > 3 else None
        post_mention_text = text[4]

        chat_id = message.chat.id
        user_ids = [member.user.id async for member in app.get_chat_members(chat_id)]

        if not user_ids:
            await message.reply("У чаті відсутні учасники.")
            return

        user_chunks = [user_ids[i:i + chunk_size] for i in range(0, len(user_ids), chunk_size)]

        sent_messages = []
        chat_id = message.chat.id
        user_id = message.from_user.id
        time = datetime.datetime.now()

        save_call_info(chat_id, user_id, time)

        for chunk in user_chunks:
            mentions = [f"[{mention_text}]({mention_user(user_id)})" for user_id in chunk]
            mention_message = " ".join(mentions)

            button = [[InlineKeyboardButton("Перейти", url=button_link)]] if button_link else None
            button_markup = InlineKeyboardMarkup(button) if button else None

            full_message = f"{mention_message} {post_mention_text}" if button_link else f"{mention_message} {post_mention_text}"

            try:
                sent_message = await app.send_message(chat_id, full_message, reply_markup=button_markup)
                sent_messages.append(sent_message)
            except Exception as e:
                await message.reply(f"Сталася помилка при відправленні повідомлення: {e}")

        # Зачекайте delete_delay секунд перед видаленням повідомлень.
        

    except ChannelInvalid:
        await message.reply("Будь ласка, використовуйте цю команду в груповому чаті.")

    # Видалення старих повідомлень, якщо вже було вказано час видалення
    

# Команда для зміни часу видалення

    except ChannelInvalid:
        await message.reply("Будь ласка, використовуйте цю команду в груповому чаті.")


def mention_user(user_id):
    return f"tg://user?id={user_id}"



app.run()
