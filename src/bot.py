import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from services.stock_service import StockService
from dotenv import load_dotenv

load_dotenv()

import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Handler functions ---
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_message = (
        f"Xin chào {user.mention_html()}! 👋\n\n"
        "Tôi là bot tra cứu giá cổ phiếu.\n"
        "Gửi mã cổ phiếu (VD: VNM, ACB, VIC,...) để nhận giá hiện tại.\n"
        "Hoặc dùng lệnh /price <mã cổ phiếu>\n\n"
        "Ví dụ: /price VNM"
    )
    await update.message.reply_html(welcome_message)

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Các lệnh có sẵn:\n"
        "/start - Khởi động bot\n"
        "/help - Hiển thị trợ giúp\n"
        "/price <mã> - Xem giá cổ phiếu\n\n"
        "Hoặc bạn có thể gửi trực tiếp mã cổ phiếu (VD: VNM)"
    )
    await update.message.reply_text(help_text)

async def price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Vui lòng nhập mã cổ phiếu. Ví dụ: /price VNM")
        return
    stock_code = context.args[0].upper()
    await reply_stock_price(update, stock_code)

async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    stock_code = update.message.text.upper()
    if 2 <= len(stock_code) <= 5 and stock_code.isalpha():
        await reply_stock_price(update, stock_code)
    else:
        await update.message.reply_text(
            "Vui lòng gửi mã cổ phiếu hợp lệ (2-5 ký tự). Ví dụ: VNM, ACB, VIC"
        )

async def reply_stock_price(update: Update, stock_code: str) -> None:
    try:
        msg = await update.message.reply_text(f"🔄 Đang tra cứu giá {stock_code}...")
        result = StockService.get_stock_price(stock_code)
        await update.message.reply_text(result)
        await msg.delete()
    except Exception as e:
        error_message = f"❌ Lỗi khi tra cứu giá {stock_code}: {str(e)}"
        logger.error(error_message)
        await update.message.reply_text(error_message)

# --- Main bot setup ---
def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("No token found! Please set TELEGRAM_BOT_TOKEN environment variable.")
        return
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("price", price_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main() 