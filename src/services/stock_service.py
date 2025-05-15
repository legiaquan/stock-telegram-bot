from vnstock import price_depth, stock_historical_data
import matplotlib.pyplot as plt
import datetime

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

    @staticmethod
    def get_history_chart(symbol: str, days: int = 30) -> str:
        """Lấy lịch sử giá và vẽ chart, trả về đường dẫn file ảnh."""
        try:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=days)
            df = stock_historical_data(symbol=symbol, start_date=str(start_date), end_date=str(end_date), resolution='1D', type='stock')
            if df.empty:
                return None
            plt.figure(figsize=(10, 5))
            plt.plot(df['time'], df['close'], marker='o', label='Giá đóng cửa')
            plt.title(f'Lịch sử giá {symbol} ({days} ngày gần nhất)')
            plt.xlabel('Ngày')
            plt.ylabel('Giá đóng cửa (VND)')
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            img_path = f"/tmp/{symbol}_history.png"
            plt.savefig(img_path)
            plt.close()
            return img_path
        except Exception as e:
            return None

    @staticmethod
    def get_rsi(symbol: str, days: int = 30, period: int = 14) -> str:
        """Tính chỉ số RSI (Relative Strength Index) cho mã cổ phiếu."""
        import pandas as pd
        try:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=days)
            df = stock_historical_data(symbol=symbol, start_date=str(start_date), end_date=str(end_date), resolution='1D', type='stock')
            if df.empty or 'close' not in df:
                return f"Không lấy được dữ liệu giá để tính RSI cho mã {symbol}."
            close = df['close']
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            latest_rsi = rsi.iloc[-1]
            if pd.isna(latest_rsi):
                return f"Không đủ dữ liệu để tính RSI cho mã {symbol}."
            return f"RSI {period} ngày gần nhất của {symbol}: {latest_rsi:.2f}"
        except Exception as e:
            return f"Lỗi khi tính RSI cho mã {symbol}: {str(e)}"

    @staticmethod
    def get_pe(symbol: str) -> str:
        """Lấy chỉ số P/E của mã cổ phiếu."""
        try:
            from vnstock.fundamental import stock_evaluation
            df = stock_evaluation(symbol)
            if df is None or df.empty or 'PE' not in df:
                return f"Không lấy được dữ liệu P/E cho mã {symbol}."
            latest_pe = df['PE'].dropna().iloc[-1] if not df['PE'].dropna().empty else None
            if latest_pe is None:
                return f"Không tìm thấy chỉ số P/E cho mã {symbol}."
            return f"Chỉ số P/E gần nhất của {symbol}: {latest_pe}"
        except Exception as e:
            return f"Lỗi khi lấy P/E cho mã {symbol}: {str(e)}"
