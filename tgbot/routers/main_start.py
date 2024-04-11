# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery

from tgbot.database.db_settings import Settingsx
from tgbot.keyboards.inline_user import user_support_finl
from tgbot.keyboards.reply_main import menu_frep
from tgbot.utils.const_functions import ded
from tgbot.utils.misc.bot_filters import IsBuy, IsRefill, IsWork
from tgbot.utils.misc.bot_models import FSM, ARS

# Callbacks à ignorer pour les achats
prohibit_buy = [
    'buy_category_swipe',
    'buy_category_open',
    'buy_position_swipe',
    'buy_position_open',
    'buy_item_open',
    'buy_item_confirm',
]

# Callbacks à ignorer pour les recharges
prohibit_refill = [
    'user_refill',
    'user_refill_method',
    'Pay:',
    'Pay:QIWI',
    'Pay:Yoomoney',
]

router = Router(name=__name__)


################################################################################
###################### STATUT DES TRAVAUX TECHNIQUES ###########################
# Filtre pour les travaux techniques - message
@router.message(IsWork())
async def filter_work_message(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_settings = Settingsx.get()

    if get_settings.misc_support != "None":
        return await message.answer(
            "<b>⛔ Le bot est en maintenance technique.</b>",
            reply_markup=user_support_finl(get_settings.misc_support),
        )

    await message.answer("<b>⛔ Le bot est en maintenance technique.</b>")


# Filtre pour les travaux techniques - callback
@router.callback_query(IsWork())
async def filter_work_callback(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await call.answer("⛔ Le bot est en maintenance technique.", True)


################################################################################
############################### STATUT DES ACHATS ###############################
# Filtre pour la disponibilité des achats - message
@router.message(IsBuy(), F.text == "🎁 Acheter")
@router.message(IsBuy(), StateFilter('here_item_count'))
async def filter_buy_message(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer("<b>⛔ Les achats sont temporairement désactivés.</b>")


# Filtre pour la disponibilité des achats - callback
@router.callback_query(IsBuy(), F.data.startswith(prohibit_buy))
async def filter_buy_callback(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await call.answer("⛔ Les achats sont temporairement désactivés.", True)


################################################################################
############################### STATUT DES RECHARGES ###########################
# Filtre pour la disponibilité des recharges - message
@router.message(IsRefill(), StateFilter('here_pay_amount'))
async def filter_refill_message(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer("<b>⛔ La recharge est temporairement désactivée.</b>")


# Filtre pour la disponibilité des recharges - callback
@router.callback_query(IsRefill(), F.data.startswith(prohibit_refill))
async def filter_refill_callback(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await call.answer("⛔ La recharge est temporairement désactivée.", True)


################################################################################
##################################### DIVERS ###################################
# Ouverture du menu principal
@router.message(F.text.in_(('🔙 Menu principal', '/start')))
async def main_start(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        ded("""
            🔸 Le bot est prêt à être utilisé.
            🔸 Si les boutons d'assistance ne s'affichent pas,
            🔸 Tapez /start
        """),
        reply_markup=menu_frep(message.from_user.id),
    )
