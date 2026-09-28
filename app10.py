from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 10: News Triggers & Professional Responsibility",
    page_icon="📰",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab10_step" not in st.session_state:
    st.session_state.lab10_step = 1

# --- Sidebar เมนูด้านซ้าย ---
st.sidebar.markdown("### 📰 LAB 10 Workflow")

steps_name = {
    1: "1. News Trigger: ข่าวที่ 1 (ยาขาดแคลน)",
    2: "2. News Trigger: ข่าวที่ 2 (การโฆษณา)",
    3: "3. News Trigger: ข่าวที่ 3 (Social Media)",
    4: "4. Change One Factor",
    5: "5. Whose Responsibility?",
    6: "6. Final Challenge (Framework)",
    7: "7. Final Reflection (Lab 10)",
}

current_index = list(steps_name.keys()).index(st.session_state.lab10_step)

selected_step_name = st.sidebar.radio(
    "เลือกกิจกรรม LAB 10:",
    list(steps_name.values()),
    index=current_index,
    key="lab10_menu_selection",
)

for s_num, s_title in steps_name.items():
    if s_title == selected_step_name:
        st.session_state.lab10_step = s_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อกิจกรรมด้านบนเพื่อเปลี่ยนหน้า")


# ==========================================
# 1. News Trigger: ข่าวที่ 1 — ยาขาดแคลน
# ==========================================
if st.session_state.lab10_step == 1:
    st.title("📰 News Trigger: ข่าวที่ 1 — ยาขาดแคลน / การจัดสรรยา")
    st.info(
        "**สถานการณ์ย่อ:** ยาชนิดหนึ่งขาดแคลน ทำให้โรงพยาบาลหรือร้านยาบางแห่งมีจำนวนยาไม่เพียงพอต่อความต้องการ ขณะเดียวกันผู้ป่วยบางรายจำเป็นต้องได้รับยาอย่างต่อเนื่อง ขณะที่ผู้ป่วยรายอื่นก็มีความจำเป็นเช่นกัน"
    )

    with st.form("lab10_news1_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        st.markdown("### คำถาม 1: “จากข่าวนี้ ใครควรรับผิดชอบมากที่สุด?”")
        vote_choice = st.radio(
            "เลือกตัวเลือก:",
            [
                "A. เภสัชกร",
                "B. ผู้ประกอบการ/องค์กร",
                "C. ผู้ประกอบวิชาชีพอื่น",
                "D. หน่วยงานรัฐ",
                "E. ผู้บริโภค/ประชาชน",
                "F. ทุกฝ่ายร่วมกัน"
            ],
            key="n1_vote"
        )
        
        st.markdown("---")
        st.markdown("### คำถาม 2: Stakeholder Map & Analysis")
        st.markdown("วิเคราะห์ผลกระทบ (ผู้ป่วย, ประชาชน, เภสัชกร, องค์กร, รัฐ, วิชาชีพ) และตอบคำถาม:")
        stake_ans = st.text_area("“ถ้าผลประโยชน์ของแต่ละฝ่ายไม่ตรงกัน เราควรให้ความสำคัญกับใคร และเพราะอะไร?”", key="n1_stake")
        
        st.markdown("---")
        st.markdown("### คำถาม 3: Individual → Profession → Society")
        i_lvl = st.text_area("ระดับที่ 1 (Individual): เภสัชกรควรทำอะไร?", key="n1_i")
        p_lvl = st.text_area("ระดับที่ 2 (Profession): ถ้าเภสัชกรหลายคนทำแบบเดียวกัน จะเกิดอะไรกับวิชาชีพ?", key="n1_p")
        s_lvl = st.text_area("ระดับที่ 3 (Society): ถ้าสิ่งนี้เกิดขึ้นในสังคมวงกว้าง จะเกิดผลอะไร?", key="n1_s")
        
        st.markdown("---")
        st.markdown("### 💊 คำถามเฉพาะข่าว 1: “ถ้ายามีไม่พอสำหรับทุกคน เราควรจัดสรรอย่างไร?”")
        st.markdown("จัดลำดับความสำคัญ (1-4 โดยระบุอันดับหรืออธิบายการจัดลำดับ):")
        allocation_ans = st.text_area(
            "จัดลำดับ (ผู้ป่วยฉุกเฉิน / ผู้ป่วยใช้ยาต่อเนื่อง / ผู้ป่วยเสี่ยงสูง / ผู้ป่วยใช้ยาทางเลือกได้):",
            key="n1_alloc"
        )
        
        sub_n1 = st.form_submit_button("ส่งคำตอบ ข่าวที่ 1")

        if sub_n1 and student_id:
            combined_n1 = f"Vote: {vote_choice} | Stake: {stake_ans} | I:{i_lvl}|P:{p_lvl}|S:{s_lvl} | Alloc: {allocation_ans}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab10 - News 1 Shortage",
                "Data": f"[{student_id}] {combined_n1}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab10_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab10_Responses", data=updated)
                    st.success("บันทึกคำตอบข่าวที่ 1 สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_n1:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผล Quick Vote (ข่าวที่ 1)")
    if conn:
        try:
            df = conn.read(worksheet="Lab10_Responses", ttl=5)
            n1_df = df[df["Step"] == "Lab10 - News 1 Shortage"]
            if not n1_df.empty:
                votes = n1_df["Data"].apply(lambda x: x.split("Vote: ")[1].split(" |")[0].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
            else:
                st.info("ยังไม่มีข้อมูลผลโหวต")
        except:
            pass


# ==========================================
# 2. News Trigger: ข่าวที่ 2 — การโฆษณาผลิตภัณฑ์สุขภาพ
# ==========================================
elif st.session_state.lab10_step == 2:
    st.title("📰 News Trigger: ข่าวที่ 2 — การโฆษณาผลิตภัณฑ์สุขภาพกับความรับผิดชอบของเภสัชกร")
    st.info(
        "**สถานการณ์ย่อ:** ผลิตภัณฑ์สุขภาพชนิดหนึ่งได้รับความนิยมอย่างมากในสื่อออนไลน์ มีการใช้ข้อความที่ทำให้ผู้บริโภคเข้าใจว่าผลิตภัณฑ์มีประสิทธิผลสูง เภสัชกรที่เกี่ยวข้องกับองค์กรพบว่าข้อมูลบางส่วนอาจทำให้ผู้บริโภคเข้าใจเกินกว่าหลักฐานที่มีอยู่"
    )

    with st.form("lab10_news2_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        st.markdown("### คำถาม 1: “จากข่าวนี้ ใครควรรับผิดชอบมากที่สุด?”")
        vote_choice = st.radio(
            "เลือกตัวเลือก:",
            [
                "A. เภสัชกร",
                "B. ผู้ประกอบการ/องค์กร",
                "C. ผู้ประกอบวิชาชีพอื่น",
                "D. หน่วยงานรัฐ",
                "E. ผู้บริโภค/ประชาชน",
                "F. ทุกฝ่ายร่วมกัน"
            ],
            key="n2_vote"
        )
        
        st.markdown("---")
        st.markdown("### คำถาม 2 & 3: Stakeholder Map & 3 Levels Analysis")
        stake_ans = st.text_area("Stakeholder Map: ใครได้/เสียอะไร และควรให้ความสำคัญกับใคร?", key="n2_stake")
        lvl_ans = st.text_area("วิเคราะห์ 3 ระดับ (Individual → Profession → Society):", key="n2_lvl")
        
        st.markdown("---")
        st.markdown("### 📢 คำถามเฉพาะข่าว 2: “เภสัชกรควรทำอย่างไรเมื่อความรับผิดชอบต่อองค์กรอาจขัดกับความรับผิดชอบต่อผู้บริโภค?”")
        specific_n2 = st.text_area("พิมพ์แนวทางการตัดสินใจและเหตุผลของคุณ:", key="n2_spec")
        
        sub_n2 = st.form_submit_button("ส่งคำตอบ ข่าวที่ 2")

        if sub_n2 and student_id:
            combined_n2 = f"Vote: {vote_choice} | Stake: {stake_ans} | Levels: {lvl_ans} | Specific: {specific_n2}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab10 - News 2 Advertising",
                "Data": f"[{student_id}] {combined_n2}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab10_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab10_Responses", data=updated)
                    st.success("บันทึกคำตอบข่าวที่ 2 สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_n2:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผล Quick Vote (ข่าวที่ 2)")
    if conn:
        try:
            df = conn.read(worksheet="Lab10_Responses", ttl=5)
            n2_df = df[df["Step"] == "Lab10 - News 2 Advertising"]
            if not n2_df.empty:
                votes = n2_df["Data"].apply(lambda x: x.split("Vote: ")[1].split(" |")[0].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
            else:
                st.info("ยังไม่มีข้อมูลผลโหวต")
        except:
            pass


# ==========================================
# 3. News Trigger: ข่าวที่ 3 — Social Media
# ==========================================
elif st.session_state.lab10_step == 3:
    st.title("📰 News Trigger: ข่าวที่ 3 — เภสัชกรกับข้อมูลสุขภาพบน Social Media")
    st.info(
        "**สถานการณ์ย่อ:** เภสัชกรคนหนึ่งทำคอนเทนต์ให้ความรู้เรื่องยาและสุขภาพบน Social Media มีผู้ติดตามจำนวนมาก เนื้อหาช่วยให้ประชาชนเข้าใจเรื่องสุขภาพมากขึ้น แต่เมื่อมีผู้ติดตามนำคำแนะนำไปใช้กับตนเองโดยไม่ได้ปรึกษาผู้เชี่ยวชาญ ความรับผิดชอบของเภสัชกรควรอยู่ตรงไหน?"
    )

    with st.form("lab10_news3_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        st.markdown("### คำถาม 1: “จากข่าวนี้ ใครควรรับผิดชอบมากที่สุด?”")
        vote_choice = st.radio(
            "เลือกตัวเลือก:",
            [
                "A. เภสัชกร",
                "B. ผู้ประกอบการ/องค์กร",
                "C. ผู้ประกอบวิชาชีพอื่น",
                "D. หน่วยงานรัฐ",
                "E. ผู้บริโภค/ประชาชน",
                "F. ทุกฝ่ายร่วมกัน"
            ],
            key="n3_vote"
        )
        
        st.markdown("---")
        st.markdown("### คำถาม 2 & 3: Stakeholder Map & 3 Levels Analysis")
        stake_ans = st.text_area("Stakeholder Map และการให้น้ำหนักความสำคัญ:", key="n3_stake")
        lvl_ans = st.text_area("วิเคราะห์ 3 ระดับ (Individual → Profession → Society):", key="n3_lvl")
        
        st.markdown("---")
        st.markdown("### 📱 คำถามเฉพาะข่าว 3: “การให้ความรู้ประชาชนผ่าน Social Media เป็นเพียงการให้ข้อมูล หรือเป็นความรับผิดชอบทางวิชาชีพด้วย?”")
        specific_n3 = st.text_area("พิมพ์ความเห็นและการวิเคราะห์ของคุณ:", key="n3_spec")
        
        sub_n3 = st.form_submit_button("ส่งคำตอบ ข่าวที่ 3")

        if sub_n3 and student_id:
            combined_n3 = f"Vote: {vote_choice} | Stake: {stake_ans} | Levels: {lvl_ans} | Specific: {specific_n3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab10 - News 3 SocialMedia",
                "Data": f"[{student_id}] {combined_n3}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab10_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab10_Responses", data=updated)
                    st.success("บันทึกคำตอบข่าวที่ 3 สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_n3:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผล Quick Vote (ข่าวที่ 3)")
    if conn:
        try:
            df = conn.read(worksheet="Lab10_Responses", ttl=5)
            n3_df = df[df["Step"] == "Lab10 - News 3 SocialMedia"]
            if not n3_df.empty:
                votes = n3_df["Data"].apply(lambda x: x.split("Vote: ")[1].split(" |")[0].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
            else:
                st.info("ยังไม่มีข้อมูลผลโหวต")
        except:
            pass


# ==========================================
# 4. Change One Factor
# ==========================================
elif st.session_state.lab10_step == 4:
    st.title("🔄 Change One Factor")
    st.markdown("### ข่าว: “เภสัชกรให้ข้อมูลเกี่ยวกับยาแก่ผู้ป่วยไม่ครบถ้วน”")

    with st.form("lab10_factor_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        case_cond = st.selectbox(
            "เลือกกรณีการเปลี่ยนปัจจัย:",
            [
                "กรณี A: ผู้ป่วยเป็นคนทั่วไป",
                "กรณี B: ผู้ป่วยเป็นเด็ก",
                "กรณี C: ผู้ป่วยมีความเสี่ยงสูง",
                "กรณี D: เภสัชกรมีเวลาจำกัดมาก",
                "กรณี E: การให้ข้อมูลนั้นทำให้ร้านเสียรายได้"
            ]
        )
        
        decision_change = st.radio("“เมื่อเปลี่ยนข้อมูลเพียงข้อเดียว การตัดสินใจของคุณเปลี่ยนหรือไม่?”", ["เปลี่ยน", "ไม่เปลี่ยน", "ปรับเปลี่ยนบางส่วน"])
        reason_text = st.text_area("อธิบายเหตุผลประกอบ:")
        
        sub_fact = st.form_submit_button("ส่งผล Change One Factor")

        if sub_fact and group_name:
            tag = case_cond.split(":")[0]
            combined_f = f"Cond: {tag} | Decision: {decision_change} | Reason: {reason_text}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab10 - Change One Factor",
                "Data": f"[{group_name}] {combined_f}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab10_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab10_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_fact:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Change One Factor")
    if conn:
        try:
            df = conn.read(worksheet="Lab10_Responses", ttl=5)
            f_df = df[df["Step"] == "Lab10 - Change One Factor"]
            if not f_df.empty:
                st.dataframe(f_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 5. Whose Responsibility?
# ==========================================
elif st.session_state.lab10_step == 5:
    st.title("👥 Whose Responsibility?")
    st.markdown("### สถานการณ์: “ยาปฏิชีวนะถูกใช้ไม่เหมาะสมในชุมชน”")

    with st.form("lab10_resp_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        p_resp = st.text_area("1. Primary responsibility (ความรับผิดชอบหลักอยู่ที่ใคร):")
        s_resp = st.text_area("2. Shared responsibility (ความรับผิดชอบร่วมกันมีใครบ้าง):")
        sys_resp = st.text_area("3. System responsibility (ความรับผิดชอบเชิงระบบระดับมหภาค):")
        
        discussion_q = st.text_area("“การมีความรับผิดชอบร่วมกัน หมายความว่าเภสัชกรไม่มีความรับผิดชอบหรือไม่? จงอธิบาย”:")
        
        sub_resp = st.form_submit_button("ส่งผล Whose Responsibility")

        if sub_resp and group_name:
            combined_r = f"Primary: {p_resp} | Shared: {s_resp} | System: {sys_resp} | Discuss: {discussion_q}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab10 - Whose Responsibility",
                "Data": f"[{group_name}] {combined_r}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab10_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab10_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_resp:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Whose Responsibility")
    if conn:
        try:
            df = conn.read(worksheet="Lab10_Responses", ttl=5)
            r_df = df[df["Step"] == "Lab10 - Whose Responsibility"]
            if not r_df.empty:
                st.dataframe(r_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 6. Final Challenge (Framework)
# ==========================================
elif st.session_state.lab10_step == 6:
    st.title("🏆 Final Challenge — Case: “ความน่าเชื่อถือของวิชาชีพ”")
    st.info(
        "**สถานการณ์:** มีข้อมูลเกี่ยวกับผลิตภัณฑ์สุขภาพชนิดหนึ่งที่กำลังได้รับความนิยมในสังคม ประชาชนจำนวนมากเชื่อว่ามีประโยชน์จากข้อมูลออนไลน์ แต่เภสัชกรพบว่าข้อมูลบางส่วนยังไม่มีหลักฐานเพียงพอ การออกมาให้อย่างระมัดระวังอาจขัดแย้งกับผู้เกี่ยวข้องและกระทบองค์กร เภสัชกรควรตัดสินใจอย่างไร?"
    )
    st.markdown("วิเคราะห์ตาม Framework จาก Labs 1–9: **FACTS → STAKEHOLDERS → ETHICAL ISSUE → VALUES / RESPONSIBILITY → RULES → OPTIONS → CONSEQUENCES → DECISION & JUSTIFICATION**")

    with st.form("lab10_final_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        fc1 = st.text_input("1. FACTS (ข้อเท็จจริง):")
        fc2 = st.text_input("2. STAKEHOLDERS (ผู้มีส่วนได้เสีย):")
        fc3 = st.text_input("3. ETHICAL ISSUE (ปัญหาจริยธรรม):")
        fc4 = st.text_input("4. VALUES / RESPONSIBILITY (คุณค่าและหน้าที่):")
        fc5 = st.text_input("5. RULES (กฎหมายและมาตรฐาน):")
        fc6 = st.text_input("6. OPTIONS (ทางเลือก):")
        fc7 = st.text_input("7. CONSEQUENCES (ผลกระทบ):")
        fc8 = st.text_area("8. DECISION & JUSTIFICATION (การตัดสินใจและเหตุผลสนับสนุน):")
        
        sub_fc = st.form_submit_button("ส่ง Final Challenge Framework")

        if sub_fc and group_name:
            combined_fc = f"F1:{fc1}|F2:{fc2}|F3:{fc3}|F4:{fc4}|F5:{fc5}|F6:{fc6}|F7:{fc7}|F8:{fc8}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab10 - Final Challenge",
                "Data": f"[{group_name}] {combined_fc}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab10_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab10_Responses", data=updated)
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
            df = conn.read(worksheet="Lab10_Responses", ttl=5)
            fc_df = df[df["Step"] == "Lab10 - Final Challenge"]
            if not fc_df.empty:
                st.dataframe(fc_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 7. Final Reflection (Lab 10)
# ==========================================
elif st.session_state.lab10_step == 7:
    st.title("🎯 Final Reflection (Lab 10 - ปิดรายวิชาสมบูรณ์)")
    st.markdown("สะท้อนความคิดเห็นส่วนบุคคล 3 ข้อสุดท้าย")

    with st.form("lab10_reflection_form"):
        student_id = st.text_input("รหัสนิสิต (ระบุหรือไม่ระบุก็ได้):")
        
        r1 = st.text_area("1. Before (ก่อนเรียน Lab นี้ ฉันมองความรับผิดชอบของเภสัชกรต่อสังคมอย่างไร):")
        r2 = st.text_area("2. Now (ตอนนี้ฉันคิดว่าความรับผิดชอบของเภสัชกรต่อสังคมคืออะไร):")
        r3 = st.text_area("3. Next (เมื่อเป็นเภสัชกร ฉันจะทำอะไรเพื่อรักษาความไว้วางใจของสังคมต่อวิชาชีพ):")
        
        sub_ref = st.form_submit_button("ส่ง Final Reflection สมบูรณ์")

        if sub_ref and student_id:
            sid_val = "Anonymous" if not student_id else student_id
            combined_ref = f"Before: {r1} | Now: {r2} | Next: {r3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab10 - Final Reflection",
                "Data": f"[{sid_val}] {combined_ref}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab10_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab10_Responses", data=updated)
                    st.success("บันทึก Final Reflection สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_ref:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางรวบรวม Final Reflection ปิดรายวิชา")
    if conn:
        try:
            df = conn.read(worksheet="Lab10_Responses", ttl=5)
            ref_df = df[df["Step"] == "Lab10 - Final Reflection"]
            if not ref_df.empty:
                st.dataframe(ref_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass