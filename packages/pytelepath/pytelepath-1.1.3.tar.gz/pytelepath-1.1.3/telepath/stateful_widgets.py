import dataclasses
import enum
from collections import OrderedDict
from itertools import chain

import telegram as t
import telepath as tp
from typing import Any
from _callbacks import _unpack_convert


@dataclasses.dataclass
class TgBtn:
    text: str
    btn_id: str
    btn_type: str
    msg_type: str
    value: Any = None
    checked: bool | None = None
    corr_id: str | None = None
    
    
    @staticmethod
    def checked_text_view(checked, text):
        return tp.with_checked_emoji(checked, text)
    
    
    def __call__(self, value=None, checked=None, corr_id=None):
        new = dataclasses.replace(self)
        new.value = value or new.value
        new.checked = checked or new.checked
        new.corr_id = corr_id or new.corr_id
        return new
    
    
    def text(self):
        if self.btn_model.checked is not None:
            return self.__class__.checked_text_view(self.cbdo.checked, self._text)
        else:
            return
    
    
    def callback_data(self) -> str:
        return tp.CoolBackData(self.msg_type, self.btn_type, self.btn_id,
                               self.value, self.checked, self.corr_id).pack()
    
    
    def to_tg(self) -> (str, str):
        return self.text(), self.callback_data()
    
    
    @staticmethod
    def from_str(text, cbd):
        l = cbd.split("/")
        checked = _unpack_convert(l[4], bool)
        version = _unpack_convert(l[6], int) or 2  # v2 for now
        l = list(map(_unpack_convert, l))
        msg_type, btn_type, btn_id, value, _, corr_id, _ = l
        return TgBtn(text, btn_id, btn_type, msg_type, value, checked, corr_id)
    
    
    # class PtbTgBtn(TgBtn):
    def to_ptb(self) -> t.InlineKeyboardButton:
        return t.InlineKeyboardButton(*self.to_tg())
    
    
    @staticmethod
    def from_ptb(ikb: t.InlineKeyboardButton):
        return TgBtn.from_str(ikb.text, tp.CoolBackData.from_str(ikb.callback_data))


class InlineKeyboard:
    
    def __init__(self, kb_tree):
        self.kb_tree: list[list[TgBtn]] = kb_tree
        pairs = [(b.id, b) for b in chain.from_iterable(kb_tree)]
        self.btn_dict = OrderedDict(pairs)
    
    
    @staticmethod
    def from_markup(mu: t.InlineKeyboardMarkup):
        kb_tree = []
        for row in mu.inline_keyboard:
            kb_row = [TgBtn.from_ptb(b) for b in row]
            kb_tree.append(kb_row)
        return InlineKeyboard(kb_tree)
    
    
    @staticmethod
    def from_list(btn_list):
        return InlineKeyboard([[b] for b in btn_list])
    
    
    def compile(self):
        rows = [[tp.ikb(b.text(), callback_data=b.callback_data()) for b in row] for row in self.kb_tree]
        return t.InlineKeyboardMarkup(rows)


class KbLayout(enum.Enum):
    COL = 1
    ROW = 2
    CUSTOM = 3


class Message:
    def __init__(self, text, kb):
        self.text = text
        self.kb = kb
