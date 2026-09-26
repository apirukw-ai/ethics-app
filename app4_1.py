from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 4.1: Ethical Lens & Case Analysis",
    page_icon="🔍",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab4_1_step" not in st.session_state:
    st.session_state.lab4_1_step = 1

# --- Sidebar เมนูด้านซ้าย ---
st.sidebar.markdown("### 🔍 LAB 4.1 Workflow")

steps_name = {
    1: "Activity 1: Ethical Lens (Before Viewing)",
    2: "Activity 2: Watch the Case (Case Card)",
}

current_index = list(steps_name.keys()).index(st.session_state.lab4_1_step)

selected_step_name = st.sidebar.radio(
    "เลือกกิจกรรม LAB 4.1:",
    list(steps_name.values()),
    index=current_index,
    key="lab4_1_menu_selection",
)

for s_num, s_title in steps_name.items():
    if s_title == selected_step_name:
        st.session_state.lab4_1_step = s_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อกิจกรรมด้านบนเพื่อเปลี่ยนหน้า")


# ==========================================
# 1. Activity 1 — Before viewing — Ethical Lens
# ==========================================
if st.session_state.lab4_1_step == 1:
    st.title("👓 Activity 1 — Before viewing: Ethical Lens")
    st.markdown("### “ถ้าคุณเห็นเหตุการณ์หนึ่งที่ดูเหมือนผิดจริยธรรม คุณจะดูอะไรเป็นอันดับแรก?”")
    st.info("💡 กรุณาเลือก **2 ข้อ** ที่คุณให้ความสำคัญที่สุด")

    lens_options = [
        "การกระทำ",
        "เจตนา",
        "ผลกระทบ",
        "ผู้ได้รับผลกระทบ",
        "กฎ/กฎหมาย",
        "คุณค่าที่เกี่ยวข้อง",
        "ความรับผิดชอบของผู้ประกอบวิชาชีพ"
    ]

    with st.form("lab4_1_act1_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        # ใช้ multiselect ให้เลือกได้สูงสุด 2 ข้อ
        selected_choices = st.multiselect(
            "เลือก 2 ข้อที่คุณให้ความสำคัญที่สุด:",
            lens_options,
            max_selections=2
        )
        
        sub_a1 = st.form_submit_button("ส่งคำตอบ Ethical Lens")

        if sub_a1 and student_id:
            if len(selected_choices) == 2:
                combined_choices = " + ".join(selected_choices)
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab4.1 - Act 1 Ethical Lens",
                    "Data": f"[{student_id}] {combined_choices}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab4_1_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab4_1_Responses", data=updated)
                        st.success("บันทึกผลโหวต Ethical Lens สำเร็จ!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else:
                    st.success("บันทึกจำลองสำเร็จ!")
            else:
                st.warning("กรุณาเลือกให้ครบถ้วนพอดี 2 ข้อครับ")
        elif sub_a1:
            st.warning("กรุณากรอกรหัสนิสิตและเลือกคำตอบก่อนส่ง")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผล Vote (Ethical Lens)")
    if conn:
        try:
            df = conn.read(worksheet="Lab4_1_Responses", ttl=5)
            act1_df = df[df["Step"] == "Lab4.1 - Act 1 Ethical Lens"]
            if not act1_df.empty:
                # แยกแกะข้อที่เลือกมารวมนับความถี่ (เนื่องจาก 1 คนเลือก 2 ข้อคั่นด้วย " + ")
                all_selections = []
                for item in act1_df["Data"]:
                    if "]" in item:
                        choices_part = item.split("] ")[1]
                        split_c = choices_part.split(" + ")
                        all_selections.extend(split_c)
                
                if all_selections:
                    s_series = pd.Series(all_selections)
                    st.bar_chart(s_series.value_counts())
                else:
                    st.info("ยังไม่มีข้อมูลเพียงพอสำหรับสร้างกราฟ")
            else:
                st.info("ยังไม่มีข้อมูลผลโหวตในระบบ")
        except:
            pass


# ==========================================
# 2. Activity 2 — Watch the Case
# ==========================================
elif st.session_state.lab4_1_step == 2:
    st.title("🎬 Activity 2 — Watch the Case (Ethical Case Card)")
    st.markdown("ระหว่างดูหนัง/คลิป ให้แต่ละกลุ่มร่วมกันวิเคราะห์และบันทึกข้อมูลตามประเด็นด้านล่างนี้")

    with st.form("lab4_1_act2_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        
        c_a = st.text_area("A. What happened? (เกิดอะไรขึ้น?)")
        c_b = st.text_area("B. Who is affected? (ใครได้รับผลกระทบ?)")
        c_c = st.text_area("C. What is the ethical issue? (ปัญหาจริยธรรมคืออะไร?)")
        c_d = st.text_area("D. What values are involved? (มีคุณค่าหรือหลักจริยธรรมอะไรเกี่ยวข้อง?)")
        c_e = st.text_area("E. What should the person do? (ควรทำอย่างไร?)")
        
        sub_a2 = st.form_submit_button("ส่งคำตอบ Case Card")

        if sub_a2 and group_name:
            combined_case = f"A: {c_a} | B: {c_b} | C: {c_c} | D: {c_d} | E: {c_e}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4.1 - Act 2 Case Card",
                "Data": f"[{group_name}] {combined_case}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_1_Responses", data=updated)
                    st.success("บันทึก Ethical Case Card สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a2:
            st.warning("กรุณาระบุชื่อกลุ่มก่อนส่งคำตอบ")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผลวิเคราะห์ Case Card ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab4_1_Responses", ttl=5)
            p2_df = df[df["Step"] == "Lab4.1 - Act 2 Case Card"]
            if not p2_df.empty:
                st.dataframe(p2_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูลการวิเคราะห์ Case Card")
        except:
            pass