import streamlit as st
from PIL import Image

# ตั้งชื่อหน้าเว็บและไอคอน
st.set_page_config(page_title="Profile", page_icon="👤", layout="centered")

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
st.title("👤 Profile Page")
st.write("---")

# ---- INTRO ----
col1, col2 = st.columns([1, 2])

with col1:
    # หากมีรูปสามารถใส่ได้ เช่น profile.jpg
    st.image("images/profile.jpg", width=300)

with col2:
    st.subheader("ศุภวิชญ์ พรหมเจริญ")
    st.write("🎓 รหัสนักศึกษา : 2213110345")
    st.write("💻 สาขา : Information Technology")
    st.write("สวัสดีครับ ผมเป็นนักศึกษาปีที่ 4 ที่ชื่นชอบการเขียนโปรแกรมและเรียนรู้สิ่งใหม่ๆ โดยเฉพาะด้าน AI และ Machine Learning ซึ่งสามารถนำมาสร้างโซลูชันเพื่อพัฒนาสังคมและสิ่งแวดล้อมได้ครับ")

# ---- SECTION: ความสนใจ ----
st.write("---")
st.header("💡 ความสนใจใน Data Science / Data Mining")
st.write("""
ผมสนใจการนำข้อมูลมาวิเคราะห์และสร้างโมเดล Machine Learning เพื่อมาแก้ปัญหาจริง เช่น  
- การทำ Image Classification เพื่อตรวจจับภาพ
- การทำ Data Visualization เพื่อให้เข้าใจง่าย  
- การใช้ Python และ Excel เพื่อเตรียมข้อมูลสำหรับวิเคราะห์ข้อมูล  

ผมเชื่อว่าการเข้าใจและประยุกต์ใช้ข้อมูลอย่างถูกต้อง จะช่วยให้เป็นประโยชน์และยั่งยืนต่อสังคมได้ครับ
""")

# ---- SECTION: ประสบการณ์ ----
st.write("---")
st.header("📁 กิจกรรมที่เข้าร่วม")

project_col1, project_col2 = st.columns(2)

with project_col1:
    st.subheader("🕵 AI For Cybersecurity")
    st.image("images/cyber.jpg", width=500)
    st.write("เข้าร่วม Workshop การทำ Deep fake ภายใต้โครงการ Cybersecurity Penetration Testing ของสถาบันการจัดการปัญญาภิวัฒน์ เมื่อวันที่ 24 พฤศจิกายน 2567")
    # st.markdown("[🔗 ดูรายละเอียดเพิ่มเติม](#)")

with project_col2:
    st.subheader("👨🏻‍💻 Smart IoT with AI")
    st.image("images/iot.jpg", width=500)
    st.write("เข้าร่วมอบรมการทำ Image Classification ภายใต้โครงการ Hackathon Innovative Application for Smart Life Season 3 เมื่อวันที่ 24 กันยายน 2568")
    # st.markdown("[🔗 ดูรายละเอียดเพิ่มเติม](#)")

# ---- SECTION: SKILLSET ----
st.write("---")
st.header("📌 Skillset")

skills = {
    "Python": "⭐⭐⭐⭐",
    "MS Excel": "⭐⭐⭐",
    "Git / GitHub": "⭐⭐⭐",
    "Streamlit": "⭐⭐",
    "Data Visualization (Matplotlib)": "⭐⭐",
    "Machine Learning (scikit-learn)": "⭐⭐"
}

for skill, level in skills.items():
    st.write(f"- {skill}: {level}")

# ---- FOOTER ----
st.write("---")
st.caption("ITE-436 : Big Data and Data Mining")
