from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 8: System-Level Ethics & Industrial Pharmacy",
    page_icon="🏭",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab8_step" not in st.session_state:
    st.session_state.lab8_step = 1

# --- Sidebar เมนูด้านซ้าย ---
st.sidebar.markdown("### 🏭 LAB 8 Workflow")

steps_name = {
    1: "Case 1 - Step 1: First Vote",
    2: "Case 1 - Step 2: Analyze & Tension",
    3: "Case 1 - Step 3: Decision-Reason-Impact",
    4: "Case 1 - Step 4 & 5: Challenge & Re-Vote",
    5: "Case 2 - Step 1: First Vote",
    6: "Case 2 - Step 2: Responsibility Matrix",
    7: "Case 2 - Step 3: Tension Map",
    8: "Case 2 - Step 4: Challenge Scenarios",
    9: "Case 2 - Step 5: Final Re-Vote",
    10: "Final Reflection & Debrief",
}

current_index = list(steps_name.keys()).index(st.session_state.lab8_step)

selected_step_name = st.sidebar.radio(
    "เลือกกิจกรรม LAB 8:",
    list(steps_name.values()),
    index=current_index,
    key="lab8_menu_selection",
)

for s_num, s_title in steps_name.items():
    if s_title == selected_step_name:
        st.session_state.lab8_step = s_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อกิจกรรมด้านบนเพื่อเปลี่ยนหน้า")


# ==========================================
# Case 1 - Step 1: First Vote
# ==========================================
if st.session_state.lab8_step == 1:
    st.title("🗳️ Case 1 (Step 1) — First Vote")
    st.markdown("### เมื่อผู้ป่วยรายหนึ่งทำให้เกิดคำถามต่อระบบยา: “ข้อใดควรเป็นหลักสำคัญในการตัดสินใจเกี่ยวกับการผลิตยาสำหรับโรคที่พบได้น้อย?”")
    st.info("💡 เลือกได้มากกว่า 1 ข้อ")

    with st.form("lab8_c1_s1_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        c1_opts = [
            "ความจำเป็นของผู้ป่วย",
            "สิทธิด้านสุขภาพ",
            "ความปลอดภัย",
            "จำนวนผู้ป่วย",
            "ความคุ้มค่าทางเศรษฐศาสตร์",
            "ความรับผิดชอบต่อสังคม",
            "ความเป็นไปได้ในการผลิต",
            "ความยั่งยืนของระบบยา",
            "ความรับผิดชอบของบริษัท",
            "อื่น ๆ"
        ]
        
        selected_c1_votes = []
        st.markdown("เลือกปัจจัยที่ควรให้ความสำคัญ:")
        for opt in c1_opts:
            if st.checkbox(opt, key=f"c1_opt_{opt}"):
                selected_c1_votes.append(opt)
                
        sub_c1_s1 = st.form_submit_button("ส่งผลโหวต Case 1")

        if sub_c1_s1 and student_id:
            if selected_c1_votes:
                combined_v1 = ", ".join(selected_c1_votes)
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab8 - Case1 Step1 Vote",
                    "Data": f"[{student_id}] Factors: {combined_v1}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab8_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab8_Responses", data=updated)
                        st.success("บันทึกสำเร็จ!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else:
                    st.success("บันทึกจำลองสำเร็จ!")
            else:
                st.warning("กรุณาเลือกอย่างน้อย 1 ข้อ")
        elif sub_c1_s1:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผลโหวต Case 1 - Step 1")
    if conn:
        try:
            df = conn.read(worksheet="Lab8_Responses", ttl=5)
            c1_s1_df = df[df["Step"] == "Lab8 - Case1 Step1 Vote"]
            if not c1_s1_df.empty:
                all_factors = []
                for item in c1_s1_df["Data"]:
                    if "Factors: " in item:
                        part = item.split("Factors: ")[1]
                        all_factors.extend([x.strip() for x in part.split(",")])
                if all_factors:
                    st.bar_chart(pd.Series(all_factors).value_counts())
        except:
            pass


# ==========================================
# Case 1 - Step 2: Analyze & Tension Map
# ==========================================
elif st.session_state.lab8_step == 2:
    st.title("📋 Case 1 (Step 2) — Analyze & Tension Map")
    st.markdown("วิเคราะห์รอบด้าน (Patient, Society, Organization, Profession, System) และพิจารณา Ethical Tension")

    with st.form("lab8_c1_s2_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        
        a = st.text_area("A. Patient: ผู้ป่วยต้องการอะไร?")
        b = st.text_area("B. Society: สังคมต้องการอะไร?")
        c = st.text_area("C. Organization: บริษัทต้องพิจารณาอะไร?")
        d = st.text_area("D. Profession: เภสัชกรมีความรับผิดชอบอะไร?")
        e = st.text_area("E. System: ถ้าตัดสินใจแบบนี้ จะส่งผลต่อระบบยาอย่างไร?")
        
        tension_ans = st.text_area("Ethical Tension: “การที่โรคพบได้น้อย ควรทำให้สิทธิในการเข้าถึงยาลดลงหรือไม่? จงอธิบาย”")
        
        sub_c1_s2 = st.form_submit_button("ส่งผลวิเคราะห์ Case 1")

        if sub_c1_s2 and group_name:
            combined_an = f"Patient: {a} | Society: {b} | Org: {c} | Prof: {d} | System: {e} | Tension: {tension_ans}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab8 - Case1 Step2 Analyze",
                "Data": f"[{group_name}] {combined_an}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab8_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab8_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_c1_s2:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผลการวิเคราะห์ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab8_Responses", ttl=5)
            c1_s2_df = df[df["Step"] == "Lab8 - Case1 Step2 Analyze"]
            if not c1_s2_df.empty:
                st.dataframe(c1_s2_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Case 1 - Step 3: Decision-Reason-Impact
# ==========================================
elif st.session_state.lab8_step == 3:
    st.title("🎯 Case 1 (Step 3) — Decision → Reason → Impact")
    st.markdown("อภิปรายและตอบคำถามในรูปแบบโครงสร้าง Decision → Reason → Potential Consequence")

    with st.form("lab8_c1_s3_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        q1 = st.text_area("1. สิทธิด้านสุขภาพในประเทศไทยเกี่ยวข้องกับกรณีนี้อย่างไร?")
        q2 = st.text_area("2. ปัญหายากำพร้าในประเทศไทยและต่างประเทศมีประเด็นอะไรที่ควรพิจารณา?")
        q3_dec = st.text_area("3. Decision: หากคุณเป็นผู้มีอำนาจตัดสินใจของบริษัท คุณจะตัดสินใจอย่างไร?")
        q3_reas = st.text_area("Reason: เหตุผลรองรับการตัดสินใจ:")
        q3_imp = st.text_area("Impact: ผลกระทบที่อาจเกิดขึ้นตามมา:")
        
        sub_c1_s3 = st.form_submit_button("ส่งผล Decision → Reason → Impact")

        if sub_c1_s3 and group_name:
            combined_dri = f"Q1: {q1} | Q2: {q2} | Dec: {q3_dec} | Reas: {q3_reas} | Imp: {q3_imp}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab8 - Case1 Step3 DRI",
                "Data": f"[{group_name}] {combined_dri}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab8_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab8_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_c1_s3:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล DRI ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab8_Responses", ttl=5)
            c1_s3_df = df[df["Step"] == "Lab8 - Case1 Step3 DRI"]
            if not c1_s3_df.empty:
                st.dataframe(c1_s3_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Case 1 - Step 4 & 5: Challenge & Re-Vote
# ==========================================
elif st.session_state.lab8_step == 4:
    st.title("🔄 Case 1 (Step 4 & 5) — Challenge & Re-Vote")
    st.markdown("ทดสอบเปลี่ยนเงื่อนไข (Scenario A-E) และสรุปผล Re-Vote")

    with st.form("lab8_c1_s4_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        scen = st.selectbox(
            "เลือก Scenario ที่เปลี่ยน:",
            [
                "Scenario A: มีผู้ป่วยที่ต้องใช้ยานี้เพิ่มขึ้นจาก 1 รายเป็น 100 ราย",
                "Scenario B: ต้นทุนการผลิตสูงมากและบริษัทอาจขาดทุน",
                "Scenario C: รัฐบาลเสนอการสนับสนุนบางส่วน",
                "Scenario D: มีบริษัทอื่นเริ่มผลิตยาชนิดเดียวกัน",
                "Scenario E: ยามีความจำเป็นสูงแต่มีทางเลือกอื่นที่ราคาถูกกว่า"
            ]
        )
        shift_ans = st.radio("การตัดสินใจของคุณเปลี่ยนหรือไม่?", ["เปลี่ยน", "ไม่เปลี่ยน", "ปรับเปลี่ยนเงื่อนไขบางส่วน"])
        reason_ans = st.text_area("เพราะอะไร:")
        
        sub_c1_s4 = st.form_submit_button("ส่งผล Challenge Case 1")

        if sub_c1_s4 and group_name:
            tag = scen.split(":")[0]
            combined_ch1 = f"Scen: {tag} | Shift: {shift_ans} | Reason: {reason_ans}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab8 - Case1 Step4 Challenge",
                "Data": f"[{group_name}] {combined_ch1}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab8_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab8_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_c1_s4:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Challenge Case 1")
    if conn:
        try:
            df = conn.read(worksheet="Lab8_Responses", ttl=5)
            c1_s4_df = df[df["Step"] == "Lab8 - Case1 Step4 Challenge"]
            if not c1_s4_df.empty:
                st.dataframe(c1_s4_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Case 2 - Step 1: First Vote
# ==========================================
elif st.session_state.lab8_step == 5:
    st.title("🗳️ Case 2 (Step 1) — First Vote")
    st.markdown("### เมื่อความปลอดภัยของผู้ป่วยขัดแย้งกับความต้องการของตลาด: “อะไรคือสิ่งที่เภสัชกรต้องรับผิดชอบในสถานการณ์นี้?”")
    st.info("💡 เลือกได้มากกว่า 1 ข้อ")

    with st.form("lab8_c2_s1_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        c2_opts = [
            "ความปลอดภัยของผู้ป่วย",
            "คุณภาพของยา",
            "กฎหมาย/ข้อกำหนด",
            "จรรยาบรรณวิชาชีพ",
            "ความต้องการยาของประชาชน",
            "ความอยู่รอดของโรงงาน",
            "ความรับผิดชอบต่อนายจ้าง",
            "การแก้ปัญหาการขาดแคลนยา",
            "ความรับผิดชอบต่อสังคม"
        ]
        
        selected_c2_votes = []
        st.markdown("เลือกสิ่งที่เภสัชกรต้องรับผิดชอบ:")
        for opt in c2_opts:
            if st.checkbox(opt, key=f"c2_opt_{opt}"):
                selected_c2_votes.append(opt)
                
        sub_c2_s1 = st.form_submit_button("ส่งผลโหวต Case 2")

        if sub_c2_s1 and student_id:
            if selected_c2_votes:
                combined_v2 = ", ".join(selected_c2_votes)
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab8 - Case2 Step1 Vote",
                    "Data": f"[{student_id}] Resp: {combined_v2}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab8_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab8_Responses", data=updated)
                        st.success("บันทึกสำเร็จ!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else:
                    st.success("บันทึกจำลองสำเร็จ!")
            else:
                st.warning("กรุณาเลือกอย่างน้อย 1 ข้อ")
        elif sub_c2_s1:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผลโหวต Case 2 - Step 1")
    if conn:
        try:
            df = conn.read(worksheet="Lab8_Responses", ttl=5)
            c2_s1_df = df[df["Step"] == "Lab8 - Case2 Step1 Vote"]
            if not c2_s1_df.empty:
                all_resp = []
                for item in c2_s1_df["Data"]:
                    if "Resp: " in item:
                        part = item.split("Resp: ")[1]
                        all_resp.extend([x.strip() for x in part.split(",")])
                if all_resp:
                    st.bar_chart(pd.Series(all_resp).value_counts())
        except:
            pass


# ==========================================
# Case 2 - Step 2: Responsibility Matrix
# ==========================================
elif st.session_state.lab8_step == 6:
    st.title("📋 Case 2 (Step 2) — Professional Responsibility Matrix")
    st.markdown("วิเคราะห์ตาม Professional Responsibility Matrix")

    with st.form("lab8_c2_s2_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        m_patient = st.text_input("Patient - ผู้ป่วยเสี่ยงอะไร?")
        m_product = st.text_input("Product - ผลิตภัณฑ์มีความเสี่ยงอะไร?")
        m_process = st.text_input("Process - กระบวนการผลิตมีปัญหาอะไร?")
        m_law = st.text_input("Law - มีข้อกำหนดอะไรเกี่ยวข้อง?")
        m_prof = st.text_input("Profession - เภสัชกรมีหน้าที่อะไร?")
        m_org = st.text_input("Organization - โรงงานต้องการอะไร?")
        m_soc = st.text_input("Society - สังคมต้องการอะไร?")
        
        sub_c2_s2 = st.form_submit_button("ส่งผล Matrix")

        if sub_c2_s2 and group_name:
            combined_mat = f"Patient: {m_patient} | Product: {m_product} | Process: {m_process} | Law: {m_law} | Prof: {m_prof} | Org: {m_org} | Soc: {m_soc}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab8 - Case2 Step2 Matrix",
                "Data": f"[{group_name}] {combined_mat}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab8_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab8_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_c2_s2:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Responsibility Matrix")
    if conn:
        try:
            df = conn.read(worksheet="Lab8_Responses", ttl=5)
            c2_s2_df = df[df["Step"] == "Lab8 - Case2 Step2 Matrix"]
            if not c2_s2_df.empty:
                st.dataframe(c2_s2_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Case 2 - Step 3: Tension Map
# ==========================================
elif st.session_state.lab8_step == 7:
    st.title("🗺️ Case 2 (Step 3) — Ethical Tension Map")
    st.markdown("โครงสร้าง: **ช่วยผู้ป่วยจากภาวะขาดแคลนยา ↕️ ไม่ส่งมอบยาที่อาจไม่ปลอดภัย** และ **ความรับผิดชอบต่อนายจ้าง ↕️ ความรับผิดชอบต่อผู้ป่วยและวิชาชีพ**")

    with st.form("lab8_c2_s3_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        tension_c2 = st.text_area("“ความเร่งด่วนของสถานการณ์สามารถทำให้มาตรฐานความปลอดภัยลดลงได้หรือไม่? จงอธิบาย”")
        sub_c2_s3 = st.form_submit_button("ส่งผล Tension Map Case 2")

        if sub_c2_s3 and group_name and tension_c2:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab8 - Case2 Step3 Tension",
                "Data": f"[{group_name}] {tension_c2}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab8_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab8_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_c2_s3:
            st.warning("กรุณากรอกชื่อกลุ่มและคำตอบ")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Tension Map Case 2")
    if conn:
        try:
            df = conn.read(worksheet="Lab8_Responses", ttl=5)
            c2_s3_df = df[df["Step"] == "Lab8 - Case2 Step3 Tension"]
            if not c2_s3_df.empty:
                st.dataframe(c2_s3_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Case 2 - Step 4: Challenge Scenarios
# ==========================================
elif st.session_state.lab8_step == 8:
    st.title("⚔️ Case 2 (Step 4) — Challenge Scenarios")
    st.markdown("พิจารณาเงื่อนไขใหม่ทีละข้อ แล้วตอบว่าอะไรเปลี่ยนการตัดสินใจ และอะไรที่ไม่ควรเปลี่ยน")

    with st.form("lab8_c2_s4_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        c2_scen = st.selectbox(
            "เลือก Scenario ที่เปลี่ยน:",
            [
                "Scenario A: ถ้าไม่มีทางเลือกอื่นและผู้ป่วยกำลังเสียชีวิต",
                "Scenario B: ถ้าโรงงานสามารถปรับปรุงกระบวนการผลิตบางส่วนได้ แต่ยังไม่ผ่านมาตรฐานทั้งหมด",
                "Scenario C: ถ้ารัฐบาลประกาศภาวะฉุกเฉิน",
                "Scenario D: ถ้าผู้บริหารรับรองว่าจะรับผิดชอบความเสียหายทั้งหมด",
                "Scenario E: ถ้าเภสัชกรรู้ว่าการปฏิเสธอาจทำให้ตนเองตกงาน"
            ]
        )
        what_changes = st.text_input("อะไรเปลี่ยนการตัดสินใจของคุณ?")
        what_not = st.text_input("อะไรที่ไม่ควรเปลี่ยน (หลักการที่ต้องยึดไว้)?")
        
        sub_c2_s4 = st.form_submit_button("ส่งผล Challenge Case 2")

        if sub_c2_s4 and group_name:
            tag2 = c2_scen.split(":")[0]
            combined_ch2 = f"Scen: {tag2} | Changes: {what_changes} | NotChange: {what_not}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab8 - Case2 Step4 Challenge",
                "Data": f"[{group_name}] {combined_ch2}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab8_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab8_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_c2_s4:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Challenge Case 2")
    if conn:
        try:
            df = conn.read(worksheet="Lab8_Responses", ttl=5)
            c2_s4_df = df[df["Step"] == "Lab8 - Case2 Step4 Challenge"]
            if not c2_s4_df.empty:
                st.dataframe(c2_s4_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Case 2 - Step 5: Final Re-Vote
# ==========================================
elif st.session_state.lab8_step == 9:
    st.title("🎯 Case 2 (Step 5) — Final Re-Vote")
    st.markdown("### “ในสถานการณ์ที่มีความจำเป็นเร่งด่วน เภสัชกรควรยึดอะไรเป็นหลักในการตัดสินใจ?”")
    st.markdown("นำเสนอในรูปแบบ Decision + Reason + Potential Consequence")

    with st.form("lab8_c2_s5_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        fin_dec = st.text_area("Decision (การตัดสินใจขั้นสุดท้าย):")
        fin_reas = st.text_area("Reason (เหตุผลสนับสนุน):")
        fin_cons = st.text_area("Potential Consequence (ผลกระทบที่อาจตามมา):")
        
        sub_c2_s5 = st.form_submit_button("ส่ง Final Decision Case 2")

        if sub_c2_s5 and group_name:
            combined_fin = f"Decision: {fin_dec} | Reason: {fin_reas} | Consequence: {fin_cons}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab8 - Case2 Step5 Final",
                "Data": f"[{group_name}] {combined_fin}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab8_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab8_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_c2_s5:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Final Decision ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab8_Responses", ttl=5)
            c2_s5_df = df[df["Step"] == "Lab8 - Case2 Step5 Final"]
            if not c2_s5_df.empty:
                st.dataframe(c2_s5_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Final Reflection & Debrief
# ==========================================
elif st.session_state.lab8_step == 10:
    st.title("📝 Final Reflection & Instructor Debrief")
    st.markdown("สะท้อนความคิดเห็นส่วนบุคคลและสรุปบทเรียนภาพรวม")

    with st.form("lab8_reflection_form"):
        student_id = st.text_input("รหัสนิสิต (ระบุหรือไม่ระบุก็ได้):")
        
        r1 = st.text_area("1. Before (ตอนแรกฉันคิดว่า):")
        r2 = st.text_area("2. Challenge (สิ่งที่ทำให้การตัดสินใจยากคือ):")
        r3 = st.text_area("3. After (ตอนนี้ฉันคิดว่าเภสัชกรมีความรับผิดชอบต่อ):")
        
        sub_ref = st.form_submit_button("ส่ง Final Reflection Lab 8")

        if sub_ref and student_id:
            sid_val = "Anonymous" if not student_id else student_id
            combined_ref = f"Before: {r1} | Challenge: {r2} | After: {r3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab8 - Final Reflection",
                "Data": f"[{sid_val}] {combined_ref}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab8_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab8_Responses", data=updated)
                    st.success("บันทึก Reflection สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_ref:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("👨‍🏫 Instructor Debrief (แนวทางสรุปสำหรับผู้สอน)")
    st.markdown(
        """
        * **Case 1 (Access to medicine):** ใครควรมีส่วนรับผิดชอบต่อการเข้าถึงยาที่จำเป็นสำหรับโรคที่พบได้น้อย?
        * **Case 2 (Safe medicine):** เมื่อเกิดวิกฤต เภสัชกรจะรักษาความสมดุลระหว่างการเข้าถึงยากับความปลอดภัยอย่างไร?
        * **💡 Key Takeaway ภาพรวม:**  
          > *“เภสัชกรอุตสาหการไม่ได้รับผิดชอบเพียง ‘ผลิตยาให้ได้’ แต่ต้องรับผิดชอบต่อผู้ป่วย คุณภาพ ความปลอดภัย และสังคมด้วย”*
        """
    )
    
    st.markdown("---")
    st.subheader("📋 ตารางรวบรวม Final Reflection (Lab 8)")
    if conn:
        try:
            df = conn.read(worksheet="Lab8_Responses", ttl=5)
            ref_df = df[df["Step"] == "Lab8 - Final Reflection"]
            if not ref_df.empty:
                st.dataframe(ref_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass