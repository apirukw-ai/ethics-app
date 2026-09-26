from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 3.2: Professional Virtues & Presentation",
    page_icon="🗺️",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab3_2_step" not in st.session_state:
    st.session_state.lab3_2_step = 4

# --- Sidebar เมนูด้านซ้าย ---
st.sidebar.markdown("### 🗺️ LAB 3.2 Workflow")

steps_name = {
    4: "Activity 4: Group Presentation",
    5: "Activity 5: Peer Challenge",
    6: "Activity 6: Virtue Map",
    7: "Activity 7: Difficult Question",
    8: "Final Reflection (Lab 3)",
}

current_index = list(steps_name.keys()).index(st.session_state.lab3_2_step)

selected_step_name = st.sidebar.radio(
    "เลือกกิจกรรม LAB 3.2:",
    list(steps_name.values()),
    index=current_index,
    key="lab3_2_menu_selection",
)

for s_num, s_title in steps_name.items():
    if s_title == selected_step_name:
        st.session_state.lab3_2_step = s_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อกิจกรรมด้านบนเพื่อเปลี่ยนหน้า")


# ==========================================
# 4. Activity 4 — Group Presentation
# ==========================================
if st.session_state.lab3_2_step == 4:
    st.title("🎤 Activity 4 — Group Presentation")
    st.markdown("บันทึกสรุปโครงสร้าง Presentation ของกลุ่ม (6 หัวข้อบังคับ)")

    with st.form("lab3_2_act4_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        
        c1 = st.text_area("1. Our Value: คุณธรรมที่กลุ่มเลือกคืออะไร?")
        c2 = st.text_area("2. Why?: ทำไมจึงสำคัญ?")
        c3 = st.text_area("3. Evidence: มีข้อมูลหรือหลักฐานอะไรสนับสนุน?")
        c4 = st.text_area("4. In Practice: แสดงออกเป็นพฤติกรรมอย่างไร?")
        c5 = st.text_area("5. Conflict: มีสถานการณ์ใดที่คุณธรรมนี้อาจขัดแย้งกับคุณค่าอื่น?")
        c6 = st.text_area("6. Our Position: กลุ่มมีเหตุผลอย่างไร?")
        
        sub_a4 = st.form_submit_button("ส่งสรุป Presentation")

        if sub_a4 and group_name:
            combined_p = f"Value: {c1} | Why: {c2} | Evidence: {c3} | Practice: {c4} | Conflict: {c5} | Position: {c6}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3.2 - Act 4 Presentation",
                "Data": f"[{group_name}] {combined_p}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_2_Responses", data=updated)
                    st.success("บันทึกข้อมูล Presentation สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a4:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางรวมข้อมูล Presentation ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_2_Responses", ttl=5)
            p4_df = df[df["Step"] == "Lab3.2 - Act 4 Presentation"]
            if not p4_df.empty:
                st.dataframe(p4_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล Presentation")
        except:
            pass


# ==========================================
# 5. Activity 5 — Peer Challenge
# ==========================================
elif st.session_state.lab3_2_step == 5:
    st.title("⚔️ Activity 5 — Peer Challenge")
    st.markdown("ส่งคำถามท้าทาย (Why?, What if?, Conflict?) ไปยังกลุ่มที่นำเสนอ")

    with st.form("lab3_2_act5_form"):
        group_name = st.text_input("ชื่อกลุ่มของคุณ (ผู้ตั้งคำถาม):")
        target_group = st.text_input("กลุ่มที่ถูกถาม (เช่น กลุ่ม 2):")
        
        challenge_type = st.selectbox(
            "ประเภทคำถาม:",
            [
                "Why? (ทำไมคุณจึงคิดว่าคุณธรรมนี้สำคัญ?)",
                "What if? (ถ้าสถานการณ์เปลี่ยนไป คุณยังคิดเหมือนเดิมหรือไม่?)",
                "Conflict? (ถ้าคุณธรรมนี้ขัดแย้งกับคุณธรรมอื่น คุณจะจัดการอย่างไร?)"
            ]
        )
        question_text = st.text_area("พิมพ์ข้อความคำถามของคุณ:")
        
        sub_a5 = st.form_submit_button("ส่งคำถามท้าทาย")

        if sub_a5 and group_name and target_group and question_text:
            combined_ch = f"Target: {target_group} | Type: {challenge_type} | Q: {question_text}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3.2 - Act 5 Peer Challenge",
                "Data": f"[{group_name}] {combined_ch}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_2_Responses", data=updated)
                    st.success("ส่งคำถามท้าทายสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a5:
            st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")

    st.markdown("---")
    st.subheader("📋 รายการคำถาม Peer Challenge ทั้งหมด")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_2_Responses", ttl=5)
            p5_df = df[df["Step"] == "Lab3.2 - Act 5 Peer Challenge"]
            if not p5_df.empty:
                st.dataframe(p5_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูลคำถามท้าทาย")
        except:
            pass


# ==========================================
# 6. Activity 6 — The Professional Virtue Map
# ==========================================
elif st.session_state.lab3_2_step == 6:
    st.title("🗺️ Activity 6 — The Professional Virtue Map")
    st.markdown("ร่วมกันสร้างแผนภาพ Professional Virtue Map ของห้องเรียน")
    st.info("โครงสร้าง: Professional → Values/Virtues → Behaviors → Impact on patients/colleagues/society")

    with st.form("lab3_2_act6_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        map_input = st.text_area("สรุปข้อเสนอแนะโครงสร้างแผนภาพ Virtue Map ของกลุ่มคุณ:")
        sub_a6 = st.form_submit_button("ส่งข้อมูล Virtue Map")

        if sub_a6 and group_name and map_input:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3.2 - Act 6 Virtue Map",
                "Data": f"[{group_name}] {map_input}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_2_Responses", data=updated)
                    st.success("บันทึก Virtue Map สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a6:
            st.warning("กรุณากรอกชื่อกลุ่มและข้อมูลแผนภาพ")

    st.markdown("---")
    st.subheader("📋 ข้อมูล Virtue Map จากทุกกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_2_Responses", ttl=5)
            p6_df = df[df["Step"] == "Lab3.2 - Act 6 Virtue Map"]
            if not p6_df.empty:
                st.dataframe(p6_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล Virtue Map")
        except:
            pass


# ==========================================
# 7. Activity 7 — The Difficult Question
# ==========================================
elif st.session_state.lab3_2_step == 7:
    st.title("❓ Activity 7 — The Difficult Question")
    st.markdown("### “ถ้าคุณธรรมสองอย่างที่เรายึดถือเกิดขัดแย้งกัน เราจะเลือกอย่างไร?”")

    with st.form("lab3_2_act7_form"):
        student_id = st.text_input("รหัสนิสิต:")
        difficult_answer = st.text_area("พิมพ์แนวทางการตัดสินใจของคุณเมื่อคุณธรรมขัดแย้งกัน:")
        sub_a7 = st.form_submit_button("ส่งคำตอบ Difficult Question")

        if sub_a7 and student_id and difficult_answer:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3.2 - Act 7 Difficult Q",
                "Data": f"[{student_id}] {difficult_answer}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_2_Responses", data=updated)
                    st.success("บันทึกคำตอบสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a7:
            st.warning("กรุณากรอกรหัสนิสิตและคำตอบ")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงคำตอบของนิสิต (สำหรับอาจารย์เลือกหยิบมาอภิปราย)")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_2_Responses", ttl=5)
            p7_df = df[df["Step"] == "Lab3.2 - Act 7 Difficult Q"]
            if not p7_df.empty:
                st.dataframe(p7_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูลคำตอบ")
        except:
            pass


# ==========================================
# 8. Final Reflection (Lab 3)
# ==========================================
elif st.session_state.lab3_2_step == 8:
    st.title("🎯 Final Reflection (Lab 3)")
    st.markdown("### “จาก Lab 3 วันนี้…”")

    with st.form("lab3_2_reflection_form"):
        student_id = st.text_input("รหัสนิสิต (ระบุหรือไม่ระบุก็ได้):")
        
        r1 = st.text_input("1. คุณธรรมหนึ่งข้อที่ข้าพเจ้าคิดว่าสำคัญต่อการเป็นผู้ประกอบวิชาชีพคือ:")
        r2 = st.text_area("2. เพราะอะไร:")
        r3 = st.text_area("3. พฤติกรรมที่ข้าพเจ้าสามารถเริ่มฝึกได้ตั้งแต่ตอนเป็นนิสิตคือ:")
        r4 = st.text_area("4. สิ่งที่ข้าพเจ้ายังสงสัยเกี่ยวกับการเป็นผู้ประกอบวิชาชีพที่มีจริยธรรมคือ:")
        
        sub_ref = st.form_submit_button("ส่งแบบสะท้อนความคิด Lab 3")

        if sub_ref and student_id and r1:
            sid_val = "Anonymous" if not student_id else student_id
            combined_ref = f"Virtue: {r1} | Because: {r2} | Practice: {r3} | Doubt: {r4}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3.2 - Final Reflection",
                "Data": f"[{sid_val}] {combined_ref}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_2_Responses", data=updated)
                    st.success("บันทึก Final Reflection สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_ref:
            st.warning("กรุณากรอกรหัสนิสิตและคุณธรรมข้อที่ 1")

    st.markdown("---")
    st.subheader("📋 ตารางรวม Final Reflection (Lab 3)")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_2_Responses", ttl=5)
            ref_df = df[df["Step"] == "Lab3.2 - Final Reflection"]
            if not ref_df.empty:
                st.dataframe(ref_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล Reflection")
        except:
            pass
