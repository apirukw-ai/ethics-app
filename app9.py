from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 9: Synthesis & Professional Framework",
    page_icon="🎓",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab9_step" not in st.session_state:
    st.session_state.lab9_step = 1

# --- Sidebar เมนูด้านซ้าย ---
st.sidebar.markdown("### 🎓 LAB 9 Workflow")

steps_name = {
    1: "Opening: Context Vote",
    2: "Activity 1: Ethical Reasoning Map",
    3: "Activity 2 & 3: What's Same & Diff",
    4: "Activity 4: Transfer Case (A/B/C)",
    5: "Activity 5: Challenge (Peer Q&A)",
    6: "Activity 6: Your Framework",
    7: "Final Challenge (Case + 3 Rounds)",
    8: "Final Reflection",
}

current_index = list(steps_name.keys()).index(st.session_state.lab9_step)

selected_step_name = st.sidebar.radio(
    "เลือกกิจกรรม LAB 9:",
    list(steps_name.values()),
    index=current_index,
    key="lab9_menu_selection",
)

for s_num, s_title in steps_name.items():
    if s_title == selected_step_name:
        st.session_state.lab9_step = s_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อกิจกรรมด้านบนเพื่อเปลี่ยนหน้า")


# ==========================================
# Opening: Context Vote
# ==========================================
if st.session_state.lab9_step == 1:
    st.title("🗳️ Opening: Context Vote")
    st.markdown("### “ถ้าเป็นปัญหาเดียวกัน แต่เปลี่ยนบริบทจากร้านยา → โรงพยาบาล → โรงงานยา เราควรตัดสินใจเหมือนเดิมหรือไม่?”")

    with st.form("lab9_open_form"):
        student_id = st.text_input("รหัสนิสิต:")
        vote_choice = st.radio(
            "เลือกคำตอบของคุณ:",
            ["ควรเหมือนเดิม", "ควรต่างกัน", "ขึ้นอยู่กับสถานการณ์"]
        )
        sub_op = st.form_submit_button("ส่งผลโหวต Opening")

        if sub_op and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab9 - Opening Vote",
                "Data": f"[{student_id}] Vote: {vote_choice}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab9_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab9_Responses", data=updated)
                    st.success("บันทึกผลโหวตสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_op:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผล Vote (Opening)")
    if conn:
        try:
            df = conn.read(worksheet="Lab9_Responses", ttl=5)
            op_df = df[df["Step"] == "Lab9 - Opening Vote"]
            if not op_df.empty:
                votes = op_df["Data"].apply(lambda x: x.split("Vote: ")[1].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
            else:
                st.info("ยังไม่มีข้อมูลผลโหวต")
        except:
            pass


# ==========================================
# Activity 1 — Ethical Reasoning Map
# ==========================================
elif st.session_state.lab9_step == 2:
    st.title("🗺️ Activity 1 — Ethical Reasoning Map")
    st.markdown("ย้อนกลับไปที่ Lab 6–8 แล้วค้นหา 'รูปแบบร่วม' เปรียบเทียบระหว่าง 3 บริบท")

    with st.form("lab9_act1_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        
        m_affected = st.text_area("1. ใครได้รับผลกระทบ? (Community / Hospital / Industry)")
        m_issue = st.text_area("2. ปัญหาจริยธรรมหลักคืออะไร?")
        m_values = st.text_area("3. หลักจริยธรรมสำคัญคืออะไร?")
        m_rules = st.text_area("4. กฎหมาย/มาตรฐานที่เกี่ยวข้องมีอะไรบ้าง?")
        m_options = st.text_area("5. ทางเลือกในการแก้ปัญหาคืออะไร?")
        m_risks = st.text_area("6. ความเสี่ยงคืออะไร?")
        m_resp = st.text_area("7. ใครต้องรับผิดชอบ?")
        
        sub_a1 = st.form_submit_button("ส่งผล Ethical Reasoning Map")

        if sub_a1 and group_name:
            combined_map = f"Affected: {m_affected} | Issue: {m_issue} | Values: {m_values} | Rules: {m_rules} | Options: {m_options} | Risks: {m_risks} | Resp: {m_resp}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab9 - Act 1 Reasoning Map",
                "Data": f"[{group_name}] {combined_map}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab9_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab9_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a1:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Ethical Reasoning Map")
    if conn:
        try:
            df = conn.read(worksheet="Lab9_Responses", ttl=5)
            p1_df = df[df["Step"] == "Lab9 - Act 1 Reasoning Map"]
            if not p1_df.empty:
                st.dataframe(p1_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Activity 2 & 3 — What's Same & Diff
# ==========================================
elif st.session_state.lab9_step == 3:
    st.title("⚖️ Activity 2 & 3 — อะไรเหมือนกัน และอะไรเปลี่ยนตามบริบท?")
    st.markdown("วิเคราะห์แก่นคิดที่เหมือนกัน และอำนาจการตัดสินใจที่เปลี่ยนไปตามบริบท")

    with st.form("lab9_act23_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        same_ans = st.text_area("Activity 2: จาก Lab 6–8 มีหลักคิดอะไรที่เหมือนกัน แม้บริบทจะแตกต่างกัน?")
        diff_ans = st.text_area("Activity 3: ทำไมการตัดสินใจของเภสัชกรในแต่ละสาขา (Community / Hospital / Industry) จึงอาจแตกต่างกัน? และใครมีอำนาจตัดสินใจ/ใครได้รับผลกระทบ?")
        
        sub_a23 = st.form_submit_button("ส่งคำตอบ Act 2 & 3")

        if sub_a23 and group_name:
            combined_23 = f"Same: {same_ans} | Diff: {diff_ans}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab9 - Act 2 & 3 Same Diff",
                "Data": f"[{group_name}] {combined_23}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab9_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab9_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a23:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Activity 2 & 3")
    if conn:
        try:
            df = conn.read(worksheet="Lab9_Responses", ttl=5)
            p23_df = df[df["Step"] == "Lab9 - Act 2 & 3 Same Diff"]
            if not p23_df.empty:
                st.dataframe(p23_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Activity 4 — Transfer Case
# ==========================================
elif st.session_state.lab9_step == 4:
    st.title("🔄 Activity 4 — Transfer Case")
    st.markdown("กรณีศึกษา: ยาที่ผู้ป่วยต้องการมีราคาแพง มีทางเลือกราคาถูกกว่าแต่ข้อมูลคุณภาพต่างกัน")

    with st.form("lab9_act4_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        group_role = st.selectbox(
            "เลือกบทบาทกลุ่มของคุณ:",
            [
                "Group A: เภสัชกรชุมชน (Community)",
                "Group B: เภสัชกรโรงพยาบาล (Hospital)",
                "Group C: เภสัชกรในโรงงานยา (Industry)"
            ]
        )
        
        q1 = st.text_input("1. คุณต้องพิจารณาอะไรบ้าง?")
        q2 = st.text_input("2. ใครได้รับผลกระทบ?")
        q3 = st.text_input("3. คุณมีหน้าที่อะไร?")
        q4 = st.text_input("4. ทางเลือกมีอะไรบ้าง?")
        q5 = st.text_area("5. คุณตัดสินใจอย่างไร และเพราะอะไร?")
        
        sub_a4 = st.form_submit_button("ส่งผล Transfer Case")

        if sub_a4 and group_name:
            role_tag = group_role.split(":")[0]
            combined_tc = f"Role: {role_tag} | Consider: {q1} | Affected: {q2} | Duty: {q3} | Options: {q4} | Decision: {q5}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab9 - Act 4 Transfer Case",
                "Data": f"[{group_name}] {combined_tc}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab9_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab9_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a4:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Transfer Case แยกตามบทบาท")
    if conn:
        try:
            df = conn.read(worksheet="Lab9_Responses", ttl=5)
            p4_df = df[df["Step"] == "Lab9 - Act 4 Transfer Case"]
            if not p4_df.empty:
                st.dataframe(p4_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Activity 5 — Challenge (Peer Q&A)
# ==========================================
elif st.session_state.lab9_step == 5:
    st.title("⚔️ Activity 5 — Challenge (Peer Q&A)")
    st.markdown("ใช้คำถามท้าทาย 3 แบบ: **WHY?**, **WHAT IF?**, **WHO?**")

    with st.form("lab9_act5_form"):
        group_name = st.text_input("ชื่อกลุ่มของคุณ (ผู้ตั้งคำถาม):")
        target_group = st.text_input("กลุ่มที่ถูกท้าทาย (เช่น Group A):")
        
        ch_type = st.selectbox(
            "ประเภทคำถาม Challenge:",
            [
                "WHY? (ทำไมคุณให้ความสำคัญกับปัจจัยนี้มากกว่าอีกปัจจัย?)",
                "WHAT IF? (ถ้าข้อมูลนี้เปลี่ยน คุณยังตัดสินใจเหมือนเดิมหรือไม่?)",
                "WHO? (ถ้าคุณเป็นผู้ป่วย/ญาติ/ผู้บริหาร/เภสัชกรอีกฝ่าย คุณจะมองเรื่องนี้อย่างไร?)"
            ]
        )
        ch_q = st.text_area("พิมพ์ข้อความคำถามท้าทาย:")
        
        sub_a5 = st.form_submit_button("ส่งคำถาม Challenge")

        if sub_a5 and group_name and target_group and ch_q:
            combined_ch = f"Target: {target_group} | Type: {ch_type} | Q: {ch_q}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab9 - Act 5 Challenge QnA",
                "Data": f"[{group_name}] {combined_ch}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab9_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab9_Responses", data=updated)
                    st.success("ส่งคำถามสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a5:
            st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")

    st.markdown("---")
    st.subheader("📋 ตารางรายการคำถาม Challenge ทั้งหมด")
    if conn:
        try:
            df = conn.read(worksheet="Lab9_Responses", ttl=5)
            p5_df = df[df["Step"] == "Lab9 - Act 5 Challenge QnA"]
            if not p5_df.empty:
                st.dataframe(p5_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Activity 6 — Your Framework
# ==========================================
elif st.session_state.lab9_step == 6:
    st.title("🛠️ Activity 6 — สร้าง “Ethical Reasoning Framework” ของนิสิต")
    st.markdown("ออกแบบ 5–7 ขั้นตอนที่เภสัชกรควรใช้เมื่อเจอปัญหาจริยธรรม (ดึงจาก Lab 1–8)")

    with st.form("lab9_act6_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        f_steps = st.text_area(
            "พิมพ์ขั้นตอน Framework ของกลุ่มคุณ (เช่น 1. Facts 2. Stakeholders 3. Ethical Issue 4. Rules 5. Options 6. Consequences 7. Decision):"
        )
        
        sub_a6 = st.form_submit_button("ส่ง Framework ของกลุ่ม")

        if sub_a6 and group_name and f_steps:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab9 - Act 6 Framework",
                "Data": f"[{group_name}] {f_steps}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab9_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab9_Responses", data=updated)
                    st.success("บันทึก Framework สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a6:
            st.warning("กรุณากรอกชื่อกลุ่มและขั้นตอน Framework")

    st.markdown("---")
    st.subheader("📋 ตารางแสดง Framework ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab9_Responses", ttl=5)
            p6_df = df[df["Step"] == "Lab9 - Act 6 Framework"]
            if not p6_df.empty:
                st.dataframe(p6_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Final Challenge (Case + 3 Rounds)
# ==========================================
elif st.session_state.lab9_step == 7:
    st.title("🏆 Final Challenge — Case: “ยาที่เหลืออยู่”")
    st.markdown("วิเคราะห์เคสตาม Framework 8 ขั้นตอน พร้อมรับมือกับข้อมูลใหม่ที่เพิ่มขึ้น 3 รอบ")

    with st.form("lab9_final_case_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        st.markdown("---")
        st.markdown("#### 📝 กรอบการวิเคราะห์ตาม Framework 8 ขั้นตอน")
        fc1 = st.text_input("1. FACTS (เรารู้อะไรแล้ว / ขาดอะไร):")
        fc2 = st.text_input("2. STAKEHOLDERS (ใครได้รับผลกระทบ):")
        fc3 = st.text_input("3. ETHICAL ISSUE (ปัญหาจริยธรรมคืออะไร):")
        fc4 = st.text_input("4. VALUES / RESPONSIBILITIES (คุณค่า/หน้าที่อะไรขัดกัน):")
        fc5 = st.text_input("5. RULES / PROFESSIONAL DUTY (กฎหมาย/มาตรฐานวิชาชีพ):")
        fc6 = st.text_input("6. OPTIONS (ทางเลือกมีอะไรบ้าง):")
        fc7 = st.text_input("7. CONSEQUENCES (ผลดี-ผลเสียแต่ละทางเลือก):")
        fc8 = st.text_input("8. DECISION (จะเลือกทางใดและเหตุผล):")
        
        st.markdown("---")
        st.markdown("#### ⚡ การทดสอบด้วยข้อมูลใหม่ (Challenges)")
        round1_ans = st.text_area("ข้อมูลใหม่ 1: ถ้าผู้ป่วยไม่ได้ยาต่อเนื่องอาจเกิดผลเสียต่อสุขภาพ -> การตัดสินใจเปลี่ยนหรือไม่?")
        round2_ans = st.text_area("ข้อมูลใหม่ 2: ถ้าแพทย์สามารถพิจารณาทางเลือกอื่นได้แต่ต้องติดต่อแพทย์ก่อน -> การตัดสินใจเปลี่ยนหรือไม่?")
        round3_ans = st.text_area("ข้อมูลใหม่ 3: ถ้าผู้ป่วยมีสิทธิช่วยเหลือค่าใช้จ่ายบางส่วน -> เปลี่ยนใจหรือไม่ และ Framework ช่วยบอกให้อะไรควรเปลี่ยน/ไม่ควรเปลี่ยนอย่างไร?")
        
        sub_fc = st.form_submit_button("ส่งผล Final Challenge")

        if sub_fc and group_name:
            combined_fc = f"F1:{fc1}|F2:{fc2}|F3:{fc3}|F4:{fc4}|F5:{fc5}|F6:{fc6}|F7:{fc7}|F8:{fc8} || R1:{round1_ans}|R2:{round2_ans}|R3:{round3_ans}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab9 - Final Challenge",
                "Data": f"[{group_name}] {combined_fc}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab9_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab9_Responses", data=updated)
                    st.success("บันทึก Final Challenge สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_fc:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Final Challenge ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab9_Responses", ttl=5)
            fc_df = df[df["Step"] == "Lab9 - Final Challenge"]
            if not fc_df.empty:
                st.dataframe(fc_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Final Reflection (Lab 9)
# ==========================================
elif st.session_state.lab9_step == 8:
    st.title("🎯 Final Reflection (Lab 9 - ปิดรายวิชา)")
    st.markdown("สะท้อนมุมมองภาพรวมตลอดรายวิชา Ethics")

    with st.form("lab9_reflection_form"):
        student_id = st.text_input("รหัสนิสิต (ระบุหรือไม่ระบุก็ได้):")
        
        r1 = st.text_area("1. ก่อนเรียน Labs 1–8 ฉันคิดว่าจริยธรรมคือ:")
        r2 = st.text_area("2. ตอนนี้ฉันคิดว่าการตัดสินใจทางจริยธรรมคือ:")
        r3 = st.text_area("3. เมื่อเจอปัญหาจริยธรรมในวิชาชีพ ฉันจะเริ่มจาก:")
        
        sub_ref = st.form_submit_button("ส่ง Final Reflection รายวิชา")

        if sub_ref and student_id:
            sid_val = "Anonymous" if not student_id else student_id
            combined_ref = f"Before: {r1} | Now: {r2} | Next: {r3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab9 - Final Reflection",
                "Data": f"[{sid_val}] {combined_ref}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab9_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab9_Responses", data=updated)
                    st.success("บันทึก Final Reflection สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_ref:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางรวบรวม Final Reflection ภาพรวมรายวิชา")
    if conn:
        try:
            df = conn.read(worksheet="Lab9_Responses", ttl=5)
            ref_df = df[df["Step"] == "Lab9 - Final Reflection"]
            if not ref_df.empty:
                st.dataframe(ref_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass