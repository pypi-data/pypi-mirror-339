import itertools
from typing import Any

import telegram as t

from . import dto, stateful_widgets as sw
from ._utils import *



class MessageWithButtonsMeta(type):
    def __new__(cls, name, bases, dct):
        buttons = {name: value for name, value in dct.items() if isinstance(value, sw.TgBtn)}
        dct['buttons'] = buttons
        return super().__new__(cls, name, bases, dct)


class ChooseSaveMessage(metaclass=MessageWithButtonsMeta):
    
    def __init__(self, model: Any):
        self.model = model
    
    
    def text(self):
        return "Выберите в какие универы регаться:"
    
    
    def keyboard(self) -> list[list[sw.TgBtn]] | None:
        return None
    
    
    def from_tg(self, u: dto.TgUpd):
        kbd = sw.InlineKeyboard.btn_dict(u.kbm)
        mvs = set(self.model.__annotations__.keys())
        for btn_id in kbd:
            print(f"DebugToDelete32423423 {btn_id}")
            if btn_id in mvs:
                setattr(self.model, btn_id, kbd[btn_id].value)
        return self
    
    def to_tg(self) -> (str, t.InlineKeyboardMarkup):
        mvs = set(self.model.__annotations__.keys())
        
        kb = self.keyboard()
        flatten_kb = itertools.chain.from_iterable(kb)
        for btn in flatten_kb:
            if btn.btn_id in mvs:
                btn.value = getattr(self.model, btn.btn_id)
    
        kb = kb and sw.InlineKeyboard.to_tg(kb) or None
        return self.text(), kb
