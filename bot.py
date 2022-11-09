# import logging
import os

from datetime import datetime
from time import sleep
import telebot

from main import VideoWr

tkn = '5438183724:AAH5oxlt1zZ9u1qRKE0TSWhtdpeQKiTdqH4'


# logger = telebot.logger
# logger.setLevel(logging.DEBUG)
# logger.info('1')
class TelegaBot:

    def __init__(self):
        self.token = tkn
        self.bot = telebot.TeleBot(self.token)
        self.recorder = VideoWr()
        self.error = dict()

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
                        except Exception as error_send_video:
                            self.bot.send_message('-869214948', 'Ошибка при отправке файла: ' + str(error_send_video))
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
                    except Exception as error_send_video:
                        self.bot.send_message('-869214948', 'Ошибка при отправке файла: ' + str(error_send_video))
                    video.close()
                self.remove_file()
            else:
                self.bot.send_message(message.chat.id, 'Запись не ведется')
                self.bot.send_message(message.chat.id, str(message.chat.id))

        while True:
            try:
                self.bot.send_message('-869214948', 'Бот слушает команду..')
                self.run()

            except Exception as error:
                now = datetime.now()
                self.error.update({now.strftime('%d.%m %H:%M:%S'): error.__repr__()})
                print(self.error)
                sleep(60)

    def run(self):
        self.bot.polling(non_stop=True, skip_pending=True)

    def remove_file(self):
        sleep(2)
        try:
            os.remove('output.mp4')
        except Exception as e:
            self.bot.send_message('-869214948', 'Произошла ошибка при удалении файла:')
            self.bot.send_message('-869214948', str(e))


if __name__ == '__main__':

    while True:
        bt = TelegaBot()
        bt.handler()
