    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Setup handlers
    setup_handlers(application)
    
    # Start bot
    print("Bot is running. Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()