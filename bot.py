import telebot
from telebot import types

TOKEN = "8873078346:AAGw--bQu-XTV59Ie69YX_1YNgIJgy7vovQ"

bot = telebot.TeleBot(TOKEN)

wallet = {}

def get_balance(user):
    return wallet.get(user, 0)


@bot.message_handler(commands=["start"])
def start(message):

    user = message.chat.id

    if user not in wallet:
        wallet[user] = 0

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.add(
        "💰 Balance",
        "➕ Add Money",
        "📤 Send Money",
        "📜 History"
    )

    bot.send_message(
        user,
        "✨ My UPI Wallet Bot ✨\n\nChoose option:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: True)
def menu(message):

    user = message.chat.id

    if message.text == "💰 Balance":

        bot.send_message(
            user,
            f"💳 Wallet Balance: ₹{get_balance(user)}"
        )


    elif message.text == "➕ Add Money":

        bot.send_message(
            user,
            "Enter amount to add:"
        )

        bot.register_next_step_handler(
            message,
            add_money
        )


    elif message.text == "📤 Send Money":

        bot.send_message(
            user,
            "Enter amount to send:"
        )

        bot.register_next_step_handler(
            message,
            send_money
        )


    elif message.text == "📜 History":

        bot.send_message(
            user,
            "📜 No transactions yet"
        )


def add_money(message):

    user = message.chat.id

    try:
        amount = int(message.text)

        wallet[user] += amount

        bot.send_message(
            user,
            f"✅ Added ₹{amount}\n"
            f"New Balance: ₹{wallet[user]}"
        )

    except:
        bot.send_message(
            user,
            "Invalid amount"
        )


def send_money(message):

    user = message.chat.id

    try:
        amount = int(message.text)

        if wallet[user] >= amount:

            wallet[user] -= amount

            bot.send_message(
                user,
                f"✅ Sent ₹{amount}\n"
                f"Balance: ₹{wallet[user]}"
            )

        else:

            bot.send_message(
                user,
                "❌ Insufficient balance"
            )

    except:
        bot.send_message(
            user,
            "Invalid amount"
        )


bot.infinity_polling()