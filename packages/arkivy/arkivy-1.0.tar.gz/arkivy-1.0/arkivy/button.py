
from .utils import ar
from .label import ArLabel
from kivy.uix.button import Button
from .ripple import RectangularRippleBehavior

__all__=('ArButton',)


class ArButton(ArLabel,RectangularRippleBehavior,Button):
    pass












