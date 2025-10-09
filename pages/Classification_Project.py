# Mini_Project.py 
import json
from pathlib import Path
from io import StringIO

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="ทำนายคอร์สโอมากาเสะ", page_icon="🍣", layout="centered")

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
# background-image: url("https://images.wallpapersden.com/image/download/mountains-in-dark-night_a2hoaG6UmZqaraWkpJRpbGZsrWdubWk.jpg");
background-image: url("https://images.pexels.com/photos/66997/pexels-photo-66997.jpeg");
background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ------------------------ STYLE ------------------------
st.markdown(
    """
    <style>
      :root{
        --bg:#ffffff;
        --ink:#0f172a;
        --muted:#64748b;
        --line:#e5e7eb;
        --shadow: 0 8px 24px rgba(2,6,23,.06);
        --accent:#ef4444;           /* แดงซอฟต์ */
        --accent-weak:#fef2f2;      /* พื้นหลังแดงอ่อน */
        --accent-line:#fde2e2;      /* เส้นแดงอ่อน */
        --chip-bg:#f8fafc;
      }
      .block-container { max-width: 1000px; }

      /* HERO */
      .hero {
        background: linear-gradient(135deg, var(--accent-weak) 0%, #fff 60%);
        border: 1px solid var(--accent-line);
        border-radius: 16px;
        padding: 1.1rem 1.2rem;
        box-shadow: var(--shadow);
        margin-bottom: 1.1rem;
      }
      .hero h1 { margin:0; font-size: 2rem; font-weight: 800; color: var(--ink); }
      .subtitle { color:var(--muted); margin-top:.25rem; }

      /* KPI */
      .metric-card {
        background: var(--bg);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: .9rem 1rem;
        box-shadow: var(--shadow);
        text-align:center;
      }
      .metric-card .label { color:#6b7280; font-weight:600; font-size:.92rem; }
      .metric-card .value { color:#6b7280; font-weight:800; font-size:1.2rem; margin-top:.2rem; }

      /* ===== การ์ดมาตรฐาน: ใช้ทั้งฟอร์มและผลลัพธ์ ===== */
      .card{
        background: var(--bg);
        border:1px solid var(--line);
        border-radius:16px;
        padding: 1.15rem 1.2rem;
        box-shadow: var(--shadow);
        margin: 1.25rem 0;
      }
      /* การ์ดผลลัพธ์ (accent ซ้าย) */
      .card-accent { border-left: 6px solid var(--accent); }

      /* divider เส้นบาง */
      .divider {
        height:1px; background: linear-gradient(90deg, transparent, var(--line), transparent);
        margin: .9rem 0 1rem;
      }

      /* ชิปพารามิเตอร์ */
      .chips { display:flex; flex-wrap:wrap; gap:.6rem .7rem; margin:.8rem 0 1.1rem; }
      .chip {
        padding:.22rem .7rem; border-radius:999px; background:var(--chip-bg); color:var(--ink);
        border:1px solid var(--line); font-size:.85rem; font-weight:600;
      }

      .section-title { margin:.4rem 0 .5rem; font-weight: 800; font-size:1.05rem; color:#fff; }

      /* ปุ่มหลัก */
      .stButton > button {
        background: linear-gradient(135deg, #f97316, #ef4444);
        color:#fff; border:0; border-radius:12px; padding:.6rem .9rem; font-weight:800;
        box-shadow: 0 6px 18px rgba(239,68,68,.22);
        transition: transform .06s ease, box-shadow .15s ease, filter .15s ease;
      }
      .stButton > button:hover { transform: translateY(-1px); filter: brightness(1.03);}
      .stButton > button:active { transform: translateY(0); }

      /* ปุ่มรอง */
      .btn-ghost {
        display:inline-block; padding:.55rem .85rem; border-radius:12px; border:1px solid var(--line);
        color:var(--ink); background:#fff; font-weight:700; text-decoration:none;
      }
      .btn-ghost:hover { background:#fafafa; }

      /* Badge Top-3 probability */
      .badges { display:flex; flex-wrap:wrap; gap:.5rem; margin:.4rem 0 .2rem; }
      .badge {
        display:inline-flex; align-items:center; gap:.45rem;
        padding:.28rem .6rem; border-radius:999px; border:1px solid var(--line);
        background:#fff; box-shadow: var(--shadow); font-weight:700;
        color:#111827;
      }
      .badge .dot{ width:.55rem; height:.55rem; border-radius:99px; background: var(--accent); display:inline-block;}
      .hint { color:var(--muted); font-size:.92rem; }

      /* ปรับระยะ label widget เล็กน้อยให้แน่นขึ้น */
      label[data-testid="stWidgetLabel"] p { margin-bottom:.25rem; font-weight:700; color:#111827;}

      [data-testid="stForm"] {
      background: linear-gradient(135deg, var(--accent-weak) 0%, #fff 60%) }

      [data-testid="stFormSubmitButton"] > button:hover {
        background: #808080;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- รายชื่อฟีเจอร์ (ต้องตรงกับตอนเทรน) ----------
FEATURES = [
    "experience", "taste", "adventure", "style", "main_ing",
    "avoid", "texture", "fullness", "companion", "impression"
]

# ---------- ตัวเลือกของแบบสอบถาม ----------
CHOICES = {
    "experience": ["ผ่อนคลาย", "สดชื่น", "เข้มข้น", "หรูหรา", "สบาย ๆ"],
    "taste": ["ละมุนอ่อน ๆ", "กลมกล่อม", "เข้มข้นชัดเจน", "เผ็ดร้อน", "เปรี้ยวสดชื่น"],
    "adventure": ["ชอบแบบคุ้นเคย", "ลองได้บ้าง", "ชอบท้าทายแปลกใหม่"],
    "style": ["ดั้งเดิม", "สร้างสรรค์"],
    "main_ing": ["ปลา", "หอย", "เนื้อวัว", "ผัก", "ไม่เจาะจง"],
    "avoid": ["แพ้", "ไม่ชอบรส", "ไม่ทานด้วยเหตุผลส่วนตัว"],
    "texture": ["นุ่มละลาย", "กรอบสด", "หนึบหนับ", "ไม่เจาะจง"],
    "fullness": ["เบา ๆ", "พอดี", "อิ่มเต็มที่"],
    "companion": ["ทานคนเดียว", "ทานกับเพื่อน / แฟน", "ทานกับครอบครัว / ผู้ใหญ่"],
    "impression": ["เซอร์ไพรส์", "ประณีตละเอียด", "สนุกสนาน", "สบายใจ", "ประทับใจในรสชาติ"],
}

# ---------- โหลดโมเดล + เมทาดาทา ----------
@st.cache_resource
def load_assets(model_path: Path, meta_path: Path):
    model = joblib.load(model_path)  # Pipeline(OneHotEncoder + RandomForest)
    meta = {}
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
    return model, meta

BASE_DIR = Path(__file__).parent  # path ของไฟล์ Streamlit (pages/)

MODEL_PATH = BASE_DIR / ".." / "omakase" / "omakase_model_ohe.pkl"
META_PATH  = BASE_DIR / ".." / "omakase" / "preprocess_metadata_ohe.json"

try:
    model, meta = load_assets(MODEL_PATH, META_PATH)
except Exception as e:
    st.error(
        f"โหลดโมเดลไม่สำเร็จ: {e}\n"
        "โปรดวางไฟล์ omakase_model_ohe.pkl และ preprocess_metadata_ohe.json ไว้โฟลเดอร์เดียวกับแอป"
    )
    st.stop()

# ---------- Metrics จาก metadata ----------
cv_mean = meta.get("cv_accuracy_mean", None)
holdout = meta.get("holdout_accuracy", None)
TRAIN_ROWS = meta.get("training_rows", 100)

def pct(x):
    return f"{x*100:.2f}%" if x is not None else "—"

# ---------- helpers ----------
def apply_rare_mapping(row: dict, rare_map: dict):
    if not rare_map:
        return row
    out = dict(row)
    for col, rares in rare_map.items():
        if col in out and out[col] in set(rares):
            out[col] = "(อื่นๆ)"
    return out

def get_classes_from_pipeline(pipeline):
    """พยายามดึง classes_ จากขั้นสุดท้ายที่มี"""
    if hasattr(pipeline, "named_steps"):
        for name, step in reversed(list(pipeline.named_steps.items())):
            if hasattr(step, "classes_"):
                return step.classes_
    # fallback (อาจไม่เกิด)
    return getattr(pipeline, "classes_", None)

# ---------- HEADER ----------
st.markdown(
    '<div class="hero"><h1>🍣 ระบบแนะนำคอร์สโอมากาเสะ</h1>'
    '<div class="subtitle">เลือกความชอบของคุณ แล้วให้โมเดลช่วยแนะนำคอร์สที่เหมาะสม</div></div>',
    unsafe_allow_html=True,
)

# KPI แถวบน
cA, cB, cC = st.columns(3)
with cA:
    st.markdown(
        '<div class="metric-card"><div class="label">ข้อมูลที่ใช้เทรน</div>'
        f'<div class="value">{TRAIN_ROWS} คน</div></div>', unsafe_allow_html=True)
with cB:
    st.markdown(
        '<div class="metric-card"><div class="label">ความแม่นยำเฉลี่ย (CV mean)</div>'
        f'<div class="value">{pct(cv_mean)}</div></div>', unsafe_allow_html=True)
with cC:
    st.markdown(
        '<div class="metric-card"><div class="label">ความแม่นยำชุดทดสอบ (Holdout)</div>'
        f'<div class="value">{pct(holdout)}</div></div>', unsafe_allow_html=True)

# ---------- FORM (การ์ดเดียวกับผลลัพธ์) ----------

st.markdown(f"")

with st.form("omakase_form"):
    a = {}
    c1, c2 = st.columns(2, gap="large")

    with c1:
        a["experience"] = st.selectbox("วันนี้คุณอยากได้ประสบการณ์แบบไหน?", CHOICES["experience"], index=1)
    with c2:
        a["taste"] = st.selectbox("คุณชอบรสชาติในแนวไหนมากที่สุด?", CHOICES["taste"], index=1)

    with c1:
        a["adventure"] = st.selectbox("ระดับความผจญภัยของคุณในการลองเมนูใหม่ ๆ", CHOICES["adventure"], index=1)
    with c2:
        a["style"] = st.selectbox("ถ้าให้เลือกระหว่าง 'ดั้งเดิม' กับ 'สร้างสรรค์' คุณอยากได้สไตล์มากกว่ากัน?", CHOICES["style"], index=0)

    with c1:
        a["main_ing"] = st.selectbox("วัตถุดิบหลักที่คุณชอบที่สุด?", CHOICES["main_ing"], index=0, help="เช่น โอมากาเสะเน้นปลา/หอย/เนื้อวัว ฯลฯ")
    with c2:
        a["avoid"] = st.selectbox("อยากหลีกเลี่ยงวัตถุดิบอะไร?", CHOICES["avoid"], index=1, help="ใช้สำหรับแพ้อาหาร/ไม่ชอบรส/เหตุผลส่วนตัว")

    with c1:
        a["texture"] = st.selectbox("ชอบเนื้อสัมผัสแบบไหนเป็นพิเศษ", CHOICES["texture"], index=0)
    with c2:
        a["fullness"] = st.selectbox("คาดหวังความอิ่มจากคอร์สมื้อนี้แค่ไหน?", CHOICES["fullness"], index=1)

    with c1:
        a["companion"] = st.selectbox("มื้อนี้คุณมาทานกับใคร?", CHOICES["companion"], index=1)
    with c2:
        a["impression"] = st.selectbox("สุดท้ายนี้… คุณอยากให้เชฟทำให้รู้สึกแบบไหน?", CHOICES["impression"], index=4)

    cols = st.columns([1, 5])
    with cols[0]:
        submitted = st.form_submit_button("🔮 ทำนายคอร์ส", use_container_width=True)


# ---------- PREDICT & DISPLAY (การ์ดเดียวกับฟอร์ม + accent) ----------
if submitted:
    rare_map = meta.get("rare_values", {})
    a_mapped = apply_rare_mapping(a, rare_map)
    X = pd.DataFrame([{k: a_mapped[k] for k in FEATURES}])

    try:
        with st.spinner("กำลังทำนาย…"):
            pred = model.predict(X)[0]

        st.toast("ทำนายสำเร็จ ✨", icon="✅")

        st.markdown(f"### ✅ คอร์สที่เหมาะสมสำหรับคุณ : **{pred}**")

        # แสดง Top-3 เป็น badge + ตารางเต็ม
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)[0]
            classes = get_classes_from_pipeline(model)
            if classes is not None:
                prob_df = pd.DataFrame({"คอร์ส": classes, "prob": proba}).sort_values("prob", ascending=False)
                top3 = prob_df.head(3).copy()
                top3["pct"] = (top3["prob"]*100).round(2).astype(str) + "%"

                # Badge แสดง Top-3
                badge_html = "<div class='badges'>" + "".join(
                    [f"<span class='badge'><span class='dot'></span>{r['คอร์ส']} <span class='hint'>{r['pct']}</span></span>"
                     for _, r in top3.iterrows()]
                ) + "</div>"
                st.markdown("<div class='section-title'>ตัวเลือกอันดับต้น ๆ</div>", unsafe_allow_html=True)
                st.markdown(badge_html, unsafe_allow_html=True)

                # ตารางความน่าจะเป็น (สวยและอ่านง่าย)
                show_df = prob_df.rename(columns={"prob":"ความน่าจะเป็น"})
                show_df["ความแม่นยำ"] = (show_df["ความน่าจะเป็น"]*100).map(lambda x: f"{x:.2f}%")
                show_df = show_df.drop(columns=["ความน่าจะเป็น"]).reset_index(drop=True)

                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                st.markdown("<div class='section-title'>รายละเอียดความน่าจะเป็นของโมเดล</div>", unsafe_allow_html=True)
                st.dataframe(show_df, use_container_width=True)

        # สรุปโมเดล
        st.markdown(
            f"📊 โมเดลทำนายจากข้อมูล **{TRAIN_ROWS} คน** — "
            f"**ความแม่นยำเฉลี่ย (CV mean): {pct(cv_mean)}**, "
            f"**Holdout: {pct(holdout)}**"
        )

        # ปุ่มดาวน์โหลดผลลัพธ์ (JSON)
        result_payload = {
            "inputs": a, "inputs_mapped": a_mapped, "prediction": str(pred),
            "meta": {
                "train_rows": TRAIN_ROWS,
                "cv_accuracy_mean": cv_mean,
                "holdout_accuracy": holdout
            }
        }
        buf = StringIO()
        json.dump(result_payload, buf, ensure_ascii=False, indent=2)
        st.download_button(
            "📥 ดาวน์โหลดผลลัพธ์ (JSON)",
            data=buf.getvalue().encode("utf-8"),
            file_name=f"omakase_recommend_{str(pred)}.json",
            mime="application/json",
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"ทำนายไม่สำเร็จ: {e}")

st.caption("หมายเหตุ: โมเดลนี้ถูกฝึกจากชุดข้อมูลเพื่อการศึกษา (ITE-436)")
