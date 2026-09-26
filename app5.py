from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 5: Speaker Session & Reflection",
    page_icon="🎙️",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab5_step" not in st.session_state:
    st.session_state.lab5_step = 1

# --- Sidebar เมนูด้านซ้าย ---
st.sidebar.markdown("### 🎙️ LAB 5 Workflow")

steps_name = {
    1: "1. ก่อนพบวิทยากร — What would you do?",
    2: "2. ระหว่างสัมมนา — Listen for the Dilemma",
    3: "3. ช่วงถาม-ตอบวิทยากร (Q&A)",
    4: "4. Activity: Reality vs Classroom",
    5: "5. Final Activity — One Lesson",
}

current_index = list(steps_name.keys()).index(st.session_state.lab5_step)

selected_step_name = st.sidebar.radio(
    "เลือกกิจกรรม LAB 5:",
    list(steps_name.values()),
    index=current_index,
    key="lab5_menu_selection",
)

for s_num, s_title in steps_name.items():
    if s_title == selected_step_name:
        st.session_state.lab5_step = s_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อกิจกรรมด้านบนเพื่อเปลี่ยนหน้า")


# ==========================================
# 1. ก่อนพบวิทยากร — “What would you do?”
# ==========================================
if st.session_state.lab5_step == 1:
    st.title("🎯 ก่อนพบวิทยากร — “What would you do?”")
    st.markdown("ตอบคำถามสถานการณ์สมมิติก่อนเริ่มรับฟังประสบการณ์จริงจากวิทยากร")

    with st.form("lab5_act1_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        q1 = st.radio(
            "1. ถ้าคุณพบว่าเพื่อนร่วมงานทำสิ่งที่ไม่เหมาะสม แต่การทักท้วงอาจทำให้ความสัมพันธ์เสีย คุณจะทำอย่างไร?",
            [
                "ทักท้วงทันทีเพื่อประโยชน์ส่วนรวมและความถูกต้อง",
                "นิ่งไว้เพราะไม่อยากเสียความสัมพันธ์",
                "คุยส่วนตัวกับเพื่อนคนนั้นก่อนเบา ๆ",
                "ปรึกษาหัวหน้างานหรือผู้มีอำนาจโดยไม่บอกเพื่อนตรง ๆ",
                "อื่น ๆ"
            ]
        )
        
        q2 = st.radio(
            "2. ถ้ากฎกับสิ่งที่คุณคิดว่าดีที่สุดสำหรับผู้ป่วยไม่ตรงกัน คุณจะทำอย่างไร?",
            [
                "ยึดตามกฎระเบียบขององค์กรไว้ก่อน",
                "ยึดสิ่งที่ดีที่สุดสำหรับผู้ป่วยเป็นหลัก แม้ต้องเสี่ยง",
                "หาทางออกร่วมกับทีมหรือผู้เชี่ยวชาญเพื่อปรับเปลี่ยน",
                "ปฏิเสธการปฏิบัติงานในเคสนั้น",
                "อื่น ๆ"
            ]
        )
        
        sub_a1 = st.form_submit_button("ส่งคำตอบ What would you do?")

        if sub_a1 and student_id:
            combined_q = f"Q1: {q1} | Q2: {q2}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Act 1 What Would You Do",
                "Data": f"[{student_id}] {combined_q}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("บันทึกคำตอบสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a1:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผลคำตอบของนิสิต (Activity 1)")
    if conn:
        try:
            df = conn.read(worksheet="Lab5_Responses", ttl=5)
            p1_df = df[df["Step"] == "Lab5 - Act 1 What Would You Do"]
            if not p1_df.empty:
                st.dataframe(p1_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูลในระบบ")
        except:
            pass


# ==========================================
# 2. ระหว่างสัมมนา — “Listen for the Dilemma”
# ==========================================
elif st.session_state.lab5_step == 2:
    st.title("👂 ระหว่างสัมมนา — “Listen for the Dilemma”")
    st.markdown("จับประเด็นจากสิ่งที่วิทยากรพูดตามโครงสร้าง 6 ข้อด้านล่างนี้")

    with st.form("lab5_act2_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        c1 = st.text_area("1. Situation: เกิดสถานการณ์อะไร?")
        c2 = st.text_area("2. Ethical Challenge: ปัญหาจริยธรรมคืออะไร?")
        c3 = st.text_area("3. Stakeholders: ใครได้รับผลกระทบ?")
        c4 = st.text_area("4. Decision: ผู้ประกอบวิชาชีพตัดสินใจอย่างไร?")
        c5 = st.text_area("5. Why?: เหตุผลอะไรที่อยู่เบื้องหลังการตัดสินใจ?")
        c6 = st.text_area("6. Lesson: นิสิตเรียนรู้อะไร?")
        
        sub_a2 = st.form_submit_button("ส่งบันทึกการฟังบรรยาย")

        if sub_a2 and student_id:
            combined_listen = f"Sit: {c1} | Chal: {c2} | Stake: {c3} | Dec: {c4} | Why: {c5} | Lesson: {c6}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Act 2 Listen Dilemma",
                "Data": f"[{student_id}] {combined_listen}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("บันทึกข้อมูลการฟังสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a2:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงบันทึก Listen for the Dilemma")
    if conn:
        try:
            df = conn.read(worksheet="Lab5_Responses", ttl=5)
            p2_df = df[df["Step"] == "Lab5 - Act 2 Listen Dilemma"]
            if not p2_df.empty:
                st.dataframe(p2_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 3. ช่วงถาม-ตอบวิทยากร (Q&A)
# ==========================================
elif st.session_state.lab5_step == 3:
    st.title("🙋‍♂️ ช่วงถาม-ตอบวิทยากร (Q&A)")
    st.markdown("ส่งคำถามจากกลุ่มของคุณเพื่อร่วมสนทนากับวิทยากร")

    with st.form("lab5_act3_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        
        question_text = st.text_area(
            "พิมพ์คำถามของคุณ (ตัวอย่าง: ถ้าย้อนกลับไปตอนเกิดเหตุการณ์นั้น คุณจะตัดสินใจเหมือนเดิมหรือไม่? / ตอนนั้นอะไรตัดสินใจยากที่สุด? ฯลฯ):"
        )
        
        sub_a3 = st.form_submit_button("ส่งคำถามถึงวิทยากร")

        if sub_a3 and group_name and question_text:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Act 3 Speaker QnA",
                "Data": f"[{group_name}] Q: {question_text}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("ส่งคำถามสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a3:
            st.warning("กรุณากรอกชื่อกลุ่มและคำถาม")

    st.markdown("---")
    st.subheader("📋 รายการคำถามจากกลุ่มทั้งหมด")
    if conn:
        try:
            df = conn.read(worksheet="Lab5_Responses", ttl=5)
            p3_df = df[df["Step"] == "Lab5 - Act 3 Speaker QnA"]
            if not p3_df.empty:
                st.dataframe(p3_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีคำถาม")
        except:
            pass


# ==========================================
# 4. Activity: “Reality vs Classroom”
# ==========================================
elif st.session_state.lab5_step == 4:
    st.title("🔄 Activity: “Reality vs Classroom”")
    st.markdown("เปรียบเทียบความคิดเห็นของคุณก่อนและหลังฟังประสบการณ์จริงจากวิทยากร")

    with st.form("lab5_act4_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        before_text = st.text_area("ก่อนฟังวิทยากร ฉันคิดว่าฉันจะทำอย่างไร:")
        after_text = st.text_area("หลังฟังวิทยากร เมื่อได้ฟังประสบการณ์จริง ฉันยังคิดเหมือนเดิมหรือไม่ (เพราะอะไร):")
        
        sub_a4 = st.form_submit_button("ส่งคำตอบ Reality vs Classroom")

        if sub_a4 and student_id:
            combined_rc = f"Before: {before_text} | After: {after_text}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Act 4 Reality vs Classroom",
                "Data": f"[{student_id}] {combined_rc}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("บันทึกข้อมูลสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a4:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Reality vs Classroom")
    if conn:
        try:
            df = conn.read(worksheet="Lab5_Responses", ttl=5)
            p4_df = df[df["Step"] == "Lab5 - Act 4 Reality vs Classroom"]
            if not p4_df.empty:
                st.dataframe(p4_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 5. Final Activity — “One Lesson from a Professional”
# ==========================================
elif st.session_state.lab5_step == 5:
    st.title("🎯 Final Activity — “One Lesson from a Professional”")
    st.markdown("สะท้อนสิ่งที่ได้เรียนรู้ 3 ข้อสุดท้าย")

    with st.form("lab5_act5_form"):
        student_id = st.text_input("รหัสนิสิต (ระบุหรือไม่ระบุก็ได้):")
        
        ans1 = st.text_area("1. สิ่งหนึ่งที่ผมได้เรียนรู้จากประสบการณ์ของวิทยากรคือ:")
        ans2 = st.text_area("2. สิ่งหนึ่งที่ผมเคยคิดต่างจากเดิมคือ:")
        ans3 = st.text_area("3. เมื่อผมเข้าสู่วิชาชีพ ผมอยากเตรียมตัวเรื่อง:")
        
        sub_a5 = st.form_submit_button("ส่ง One Lesson Reflection")

        if sub_a5 and student_id:
            sid_val = "Anonymous" if not student_id else student_id
            combined_one = f"Lesson: {ans1} | Diff: {ans2} | Prep: {ans3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Act 5 One Lesson",
                "Data": f"[{sid_val}] {combined_one}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("บันทึก Final Reflection สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a5:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางรวม One Lesson from a Professional")
    if conn:
        try:
            df = conn.read(worksheet="Lab5_Responses", ttl=5)
            p5_df = df[df["Step"] == "Lab5 - Act 5 One Lesson"]
            if not p5_df.empty:
                st.dataframe(p5_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass