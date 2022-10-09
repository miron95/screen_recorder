import logging
import os
from time import sleep
import telebot

from main import VideoWr

tkn = '5584412527:AAG2H1-14oDoidHqvx5S6an-ogB0kZJq85A'
logger = telebot.logger
logger.setLevel(logging.DEBUG)


class TelegaBot:
    def __init__(self):
        self.token = tkn
        self.bot = telebot.TeleBot(self.token)
        self.recorder = VideoWr()

    def handler(self):
        @self.bot.message_handler(commands=['start'])
        def start(message: telebot.types.Message):
            if self.recorder.run:
                self.bot.send_message(message.chat.id, 'Запись уже ведется')
            else:
                self.recorder.run = True
                self.bot.send_message(message.chat.id, 'Запись начата')
                self.recorder.run_recorder()
                if self.recorder.run:
                    with open('output.mp4', 'rb') as video:
                        try:
                            self.bot.send_video(message.chat.id, video)
                        except Exception as e:
                            self.bot.send_message('489200160', str(e))
                        self.recorder.run = False
                        video.close()
                    self.remove_file()

        @self.bot.message_handler(commands=['stop'])
        def stop(message: telebot.types.Message):
            if self.recorder.run:
                self.recorder.run = False
                self.bot.send_message(message.chat.id, 'Запись остановлена')

                with open('output.mp4', 'rb') as video:
                    try:
                        self.bot.send_video(message.chat.id, video)
                    except Exception as e:
                        self.bot.send_message('489200160', str(e))
                    video.close()
                self.remove_file()
            else:
                self.bot.send_message(message.chat.id, 'Запись не ведется')
                self.bot.send_message(message.chat.id, str(message.chat.id))

        while True:
            try:
                self.bot.send_message('489200160', 'Бот слушает команду..')
                self.run()
            except Exception as e:

                sleep(20)

    def run(self):
        self.bot.polling(non_stop=True, skip_pending=True)

    def remove_file(self):
        sleep(2)
        try:
            os.remove('output.mp4')
        except Exception as e:
            self.bot.send_message('489200160', str(e))


if __name__ == '__main__':

    while True:
        bt = TelegaBot()
        bt.handler()
