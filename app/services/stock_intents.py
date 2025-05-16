from abc import ABC, abstractmethod
from app.services.stock_service import StockService

class StockIntentHandler(ABC):
    @abstractmethod
    def can_handle(self, text: str) -> bool:
        pass

    @abstractmethod
    def handle(self, text: str) -> str:
        pass

class PriceIntentHandler(StockIntentHandler):
    def can_handle(self, text: str) -> bool:
        return any(key in text.lower() for key in ["giá", "price"])

    def handle(self, text: str) -> str:
        symbol = self._extract_symbol(text)
        if not symbol:
            return "Không tìm thấy mã cổ phiếu."
        return StockService.get_stock_price(symbol)

    def _extract_symbol(self, text: str) -> str:
        import re
        match = re.search(r'(giá|price).*?([a-z]{2,5})', text.lower())
        return match.group(2).upper() if match else None

class RSIIntentHandler(StockIntentHandler):
    def can_handle(self, text: str) -> bool:
        return "rsi" in text.lower()

    def handle(self, text: str) -> str:
        symbol = self._extract_symbol(text)
        if not symbol:
            return "Không tìm thấy mã cổ phiếu."
        return StockService.get_rsi(symbol)

    def _extract_symbol(self, text: str) -> str:
        import re
        match = re.search(r'(rsi).*?([a-z]{2,5})', text.lower())
        return match.group(2).upper() if match else None

class PEIntentHandler(StockIntentHandler):
    def can_handle(self, text: str) -> bool:
        return "p/e" in text.lower() or "pe" in text.lower()

    def handle(self, text: str) -> str:
        symbol = self._extract_symbol(text)
        if not symbol:
            return "Không tìm thấy mã cổ phiếu."
        return StockService.get_pe(symbol)

    def _extract_symbol(self, text: str) -> str:
        import re
        match = re.search(r'(p[\\/.]?e).*?([a-z]{2,5})', text.lower())
        return match.group(2).upper() if match else None 