from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.config.setting import settings

WELCOME_STYLE = {
    'text': (
        "🥳Welcome to UFOOL - the Duolingo of Web3!🎉\n\n"
        "🧑‍🚀Here, you'll duel in quiz battles, master Web3, and climb the leaderboards for fame and generous rewards. \n\n"
        "🤪Bull market coming, are you ready to prove you're not just another crypto FOOL? The quest for Web3 literacy begins! 😎 \n\n"
        "💰Share $200 USDT first and let the battle on fire!🔥\n\n"
        "🙌🏻Join UFOOL now! 👉 t.me/ufool_bot\n\n\n"
    ),
    'keyboard': InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛸PLAY", settings.ufool.mini_app_url),
            InlineKeyboardButton("📢Ann", settings.ufool.ann_url),
            InlineKeyboardButton("𝕏", settings.UFOOL_X)
        ]
    ])
}
