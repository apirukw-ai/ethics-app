from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 6: Complex Cases & Uncertainty",
    page_icon="💊",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab6_step" not in st.session_state:
    st.session_state.lab6_step = 1

# --- Sidebar เมนูด้านซ้าย ---
st.sidebar.markdown("### 💊 LAB 6 Workflow")

steps_name = {
    1: "Activity 1: First Vote (Case 1)",
    2: "Activity 2: Case 1 Analysis",
    3: "Activity 3: Ethical Tension Map",
    4: "Activity 4: Challenge the Decision",
    5: "Activity 5: Case 2 Missing Info",
    6: "Activity 6: Decision Under Uncertainty",
    7: "Activity 7: Final Re-Vote",
    8: "Final Reflection (Lab 6)",
}

current_index = list(steps_name.keys()).index(st.session_state.lab6_step)

selected_step_name = st.sidebar.radio(
    "เลือกกิจกรรม LAB 6:",
    list(steps_name.values()),
    index=current_index,
    key="lab6_menu_selection",
)

for s_num, s_title in steps_name.items():
    if s_title == selected_step_name:
        st.session_state.lab6_step = s_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อกิจกรรมด้านบนเพื่อเปลี่ยนหน้า")


# ==========================================
# 1. Activity 1 — First Vote (Case 1)
# ==========================================
if st.session_state.lab6_step == 1:
    st.title("🗳️ Activity 1 — First Vote (Case 1)")
    st.markdown("### Case 1: “ผู้ป่วยควรมีสิทธิเลือกยาต้นแบบหรือยาสามัญหรือไม่?”")

    with st.form("lab6_act1_form"):
        student_id = st.text_input("รหัสนิสิต:")
        vote_choice = st.radio(
            "เลือกคำตอบของคุณ:",
            ["ควร", "ไม่ควร", "ขึ้นกับสถานการณ์", "ยังไม่แน่ใจ"]
        )
        sub_a1 = st.form_submit_button("ส่งคำตอบ First Vote")

        if sub_a1 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab6 - Act 1 First Vote",
                "Data": f"[{student_id}] Vote: {vote_choice}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab6_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab6_Responses", data=updated)
                    st.success("บันทึกผลโหวตสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a1:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผล Vote (Case 1)")
    if conn:
        try:
            df = conn.read(worksheet="Lab6_Responses", ttl=5)
            act1_df = df[df["Step"] == "Lab6 - Act 1 First Vote"]
            if not act1_df.empty:
                votes = act1_df["Data"].apply(lambda x: x.split("Vote: ")[1].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
            else:
                st.info("ยังไม่มีข้อมูลผลโหวต")
        except:
            pass


# ==========================================
# 2. Activity 2 — Case 1: Generic vs Original
# ==========================================
elif st.session_state.lab6_step == 2:
    st.title("📋 Activity 2 — Case 1: Generic vs Original")
    st.info("สถานการณ์: เภสัชกรไม่ได้ถามความต้องการของผู้ป่วย และมีเหตุผลเรื่องกำไรของร้านยาเข้ามาเกี่ยวข้อง วิเคราะห์ผ่าน Ethical Decision Canvas")

    with st.form("lab6_act2_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        
        c1 = st.text_area("1. What happened? (ข้อเท็จจริงคืออะไร?)")
        c2 = st.text_area("2. Who is affected? (ใครได้รับผลกระทบ? เช่น ผู้ป่วย, เภสัชกร, ร้านยา, ระบบสุขภาพ ฯลฯ)")
        c3 = st.text_area("3. What values are involved? (มีคุณค่าอะไรบ้าง? เช่น สิทธิ, ประโยชน์ผู้ป่วย, ผลประโยชน์ทางธุรกิจ ฯลฯ)")
        c4 = st.text_area("4. What information is missing? (เรารู้อะไรไม่พอที่จะตัดสิน?)")
        
        sub_a2 = st.form_submit_button("ส่งผลวิเคราะห์ Canvas")

        if sub_a2 and group_name:
            combined_canvas = f"What: {c1} | Who: {c2} | Values: {c3} | Missing: {c4}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab6 - Act 2 Canvas",
                "Data": f"[{group_name}] {combined_canvas}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab6_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab6_Responses", data=updated)
                    st.success("บันทึก Canvas สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a2:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Canvas ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab6_Responses", ttl=5)
            p2_df = df[df["Step"] == "Lab6 - Act 2 Canvas"]
            if not p2_df.empty:
                st.dataframe(p2_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 3. Activity 3 — Ethical Tension Map
# ==========================================
elif st.session_state.lab6_step == 3:
    st.title("🗺️ Activity 3 — Ethical Tension Map")
    st.markdown("โครงสร้างความขัดแย้ง: **Patient choice ↔ Professional responsibility ↔ Business interest**")

    with st.form("lab6_act3_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        tension_answer = st.text_area("“ตรงไหนคือจุดที่ทำให้ case นี้กลายเป็นปัญหาจริยธรรม?”")
        sub_a3 = st.form_submit_button("ส่งคำตอบ Tension Map")

        if sub_a3 and group_name and tension_answer:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab6 - Act 3 Tension Map",
                "Data": f"[{group_name}] {tension_answer}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab6_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab6_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a3:
            st.warning("กรุณากรอกชื่อกลุ่มและคำตอบ")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Ethical Tension Map")
    if conn:
        try:
            df = conn.read(worksheet="Lab6_Responses", ttl=5)
            p3_df = df[df["Step"] == "Lab6 - Act 3 Tension Map"]
            if not p3_df.empty:
                st.dataframe(p3_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 4. Activity 4 — Challenge the Decision
# ==========================================
elif st.session_state.lab6_step == 4:
    st.title("⚔️ Activity 4 — Challenge the Decision")
    st.markdown("ทดสอบเปลี่ยนเงื่อนไขสถานการณ์ แล้วพิจารณาว่า Decision เปลี่ยนหรือไม่")

    with st.form("lab6_act4_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        condition_case = st.selectbox(
            "เลือกเงื่อนไขที่เปลี่ยน:",
            [
                "เงื่อนไข 1: ถ้าผู้ป่วยไม่สามารถจ่ายค่ายาต้นแบบได้",
                "เงื่อนไข 2: ถ้าผู้ป่วยยืนยันว่าต้องการยาต้นแบบ",
                "เงื่อนไข 3: ถ้าเภสัชกรมีข้อมูลว่าผู้ป่วยรายนี้เคยมีปัญหากับยาชนิดหนึ่ง"
            ]
        )
        decision_changed = st.radio("Decision ของกลุ่มเปลี่ยนหรือไม่?", ["เปลี่ยน", "ไม่เปลี่ยน", "ปรับเปลี่ยนบางส่วน"])
        reason_text = st.text_area("อธิบายเหตุผลประกอบ:")
        
        sub_a4 = st.form_submit_button("ส่งคำตอบ Challenge Decision")

        if sub_a4 and group_name:
            cond_tag = condition_case.split(":")[0]
            combined_ch = f"Cond: {cond_tag} | Decision: {decision_changed} | Reason: {reason_text}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab6 - Act 4 Challenge Decision",
                "Data": f"[{group_name}] {combined_ch}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab6_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab6_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a4:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Challenge the Decision")
    if conn:
        try:
            df = conn.read(worksheet="Lab6_Responses", ttl=5)
            p4_df = df[df["Step"] == "Lab6 - Act 4 Challenge Decision"]
            if not p4_df.empty:
                st.dataframe(p4_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 5. Activity 5 — Case 2: ผู้ป่วยต้องการยานอนหลับ
# ==========================================
elif st.session_state.lab6_step == 5:
    st.title("💊 Activity 5 — Case 2: ผู้ป่วยต้องการยานอนหลับ")
    st.markdown("### “ถ้าคุณเป็นเภสัชกรในสถานการณ์นี้ คุณต้องรู้อะไรเพิ่มเติมก่อนตัดสินใจ?”")

    with st.form("lab6_act5_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        missing_info_list = st.text_area(
            "สร้าง Missing Information List (เช่น อายุ, โรคประจำตัว, ยาที่ใช้อยู่, ระยะเวลาที่มีอาการ, เหตุผลที่ต้องการ ฯลฯ):"
        )
        sub_a5 = st.form_submit_button("ส่ง Missing Info List")

        if sub_a5 and group_name and missing_info_list:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab6 - Act 5 Missing Info",
                "Data": f"[{group_name}] {missing_info_list}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab6_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab6_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a5:
            st.warning("กรุณากรอกชื่อกลุ่มและรายการข้อมูล")

    st.markdown("---")
    st.subheader("📋 ตารางรวบรวม Missing Information List ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab6_Responses", ttl=5)
            p5_df = df[df["Step"] == "Lab6 - Act 5 Missing Info"]
            if not p5_df.empty:
                st.dataframe(p5_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 6. Activity 6 — Decision Under Uncertainty
# ==========================================
elif st.session_state.lab6_step == 6:
    st.title("🔄 Activity 6 — Decision Under Uncertainty")
    st.markdown("จำลองการตัดสินใจทีละรอบ เมื่อได้รับข้อมูลเพิ่มเติมทีละชิ้น")

    with st.form("lab6_act6_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        r1_dec = st.text_area("Round 1 (ข้อมูลพื้นฐาน): การตัดสินใจของกลุ่มคืออะไร?")
        r2_dec = st.text_area("Round 2 (เพิ่มข้อมูล): การตัดสินใจเปลี่ยนหรือไม่ อย่างไร?")
        r3_dec = st.text_area("Round 3 (เพิ่มข้อมูลอีก): การตัดสินใจครั้งสุดท้ายคืออะไร?")
        
        sub_a6 = st.form_submit_button("ส่งผลการตัดสินใจ 3 รอบ")

        if sub_a6 and group_name:
            combined_unc = f"R1: {r1_dec} | R2: {r2_dec} | R3: {r3_dec}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab6 - Act 6 Uncertainty Rounds",
                "Data": f"[{group_name}] {combined_unc}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab6_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab6_Responses", data=updated)
                    st.success("บันทึกผลสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a6:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงการเปลี่ยนแปลงการตัดสินใจ (Uncertainty Rounds)")
    if conn:
        try:
            df = conn.read(worksheet="Lab6_Responses", ttl=5)
            p6_df = df[df["Step"] == "Lab6 - Act 6 Uncertainty Rounds"]
            if not p6_df.empty:
                st.dataframe(p6_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 7. Activity 7 — Final Re-Vote
# ==========================================
elif st.session_state.lab6_step == 7:
    st.title("🎯 Activity 7 — Final Re-Vote")
    st.markdown("### “จากสองกรณีศึกษา วันนี้ คุณคิดว่าการตัดสินใจทางจริยธรรมของเภสัชกรควรเริ่มจากอะไร?”")

    with st.form("lab6_act7_form"):
        student_id = st.text_input("รหัสนิสิต:")
        final_choice = st.selectbox(
            "เลือกจุดเริ่มต้นการตัดสินใจ:",
            [
                "กฎหมาย",
                "จรรยาบรรณ",
                "ความต้องการของผู้ป่วย",
                "ประโยชน์ของผู้ป่วย",
                "ข้อเท็จจริง",
                "หลายองค์ประกอบร่วมกัน",
                "อื่น ๆ"
            ]
        )
        sub_a7 = st.form_submit_button("ส่ง Final Re-Vote")

        if sub_a7 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab6 - Act 7 Final Vote",
                "Data": f"[{student_id}] Choice: {final_choice}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab6_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab6_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a7:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 เปรียบเทียบผลโหวต Before (Act 1) vs After (Act 7)")
    if conn:
        try:
            df = conn.read(worksheet="Lab6_Responses", ttl=5)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                st.markdown("**Before Vote (Act 1)**")
                act1_df = df[df["Step"] == "Lab6 - Act 1 First Vote"]
                if not act1_df.empty:
                    votes_b = act1_df["Data"].apply(lambda x: x.split("Vote: ")[1].strip() if "Vote: " in x else x)
                    st.bar_chart(votes_b.value_counts())
                else:
                    st.info("ยังไม่มีข้อมูล Before")
            
            with col_b2:
                st.markdown("**Final Re-Vote (Act 7)**")
                act7_df = df[df["Step"] == "Lab6 - Act 7 Final Vote"]
                if not act7_df.empty:
                    votes_a = act7_df["Data"].apply(lambda x: x.split("Choice: ")[1].strip() if "Choice: " in x else x)
                    st.bar_chart(votes_a.value_counts())
                else:
                    st.info("ยังไม่มีข้อมูล After")
        except:
            pass


# ==========================================
# Final Reflection (Lab 6)
# ==========================================
elif st.session_state.lab6_step == 8:
    st.title("📝 Final Reflection (Lab 6)")

    with st.form("lab6_reflection_form"):
        student_id = st.text_input("รหัสนิสิต (ระบุหรือไม่ระบุก็ได้):")
        
        q1 = st.text_area("1. สิ่งที่ผมเคยคิดง่ายเกินไปเกี่ยวกับการตัดสินใจทางจริยธรรมคือ:")
        q2 = st.text_area("2. สิ่งที่ผมต้องตรวจสอบก่อนตัดสินใจคือ:")
        q3 = st.text_area("3. หากพบสถานการณ์แบบนี้ในอนาคต ผมจะ:")
        
        sub_ref = st.form_submit_button("ส่ง Final Reflection Lab 6")

        if sub_ref and student_id:
            sid_val = "Anonymous" if not student_id else student_id
            combined_ref = f"Q1: {q1} | Q2: {q2} | Q3: {q3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab6 - Final Reflection",
                "Data": f"[{sid_val}] {combined_ref}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab6_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab6_Responses", data=updated)
                    st.success("บันทึก Reflection สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_ref:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางรวบรวม Final Reflection (Lab 6)")
    if conn:
        try:
            df = conn.read(worksheet="Lab6_Responses", ttl=5)
            ref_df = df[df["Step"] == "Lab6 - Final Reflection"]
            if not ref_df.empty:
                st.dataframe(ref_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass