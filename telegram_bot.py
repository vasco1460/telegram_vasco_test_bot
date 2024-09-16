import telebot
import random
import requests
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)

# Bot token
bot = telebot.TeleBot('7240972647:AAG0epBj8GM_dz9Oo4uO5vkG01_2HRwAswI')

# Default token address
DEFAULT_TOKEN_ADDRESS = '0xC3571b3f9721D07919dc42af7fce2784B56e8E3c'

# List of available commands
COMMANDS_LIST = """
📚 Available commands:
/start - Get a warm welcome
/help - Show the help message
/commands - Display this list of commands
/price - Get live price for our token
/marketcap - Show current market capitalization
/volume - Display 24-hour trading volume
/flip - Flip a coin for fun
/socials - Display our official social media links
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
    🚀 Welcome to the Crypto Community Bot! 🚀

    I'm here to help you stay informed about your favorite cryptocurrency. Whether you need price updates, market insights, or just want to flip a coin, I've got you covered!

    Use /commands to see all available commands and start exploring the exciting world of crypto with me!
    """
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
    Need help? Here's a quick guide:

    • Use /commands to see a list of all available commands
    • For price information, use /price
    • Check market cap with /marketcap
    • Get 24-hour volume with /volume
    • Have some fun with /flip to flip a coin
    • Find our social media links with /socials

    If you have any questions or issues, feel free to contact our support team!
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['commands'])
def send_commands(message):
    bot.reply_to(message, COMMANDS_LIST)

def get_token_data():
    try:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{DEFAULT_TOKEN_ADDRESS}"
        response = requests.get(url)
        data = response.json()
        logging.info(f"API Response: {data}")
        if data.get("pairs") and len(data["pairs"]) > 0:
            return data["pairs"][0]
        else:
            return None
    except Exception as e:
        logging.error(f"Error fetching data: {str(e)}")
        return None

@bot.message_handler(commands=['price'])
def send_price(message):
    pair_data = get_token_data()
    if pair_data:
        price = pair_data.get("priceUsd")
        token_name = pair_data["baseToken"]["symbol"]
        if price:
            bot.reply_to(message, f"💰 The current price of {token_name} is ${price}")
        else:
            bot.reply_to(message, f"Sorry, price data is not available for {token_name}.")
    else:
        bot.reply_to(message, "Sorry, I couldn't fetch the price data for this token.")

@bot.message_handler(commands=['marketcap'])
def send_marketcap(message):
    pair_data = get_token_data()
    if pair_data:
        marketcap = pair_data.get("fdv")
        token_name = pair_data["baseToken"]["symbol"]
        if marketcap:
            bot.reply_to(message, f"📊 The current market cap of {token_name} is ${marketcap}")
        else:
            bot.reply_to(message, f"Sorry, market cap data is not available for {token_name}.")
    else:
        bot.reply_to(message, "Sorry, I couldn't fetch the market cap data for this token.")

@bot.message_handler(commands=['volume'])
def send_volume(message):
    pair_data = get_token_data()
    if pair_data:
        volume = pair_data.get("volume", {}).get("h24")
        token_name = pair_data["baseToken"]["symbol"]
        if volume:
            bot.reply_to(message, f"📈 The 24-hour trading volume of {token_name} is ${volume}")
        else:
            bot.reply_to(message, f"Sorry, volume data is not available for {token_name}.")
    else:
        bot.reply_to(message, "Sorry, I couldn't fetch the volume data for this token.")

@bot.message_handler(commands=['flip'])
def flip_coin(message):
    result = random.choice(["Heads", "Tails"])
    bot.reply_to(message, f"🪙 The coin landed on: {result}")

@bot.message_handler(commands=['socials'])
def send_socials(message):
    socials_text = """
    🌐 Follow us on our official channels:
    • Twitter: https://twitter.com/YourCryptoProject
    • Telegram: https://t.me/YourCryptoProject
    • Discord: https://discord.gg/YourCryptoProject
    • Website: https://www.yourcryptoproject.com
    """
    bot.reply_to(message, socials_text)

# Keep the bot polling
bot.polling()