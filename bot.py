from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = "8357378826:AAH5j0DcdlWQ83We4mudtJfyORxc94VZQwM"

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
        "👋 Xin chào Thế Giới Tài Khoản!\n"
        "Chào mừng đến với hệ thống đặt hàng tự động của 🎯 *Thế Giới Tài Khoản!*\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "📦 *MENU SẢN PHẨM*\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "Chọn sản phẩm bạn muốn mua bên dưới nhé! 👇\n\n"
        "💡 Sau khi chọn, bot sẽ tự tạo QR thanh toán chính xác số tiền và nội dung chuyển khoản.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ==========================
# 2️⃣ Callback handler
# ==========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Phản hồi để Telegram không báo lỗi “loading...”
    
    data = query.data

    if data == "canvanon":
        await query.edit_message_text(
            "🧾 *Canva Pro Nonprofits*\n"
            "Giá: 200.000đ / năm\n"
            "Vui lòng quét mã QR sau để thanh toán:\n"
            "https://img.vietqr.io/image/LPB-LP07798725354-qr_only.png",
            parse_mode="Markdown"
        )
    elif data == "canvaedu":
        await query.edit_message_text("🎓 Canva Pro Education — chỉ 150.000đ / năm!")
    elif data == "ggedu":
        await query.edit_message_text("📧 Google Workspace for Education — 250.000đ / năm!")
    elif data == "ggnon":
        await query.edit_message_text("🌐 Google Workspace for Nonprofits — 200.000đ / năm!")
    elif data == "myorders":
        await query.edit_message_text("📦 Bạn chưa có đơn hàng nào.")
    elif data == "check":
        await query.edit_message_text("🔍 Hệ thống đang kiểm tra slot còn lại...")
    elif data == "refresh":
        await query.edit_message_text("🔄 Đang cập nhật dữ liệu slot...")
    elif data == "help":
        await query.edit_message_text(
            "❓ *Hướng dẫn sử dụng bot*\n\n"
            "1️⃣ Gõ /start để mở menu\n"
            "2️⃣ Chọn sản phẩm muốn mua\n"
            "3️⃣ Quét QR thanh toán\n"
            "4️⃣ Chờ bot xác nhận đơn tự động ✅",
            parse_mode="Markdown"
        )

# ==========================
# 3️⃣ Khởi chạy bot
# ==========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("🚀 Bot đang chạy với VietQR động...")
app.run_polling()


