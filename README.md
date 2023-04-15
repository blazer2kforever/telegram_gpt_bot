# Telegram bot with GPT-3

Russian README version: [![ru](https://img.shields.io/badge/lang-ru-green.svg)](https://github.com/blazer2kforever/telegram_gpt_bot/blob/main/README.ru.md)

## Description:

This is an example of a simple Telegram bot that uses the OpenAI API to respond to users' questions.

Screenshot(russian):
![Screenshot of bot working](https://i.imgur.com/H3WFmVA.jpg "That's how it works")

## Dependencies:

- Python3;
- Libraries [aiogram](https://github.com/aiogram/aiogram) and [openai](https://openai.com/blog/openai-api);

## Functionality:

- The bot responds to the user's question with an answer from the GPT model;
- A "database" is created to store a message history for each user. This allows the model to remember what was discussed in previous requests/responses;
- A simple "admin" console has been implemented in the terminal to view message history;

## How to run:

To run the bot, you need to have the latest version of Python installed, as well as the following libraries:

```bash
pip3 install aiogram
```

```bash
pip3 install openai
```

You will also need to obtain API keys for both Telegram and OpenAI.

The key for Telegram can be obtained from the @BotFather bot, and the key for OpenAI is paid and can be obtained on [their website](https://platform.openai.com).

In _setup.py_, the keys are set as constants:

```python
TELEGRAM_API = 'YOUR_TELEGRAM_KEY'
OPENAI_API = 'YOUR_OPENAI_KEY'
```

Program is launched in the usual way.

```bash
python3 run.py
```

## Configuration:

The main configuration options are set in _gpt_client.py_ and include the _AI_MODEL_ and _GPT_ROLE_.

The _AI_MODEL_ specifies the version of the GPT model to be used:

```python
AI_MODEL = 'gpt-3.5-turbo'
```

The _GPT_ROLE_ specifies the "role" of the bot:

```python
GPT_ROLE = 'You are an artificial intelligence named Marcus.'
```

More information on these options can be found in the [OpenAI API documentation](https://platform.openai.com/docs/api-reference).

## Potential Use Cases:

The Telegram-GPT combination has potential applications in commercial bots and chats. However, this example requires code refactoring and the addition of automation functions, among other things.
