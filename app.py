import streamlit as st
from openai import OpenAI
from PIL import Image
import base64

st.set_page_config(page_title="AI Sales Suite Online", layout="wide")

st.title("AI Sales Suite Online")
st.caption("Tool tạo content bán hàng từ ảnh sản phẩm")

api_key = st.text_input("Nhập OpenAI API Key", type="password")

st.sidebar.header("Chức năng")
mode = st.sidebar.radio(
    "Chọn chức năng",
    [
        "Tạo caption Facebook",
        "Phân tích ảnh sản phẩm",
        "Gợi ý prompt tạo ảnh",
        "Mô tả sản phẩm",
    ],
)

uploaded_file = st.file_uploader("Tải ảnh sản phẩm lên", type=["jpg", "jpeg", "png"])

extra_info = st.text_area(
    "Thông tin thêm",
    placeholder="Ví dụ: sản phẩm dành cho mẹ và bé, phong cách cao cấp, giá mềm...",
)

def encode_image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")

image_bytes = None
mime_type = "image/png"

if uploaded_file is not None:
    image_bytes = uploaded_file.getvalue()
    mime_type = uploaded_file.type or "image/png"
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh sản phẩm", use_container_width=True)

if st.button("Tạo nội dung"):
    if not api_key:
        st.error("Bạn cần nhập OpenAI API Key trước.")
    elif image_bytes is None:
        st.error("Bạn cần tải ảnh lên trước.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            base64_image = encode_image_to_base64(image_bytes)

            if mode == "Tạo caption Facebook":
                user_prompt = f"""
Hãy xem ảnh sản phẩm và viết:
1. 5 caption Facebook bán hàng
2. 5 tiêu đề ngắn thu hút
3. 1 đoạn CTA chốt đơn
Thông tin thêm: {extra_info}
"""
            elif mode == "Phân tích ảnh sản phẩm":
                user_prompt = f"""
Hãy phân tích ảnh sản phẩm này:
1. Sản phẩm là gì
2. Điểm nổi bật hình ảnh
3. Tệp khách hàng phù hợp
4. Gợi ý cách đăng bài bán hàng
Thông tin thêm: {extra_info}
"""
            elif mode == "Gợi ý prompt tạo ảnh":
                user_prompt = f"""
Dựa vào ảnh sản phẩm, hãy viết:
1. 5 prompt tạo ảnh quảng cáo đẹp
2. 3 prompt nền sang trọng
3. 3 prompt ảnh viral bán hàng
Viết rõ, dễ copy dùng ngay.
Thông tin thêm: {extra_info}
"""
            else:
                user_prompt = f"""
Hãy tạo mô tả sản phẩm từ ảnh này:
1. Tên sản phẩm gợi ý
2. Mô tả ngắn
3. Mô tả bán hàng chi tiết
4. 5 gạch đầu dòng lợi ích nổi bật
Thông tin thêm: {extra_info}
"""

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=1200,
            )

            result = response.choices[0].message.content
            st.subheader("Kết quả")
            st.write(result)

        except Exception as e:
            st.error(f"Lỗi: {e}")