import streamlit as st

# ตั้งชื่อหน้าเว็บและไอคอน
st.set_page_config(page_title="Youtube Article", page_icon="▶️", layout="centered")

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
# background-image: url("https://images.wallpapersden.com/image/download/mountains-in-dark-night_a2hoaG6UmZqaraWkpJRpbGZsrWdubWk.jpg");
background-image: url("https://images.pexels.com/photos/66997/pexels-photo-66997.jpeg");
background-size: cover;
}

h1 { color: #ffffff; text-shadow: 2px 2px 4px rgba(0,0,0,0.6); }
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ---- HEADER ----
st.title("📊 Article YouTube Data Analysis")
st.markdown(
    """
    <a href="https://www.notion.so/Content-YouTube-2453d2740b568034b220cad29bc8f576?source=copy_link" target="_blank" style="text-decoration: none;">
        <div style="
            display:inline-block;
            background: linear-gradient(135deg, #4f88e3, #6fa0f5);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            "onmouseover="this.style.background='linear-gradient(135deg, #6fa0f5, #4f88e3)';" 
            onmouseout="this.style.background='linear-gradient(135deg, #4f88e3, #6fa0f5)';">
            Open Notion
        </div>
    </a>
    """,
    unsafe_allow_html=True
)

# st.markdown("[Open Notion](https://www.notion.so/Content-YouTube-2453d2740b568034b220cad29bc8f576?source=copy_link)", unsafe_allow_html=True)

