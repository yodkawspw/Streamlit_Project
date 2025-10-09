
README — Omakase Recommender (ITE-436)

โปรเจกต์นี้ทำอะไร
------------------
ระบบแนะนำ “คอร์สโอมากาเสะ” จากแบบสอบถาม 10 ข้อ แล้วทำนายคอร์สที่เหมาะสมให้ผู้ใช้
โมเดลที่ใช้: OneHotEncoder + RandomForest (class_weight=balanced, n_estimators=1000, max_depth=10)
ชุดข้อมูลตัวอย่าง: 100 แถว (omakase_dataset.xlsx)


โครงสร้างไฟล์ (แนะนำ)
----------------------
C:\Omakase\
 ├─ app.py                         # เว็บแอป Streamlit
 ├─ train_omakase_ohe.py           # โค้ดเทรนโมเดลจาก Excel
 ├─ omakase_dataset.xlsx           # ชุดข้อมูล 100 แถว
 ├─ omakase_model_ohe.pkl          # โมเดลที่เทรนแล้ว (ไฟล์ผลลัพธ์)
 ├─ preprocess_metadata_ohe.json   # เมทาดาทาระหว่างเทรน (มีค่า accuracy เฉลี่ย ฯลฯ)
 └─ training_report_ohe.txt        # สรุปผลเทรน/รายงาน

แนะนำสpec เวอร์ชัน
-------------------
- Python แนะนำ 3.11 หรือ 3.12 (เสถียรสำหรับงาน ML/DL)
- Streamlit ≥ 1.30
- scikit-learn ≥ 1.3
- pandas ≥ 1.5

การติดตั้งเครื่องมือ (Windows / Miniconda แนะนำ)
-------------------------------------------------
1) ติดตั้ง Miniconda หรือ Anaconda (หากยังไม่มี)
2) สร้าง environment ใหม่ชื่อ omakase
   PowerShell:
     conda create -n omakase python=3.11 -y
     conda activate omakase
3) ติดตั้งไลบรารีที่ต้องใช้
     pip install -U pandas scikit-learn streamlit joblib openpyxl

หมายเหตุ: หากเครื่องมี Python หลายตัว ให้ตรวจว่า python/pip ชี้ไปที่ env ที่เพิ่ง activate
     where python
     python -V

การเตรียมข้อมูล
----------------
- วางไฟล์ omakase_dataset.xlsx ไว้ในโฟลเดอร์เดียวกับ train_omakase_from_excel.py
- หัวคอลัมน์ต้องใช้ชื่อฟีเจอร์ตามที่กำหนดตอนเทรน (experience, taste, adventure, style, main_ing, avoid, texture, fullness, companion, impression, และ target คือคอร์ส)

การเทรนโมเดล
-------------
1) เปิด PowerShell ไปยังโฟลเดอร์โปรเจกต์
     cd C:\Omakase
2) รันสคริปต์เทรน
     python train_omakase_from_excel.py
3) ไฟล์ผลลัพธ์ที่ได้:
   - omakase_model_ohe.pkl                (โมเดลพร้อมใช้งาน)
   - preprocess_metadata_ohe.json         (เก็บค่า cv_accuracy_mean, holdout_accuracy, training_rows, rare_values)
   - training_report_ohe.txt              (รายงานความแม่นยำ, classification report)

การรันเว็บแอป Streamlit (ใช้งานโมเดลที่เทรนแล้ว)
-------------------------------------------------
1) ตรวจว่าไฟล์ต่อไปนี้อยู่ในโฟลเดอร์เดียวกัน: app.py, omakase_model_ohe.pkl, preprocess_metadata_ohe.json
2) รันแอป
     streamlit run app.py
3) เปิดเบราว์เซอร์ตามลิงก์ที่ Streamlit แจ้ง (ปกติ http://localhost:8501)

คำสั่งสั้น ๆ ที่ใช้บ่อย
------------------------
conda activate omakase
pip install -U pandas scikit-learn streamlit joblib openpyxl
python train_omakase_from_excel.py
streamlit run app.py


--------------
โปรเจกต์ตัวอย่างเพื่อการศึกษา วิชา ITE-436: Big Data and Data Mining
