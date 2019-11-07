from models import Demo
from repositories import DemoRepository


class DemoService():

    @staticmethod
    def doSomething():
        model = Demo()
        repo = DemoRepository()
        model.add_to_something(repo.do_some_thing())

        return model.toJSON
