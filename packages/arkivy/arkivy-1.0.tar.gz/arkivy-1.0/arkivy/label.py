from kivy.properties import StringProperty
from kivy.uix.label import Label
from .utils import ar

__all__=('ArLabel',)

class ArLabel(Label):
    text=StringProperty()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #self.font_name=
        self._label.text=ar(self.text)
    def _trigger_texture_update(self, name=None, source=None, value=None):
        if source:
            if name == 'text':
                self._label.text = ar(value)
                self._trigger_texture()
            else:
                return super()._trigger_texture_update(name,source,value)




