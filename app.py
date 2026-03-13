import streamlit as st
import pandas as pd
from openai import OpenAI
from datetime import datetime

st.set_page_config(
    page_title="Affiliate AI Hub Ban Hang",
    page_icon="🛍️",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_products():
    return pd.read_csv("products.csv")

df = load_products()

# =========================
# HEADER
# =========================
st.title("🛍️ Affiliate AI Hub Ban Hang Mai Mit")
st.caption("Trang giới thiệu sản phẩm affiliate + tạo caption bán hàng cho Facebook và TikTok cho Mai Mit")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Cài đặt")

api_key = st.sidebar.text_input("Nhập OpenAI API Key", type="password")

pages = st.sidebar.radio(
    "Chọn trang",
    ["Danh sách sản phẩm", "AI tạo caption bán hàng"]
)

# =========================
# PAGE 1: PRODUCT LIST
# =========================
if pages == "Danh sách sản phẩm":
    st.subheader("Danh sách sản phẩm affiliate")

    col1, col2 = st.columns([2, 1])

    with col1:
        keyword = st.text_input("Tìm sản phẩm", placeholder="Nhập tên sản phẩm...")
    with col2:
        category_list = ["Tất cả"] + sorted(df["category"].dropna().unique().tolist())
        selected_category = st.selectbox("Lọc theo danh mục", category_list)

    filtered = df.copy()

    if keyword:
        filtered = filtered[
            filtered["name"].astype(str).str.contains(keyword, case=False, na=False)
        ]

    if selected_category != "Tất cả":
        filtered = filtered[filtered["category"] == selected_category]

    st.write(f"Đang hiển thị: **{len(filtered)}** sản phẩm")

    if filtered.empty:
        st.warning("Không tìm thấy sản phẩm phù hợp.")
    else:
        for _, row in filtered.iterrows():
            c1, c2 = st.columns([1, 2])

            with c1:
                if pd.notna(row.get("image_url", "")) and str(row["image_url"]).strip():
                    st.image(row["image_url"], use_container_width=True)
                else:
                    st.info("Chưa có ảnh")

            with c2:
                st.subheader(str(row["name"]))
                st.write(f"**Danh mục:** {row['category']}")
                st.write(f"**Giá:** {row['price']}")
                st.write(str(row["description"]))

                advantages = str(row.get("advantages", "")).strip()
                if advantages:
                    st.write("**Ưu điểm nổi bật:**")
                    for item in advantages.split("|"):
                        item = item.strip()
                        if item:
                            st.write(f"- {item}")

                affiliate_url = str(row.get("affiliate_url", "")).strip()
                if affiliate_url:
                    st.link_button("🔗 Xem sản phẩm / Link affiliate", affiliate_url)
                else:
                    st.warning("Chưa có link affiliate")

            st.divider()

# =========================
# PAGE 2: AI CAPTION
# =========================
elif pages == "AI tạo caption bán hàng":
    st.subheader("AI tạo caption bán hàng cho Facebook và TikTok")

    if not api_key:
        st.warning("Bạn hãy nhập OpenAI API Key ở thanh bên trái trước.")

    product_names = df["name"].dropna().astype(str).tolist()
    selected_product = st.selectbox("Chọn sản phẩm", product_names)

    product_row = df[df["name"] == selected_product].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        platform = st.selectbox("Nền tảng", ["Facebook", "TikTok", "Cả hai"])
        tone = st.selectbox(
            "Giọng văn",
            ["Bán hàng cuốn hút", "Gần gũi", "Sang trọng", "Viral", "Chuyên nghiệp"]
        )
        target_customer = st.text_input(
            "Khách hàng mục tiêu",
            placeholder="Ví dụ: mẹ bỉm, dân văn phòng, shop online..."
        )

    with col2:
        promo = st.text_input(
            "Ưu đãi / khuyến mãi",
            placeholder="Ví dụ: giảm 20%, freeship, quà tặng kèm..."
        )
        call_to_action = st.text_input(
            "Kêu gọi hành động",
            placeholder="Ví dụ: inbox ngay, comment để nhận link, đặt hàng hôm nay..."
        )
        extra_note = st.text_area(
            "Thông tin thêm",
            placeholder="Ví dụ: muốn caption ngắn, dễ chốt đơn, hợp đăng reel/TikTok..."
        )

    st.markdown("### Thông tin sản phẩm đang chọn")
    st.write(f"**Tên sản phẩm:** {product_row['name']}")
    st.write(f"**Danh mục:** {product_row['category']}")
    st.write(f"**Giá:** {product_row['price']}")
    st.write(f"**Mô tả:** {product_row['description']}")

    if st.button("Tạo caption bán hàng"):
        if not api_key:
            st.error("Bạn chưa nhập OpenAI API Key.")
        else:
            try:
                client = OpenAI(api_key=api_key)

                prompt = f"""
Bạn là chuyên gia content bán hàng online cho Facebook và TikTok.

Hãy viết nội dung bán hàng bằng tiếng Việt cho sản phẩm sau:
- Tên sản phẩm: {product_row['name']}
- Danh mục: {product_row['category']}
- Giá: {product_row['price']}
- Mô tả: {product_row['description']}
- Ưu điểm: {product_row.get('advantages', '')}

Yêu cầu:
- Nền tảng: {platform}
- Giọng văn: {tone}
- Khách hàng mục tiêu: {target_customer}
- Khuyến mãi: {promo}
- CTA: {call_to_action}
- Ghi chú thêm: {extra_note}

Hãy trả ra đúng cấu trúc sau:

1. 5 caption Facebook bán hàng
2. 5 caption TikTok ngắn, cuốn hút
3. 10 tiêu đề/hook mở đầu thu hút
4. 1 bài đăng bán hàng hoàn chỉnh
5. 10 hashtag phù hợp
6. 3 ý tưởng video ngắn để đăng TikTok/Reels

Viết dễ dùng ngay, thực tế, tập trung chốt đơn.
"""

                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {"role": "system", "content": "Bạn là chuyên gia content bán hàng và affiliate marketing."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1800
                )

                result = response.choices[0].message.content

                st.success("Đã tạo xong nội dung.")
                st.markdown("## Kết quả")
                st.write(result)

                st.download_button(
                    label="📥 Tải nội dung .txt",
                    data=result,
                    file_name=f"caption_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Lỗi: {e}")