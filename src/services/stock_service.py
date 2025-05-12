from vnstock import price_depth

class StockService:
    @staticmethod
    def get_stock_price(symbol: str) -> str:
        """Lấy giá khớp lệnh hiện tại của mã cổ phiếu."""
        try:
            df = price_depth(stock_list=symbol)
            if df.empty:
                return f"Không tìm thấy dữ liệu cho mã {symbol}."
            price = df.loc[df['Mã CP'] == symbol, 'Giá khớp lệnh']
            if price.empty:
                return f"Không tìm thấy giá cho mã {symbol}."
            price_value = int(price.values[0])
            return f"Giá khớp lệnh hiện tại của {symbol}: {price_value:,} VND"
        except Exception as e:
            return f"Lỗi khi lấy giá cho mã {symbol}: {str(e)}"
