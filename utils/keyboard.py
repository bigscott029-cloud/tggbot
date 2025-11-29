from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard(is_registered=False, is_coach=False):
    kb = [
        [InlineKeyboardButton("How It Works", callback_data="how_it_works")],
        [InlineKeyboardButton("Get Registered", callback_data="package_selector")],
        [InlineKeyboardButton("Help", callback_data="help")],
    ]
    if is_registered:
        kb = [
            [InlineKeyboardButton("My Stats", callback_data="stats")],
            [InlineKeyboardButton("Daily Tasks", callback_data="daily_tasks")],
            [InlineKeyboardButton("Earn Extra", callback_data="earn_extra")],
        ]
    if is_coach:
        kb.append([InlineKeyboardButton("Coach Dashboard", callback_data="coach_dashboard")])
    kb.append([InlineKeyboardButton("Back", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def help_menu_keyboard():
    from config.settings import HELP_TOPICS
    kb = [[InlineKeyboardButton(v["label"], callback_data=k)] for k, v in HELP_TOPICS.items()]
    kb.append([InlineKeyboardButton("Back", callback_data="menu")])
    return InlineKeyboardMarkup(kb)
