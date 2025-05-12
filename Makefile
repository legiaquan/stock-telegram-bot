bot:
	python3 src/bot.py

install:
	pip install -r requirements.txt

run:
	python3 src/bot.py

freeze:
	pip freeze > requirements.txt

init:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "\n✅ Đã tạo virtualenv và cài đặt dependencies."
	@echo "\n👉 Để kích hoạt môi trường ảo, chạy: source venv/bin/activate"
	@echo "👉 Để chạy bot: make bot"
