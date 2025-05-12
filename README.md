# Hệ Thống Phân Tích Cổ Phiếu Việt Nam

Hệ thống phân tích dữ liệu cổ phiếu theo thời gian thực, cung cấp các biểu đồ và phân tích chi tiết về dòng tiền, khối lượng giao dịch và các chỉ số quan trọng khác.

## Tính Năng

- Phân tích dòng tiền vào/ra theo thời gian thực
- Biểu đồ dòng tiền ròng lũy kế với phát hiện điểm đột biến
- Tỷ lệ khối lượng trung bình lệnh mua/bán
- Phân tích áp lực mua/bán
- Heatmap trực quan hóa dòng tiền
- Thống kê chi tiết về giá và khối lượng giao dịch
- Phân tích phân phối lệnh và khối lượng theo giá

## Cài Đặt

1. Clone repository:
```bash
git clone <repository_url>
cd telegram-bot-stock
```

2. Tạo môi trường ảo:
```bash
python3 -m venv venv
```

3. Kích hoạt môi trường ảo:
- macOS/Linux:
```bash
source venv/bin/activate
```
- Windows:
```bash
venv\Scripts\activate
```

4. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Sử Dụng

1. Chạy chương trình:
```bash
python3 stock.py
```

2. Nhập mã cổ phiếu cần phân tích (ví dụ: VNM, VIC, ACB...)

3. Chương trình sẽ hiển thị:
- Tóm tắt phân tích với các chỉ số quan trọng
- Biểu đồ dòng tiền ròng lũy kế
- Biểu đồ tỷ lệ khối lượng mua/bán
- Biểu đồ dòng tiền mua/bán lũy kế
- Heatmap áp lực mua/bán
- Các biểu đồ phân tích khác

4. Để thoát chương trình, gõ 'END'

## Cấu Trúc Dự Án

```
telegram-bot-stock/
├── stock.py          # File chính chứa mã nguồn
├── requirements.txt  # Danh sách các thư viện cần thiết
├── venv/            # Thư mục môi trường ảo
└── README.md        # Tài liệu hướng dẫn
```

## Yêu Cầu Hệ Thống

- Python 3.9 trở lên
- Các thư viện được liệt kê trong requirements.txt
- Kết nối internet để truy cập dữ liệu thị trường

## Các Thư Viện Chính

- pandas: Xử lý dữ liệu
- numpy: Tính toán số học
- matplotlib: Vẽ biểu đồ
- seaborn: Vẽ biểu đồ nâng cao
- vnstock: API lấy dữ liệu thị trường chứng khoán Việt Nam

## Lưu Ý

- Dữ liệu được cập nhật theo thời gian thực từ thị trường
- Một số chức năng có thể bị giới hạn bởi API của vnstock
- Nên sử dụng môi trường ảo để tránh xung đột với các dự án Python khác

## Đóng Góp

Mọi đóng góp đều được hoan nghênh. Vui lòng:
1. Fork dự án
2. Tạo nhánh tính năng mới
3. Commit thay đổi
4. Tạo Pull Request

## Giấy Phép

[MIT License](https://opensource.org/licenses/MIT)
