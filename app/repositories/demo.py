import os


class DemoRepository():
    currentPath = os.path.dirname(os.path.realpath(__file__))
    parentPath = os.path.abspath(os.path.join(currentPath, os.pardir))
    ml_model_directory = parentPath + '/MLModel/'

    def __init__(self):
        pass

    def do_some_thing(self):
        return ['ok', 'ok']
