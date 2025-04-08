import dataclasses
from collections import OrderedDict
from typing import Any

import telegram as t

import telepath as tp

import copy



class TgBtn:
    def __init__(self, text: str= None, btn_id: str= None, btn_type: str= None, msg_type: str= None, value: Any = None):
        self.text = text
        self.btn_id = btn_id
        self.btn_type = btn_type
        self.msg_type = msg_type
        self.value = value
        self.is_dead = False
    
    
    def _callback_data(self) -> str:
        if self.is_dead:
            return "dead"
        else:
            return tp.CoolBackData2(self.msg_type, self.btn_type, self.btn_id, self.value).pack()
    
    
    def _text(self) -> str:
        return self.text
    
    
    def to_tg(self):
        return tp.IKCB(self._text(), self._callback_data())
    
    def from_tg(self, cbdstr):
        self.is_dead = cbdstr == "dead"
        cbd = None if self.is_dead else tp.CoolBackData2().unpack(cbdstr)
        self.msg_type = cbd and cbd.msg_type or None
        self.btn_type = cbd and cbd.btn_type or None
        self.btn_id = cbd and cbd.btn_id or None
        self.value = cbd.value if cbd is not None else None
        return self
    
    def __call__(self, text: str = None, btn_id: str = None, btn_type: str = None, msg_type: str = None, value: Any = None, is_dead: bool = None):
        bc = copy.copy(self)
        bc.text = text or bc.text
        bc.btn_id = btn_id or bc.btn_id
        bc.btn_type = btn_type or bc.btn_type
        bc.msg_type = msg_type or bc.msg_type
        bc.value = value if value is not None else bc.value
        bc.is_dead = is_dead if is_dead is not None else bc.is_dead
        return bc


class ValueTgBtn(TgBtn):
    
    def _text(self) -> str:
        return str(self.value)


class CheckableTgBtn(ValueTgBtn):
    
    def __init__(self, text: str, checked: bool, btn_id: str, btn_type: str, msg_type: str):
        super().__init__(text, btn_id, btn_type, msg_type, value=checked)
    
    
    def _text(self) -> str:
        return tp.with_checked_emoji(self.value, self.text)


class InlineKeyboard:
    
    @staticmethod
    def btn_dict(mu: t.InlineKeyboardMarkup) -> dict[str, TgBtn]:
        btn_dict = OrderedDict()
        for row in mu.inline_keyboard:
            for b in row:
                tgb = TgBtn().from_tg(b.callback_data)
                btn_dict[tgb.btn_id] = tgb
        return btn_dict
    
    
    @staticmethod
    def to_tg(kb_tree) -> t.InlineKeyboardMarkup:
        rows = []
        for row in kb_tree:
            new_row = [b.to_tg() for b in row]
            rows.append(new_row)
        return t.InlineKeyboardMarkup(rows)
