from telegram.ext import Updater, CommandHandler
import requests

# تنظیمات اولیه
BOT_TOKEN = "YOUR_BOT_TOKEN"  # توکنی که از BotFather گرفتی
PANEL_URL = "YOUR_PANEL_URL"  # آدرس پنل (مثل http://your-server:port)
PANEL_USERNAME = "YOUR_PANEL_USERNAME"  # نام کاربری پنل
PANEL_PASSWORD = "YOUR_PANEL_PASSWORD"  # رمز عبور پنل

def start(update, context):
    update.message.reply_text("سلام! برای دیدن کانفیگ‌ها از /configs استفاده کن.")

def get_configs():
    try:
        # ورود به پنل (برای سنایی/علیرضا)
        login_url = f"{PANEL_URL}/login"
        configs_url = f"{PANEL_URL}/panel/api/inbounds/list"
        login_data = {"username": PANEL_USERNAME, "password": PANEL_PASSWORD}
        session = requests.Session()
        session.post(login_url, json=login_data)
        response = session.get(configs_url)
        return response.json()
    except:
        return None

def configs(update, context):
    data = get_configs()
    if data:
        message = "کانفیگ‌های پنل:\n"
        for inbound in data.get("obj", []):
            for client in inbound.get("clients", []):
                message += f"کاربر: {client['email']}\nلینک: {client['subId']}\nحجم: {client['totalGB']} GB\nانقضا: {client['expiryTime']}\n\n"
        update.message.reply_text(message)
    else:
        update.message.reply_text("خطا در اتصال به پنل!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("configs", configs))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()