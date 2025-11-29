from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from .start import start, show_menu
from .callbacks import button_handler
from .payments import handle_payment_screenshot
from .admin import get_admin_handlers

def register_all_handlers(app: Application):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_payment_screenshot))
    for handler in get_admin_handlers():
        app.add_handler(handler)
