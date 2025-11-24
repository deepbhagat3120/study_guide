!pip install python-telegram-bot PyPDF2 google-genai

import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from google import genai
import PyPDF2

BOT_TOKEN = "8303688288:AAE3LUx8CoyZ1zx6vUI6J86C91zDw10bqQc"
GEMINI_KEY = "AIzaSyCgj6pHXWsNpOgyDEIQmel5XIMwQW2y0j8"

client = genai.Client(api_key=GEMINI_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a PDF and I will summarize it.")

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = await update.message.document.get_file()
        file_path = "temp.pdf"
        await file.download_to_drive(file_path)

        reader = PyPDF2.PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            await update.message.reply_text("Could not extract text.")
            return

        prompt = (
            "Summarize this study material in clear bullet points. "
            "Keep it short, concise, simple and helpful for last minute revisions during exams.\n\n" + text
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        summary = response.text[:4000]

        await update.message.reply_text(summary)

    except Exception:
        await update.message.reply_text("Error while processing PDF.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))

    await app.run_polling()

# Run inside Jupyter / Colab
import nest_asyncio
nest_asyncio.apply()

import asyncio
asyncio.run(main())

