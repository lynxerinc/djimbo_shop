# - *- coding: utf- 8 - *-
from aiogram import Router
from aiogram.filters import ExceptionMessageFilter
from aiogram.handlers import ErrorHandler

from tgbot.utils.misc.bot_logging import bot_logger

router = Router(name=__name__)


# Erreur lors de la tentative de modification d'un message sans aucun changement
@router.errors(ExceptionMessageFilter(
    "Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message")
)
class MyHandler(ErrorHandler):
    async def handle(self):
        # Journaliser l'exception avec tous les détails pertinents
        bot_logger.exception(
            f"====================\n"
            f"Nom de l'exception : {self.exception_name}\n"
            f"Message de l'exception : {self.exception_message}\n"
            f"===================="
        )
