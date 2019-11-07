from .base import BaseModel


class Demo(BaseModel):
    ''' Study of sounnd is refered to as Acoustics'''

    something = []

    def __init__(self):
        BaseModel.__init__(self)

    def add_to_something(self, arr):
        self.something = arr
