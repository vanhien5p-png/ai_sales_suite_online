import streamlit as st
import pandas as pd
from openai import OpenAI
from datetime import datetime
import os

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


def format_price(value):
    """Hien thi gia dang 499.000 đ; giu nguyen so trong products.csv."""
    try:
        return f"{int(float(value)):,}".replace(",", ".") + " đ"
    except (TypeError, ValueError):
        return str(value)


def save_products(dataframe):
    """Ghi danh sach san pham xuong products.csv va xoa cache de nap lai."""
    dataframe.to_csv("products.csv", index=False)
    st.cache_data.clear()


# =========================
# CAPTION HISTORY
# =========================
HISTORY_FILE = "caption_history.csv"
HISTORY_COLUMNS = ["time", "product", "platform", "tone", "content"]


def load_history():
    """Doc lich su caption tu file CSV; tra ve DataFrame rong neu chua co."""
    if os.path.exists(HISTORY_FILE):
        try:
            hist = pd.read_csv(HISTORY_FILE).fillna("")
        except Exception:
            return pd.DataFrame(columns=HISTORY_COLUMNS)
        for col in HISTORY_COLUMNS:
            if col not in hist.columns:
                hist[col] = ""
        return hist[HISTORY_COLUMNS]
    return pd.DataFrame(columns=HISTORY_COLUMNS)


def save_caption_to_history(product, platform, tone, content):
    """Them mot caption vua tao vao file lich su."""
    entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "product": product,
        "platform": platform,
        "tone": tone,
        "content": content,
    }
    hist = load_history()
    hist = pd.concat([hist, pd.DataFrame([entry])], ignore_index=True)
    hist.to_csv(HISTORY_FILE, index=False)

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
    ["Danh sách sản phẩm", "AI tạo caption bán hàng", "Quản lý sản phẩm", "Lịch sử caption"]
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
                st.write(f"**Giá:** {format_price(row['price'])}")
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
    st.write(f"**Giá:** {format_price(product_row['price'])}")
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
- Giá: {format_price(product_row['price'])}
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

                save_caption_to_history(
                    product_row['name'], platform, tone, result
                )
                st.session_state["last_caption"] = result
                st.session_state["last_caption_product"] = str(product_row['name'])

                st.success("Đã tạo xong nội dung và lưu vào Lịch sử caption.")

            except Exception as e:
                st.error(f"Lỗi: {e}")

    if st.session_state.get("last_caption"):
        st.markdown("## Kết quả gần nhất")
        st.caption(f"Sản phẩm: {st.session_state.get('last_caption_product', '')}")
        st.write(st.session_state["last_caption"])
        st.download_button(
            label="📥 Tải nội dung .txt",
            data=st.session_state["last_caption"],
            file_name=f"caption_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="download_last_caption",
        )

# =========================
# PAGE 3: PRODUCT MANAGEMENT
# =========================
elif pages == "Quản lý sản phẩm":
    st.subheader("Quản lý sản phẩm")
    st.caption("Thêm, sửa, xóa sản phẩm — dữ liệu được lưu thẳng vào products.csv.")

    st.write(f"Hiện có: **{len(df)}** sản phẩm")
    if not df.empty:
        overview = df[["name", "category", "price"]].copy()
        overview["price"] = overview["price"].apply(format_price)
        overview.columns = ["Tên sản phẩm", "Danh mục", "Giá"]
        st.dataframe(overview, use_container_width=True, hide_index=True)

    tab_add, tab_edit, tab_delete = st.tabs(
        ["➕ Thêm sản phẩm", "✏️ Sửa sản phẩm", "🗑️ Xóa sản phẩm"]
    )

    # ---------- ADD ----------
    with tab_add:
        with st.form("form_add_product"):
            add_name = st.text_input("Tên sản phẩm *")
            add_col1, add_col2 = st.columns(2)
            with add_col1:
                add_category = st.text_input(
                    "Danh mục",
                    placeholder="Ví dụ: Gia dụng, Bao bì quà tặng..."
                )
                add_image = st.text_input("Link ảnh sản phẩm (image_url)")
            with add_col2:
                add_price = st.number_input(
                    "Giá (VNĐ)", min_value=0, step=1000, value=0, format="%d"
                )
                add_affiliate = st.text_input("Link affiliate")
            add_desc = st.text_area("Mô tả")
            add_adv = st.text_input(
                "Ưu điểm nổi bật", placeholder="Cách nhau bằng dấu |, ví dụ: Nhỏ gọn|Dễ dùng"
            )
            add_submit = st.form_submit_button("Thêm sản phẩm")

        if add_submit:
            new_name = add_name.strip()
            if not new_name:
                st.error("Tên sản phẩm không được để trống.")
            elif new_name in df["name"].astype(str).tolist():
                st.error("Đã có sản phẩm trùng tên này, hãy chọn tên khác.")
            else:
                new_row = {
                    "name": new_name,
                    "category": add_category.strip(),
                    "price": int(add_price),
                    "image_url": add_image.strip(),
                    "affiliate_url": add_affiliate.strip(),
                    "description": add_desc.strip(),
                    "advantages": add_adv.strip(),
                }
                save_products(pd.concat([df, pd.DataFrame([new_row])], ignore_index=True))
                st.success(f"Đã thêm sản phẩm: {new_name}")
                st.rerun()

    # ---------- EDIT ----------
    with tab_edit:
        if df.empty:
            st.info("Chưa có sản phẩm nào để sửa.")
        else:
            edit_names = df["name"].astype(str).tolist()
            edit_selected = st.selectbox("Chọn sản phẩm cần sửa", edit_names)
            edit_row = df[df["name"].astype(str) == edit_selected].iloc[0]
            edit_index = df[df["name"].astype(str) == edit_selected].index[0]

            with st.form(f"form_edit_product_{edit_selected}"):
                new_name = st.text_input("Tên sản phẩm *", value=str(edit_row["name"]))
                e_col1, e_col2 = st.columns(2)
                with e_col1:
                    new_category = st.text_input(
                        "Danh mục", value=str(edit_row.get("category", ""))
                    )
                    new_image = st.text_input(
                        "Link ảnh sản phẩm (image_url)",
                        value=str(edit_row.get("image_url", ""))
                        if pd.notna(edit_row.get("image_url", ""))
                        else "",
                    )
                with e_col2:
                    try:
                        current_price = int(float(edit_row["price"]))
                    except (TypeError, ValueError):
                        current_price = 0
                    new_price = st.number_input(
                        "Giá (VNĐ)",
                        min_value=0,
                        step=1000,
                        value=current_price,
                        format="%d",
                    )
                    new_affiliate = st.text_input(
                        "Link affiliate",
                        value=str(edit_row.get("affiliate_url", ""))
                        if pd.notna(edit_row.get("affiliate_url", ""))
                        else "",
                    )
                new_desc = st.text_area(
                    "Mô tả", value=str(edit_row.get("description", ""))
                )
                new_adv = st.text_input(
                    "Ưu điểm nổi bật (cách nhau bằng dấu |)",
                    value=str(edit_row.get("advantages", ""))
                    if pd.notna(edit_row.get("advantages", ""))
                    else "",
                )
                edit_submit = st.form_submit_button("Lưu thay đổi")

            if edit_submit:
                cleaned_name = new_name.strip()
                if not cleaned_name:
                    st.error("Tên sản phẩm không được để trống.")
                elif cleaned_name != edit_selected and cleaned_name in edit_names:
                    st.error("Đã có sản phẩm trùng tên này, hãy chọn tên khác.")
                else:
                    updated = df.copy()
                    updated.loc[edit_index, "name"] = cleaned_name
                    updated.loc[edit_index, "category"] = new_category.strip()
                    updated.loc[edit_index, "price"] = int(new_price)
                    updated.loc[edit_index, "image_url"] = new_image.strip()
                    updated.loc[edit_index, "affiliate_url"] = new_affiliate.strip()
                    updated.loc[edit_index, "description"] = new_desc.strip()
                    updated.loc[edit_index, "advantages"] = new_adv.strip()
                    save_products(updated)
                    st.success(f"Đã cập nhật sản phẩm: {cleaned_name}")
                    st.rerun()

    # ---------- DELETE ----------
    with tab_delete:
        if df.empty:
            st.info("Chưa có sản phẩm nào để xóa.")
        elif len(df) <= 1:
            st.warning(
                "Danh sách chỉ còn 1 sản phẩm nên không xóa được — "
                "các trang khác cần ít nhất 1 sản phẩm để hoạt động."
            )
        else:
            delete_selected = st.selectbox(
                "Chọn sản phẩm cần xóa", df["name"].astype(str).tolist()
            )
            st.warning(f"Xóa hẳn sản phẩm: **{delete_selected}** — không khôi phục được.")
            confirm_delete = st.checkbox("Tôi chắc chắn muốn xóa sản phẩm này")
            if st.button("Xóa sản phẩm", disabled=not confirm_delete):
                remaining = df[df["name"].astype(str) != delete_selected]
                save_products(remaining.reset_index(drop=True))
                st.success(f"Đã xóa sản phẩm: {delete_selected}")
                st.rerun()

# =========================
# PAGE 4: CAPTION HISTORY
# =========================
elif pages == "Lịch sử caption":
    st.subheader("Lịch sử caption đã tạo")
    st.caption(
        "Caption được lưu trên máy đang chạy app. Với bản chạy online, "
        "lịch sử có thể mất khi app khởi động lại — hãy tải file .txt về để giữ lâu dài."
    )

    history = load_history()

    if history.empty:
        st.info("Chưa có caption nào được lưu. Hãy sang trang 'AI tạo caption bán hàng' để tạo caption đầu tiên.")
    else:
        st.write(f"Đã lưu: **{len(history)}** caption (mới nhất ở trên)")

        for idx in reversed(history.index.tolist()):
            row = history.loc[idx]
            label = f"{row['time']} — {row['product']} ({row['platform']})"
            with st.expander(label):
                st.write(f"**Giọng văn:** {row['tone']}")
                st.markdown(str(row["content"]))
                dl_col, del_col = st.columns([1, 1])
                with dl_col:
                    st.download_button(
                        label="📥 Tải .txt",
                        data=str(row["content"]),
                        file_name=f"caption_{str(row['time']).replace(':', '').replace(' ', '_').replace('-', '')}.txt",
                        mime="text/plain",
                        key=f"download_history_{idx}",
                    )
                with del_col:
                    if st.button("🗑️ Xóa caption này", key=f"delete_history_{idx}"):
                        history = history.drop(index=idx).reset_index(drop=True)
                        history.to_csv(HISTORY_FILE, index=False)
                        st.rerun()

        st.divider()
        confirm_clear = st.checkbox("Tôi chắc chắn muốn xóa toàn bộ lịch sử caption")
        if st.button("Xóa toàn bộ lịch sử", disabled=not confirm_clear):
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
            st.success("Đã xóa toàn bộ lịch sử caption.")
            st.rerun()