OS := $(shell uname -s 2>/dev/null || echo Windows_NT)

ifeq ($(OS),Windows_NT)
    PYTHON=python3
    VENV_ACTIVATE=venv\Scripts\activate
    VENV_PYTHON=venv\Scripts\python.exe
    PIP_INSTALL=$(VENV_PYTHON) -m pip install
    SHELL_COMMENT=rem
else
    PYTHON=python3
    VENV_ACTIVATE=. venv/bin/activate
    VENV_PYTHON=venv/bin/python
    PIP_INSTALL=$(VENV_PYTHON) -m pip install
    SHELL_COMMENT=\#
endif

.PHONY: init bot api install run freeze clean install-deps help

# Check if we're using problematic Python 3.13
check-python:
	@$(PYTHON) -c "import sys; print(f'Python version: {sys.version}'); exit(0 if sys.version_info < (3, 13) else 1)" || \
	echo "Python 3.13 detected. Using binary-only installation strategy."

init: check-python
	@echo "🔧 Creating virtual environment..."
	$(PYTHON) -m venv venv
	@echo "Upgrading core packages..."
	$(VENV_PYTHON) -m pip install --upgrade pip setuptools wheel
	@echo "Installing dependencies with binary-only strategy..."
	@$(MAKE) install-deps
	@echo ""
	@echo "Đã tạo virtualenv và cài đặt dependencies."
	@echo "Để kích hoạt môi trường ảo, chạy: $(VENV_ACTIVATE)"
	@echo "Để chạy bot: make bot"

# Install dependencies with numpy-safe approach
install-deps:
	@echo "Installing dependencies safely..."
	@echo "Clearing pip cache to avoid corrupted packages..."
	$(VENV_PYTHON) -m pip cache purge
	@echo "Installing NumPy (binary wheels only)..."
	$(PIP_INSTALL) --only-binary=all numpy || \
	$(PIP_INSTALL) --only-binary=all "numpy<2.1" || \
	$(PIP_INSTALL) --find-links https://pypi.org/simple/ --only-binary=all numpy || \
	(echo "Failed to install NumPy. Please check your Python version." && exit 1)
	@echo "Installing other dependencies..."
	$(PIP_INSTALL) --only-binary=all -r requirements.txt || \
	$(PIP_INSTALL) -r requirements.txt --prefer-binary || \
	echo "Some packages may have failed to install. Check manually if needed."

# Alternative installation method if requirements.txt has numpy
install-manual:
	@echo "Manual installation approach..."
	$(VENV_PYTHON) -m pip install --upgrade pip setuptools wheel
ifeq ($(OS),Windows_NT)
	@powershell -Command "Get-Content requirements.txt | Where-Object { \$_ -and -not \$_.StartsWith('#') } | ForEach-Object { \
		Write-Output ('Installing ' + \$_); \
		& '$(VENV_PYTHON)' -m pip install --only-binary=all \$_ -ErrorAction SilentlyContinue; \
		& '$(VENV_PYTHON)' -m pip install --prefer-binary \$_ -ErrorAction SilentlyContinue; \
	}"
else
	@cat requirements.txt | grep -v "^#" | grep -v "^$$" | while read package; do \
		echo "Installing $$package..."; \
		$(PIP_INSTALL) --only-binary=all "$$package" || \
		$(PIP_INSTALL) --prefer-binary "$$package" || \
		echo "Failed to install $$package - skipping"; \
	done
endif

bot:
	$(VENV_PYTHON) app/bot.py

api:
	$(VENV_PYTHON) -m uvicorn app.main:app --reload

install:
	@$(MAKE) install-deps

run:
	$(VENV_PYTHON) app/bot.py

freeze:
	$(VENV_PYTHON) -m pip freeze > requirements.txt

# Clean up virtual environment
clean:
	@echo "Cleaning up virtual environment..."
ifeq ($(OS),Windows_NT)
	if exist venv rmdir /S /Q venv
else
	rm -rf venv
endif
	@echo "Virtual environment removed."

# Reinstall everything from scratch
reset: clean init

# Check what's installed
list:
	$(VENV_PYTHON) -m pip list

# Help target
help:
	@echo "Available commands:"
	@echo "  make init         - Create virtual environment and install dependencies"
	@echo "  make install-deps - Install dependencies with binary-only strategy"
	@echo "  make install-manual - Manual installation with fallbacks"
	@echo "  make bot          - Run the bot"
	@echo "  make api          - Run the API server"
	@echo "  make run          - Run the bot (alias)"
	@echo "  make freeze       - Generate requirements.txt"
	@echo "  make clean        - Remove virtual environment"
	@echo "  make reset        - Clean and reinitialize"
	@echo "  make list         - Show installed packages"
	@echo "  make help         - Show this help"