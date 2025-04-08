import telegram as ptb

IKB = ptb.InlineKeyboardButton
IKCB = lambda text, cbd: ptb.InlineKeyboardButton(text, callback_data=cbd)
IKM = ptb.InlineKeyboardMarkup