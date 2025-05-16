from app.services.stock_intents import PriceIntentHandler, RSIIntentHandler, PEIntentHandler

class StockIntentResolver:
    def __init__(self):
        self.handlers = [
            PriceIntentHandler(),
            RSIIntentHandler(),
            PEIntentHandler(),
        ]

    def resolve(self, text: str) -> str:
        for handler in self.handlers:
            if handler.can_handle(text):
                return handler.handle(text)
        return "Xin lỗi, tôi chưa hiểu yêu cầu. Bạn vui lòng hỏi lại rõ hơn!" 