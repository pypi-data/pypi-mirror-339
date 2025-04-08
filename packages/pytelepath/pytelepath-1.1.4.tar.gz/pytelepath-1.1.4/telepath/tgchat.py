import dto



class TgBotChat:
    
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.state = "freedom"
    
    def on_message(self, u: dto.TgUpd):
        ...
    
    def on_command(self, u: dto.TgUpd):
        ...

    def on_ikb_callback(self, u: dto.TgUpd):
        ...