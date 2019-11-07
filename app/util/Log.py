import datetime


class Log:
    LEVEL_ERROR = "err: "
    LEVEL_INPUT = "input: "
    LEVEL_OUTPUT = "output: "

    @staticmethod
    def info(_id, level, data):
        print("time: " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f"), "_id: " + _id, level, data,
              sep='   ')
