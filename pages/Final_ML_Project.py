# streamlit_app.py
import streamlit as st
from PIL import Image
from ultralytics import YOLO
import tempfile
import os
import cv2
import numpy as np
from io import BytesIO  # สำหรับบันทึกไฟล์ชั่วคราวใน memory

# ---------- ตั้งค่า Streamlit ----------
st.set_page_config(page_title="Image Detection", page_icon="🔎", layout="centered")

# ---------- Background Image & CSS ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.pexels.com/photos/66997/pexels-photo-66997.jpeg");
    background-size: cover;
    background-attachment: fixed;
}
h1 { color: #ffffff; text-shadow: 2px 2px 4px rgba(0,0,0,0.6); }
.stImage > figcaption { text-align: center; font-weight: 600; color: #374151; }
div.stFileUploader > label > div[data-testid="stFileUploadDropzone"] { border: 2px dashed #ef4444; border-radius: 12px; padding: 1rem; background-color: rgba(255,255,255,0.9); }
</style>
""", unsafe_allow_html=True)

# ---------- โหลด YOLOv8 model ----------
BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "..", "YOLOv8", "runs", "detect", "train", "weights", "best.pt")

if not os.path.exists(model_path):
    st.error(f"ไม่พบไฟล์โมเดล: {model_path}")
    st.stop()

model = YOLO(model_path)

# ---------- หน้าเว็บ ----------
st.title("♻️ Recyclable Waste Detection")
st.write("อัปโหลดรูปภาพขวดพลาสติก, ขวดแก้ว, หรือกระป๋องเพื่อให้โมเดลตรวจจับขยะที่รีไซเคิลได้")

# ---------- อัปโหลดรูป ----------
uploaded_file = st.file_uploader("เลือกภาพของคุณ...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")

    st.write("---")

    # บันทึกรูปชั่วคราว
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        temp_path = tmp_file.name
        img.save(temp_path)

    # ตรวจจับขยะ
    results = model.predict(source=temp_path)

    # แปลง BGR → RGB → PIL
    annotated_img = results[0].plot()
    annotated_img_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    annotated_img_pil = Image.fromarray(annotated_img_rgb)

    # แสดงรูปซ้าย-ขวา
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h5 style='text-align: center;'>📤 Uploaded Image</h5>", unsafe_allow_html=True)
        st.image(img, use_container_width=True)
    with col2:
        st.markdown("<h5 style='text-align: center;'>✅ Detected Image</h5>", unsafe_allow_html=True)
        st.image(annotated_img_pil, use_container_width=True)

    # ---------- ปุ่มดาวน์โหลดรูป ----------
    buf = BytesIO()
    annotated_img_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="💾 ดาวน์โหลดผลลัพธ์ (PNG)",
        data=byte_im,
        file_name="detected_image.png",
        mime="image/png",
        use_container_width=True
    )

    # ลบไฟล์ชั่วคราว
    os.remove(temp_path)
    st.markdown('</div>', unsafe_allow_html=True)
