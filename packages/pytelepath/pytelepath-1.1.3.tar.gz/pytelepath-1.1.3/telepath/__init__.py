import telegram as ptb

from ._callbacks import CoolBackData
from . import stateful_widgets as sw
from . import decrs, dto, logs, tgmixins, tgmixins

ikb = ptb.InlineKeyboardButton
ikcb = lambda text, cbd: ptb.InlineKeyboardButton(text, callback_data=cbd)
ikm = ptb.InlineKeyboardMarkup


def one_row_ikbm(btns: list):
    kb = [[ptb.InlineKeyboardButton(btn[0], callback_data=btn[1]) for btn in btns]]
    return ptb.InlineKeyboardMarkup(kb)


def one_col_ikbm(btns: list):
    kb = [[ptb.InlineKeyboardButton(btn[0], callback_data=btn[1])] for btn in btns]
    return ptb.InlineKeyboardMarkup(kb)


def with_checked_emoji(checked, text):
    return f"{'✅ ' if checked else ''}{text}"


def with_correct_taped_emoji(text, is_correct, is_taped):
    prepend = ""
    if is_correct:
        prepend = "✅ "
    elif is_taped:
        prepend = "❌ "
    nice_text = f"{prepend}{text}"
    return nice_text


class BtnGen:
    def __init__(self, msg_type, btn_type):
        self.msg_type = msg_type
        self.btn_type = btn_type
    
    
    def btn(self, text: str, btn_id, value=None):
        return sw.TgBtn.from_params(text, btn_id, self.btn_type, self.msg_type, value=value)

    def __call__(self, text: str, btn_id, value=None):
        return self.btn(text, btn_id, value)
    

class TgMsg:
    def text(self):
        ...
    
    
    def inline_keyboard(self):
        ...
    
    
    async def on_ikb_callback(self, u: dto.TgUpd):
        ...
    
    
    def _btn_gen(self, btn_type):
        return BtnGen(self.MSG_TYPE, btn_type)
