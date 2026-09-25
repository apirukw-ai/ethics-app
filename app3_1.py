from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 3.1: Professional Virtues & Behaviors",
    page_icon="🛡️",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab3_1_step" not in st.session_state:
    st.session_state.lab3_1_step = 1

# --- Sidebar เมนูด้านซ้าย ---
st.sidebar.markdown("### 🛡️ LAB 3.1 Workflow")

steps_name = {
    1: "Activity 1: Individual Vote",
    2: "Activity 2: Group Inquiry",
    3: "Activity 3: From Value to Behavior",
}

current_index = list(steps_name.keys()).index(st.session_state.lab3_1_step)

selected_step_name = st.sidebar.radio(
    "เลือกกิจกรรม LAB 3.1:",
    list(steps_name.values()),
    index=current_index,
    key="lab3_1_menu_selection",
)

for s_num, s_title in steps_name.items():
    if s_title == selected_step_name:
        st.session_state.lab3_1_step = s_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อกิจกรรมด้านบนเพื่อเปลี่ยนหน้า")


# ==========================================
# 1. Activity 1 — Individual Vote
# ==========================================
if st.session_state.lab3_1_step == 1:
    st.title("🗳️ Activity 1 — Individual Vote")
    st.markdown("### “ถ้าต้องเลือกคุณสมบัติสำคัญที่สุดเพียง 3 ข้อของผู้ประกอบวิชาชีพที่ดี คุณจะเลือกอะไร?”")

    with st.form("lab3_1_act1_form"):
        student_id = st.text_input("รหัสนิสิต:")
        virtues_choice = st.text_area("พิมพ์คุณสมบัติ 3 ข้อของคุณ (เช่น ซื่อสัตย์, รับผิดชอบ, เห็นอกเห็นใจ):")
        sub_a1 = st.form_submit_button("ส่งคำตอบ (3 คุณสมบัติ)")

        if sub_a1 and student_id and virtues_choice:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3.1 - Act 1 Virtues",
                "Data": f"[{student_id}] Top 3 Virtues: {virtues_choice}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_1_Responses", data=updated)
                    st.success("บันทึกคำตอบสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a1:
            st.warning("กรุณากรอกรหัสนิสิตและคุณสมบัติให้ครบถ้วน")

    st.markdown("---")
    st.markdown("### 🧠 คำถามสะท้อนคิดต่อ: “แล้วอะไรทำให้เราจัดความสำคัญแตกต่างกัน?”")
    
    with st.form("lab3_1_act1_reflection_form"):
        student_id_ref = st.text_input("รหัสนิสิต (สำหรับส่วนคำถามสะท้อนคิด):")
        reflection_text = st.text_area("พิมพ์เหตุผลของคุณว่าอะไรทำให้การจัดลำดับความสำคัญแตกต่างกัน:")
        sub_ref = st.form_submit_button("ส่งคำตอบสะท้อนคิด")

        if sub_ref and student_id_ref and reflection_text:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3.1 - Act 1 Reflection",
                "Data": f"[{student_id_ref}] Reflection: {reflection_text}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_1_Responses", data=updated)
                    st.success("บันทึกคำตอบสะท้อนคิดสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_ref:
            st.warning("กรุณากรอกรหัสนิสิตและคำตอบสะท้อนคิด")

    st.markdown("---")
    st.subheader("📊 ตารางแสดงข้อมูลคำตอบ Activity 1")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_1_Responses", ttl=5)
            p1_df = df[df["Step"].str.contains("Lab3.1 - Act 1", na=False)]
            if not p1_df.empty:
                st.dataframe(p1_df[["Timestamp", "Step", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูลใน Activity 1")
        except:
            pass


# ==========================================
# 2. Activity 2 — Group Inquiry
# ==========================================
elif st.session_state.lab3_1_step == 2:
    st.title("🔍 Activity 2 — Group Inquiry")
    st.markdown("แต่ละกลุ่มเลือก/ได้รับ คุณธรรม 1–2 ประเด็น แล้วค้นคว้าตอบคำถามทั้ง 4 ข้อด้านล่างนี้")

    with st.form("lab3_1_act2_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        target_virtue = st.text_input("คุณธรรมที่กลุ่มได้รับศึกษา (เช่น ความซื่อสัตย์):")
        
        q1 = st.text_area("Question 1: คุณธรรมนี้หมายถึงอะไร?")
        q2 = st.text_area("Question 2: ทำไมจึงสำคัญต่อผู้ประกอบวิชาชีพ?")
        q3 = st.text_area("Question 3: ถ้าบุคคลมีคุณธรรมนี้จริง เราควรเห็นพฤติกรรมอะไร?")
        q4 = st.text_area("Question 4: มีสถานการณ์ใดที่คุณธรรมนี้อาจขัดแย้งกับคุณค่าอื่น?")
        
        sub_a2 = st.form_submit_button("ส่งคำตอบ Group Inquiry")

        if sub_a2 and group_name and target_virtue:
            combined_q = f"Virtue: {target_virtue} | Q1: {q1} | Q2: {q2} | Q3: {q3} | Q4: {q4}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3.1 - Act 2 Group Inquiry",
                "Data": f"[{group_name}] {combined_q}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_1_Responses", data=updated)
                    st.success("บันทึกคำตอบ Group Inquiry สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a2:
            st.warning("กรุณากรอกชื่อกลุ่มและคุณธรรมที่ศึกษา")

    st.markdown("---")
    st.subheader("📋 ตารางรวมผลงานค้นคว้าของแต่ละกลุ่ม (Activity 2)")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_1_Responses", ttl=5)
            p2_df = df[df["Step"] == "Lab3.1 - Act 2 Group Inquiry"]
            if not p2_df.empty:
                st.dataframe(p2_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล Group Inquiry")
        except:
            pass


# ==========================================
# 3. Activity 3 — From “Value” to “Behavior”
# ==========================================
elif st.session_state.lab3_1_step == 3:
    st.title("🎯 Activity 3 — From “Value” to “Behavior”")
    st.markdown("เปลี่ยนคำที่เป็นนามธรรมให้เป็นพฤติกรรมที่สังเกตได้จริง")

    with st.form("lab3_1_act3_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        value_input = st.text_input("คุณธรรม/ค่านิยม (เช่น ความรับผิดชอบ):")
        
        behavior_obs = st.text_area("พฤติกรรมที่สังเกตได้:")
        scenario_obs = st.text_area("สถานการณ์ที่อาจเกิดขึ้น:")
        consequence_obs = st.text_area("ถ้าไม่ทำตามคุณธรรมนี้จะเกิดอะไรขึ้น:")
        
        sub_a3 = st.form_submit_button("ส่งคำตอบ Value to Behavior")

        if sub_a3 and group_name and value_input:
            combined_b = f"Value: {value_input} | Behavior: {behavior_obs} | Scenario: {scenario_obs} | Consequence: {consequence_obs}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3.1 - Act 3 Value to Behavior",
                "Data": f"[{group_name}] {combined_b}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_1_Responses", data=updated)
                    st.success("บันทึก Value to Behavior สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a3:
            st.warning("กรุณากรอกชื่อกลุ่มและคุณธรรม/ค่านิยม")

    st.markdown("---")
    st.subheader("📋 ตารางสรุปพฤติกรรมเชิงประจักษ์ของแต่ละกลุ่ม (Activity 3)")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_1_Responses", ttl=5)
            p3_df = df[df["Step"] == "Lab3.1 - Act 3 Value to Behavior"]
            if not p3_df.empty:
                st.dataframe(p3_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล Value to Behavior")
        except:
            pass