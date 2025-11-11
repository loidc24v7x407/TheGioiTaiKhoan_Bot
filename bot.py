from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# ✅ Lấy token từ biến môi trường trên Render
TOKEN = os.getenv("8357378826:AAEGJX9YAowcWbRzVVoYktme9IF-ZbDsJHA")

if not TOKEN:
    print("❌ LỖI: BOT_TOKEN chưa được khai báo trong Render > Environment tab.")
    exit()

# ==========================
# 1️⃣ /start command
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_keyboard = [
        [InlineKeyboardButton("💼 Canva Pro Nonprofits", callback_data="canvanon")],
        [InlineKeyboardButton("💼 Canva Pro Education", callback_data="canvaedu")],
        [InlineKeyboardButton("💼 Google Workspace Education", callback_data="ggedu")],
        [InlineKeyboardButton("💼 Google Workspace Nonprofits", callback_data="ggnon")],
        [
            InlineKeyboardButton("🧾 Đơn hàng của tôi", callback_data="myorders"),
            InlineKeyboardButton("🔍 Tra cứu", callback_data="check")
        ],
        [InlineKeyboardButton("🔄 Làm mới / Check slot", callback_data="refresh")],
        [InlineKeyboardButton("❓ Hướng dẫn", callback_data="help")]
    ]

    reply_markup = InlineKeyboardMarkup(menu_keyboard)

    await update.message.reply_text(
        "👋 Xin chào *Thế Giới Tài Khoản!*\n"
        "Chào mừng đến với hệ thống đặt hàng tự động 🎯\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "📦 *MENU SẢN PHẨM*\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "Chọn sản phẩm bạn muốn mua bên dưới nhé! 👇\n\n"
        "💡 Sau khi chọn, bot sẽ gửi QR thanh toán tự động qua VietQR.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ==========================
# 2️⃣ Callback handler
# ==========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # bắt buộc có dòng này

    data = query.data
    vietqr_base = "https://img.vietqr.io/image/LPB-LP07798725354-qr_only.png"

    if data == "canvanon":
        await query.edit_message_text(
            text=(
                "🧾 *Canva Pro Nonprofits*\n"
                "💰 Giá: 100.000đ / năm\n\n"
                "📲 Quét mã QR bên dưới để thanh toán:\n"
                f"{vietqr_base}\n\n"
                "➡ Sau khi chuyển, nhắn tin "đã chuyển" để xác nhận!"
            ),
            parse_mode="Markdown"
        )

    elif data == "canvaedu":
        await query.edit_message_text(
            text="🎓 *Canva Pro Education*\n💰 Giá: 50.000đ / năm\n📲 Quét QR để thanh toán:\n"
                 f"{vietqr_base}",
            parse_mode="Markdown"
        )

    elif data == "ggedu":
        await query.edit_message_text(
            text="📧 *Google Workspace Education*\n💰 Giá: 5.000.000đ / năm\n📲 Thanh toán tại:\n"
                 f"{vietqr_base}",
            parse_mode="Markdown"
        )

    elif data == "ggnon":
        await query.edit_message_text(
            text="🌐 *Google Workspace Nonprofits*\n💰 Giá: 8.000.000đ / năm\n📲 Thanh toán tại:\n"
                 f"{vietqr_base}",
            parse_mode="Markdown"
        )

    elif data == "myorders":
        await query.edit_message_text("📦 Bạn chưa có đơn hàng nào. Hãy đặt thử ngay nhé!")

    elif data == "check":
        await query.edit_message_text("🔍 Hệ thống đang kiểm tra slot còn lại...")

    elif data == "refresh":
        await query.edit_message_text("🔄 Cập nhật dữ liệu slot mới nhất...")

    elif data == "help":
        await query.edit_message_text(
            "❓ *Hướng dẫn sử dụng bot*\n\n"
            "1️⃣ Gõ /start để mở menu.\n"
            "2️⃣ Chọn sản phẩm bạn muốn mua.\n"
            "3️⃣ Quét QR để thanh toán đúng số tiền.\n"
            "4️⃣ Gửi ảnh biên lai để xác nhận đơn ✅",
            parse_mode="Markdown"
        )

# ==========================
# 3️⃣ Chạy bot
# ==========================
def main():
    print("🚀 Bot đang chạy với VietQR động...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
