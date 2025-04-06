import pkgutil

def fun(filename: str) -> bytes:
    return pkgutil.get_data(__name__, f"fun/{filename}")

def list_fun() -> list[str]:
    return [
        "alaki.json.enc",
        "chandsaletbod.json.enc",
        "chanvaghte.json.enc",
        "dastan.json.enc",
        "deghatkardin.json.enc",
        "dialog.json.enc",
        "eteraf.json.enc",
        "fantezi.json.enc",
        "khaterat.json.enc",
        "mrghazi.json.enc",
        "panapa.json.enc",
        "ravanshenasi.json.enc",
    ]


from .bot import (
    Bot, 
    CopyTextButton, 
    ChatPhoto, 
    InputMedia, 
    InputMediaPhoto,
    InputMediaVideo, 
    InputMediaAnimation, 
    InputMediaAudio, 
    InputMediaDocument, 
    InputFile,
    User,
    File
)
from .filter import Filters
from .ReplyKeyboard import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo as ReplyWebAppInfo
from .InlineKeyboard import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo as InlineWebAppInfo
from .update_wrapper import (
    UpdateWrapper, 
    CallbackQuery, 
    Message, 
    Chat,
    ChatMember,
    PhotoSize,
    Audio,
    Document,
    Voice,
    Location,
    Video,
    Invoice,
    Sticker
)
from .Database import Database
from .states import (
    State,
    TimedState,
    ChatState,
    StateMachine,
    AsyncState,
    AsyncChatState,
    StateManager
)

__all__ = [
    'Bot',
    'CopyTextButton',
    'ChatPhoto',
    'ReplyKeyboardMarkup', 
    'KeyboardButton',
    'InlineKeyboardMarkup', 
    'InlineKeyboardButton',
    'WebAppInfo',
    'InputMedia',
    'InputMediaPhoto',
    'InputMediaVideo',
    'InputMediaAnimation',
    'InputMediaAudio',
    'InputMediaDocument',
    'InputFile',
    'Filters',
    'Database',
    'State',
    'TimedState',
    'ChatState',
    'StateMachine',
    'AsyncState',
    'AsyncChatState',
    'StateManager',
    'UpdateWrapper',
    'CallbackQuery',
    'Message',
    'User',
    'Chat',
    'ChatParameter',
    'ChatMember',
    'PhotoSize',
    'Audio',
    'Document',
    'Voice',
    'Location',
    'Video',
    'Invoice',
    'Sticker',
    'SuccessfulPayment',
    'File'
]