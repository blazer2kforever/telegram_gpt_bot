from aiogram import Bot, Dispatcher, executor, types

MAX_MESSAGE_LENGTH = 4096

START_MSG = 'Привет!🙌\nЯ – Маркус😇\Можешь задавать свой вопроc🙃'
RESET_MSG = 'История переписки очищена🗑️'

INFO_START_POLLING = 'Диспетчер запущен'
INFO_LENGTH_NORMAL = 'Длина сообщения нормальная'
INFO_LENGTH_EXCEEDED = 'Длина сообщения превышена'
INFO_AI = 'GPT в процессе'

ERROR_MSG = 'Что-то пошло не так...🤨'

class TelegramBot:
    def __init__(self, api_key, gpt, db, terminal):
        self.bot = Bot(token = api_key)
        self.dp = Dispatcher(self.bot)
        self.gpt = gpt
        self.db = db
        self.terminal = terminal

    def register_handlers(self):
        self.dp.register_message_handler(self.start_handler, commands=['start'])
        self.dp.register_message_handler(self.reset_handler, commands=['reset'])
        self.dp.register_message_handler(self.echo_handler)

    def start_bot(self):
        self.register_handlers()
        self.terminal.p_system(INFO_START_POLLING)
        executor.start_polling(self.dp, skip_updates=True)

    async def start_handler(self, message: types.Message):
        self.terminal.p_user(message.text, message.from_user.username, message.from_user.id)
        await message.reply(START_MSG)
        self.terminal.p_bot(START_MSG, message.from_user.id)

    async def reset_handler(self, message: types.Message):
        self.terminal.p_user(message.text, message.from_user.username, message.from_user.id)
        self.db.delete_history(message.from_user.id)
        await message.reply(RESET_MSG)
        self.terminal.p_bot(RESET_MSG, message.from_user.id)
    
    async def echo_handler(self, message: types.Message):
        self.terminal.p_user(message.text, message.from_user.username, message.from_user.id)
        self.terminal.p_system(INFO_AI)

        response = await self.gpt.generate_response(message.text, message.from_user.username, message.from_user.id)
        if response != None:
          if len(response) <= MAX_MESSAGE_LENGTH:
            await message.reply(response)
            self.terminal.p_bot(response, message.from_user.id)
            self.terminal.p_system(INFO_LENGTH_NORMAL, message.from_user.id)
          else:
            self.terminal.p_system(INFO_LENGTH_EXCEEDED, message.from_user.id)
            while len(response) > 0:
                chopped = response[:MAX_MESSAGE_LENGTH]
                response = response[MAX_MESSAGE_LENGTH:]
                await self.bot.send_message(message.chat.id, chopped)
                self.terminal.p_bot(chopped, message.from_user.id)
        else:
          await message.reply(ERROR_MSG)
          self.terminal.p_bot(ERROR_MSG, message.from_user.id)