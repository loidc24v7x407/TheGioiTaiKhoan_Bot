from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# ✅ Lấy token từ biến môi trường (Render -> Environment -> BOT_TOKEN)
TOKEN = os.getenv("BOT_TOKEN")
print("🔍 DEBUG TOKEN:", TOKEN)  # thêm dòng này
if not TOKEN:
    print("❌ LỖI: BOT_TOKEN chưa được khai báo trong Render > Environment tab.")
    exit()

# ==========================
# 1️⃣ Lệnh /start
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
# 2️⃣ Xử lý khi bấm nút menu
# ==========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # tránh lỗi “loading...”

    data = query.data
    vietqr_base = "https://img.vietqr.io/image/LPB-LP07798725354-qr_only.png"

    if data == "canvanon":
        text = (
            "🧾 *Canva Pro Nonprofits*\n"
            "💰 Giá: 200.000đ / năm\n\n"
            "📲 Quét mã QR bên dưới để thanh toán:\n"
            f"{vietqr_base}\n\n"
            "➡ Sau khi chuyển, gửi ảnh biên lai để xác nhận đơn nhé!"
        )

    elif data == "canvaedu":
        text = (
            "🎓 *Canva Pro Education*\n"
            "💰 Giá: 150.000đ / năm\n"
            f"📲 Quét QR để thanh toán:\n{vietqr_base}"
        )

    elif data == "ggedu":
        text = (
            "📧 *Google Workspace Education*\n"
            "💰 Giá: 250.000đ / năm\n"
            f"📲 Thanh toán tại:\n{vietqr_base}"
        )

    elif data == "ggnon":
        text = (
            "🌐 *Google Workspace Nonprofits*\n"
            "💰 Giá: 200.000đ / năm\n"
            f"📲 Thanh toán tại:\n{vietqr_base}"
        )

    elif data == "myorders":
        text = "📦 Bạn chưa có đơn hàng nào. Hãy đặt thử ngay nhé!"

    elif data == "check":
        text = "🔍 Hệ thống đang kiểm tra slot còn lại..."

    elif data == "refresh":
        text = "🔄 Cập nhật dữ liệu slot mới nhất..."

    elif data == "help":
        text = (
            "❓ *Hướng dẫn sử dụng bot*\n\n"
            "1️⃣ Gõ /start để mở menu.\n"
            "2️⃣ Chọn sản phẩm bạn muốn mua.\n"
            "3️⃣ Quét QR để thanh toán đúng số tiền.\n"
            "4️⃣ Gửi ảnh biên lai để xác nhận đơn ✅"
        )

    else:
        text = "⚠️ Lựa chọn không hợp lệ, vui lòng thử lại!"

    await query.edit_message_text(text=text, parse_mode="Markdown")

# ==========================
# 3️⃣ Khởi chạy bot
# ==========================
def main():
    print("🚀 Bot đang chạy với VietQR động...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()


