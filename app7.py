from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 7: Competing Obligations & Crisis",
    page_icon="⚖️",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab7_step" not in st.session_state:
    st.session_state.lab7_step = 1

# --- Sidebar เมนูด้านซ้าย ---
st.sidebar.markdown("### ⚖️ LAB 7 Workflow")

steps_name = {
    1: "Case 1 - Step 1: First Vote",
    2: "Case 1 - Step 2: Analyze",
    3: "Case 1 - Step 3: Discuss",
    4: "Case 1 - Step 4 & 5: Change Factor & Re-Vote",
    5: "Case 2 - Step 1: First Vote",
    6: "Case 2 - Step 2: Tension Map",
    7: "Case 2 - Step 3: Decision Ladder",
    8: "Case 2 - Step 4: Challenge",
    9: "Case 2 - Step 5: Final Re-Vote",
    10: "Final Reflection (Lab 7)",
}

current_index = list(steps_name.keys()).index(st.session_state.lab7_step)

selected_step_name = st.sidebar.radio(
    "เลือกกิจกรรม LAB 7:",
    list(steps_name.values()),
    index=current_index,
    key="lab7_menu_selection",
)

for s_num, s_title in steps_name.items():
    if s_title == selected_step_name:
        st.session_state.lab7_step = s_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อกิจกรรมด้านบนเพื่อเปลี่ยนหน้า")


# ==========================================
# Case 1 - Step 1: First Vote
# ==========================================
if st.session_state.lab7_step == 1:
    st.title("🗳️ Case 1 (Step 1) — First Vote")
    st.markdown("### เมื่อผู้ป่วยสองคนต้องการความช่วยเหลือพร้อมกัน: “ในสถานการณ์นี้ อะไรควรมาก่อน และอะไรควรทำต่อไป?”")

    with st.form("lab7_c1_s1_form"):
        student_id = st.text_input("รหัสนิสิต:")
        vote_choice = st.radio(
            "ตอนนี้เภสัชกรควรทำอะไร?",
            [
                "A. รักษาสัญญากับนางมาดีและพูดคุยกับเธอก่อน",
                "B. หยุดการพูดคุยและให้บริการนางอุไรทันที",
                "C. อธิบายสถานการณ์กับนางมาดี แล้วช่วยนางอุไรก่อน",
                "D. ขอความช่วยเหลือจากเภสัชกร/บุคลากรคนอื่น",
                "E. มีวิธีอื่นที่เหมาะสมกว่า"
            ]
        )
        sub_s1 = st.form_submit_button("ส่งผลโหวต Case 1")

        if sub_s1 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab7 - Case1 Step1 Vote",
                "Data": f"[{student_id}] Vote: {vote_choice}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab7_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab7_Responses", data=updated)
                    st.success("บันทึกผลโหวตสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_s1:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผล Vote (Case 1 - Step 1)")
    if conn:
        try:
            df = conn.read(worksheet="Lab7_Responses", ttl=5)
            c1_s1_df = df[df["Step"] == "Lab7 - Case1 Step1 Vote"]
            if not c1_s1_df.empty:
                votes = c1_s1_df["Data"].apply(lambda x: x.split("Vote: ")[1].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
            else:
                st.info("ยังไม่มีข้อมูลผลโหวต")
        except:
            pass


# ==========================================
# Case 1 - Step 2: Analyze
# ==========================================
elif st.session_state.lab7_step == 2:
    st.title("📋 Case 1 (Step 2) — Analyze")
    st.markdown("แต่ละกลุ่มร่วมกันวิเคราะห์ตามประเด็นด้านล่างนี้")

    with st.form("lab7_c1_s2_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        
        c1 = st.text_area("1. What happened? (เกิดอะไรขึ้นจริง ๆ)")
        c2 = st.text_area("2. Who are the stakeholders? (ใครบ้างที่ได้รับผลกระทบ)")
        c3 = st.text_area("3. What values are involved? (เช่น ความรับผิดชอบ, การเคารพผู้ป่วย, การไม่ก่ออันตราย, การทำประโยชน์, ความเป็นธรรม, การรักษาคำพูด)")
        c4_a = st.text_input("4. Ethical Conflict - คุณค่า A:")
        c4_b = st.text_input("Ethical Conflict - คุณค่า B:")
        
        sub_s2 = st.form_submit_button("ส่งผลวิเคราะห์ Case 1")

        if sub_s2 and group_name:
            combined_analyze = f"What: {c1} | Stakeholders: {c2} | Values: {c3} | Conflict: [{c4_a}] VS [{c4_b}]"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab7 - Case1 Step2 Analyze",
                "Data": f"[{group_name}] {combined_analyze}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab7_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab7_Responses", data=updated)
                    st.success("บันทึกการวิเคราะห์สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_s2:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผลการวิเคราะห์ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab7_Responses", ttl=5)
            c1_s2_df = df[df["Step"] == "Lab7 - Case1 Step2 Analyze"]
            if not c1_s2_df.empty:
                st.dataframe(c1_s2_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Case 1 - Step 3: Discuss
# ==========================================
elif st.session_state.lab7_step == 3:
    st.title("💬 Case 1 (Step 3) — Discuss")
    st.markdown("### “ถ้าคุณเป็นเภสัชกร คุณจะอธิบายกับคนที่ไม่ได้รับบริการก่อนอย่างไร?”")

    with st.form("lab7_c1_s3_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        discussion_text = st.text_area("พิมพ์แนวทางการอธิบายของคุณ:")
        sub_s3 = st.form_submit_button("ส่งแนวทางการอธิบาย")

        if sub_s3 and group_name and discussion_text:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab7 - Case1 Step3 Discuss",
                "Data": f"[{group_name}] {discussion_text}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab7_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab7_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_s3:
            st.warning("กรุณากรอกชื่อกลุ่มและคำตอบ")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงแนวทางการอธิบายของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab7_Responses", ttl=5)
            c1_s3_df = df[df["Step"] == "Lab7 - Case1 Step3 Discuss"]
            if not c1_s3_df.empty:
                st.dataframe(c1_s3_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Case 1 - Step 4 & 5: Change Factor & Re-Vote
# ==========================================
elif st.session_state.lab7_step == 4:
    st.title("🔄 Case 1 (Step 4 & 5) — Change Factor & Re-Vote")
    st.markdown("ทดสอบเปลี่ยนเงื่อนไข Scenario (A, B, C, D) แล้วดูว่าการจัดลำดับความสำคัญเปลี่ยนหรือไม่")

    with st.form("lab7_c1_s4_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        scenario_choice = st.selectbox(
            "เลือก Scenario ที่เปลี่ยน:",
            [
                "Scenario A: ทารกไม่ได้ป่วยหนัก แต่ผู้ปกครองอ่านหนังสือไม่ออก",
                "Scenario B: นางมาดีมีอาการเจ็บหน้าอกและเริ่มมีอาการผิดปกติ",
                "Scenario C: ไม่มีเภสัชกรหรือบุคลากรคนอื่นช่วยได้",
                "Scenario D: นางมาดีรอมาแล้ว 40 นาที"
            ]
        )
        priority_changed = st.radio("การจัดลำดับความสำคัญของคุณเปลี่ยนหรือไม่?", ["เปลี่ยน", "ไม่เปลี่ยน", "ปรับเปลี่ยนเล็กน้อย"])
        reason_text = st.text_area("อธิบายเหตุผลประกอบ (Before -> After):")
        
        sub_s4 = st.form_submit_button("ส่งผล Re-Vote ตาม Scenario")

        if sub_s4 and group_name:
            scen_tag = scenario_choice.split(":")[0]
            combined_s4 = f"Scen: {scen_tag} | Changed: {priority_changed} | Reason: {reason_text}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab7 - Case1 Step4 Re-Vote",
                "Data": f"[{group_name}] {combined_s4}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab7_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab7_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_s4:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผลเปรียบเทียบการเปลี่ยนเงื่อนไข (Case 1)")
    if conn:
        try:
            df = conn.read(worksheet="Lab7_Responses", ttl=5)
            c1_s4_df = df[df["Step"] == "Lab7 - Case1 Step4 Re-Vote"]
            if not c1_s4_df.empty:
                st.dataframe(c1_s4_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Case 2 - Step 1: First Vote
# ==========================================
elif st.session_state.lab7_step == 5:
    st.title("🗳️ Case 2 (Step 1) — First Vote")
    st.markdown("### ความลับของผู้ป่วย VS ความปลอดภัยของผู้อื่น: “สิ่งใดควรได้รับการคุ้มครองในสถานการณ์นี้?”")
    st.info("💡 เลือกได้มากกว่า 1 ข้อ (พิมพ์ระบุข้อที่เลือก)")

    with st.form("lab7_c2_s1_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        c2_opts = [
            "ความลับของผู้ป่วย",
            "ความปลอดภัยของบุคคลอื่น",
            "สิทธิของผู้ป่วย",
            "สิทธิของผู้ที่อาจได้รับอันตราย",
            "ความไว้วางใจระหว่างผู้ป่วยกับผู้รักษา",
            "ความรับผิดชอบของผู้ประกอบวิชาชีพ",
            "กฎหมาย/ข้อกำหนดที่เกี่ยวข้อง"
        ]
        
        selected_c2 = []
        st.markdown("เลือกหัวข้อที่ต้องการคุ้มครอง:")
        for opt in c2_opts:
            if st.checkbox(opt, key=f"c2_opt_{opt}"):
                selected_c2.append(opt)
                
        sub_c2_s1 = st.form_submit_button("ส่งผลโหวต Case 2")

        if sub_c2_s1 and student_id:
            if selected_c2:
                combined_c2 = ", ".join(selected_c2)
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab7 - Case2 Step1 Vote",
                    "Data": f"[{student_id}] Protect: {combined_c2}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab7_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab7_Responses", data=updated)
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
            df = conn.read(worksheet="Lab7_Responses", ttl=5)
            c2_s1_df = df[df["Step"] == "Lab7 - Case2 Step1 Vote"]
            if not c2_s1_df.empty:
                all_c2 = []
                for item in c2_s1_df["Data"]:
                    if "Protect: " in item:
                        part = item.split("Protect: ")[1]
                        all_c2.extend([x.strip() for x in part.split(",")])
                if all_c2:
                    st.bar_chart(pd.Series(all_c2).value_counts())
        except:
            pass


# ==========================================
# Case 2 - Step 2: Tension Map
# ==========================================
elif st.session_state.lab7_step == 6:
    st.title("🗺️ Case 2 (Step 2) — Ethical Tension Map")
    st.markdown("โครงสร้าง: **Confidentiality ↕️ Protection from Harm**")

    with st.form("lab7_c2_s2_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        tension_consequence = st.text_area("ถ้าเลือกด้านหนึ่งมากเกินไป จะเกิดผลเสียอะไร? (วิเคราะห์ผลกระทบทั้งสองด้าน):")
        sub_c2_s2 = st.form_submit_button("ส่งผล Tension Map")

        if sub_c2_s2 and group_name and tension_consequence:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab7 - Case2 Step2 Tension Map",
                "Data": f"[{group_name}] {tension_consequence}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab7_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab7_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_c2_s2:
            st.warning("กรุณากรอกชื่อกลุ่มและคำตอบ")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Tension Map")
    if conn:
        try:
            df = conn.read(worksheet="Lab7_Responses", ttl=5)
            c2_s2_df = df[df["Step"] == "Lab7 - Case2 Step2 Tension Map"]
            if not c2_s2_df.empty:
                st.dataframe(c2_s2_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Case 2 - Step 3: Decision Ladder
# ==========================================
elif st.session_state.lab7_step == 7:
    st.title("🪜 Case 2 (Step 3) — Decision Ladder")
    st.markdown("ตอบคำถามตามลำดับขั้นบันได 7 ระดับ")

    with st.form("lab7_c2_s3_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        l1 = st.text_input("Level 1: ข้อมูลที่เรารู้คืออะไร?")
        l2 = st.text_input("Level 2: ข้อมูลอะไรที่เรายังไม่รู้?")
        l3 = st.text_input("Level 3: ใครอาจได้รับอันตราย?")
        l4 = st.text_input("Level 4: ทางเลือกที่เป็นไปได้มีอะไรบ้าง?")
        l5 = st.text_input("Level 5: แต่ละทางเลือกมีผลดี–ผลเสียอย่างไร?")
        l6 = st.text_input("Level 6: มีหน้าที่หรือกฎวิชาชีพอะไรที่ต้องพิจารณา?")
        l7 = st.text_input("Level 7: เราจะตัดสินใจอย่างไร และเพราะอะไร?")
        
        sub_c2_s3 = st.form_submit_button("ส่งผล Decision Ladder")

        if sub_c2_s3 and group_name:
            combined_ladder = f"L1: {l1} | L2: {l2} | L3: {l3} | L4: {l4} | L5: {l5} | L6: {l6} | L7: {l7}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab7 - Case2 Step3 Ladder",
                "Data": f"[{group_name}] {combined_ladder}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab7_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab7_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_c2_s3:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Decision Ladder")
    if conn:
        try:
            df = conn.read(worksheet="Lab7_Responses", ttl=5)
            c2_s3_df = df[df["Step"] == "Lab7 - Case2 Step3 Ladder"]
            if not c2_s3_df.empty:
                st.dataframe(c2_s3_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Case 2 - Step 4: Challenge
# ==========================================
elif st.session_state.lab7_step == 8:
    st.title("⚔️ Case 2 (Step 4) — Challenge")
    st.markdown("รับเงื่อนไขใหม่ แล้วพิจารณาว่าข้อมูลใหม่นี้ทำให้การตัดสินใจเปลี่ยนหรือไม่")

    with st.form("lab7_c2_s4_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        new_cond = st.selectbox(
            "เงื่อนไขใหม่ที่ได้รับ:",
            [
                "เงื่อนไข 1: ผู้ป่วยบอกว่าเป็นเพียงความคิดชั่วคราว",
                "เงื่อนไข 2: ผู้ป่วยระบุบุคคลเป้าหมายอย่างชัดเจน",
                "เงื่อนไข 3: ผู้ป่วยไม่มีอาวุธและอยู่ในการควบคุม",
                "เงื่อนไข 4: บุคคลเป้าหมายอยู่ใกล้ผู้ป่วย",
                "เงื่อนไข 5: ทีมรักษามีข้อมูลเพิ่มเติมเกี่ยวกับความเสี่ยง"
            ]
        )
        decision_shift = st.radio("ข้อมูลใหม่นี้ทำให้การตัดสินใจเปลี่ยนหรือไม่?", ["เปลี่ยน", "ไม่เปลี่ยน", "ต้องรอบคอบขึ้น"])
        reason_c2 = st.text_area("อธิบายเหตุผล:")
        
        sub_c2_s4 = st.form_submit_button("ส่งผล Challenge")

        if sub_c2_s4 and group_name:
            cond_tag2 = new_cond.split(":")[0]
            combined_ch2 = f"Cond: {cond_tag2} | Shift: {decision_shift} | Reason: {reason_c2}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab7 - Case2 Step4 Challenge",
                "Data": f"[{group_name}] {combined_ch2}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab7_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab7_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_c2_s4:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Challenge (Case 2)")
    if conn:
        try:
            df = conn.read(worksheet="Lab7_Responses", ttl=5)
            c2_s4_df = df[df["Step"] == "Lab7 - Case2 Step4 Challenge"]
            if not c2_s4_df.empty:
                st.dataframe(c2_s4_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Case 2 - Step 5: Final Re-Vote
# ==========================================
elif st.session_state.lab7_step == 9:
    st.title("🎯 Case 2 (Step 5) — Final Re-Vote")
    st.markdown("### “เมื่อหลักจริยธรรมขัดแย้งกัน การตัดสินใจที่ดีควรเริ่มจากอะไร?”")

    with st.form("lab7_c2_s5_form"):
        student_id = st.text_input("รหัสนิสิต:")
        final_choice_c2 = st.selectbox(
            "เลือกจุดเริ่มต้นการตัดสินใจ:",
            [
                "A. หลักจริยธรรมข้อใดข้อหนึ่ง",
                "B. ความต้องการของผู้ป่วย",
                "C. ความปลอดภัย",
                "D. กฎหมาย/กฎวิชาชีพ",
                "E. ข้อเท็จจริงและระดับความเสี่ยง",
                "F. พิจารณาหลายปัจจัยร่วมกัน"
            ]
        )
        discussion_note = st.text_area("เหตุผลทำไมคำตอบจึงเปลี่ยนหรือไม่เปลี่ยนจากครั้งแรก:")
        sub_c2_s5 = st.form_submit_button("ส่ง Final Re-Vote")

        if sub_c2_s5 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab7 - Case2 Step5 Final Vote",
                "Data": f"[{student_id}] Choice: {final_choice_c2} | Note: {discussion_note}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab7_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab7_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_c2_s5:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผล Final Re-Vote (Case 2)")
    if conn:
        try:
            df = conn.read(worksheet="Lab7_Responses", ttl=5)
            c2_s5_df = df[df["Step"] == "Lab7 - Case2 Step5 Final Vote"]
            if not c2_s5_df.empty:
                votes_final = c2_s5_df["Data"].apply(lambda x: x.split("|")[0].replace("Choice: ", "").strip() if "Choice: " in x else x)
                st.bar_chart(votes_final.value_counts())
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# Final Reflection (Lab 7)
# ==========================================
elif st.session_state.lab7_step == 10:
    st.title("📝 Final Reflection (Lab 7)")

    with st.form("lab7_reflection_form"):
        student_id = st.text_input("รหัสนิสิต (ระบุหรือไม่ระบุก็ได้):")
        
        r1 = st.text_area("1. Before (ตอนแรกฉันคิดว่า):")
        r2 = st.text_area("2. Changed (สิ่งที่ทำให้ฉันเปลี่ยนความคิดคือ):")
        r3 = st.text_area("3. Next time (ถ้าเจอสถานการณ์จริง ฉันจะ):")
        
        sub_ref = st.form_submit_button("ส่ง Final Reflection Lab 7")

        if sub_ref and student_id:
            sid_val = "Anonymous" if not student_id else student_id
            combined_ref = f"Before: {r1} | Changed: {r2} | Next: {r3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab7 - Final Reflection",
                "Data": f"[{sid_val}] {combined_ref}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab7_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab7_Responses", data=updated)
                    st.success("บันทึก Reflection สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_ref:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางรวบรวม Final Reflection (Lab 7)")
    if conn:
        try:
            df = conn.read(worksheet="Lab7_Responses", ttl=5)
            ref_df = df[df["Step"] == "Lab7 - Final Reflection"]
            if not ref_df.empty:
                st.dataframe(ref_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass