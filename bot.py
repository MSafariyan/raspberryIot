import logging
import RPi.GPIO as GPIO
from device import my_Device
import device
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "1468572392:AAFWeVrG3UdzpXfWQb21mp04kKDNbkpwQPQ"
PROXY_URL = "socks5://127.0.0.1:9050"
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
bot = Bot(token=API_TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)
adminUsername = ["@MSafariyan","@Davoodeh"]

relay = my_Device(11,"out")
relay.toggle(0)


@dp.message_handler(commands="start")
async def start_cmd_handler(message: types.Message):
    if message.from_user.mention in adminUsername:
        keyboard_markup = types.ReplyKeyboardMarkup(
            row_width=3, one_time_keyboard=False
        )
        # default row_width is 3, so here we can omit it actually
        # kept for clearness
        btns_text = ("Turn on relay", "Turn off relay","relay Status")
        keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
        # adds buttons as a new row to the existing keyboard
        # the behaviour doesn't depend on row_width attribute
        await message.reply("how can i help you :D", reply_markup=keyboard_markup)
    else:
        await message.reply("you are not an admin, access denied.")



@dp.message_handler()
async def all_msg_handler(message: types.Message):
    # pressing of a KeyboardButton is the same as sending the regular message with the same text
    # so, to handle the responses from the keyboard, we need to use a message_handler
    # in real bot, it's better to define message_handler(text="...") for each button
    # but here for the simplicity only one handler is defined
    if message.from_user.mention in adminUsername:
        button_text = message.text
        logger.debug("The answer is %r", button_text)  # print the text we've got

        if "relay" and "on" in button_text:
            relay.toggle(1)
            reply_text = "Relay turned on"
        elif "relay" and "off" in button_text:
            relay.toggle(0)
            reply_text = "Relay turned off"
        elif "relay Status" in button_text:
            reply_text = "your relay is " + relay.state()
        else:
            reply_text = "what?"

        await message.answer(reply_text, reply_markup=types.ReplyKeyboardMarkup())
        # with message, we send types.ReplyKeyboardRemove() to hide the keyboard
    else:
        await message.answer("you are not allow to use this bot.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
