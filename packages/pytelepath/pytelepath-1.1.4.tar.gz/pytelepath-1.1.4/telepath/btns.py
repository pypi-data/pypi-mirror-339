import dataclasses
from typing import Any

import telegram
from telepath._callbacks import _pack_convert, _unpack_convert



@dataclasses.dataclass
class TgBtnInfo:
    msg_type: str
    btn_type: str
    btn_id: str
    value: Any
    is_dead: bool = False
    
    
    def to_tg(self) -> (str, str):
        target = [self.msg_type, self.btn_type, self.btn_id, self.value, self.version]
        target = [_pack_convert(v) for v in target]
        cbd = "/".join(target)
        assert len(cbd) <= 64
        
        return cbd


@dataclasses.dataclass
class CallbackData:
    cbd: str
    
    
    def to_dict(self):
        l = self.cbd.split("/")
        l = list(map(_unpack_convert, l))
        msg_type, btn_type, btn_id, value, version = l
        return TgButton("", msg_type, btn_type, btn_id, value)

@dataclasses.dataclass
class TgButton:
    text: str
    info: TgBtnInfo


# ikb = {'text': '', 'callback_data': ''}
# text, cbd = ikb['text'], CallbackData(ikb['callback_data'])
# TgButton(text, TgBtnInfo(*cbd.__dict__))
