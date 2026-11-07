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

### 3. Quản lý sản phẩm
- Thêm, sửa, xóa sản phẩm ngay trên giao diện web; dữ liệu lưu thẳng vào `products.csv`, không cần sửa file bằng tay.
- Chặn tên trống/tên trùng; không cho xóa khi danh sách chỉ còn 1 sản phẩm.

### 4. Lịch sử caption
- Mỗi caption tạo thành công được tự động lưu kèm tên sản phẩm, nền tảng, giọng văn và thời gian tạo vào file `caption_history.csv`.
- Xem lại, tải lại từng caption dạng `.txt`, xóa từng mục hoặc xóa toàn bộ lịch sử.
- Lưu ý: lịch sử lưu trên máy đang chạy app; với bản deploy online, lịch sử có thể mất khi app khởi động lại — nên tải `.txt` về để giữ lâu dài. File này đã được đưa vào `.gitignore`, không commit lên GitHub.

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
