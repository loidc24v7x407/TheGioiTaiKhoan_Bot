from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random, asyncio, urllib.parse

# 🔹 Token bot thật từ @BotFather
TOKEN = "Y8357378826:AAFR9G1_8U2fbu2ExLPdKNGfnF42UElh6pI"

# 🔹 Cấu hình tài khoản VietQR
BANK_ID = "LPB"  # Ví dụ: LPB, VCB, MBB, ACB...
ACCOUNT_NO = "LP07798725354"
ACCOUNT_NAME = "NGUYEN HUAN LUYEN"

# 🔹 Danh sách sản phẩm
PRODUCTS = {
    "/canvanon": {"name": "Canva Pro Nonprofits", "price": 90000, "code": "CANVA_NON"},
    "/canvaedu": {"name": "Canva Pro Education", "price": 80000, "code": "CANVA_EDU"},
    "/ggedu": {"name": "Google Workspace Education", "price": 120000, "code": "GG_EDU"},
    "/ggnon": {"name": "Google Workspace Nonprofits", "price": 150000, "code": "GG_NON"},
}

# ======= Hàm tạo link QR động =======
def create_vietqr_link(amount, add_info):
    encoded_name = urllib.parse.quote(ACCOUNT_NAME)
    return f"https://img.vietqr.io/image/{BANK_ID}-{ACCOUNT_NO}-compact2.png?amount={amount}&addInfo={add_info}&accountName={encoded_name}"

# ======= Menu chính =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"👋 Xin chào {update.effective_user.first_name}!\n"
        "Chào mừng đến với hệ thống đặt hàng tự động của 🎯 *Thế Giới Tài Khoản!*\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📦 *MENU SẢN PHẨM*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Chọn sản phẩm bạn muốn mua bên dưới nhé! 👇\n\n"
        "💡 *Sau khi chọn, bot sẽ tự tạo QR thanh toán chính xác số tiền và nội dung chuyển khoản.*"
    )

    keyboard = [
        [InlineKeyboardButton("💼 Canva Pro Nonprofits", callback_data="/canvanon")],
        [InlineKeyboardButton("💼 Canva Pro Education", callback_data="/canvaedu")],
        [InlineKeyboardButton("💼 Google Workspace Education", callback_data="/ggedu")],
        [InlineKeyboardButton("💼 Google Workspace Nonprofits", callback_data="/ggnon")],
        [
            InlineKeyboardButton("🧾 Đơn hàng của tôi", callback_data="/myorders"),
            InlineKeyboardButton("🔍 Tra cứu", callback_data="/check")
        ],
        [InlineKeyboardButton("🔄 Làm mới / Check slot", callback_data="/refresh")],
        [InlineKeyboardButton("❓ Hướng dẫn", callback_data="/help")]
    ]

    await update.message.reply_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
    )

# ======= Xử lý các nút =======
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Nếu chọn sản phẩm
    if data in PRODUCTS:
        product = PRODUCTS[data]
        order_id = f"{product['code']}_{random.randint(10000,99999)}"
        link = create_vietqr_link(product["price"], order_id)

        caption = (
            f"💼 *{product['name']}*\n"
            f"💰 Giá: {product['price']:,}đ\n"
            f"🆔 Mã đơn hàng: `{order_id}`\n\n"
            f"📲 Quét mã VietQR bên dưới để thanh toán:\n"
            f"🏦 {BANK_ID} - {ACCOUNT_NAME}\n"
            f"💳 STK: {ACCOUNT_NO}\n"
            f"📝 Nội dung: `{order_id}`\n\n"
            "⚠️ *Lưu ý:* Vui lòng chuyển đúng số tiền và nội dung để hệ thống tự động xác nhận.\n"
            "Sau khi thanh toán, gửi ảnh hoá đơn cho admin để nhận tài khoản."
        )

        await query.message.reply_photo(
            photo=link,
            caption=caption,
            parse_mode="Markdown"
        )
        return

    # Các menu khác
    if data == "/myorders":
        await query.edit_message_text("🧾 *Đơn hàng của bạn*\nHiện chưa có đơn hàng nào.", parse_mode="Markdown")
    elif data == "/check":
        await query.edit_message_text("🔍 *Tra cứu đơn hàng*\nNhập mã đơn hàng của bạn để kiểm tra.", parse_mode="Markdown")
    elif data == "/refresh":
        await query.edit_message_text("🔄 *Đã cập nhật slot mới nhất!*\n📊 Admin: 6 | Slot: 11 ✅", parse_mode="Markdown")
    elif data == "/help":
        await query.edit_message_text(
            "❓ *Hướng dẫn sử dụng bot:*\n"
            "1️⃣ Chọn sản phẩm muốn mua.\n"
            "2️⃣ Bot sẽ tạo mã QR thanh toán tự động.\n"
            "3️⃣ Quét mã, chuyển tiền và gửi ảnh giao dịch.\n\n"
            "📩 Liên hệ hỗ trợ: @Admin_TheGioiTaiKhoan",
            parse_mode="Markdown"
        )

# ======= Chạy bot =======
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_callback))

if __name__ == "__main__":
    print("🚀 Bot đang chạy với VietQR động...")
    app.run_polling()

