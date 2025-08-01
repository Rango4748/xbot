#!/bin/bash

echo "🔧 در حال نصب ربات XUI پنل..."

# نصب پیش‌نیازها
sudo apt update
sudo apt install -y python3 python3-pip git

# کلون کردن پروژه
git clone https://github.com/Rango4748/xbot.git
cd xbot || exit

# نصب کتابخانه‌ها
pip3 install -r requirements.txt

# گرفتن اطلاعات از کاربر
read -p "Enter your Telegram Bot Token: " BOT_TOKEN
read -p "Enter your Panel URL (e.g., http://your-server:port): " PANEL_URL
read -p "Enter your Panel Username: " PANEL_USERNAME
read -p "Enter your Panel Password: " PANEL_PASSWORD

# ساخت فایل config.json
cat <<EOF > config.json
{
  "BOT_TOKEN": "$BOT_TOKEN",
  "PANEL_URL": "$PANEL_URL",
  "PANEL_USERNAME": "$PANEL_USERNAME",
  "PANEL_PASSWORD": "$PANEL_PASSWORD"
}
EOF

# اجرای ربات در بک‌گراند
nohup python3 bot.py > log.txt 2>&1 &

echo "✅ ربات با موفقیت نصب و اجرا شد!"
echo "📄 لاگ‌ها: tail -f log.txt"
