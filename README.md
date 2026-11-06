# AI Sales Suite — Affiliate AI Hub Bán Hàng

Web app Streamlit hỗ trợ bán hàng affiliate: trưng bày danh sách sản phẩm kèm link affiliate, và dùng AI (OpenAI) để tự động viết caption bán hàng cho Facebook và TikTok.

## Tính năng chính

### 1. Danh sách sản phẩm affiliate
- Hiển thị sản phẩm từ file `products.csv`: ảnh, tên, danh mục, giá, mô tả, ưu điểm nổi bật và nút link affiliate.
- Tìm kiếm theo tên sản phẩm và lọc theo danh mục.

### 2. AI tạo caption bán hàng
- Chọn sản phẩm, nền tảng (Facebook / TikTok / cả hai), giọng văn (cuốn hút, gần gũi, sang trọng, viral, chuyên nghiệp), khách hàng mục tiêu, ưu đãi và CTA.
- AI (model `gpt-4.1-mini`) trả về trọn gói nội dung để dùng ngay:
  1. 5 caption Facebook bán hàng
  2. 5 caption TikTok ngắn, cuốn hút
  3. 10 tiêu đề/hook mở đầu
  4. 1 bài đăng bán hàng hoàn chỉnh
  5. 10 hashtag phù hợp
  6. 3 ý tưởng video ngắn cho TikTok/Reels
- Tải kết quả về dạng file `.txt`.

## Cấu trúc thư mục

```
ai_sales_suite_online/
├── app.py            # Toàn bộ giao diện và logic của app (Streamlit)
├── products.csv      # Dữ liệu sản phẩm affiliate
├── requirements.txt  # Thư viện cần cài: streamlit, pandas, openai
└── README.md
```

## Định dạng dữ liệu `products.csv`

Mỗi dòng là một sản phẩm, gồm các cột:

| Cột | Ý nghĩa |
|---|---|
| `name` | Tên sản phẩm |
| `category` | Danh mục |
| `price` | Giá (số, đơn vị VNĐ) |
| `image_url` | Link ảnh sản phẩm |
| `affiliate_url` | Link affiliate của sản phẩm |
| `description` | Mô tả ngắn |
| `advantages` | Các ưu điểm, cách nhau bằng dấu `\|` |

Muốn thêm/sửa sản phẩm chỉ cần sửa file `products.csv` rồi nạp lại trang.

## Cài đặt và chạy local

Yêu cầu: Python 3.10 trở lên.

```bash
pip install -r requirements.txt
streamlit run app.py
```

App mở tại `http://localhost:8501`.

## Cách sử dụng

1. Mở trang **Danh sách sản phẩm** để xem, tìm và lọc sản phẩm.
2. Chuyển sang trang **AI tạo caption bán hàng**.
3. Nhập **OpenAI API Key** ở thanh bên trái (key chỉ dùng trong phiên làm việc, app không lưu lại).
4. Chọn sản phẩm và các tuỳ chọn, bấm **Tạo caption bán hàng**, rồi tải file `.txt` kết quả nếu cần.

## Triển khai online

Repo này có thể deploy trực tiếp lên [Streamlit Community Cloud](https://streamlit.io/cloud): chọn repo, file chính là `app.py`. Người dùng tự nhập OpenAI API Key của mình ngay trên giao diện nên không cần cấu hình secret cho app.

## Ghi chú

- Dữ liệu trong `products.csv` hiện là dữ liệu mẫu (link affiliate là `example.com`) — thay bằng sản phẩm và link thật khi đưa vào sử dụng.
- Chi phí gọi AI tính theo OpenAI API Key của người sử dụng app.
