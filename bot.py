from telegram.ext import Updater, CommandHandler
import requests
import json
import datetime

# خواندن تنظیمات از config.json
with open("config.json") as f:
    config = json.load(f)

BOT_TOKEN = config["BOT_TOKEN"]
PANEL_URL = config["PANEL_URL"]
PANEL_USERNAME = config["PANEL_USERNAME"]
PANEL_PASSWORD = config["PANEL_PASSWORD"]

def start(update, context):
    update.message.reply_text("سلام! برای دیدن کانفیگ‌ها از /configs استفاده کن.")

def get_configs():
    try:
        login_url = f"{PANEL_URL}/login"
        configs_url = f"{PANEL_URL}/panel/api/inbounds/list"
        login_data = {"username": PANEL_USERNAME, "password": PANEL_PASSWORD}
        session = requests.Session()
        login_response = session.post(login_url, json=login_data)

        if login_response.status_code != 200:
            return None

        response = session.get(configs_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def configs(update, context):
    data = get_configs()
    if data:
        message = "📡 کانفیگ‌های موجود:\n\n"
        for inbound in data.get("obj", []):
            for client in inbound.get("clients", []):
                expiry = int(client.get("expiryTime", 0))
                expiry_str = "ندارد"
                if expiry > 0:
                    dt = datetime.datetime.fromtimestamp(expiry)
                    expiry_str = dt.strftime("%Y-%m-%d %H:%M")

                message += (
                    f"👤 کاربر: {client.get('email', 'بدون‌نام')}\n"
                    f"🧩 SubID: {client.get('subId', '-')}\n"
                    f"📦 حجم: {client.get('totalGB', '-')} GB\n"
                    f"⏰ انقضا: {expiry_str}\n\n"
                )
        update.message.reply_text(message)
    else:
        update.message.reply_text("❌ خطا در اتصال به پنل یا دریافت اطلاعات.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("configs", configs))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
