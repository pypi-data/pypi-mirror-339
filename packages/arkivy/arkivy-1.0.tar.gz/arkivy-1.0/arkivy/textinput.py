from kivy.uix.accordion import StringProperty
from kivy.uix.textinput import TextInput
from .utils import ar

__all__=('ArTextInput','ArTextInputBase',)

class ArTextInput(TextInput):
    t=StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_direction='rtl'
    def insert_text(self, substring, from_undo=False):
        self.t+=substring
        self.text=ar(self.t)
    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.t=self.t[:-1]
        self.text=ar(self.t)


class ArTextInputBase:
    t=StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_direction='rtl'
    def insert_text(self, substring, from_undo=False):
        self.t+=substring
        self.text=ar(self.t)
    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.t=self.t[:-1]
        self.text=ar(self.t)




