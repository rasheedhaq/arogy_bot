"""
Main entry point for Arogyamitra Telegram Bot
"""
from telegram.ext import Application
from app.config import TELEGRAM_BOT_TOKEN
from app.bot_intelligent import setup_handlers

def main():
    """Start the bot"""
    print("Starting Arogyamitra Bot...")
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Setup handlers
    setup_handlers(application)
    
    # Start bot
    print("Bot is running. Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()