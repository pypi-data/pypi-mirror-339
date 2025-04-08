from arabic_reshaper import reshape
from bidi.algorithm import get_display


def ar(text):
    return get_display(reshape(text))












