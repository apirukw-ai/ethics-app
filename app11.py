from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 11: Role Model & Professional Identity",
    page_icon="🌟",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab11_step" not in st.session_state:
    st.session_state.lab11_step = 1

# --- Sidebar เมนูด้านซ้าย ---
st.sidebar.markdown("### 🌟 LAB 11 Workflow")

steps_name = {
    1: "1. Role Model: ใครคือเภสัชกรต้นแบบ?",
    2: "2. What Do You Admire? (เลือกคุณธรรม)",
    3: "3. Role Model Challenge",
    4: "4. Role Model ≠ Perfect Person",
    5: "5. From Role Model → My Identity",
    6: "6. Final Challenge: ไม่มีคำตอบที่สบายใจ",
    7: "7. Final Reflection (ปิดรายวิชา)",
}

current_index = list(steps_name.keys()).index(st.session_state.lab11_step)

selected_step_name = st.sidebar.radio(
    "เลือกกิจกรรม LAB 11:",
    list(steps_name.values()),
    index=current_index,
    key="lab11_menu_selection",
)

for s_num, s_title in steps_name.items():
    if s_title == selected_step_name:
        st.session_state.lab11_step = s_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อกิจกรรมด้านบนเพื่อเปลี่ยนหน้า")


# ==========================================
# 1. Role Model — ใครคือเภสัชกรต้นแบบของฉัน?
# ==========================================
if st.session_state.lab11_step == 1:
    st.title("👤 1. Role Model — ใครคือเภสัชกรต้นแบบของฉัน?")
    st.info("“เลือกเภสัชกร 1 คนที่สะท้อนคุณค่าที่คุณอยากมีในวิชาชีพ (อาจเป็นอาจารย์, เภสัชกรชุมชน/รพ./อุตสาหกรรม, จากข่าว หรือคนใกล้ตัว)”")

    with st.form("lab11_act1_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        role_model_name = st.text_input("ชื่อ/ตำแหน่งของเภสัชกรต้นแบบที่กลุ่มเลือก:")
        reason_chosen = st.text_area("“คนนี้ทำอะไรที่ทำให้ฉันเห็นคุณค่าของความเป็นเภสัชกร?”")
        
        sub_a1 = st.form_submit_button("ส่งข้อมูล Role Model")

        if sub_a1 and group_name and role_model_name:
            combined_rm = f"Role Model: {role_model_name} | Reason: {reason_chosen}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab11 - Act 1 Role Model",
                "Data": f"[{group_name}] {combined_rm}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab11_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab11_Responses", data=updated)
                    st.success("บันทึกข้อมูลสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a1:
            st.warning("กรุณากรอกชื่อกลุ่มและชื่อ Role Model")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Role Model ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab11_Responses", ttl=5)
            p1_df = df[df["Step"] == "Lab11 - Act 1 Role Model"]
            if not p1_df.empty:
                st.dataframe(p1_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 2. What Do You Admire?
# ==========================================
elif st.session_state.lab11_step == 2:
    st.title("💎 2. What Do You Admire?")
    st.markdown("เลือกคุณธรรม/คุณค่าทางวิชาชีพ 3 ข้อที่สะท้อนจากต้นแบบของคุณ")
    st.info("💡 เลือกได้ 3 ข้อจากรายการด้านล่าง")

    with st.form("lab11_act2_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        virtues_list = [
            "ความรับผิดชอบ",
            "ซื่อสัตย์",
            "เสียสละ",
            "เคารพผู้ป่วย",
            "ยึดความปลอดภัย",
            "กล้าตัดสินใจ",
            "ความเป็นธรรม",
            "ความเห็นอกเห็นใจ",
            "ความรับผิดชอบต่อสังคม",
            "การเรียนรู้ตลอดชีวิต"
        ]
        
        selected_virtues = []
        for v in virtues_list:
            if st.checkbox(v, key=f"v_{v}"):
                selected_virtues.append(v)
                
        behavior_explain = st.text_area("“มีพฤติกรรมอะไรที่แสดงให้เห็นว่าบุคคลนี้มีคุณค่านั้น?” (ยกตัวอย่างพฤติกรรมประกอบ):")
        
        sub_a2 = st.form_submit_button("ส่งข้อมูล What Do You Admire")

        if sub_a2 and group_name:
            if len(selected_virtues) > 0:
                joined_v = ", ".join(selected_virtues)
                combined_adm = f"Virtues: {joined_v} | Behaviors: {behavior_explain}"
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab11 - Act 2 Admire",
                    "Data": f"[{group_name}] {combined_adm}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab11_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab11_Responses", data=updated)
                        st.success("บันทึกสำเร็จ!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else:
                    st.success("บันทึกจำลองสำเร็จ!")
            else:
                st.warning("กรุณาเลือกคุณธรรมอย่างน้อย 1 ข้อ")
        elif sub_a2:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผลคุณธรรมที่ชื่นชม")
    if conn:
        try:
            df = conn.read(worksheet="Lab11_Responses", ttl=5)
            p2_df = df[df["Step"] == "Lab11 - Act 2 Admire"]
            if not p2_df.empty:
                st.dataframe(p2_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 3. Role Model Challenge
# ==========================================
elif st.session_state.lab11_step == 3:
    st.title("⚔️ 3. Role Model Challenge")
    st.markdown("ทดสอบมุมมองต่อ Role Model ผ่าน 3 คำถามท้าทาย")

    with st.form("lab11_act3_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        q_why = st.text_area("1. WHY? ทำไมคุณจึงคิดว่านี่เป็นคุณธรรมที่สำคัญ?")
        q_whatif = st.text_area("2. WHAT IF? ถ้าสถานการณ์เปลี่ยน คุณยังคิดว่าเขาควรทำแบบเดิมหรือไม่?")
        q_conf = st.text_area("3. CONFLICT? ถ้าคุณธรรม 2 อย่างขัดแย้งกัน (เช่น ความเมตตา vs ความปลอดภัย) คุณจะเลือกอะไร?")
        
        sub_a3 = st.form_submit_button("ส่งผล Role Model Challenge")

        if sub_a3 and group_name:
            combined_ch = f"Why: {q_why} | WhatIf: {q_whatif} | Conflict: {q_conf}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab11 - Act 3 Challenge",
                "Data": f"[{group_name}] {combined_ch}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab11_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab11_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a3:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Role Model Challenge")
    if conn:
        try:
            df = conn.read(worksheet="Lab11_Responses", ttl=5)
            p3_df = df[df["Step"] == "Lab11 - Act 3 Challenge"]
            if not p3_df.empty:
                st.dataframe(p3_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 4. Role Model ≠ Perfect Person
# ==========================================
elif st.session_state.lab11_step == 4:
    st.title("⚖️ 4. Role Model ≠ Perfect Person")
    st.markdown("### “เภสัชกรต้นแบบจำเป็นต้องเป็นคนที่สมบูรณ์แบบหรือไม่?”")

    with st.form("lab11_act4_form"):
        student_id = st.text_input("รหัสนิสิต:")
        vote_perf = st.radio("เลือกคำตอบ:", ["YES (ต้องสมบูรณ์แบบ)", "NO (ไม่ต้องสมบูรณ์แบบก็ได้)", "DEPENDS (ขึ้นอยู่กับบริบท)"])
        comment_perf = st.text_area("เหตุผลสนับสนุนความคิดเห็น:")
        
        sub_a4 = st.form_submit_button("ส่งผลโหวต Perfect Person")

        if sub_a4 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab11 - Act 4 Perfect Vote",
                "Data": f"[{student_id}] Vote: {vote_perf} | Note: {comment_perf}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab11_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab11_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a4:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผลโหวต (Role Model ≠ Perfect Person)")
    if conn:
        try:
            df = conn.read(worksheet="Lab11_Responses", ttl=5)
            p4_df = df[df["Step"] == "Lab11 - Act 4 Perfect Vote"]
            if not p4_df.empty:
                votes = p4_df["Data"].apply(lambda x: x.split("|")[0].replace("Vote: ", "").strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 5. From Role Model → My Professional Identity
# ==========================================
elif st.session_state.lab11_step == 5:
    st.title("🎯 5. From Role Model → My Professional Identity")
    st.markdown("### “My Pharmacist” — สร้างเอกลักษณ์ความเป็นเภสัชกรในแบบของคุณเอง")

    with st.form("lab11_act5_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        s1 = st.text_input("1. ฉันอยากเป็นเภสัชกรที่...")
        s2 = st.text_input("2. ยึดถือคุณค่าอะไร?")
        s3 = st.text_input("3. แสดงคุณค่านั้นผ่านพฤติกรรมอะไร?")
        s4 = st.text_input("4. จะไม่ยอมทำอะไร แม้มีแรงกดดัน?")
        s5 = st.text_input("5. จะรับผิดชอบต่อใครบ้าง?")
        
        statement_sum = st.text_area("สรุปเป็น “My Professional Ethics Statement” (สั้น ๆ 3–5 ประโยค):")
        
        sub_a5 = st.form_submit_button("ส่ง Professional Identity Statement")

        if sub_a5 and student_id:
            combined_id = f"Identity: {s1}, {s2}, {s3}, {s4}, {s5} || Statement: {statement_sum}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab11 - Act 5 Identity Statement",
                "Data": f"[{student_id}] {combined_id}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab11_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab11_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a5:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Professional Identity ของนิสิต")
    if conn:
        try:
            df = conn.read(worksheet="Lab11_Responses", ttl=5)
            p5_df = df[df["Step"] == "Lab11 - Act 5 Identity Statement"]
            if not p5_df.empty:
                st.dataframe(p5_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 6. Final Challenge: ไม่มีคำตอบที่สบายใจ
# ==========================================
elif st.session_state.lab11_step == 6:
    st.title("🏆 6. Final Challenge — Case: “ไม่มีคำตอบที่สบายใจ”")
    st.info(
        "**สถานการณ์:** คุณเป็นเภสัชกรที่พบว่าการตัดสินใจของคุณในวันนี้อาจช่วยผู้ป่วยคนหนึ่งได้ทันที แต่ขณะเดียวกันอาจทำให้เกิดปัญหากับองค์กรหรือผู้เกี่ยวข้องในภายหลัง คุณมีข้อมูลไม่ครบ และไม่มีทางเลือกใดที่ปราศจากผลเสียทั้งหมด คุณจะตัดสินใจอย่างไร?"
    )
    st.markdown("วิเคราะห์ตาม Framework และตอบคำถามสะท้อนตัวตน")

    with st.form("lab11_final_case_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        fc1 = st.text_input("1. FACTS:")
        fc2 = st.text_input("2. STAKEHOLDERS:")
        fc3 = st.text_input("3. ETHICAL ISSUE:")
        fc4 = st.text_input("4. VALUES / RESPONSIBILITY:")
        fc5 = st.text_input("5. RULES:")
        fc6 = st.text_input("6. OPTIONS:")
        fc7 = st.text_input("7. CONSEQUENCES:")
        fc8 = st.text_input("8. DECISION:")
        fc9 = st.text_area("9. JUSTIFICATION:")
        
        reflection_q = st.text_area("🔥 คำถามสุดท้าย: “การตัดสินใจนี้สะท้อนว่าคุณกำลังเป็นเภสัชกรแบบไหน?”")
        
        sub_fc = st.form_submit_button("ส่งผล Final Challenge รายวิชา")

        if sub_fc and group_name:
            combined_fc = f"F1:{fc1}|F2:{fc2}|F3:{fc3}|F4:{fc4}|F5:{fc5}|F6:{fc6}|F7:{fc7}|F8:{fc8}|F9:{fc9} || Reflection: {reflection_q}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab11 - Final Challenge",
                "Data": f"[{group_name}] {combined_fc}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab11_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab11_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
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
            df = conn.read(worksheet="Lab11_Responses", ttl=5)
            fc_df = df[df["Step"] == "Lab11 - Final Challenge"]
            if not fc_df.empty:
                st.dataframe(fc_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# 7. Final Reflection (ปิดรายวิชาสมบูรณ์)
# ==========================================
elif st.session_state.lab11_step == 7:
    st.title("🎓 7. Final Reflection (ปิดรายวิชาสมบูรณ์)")
    st.markdown("สะท้อนความคิดเห็นส่วนบุคคลส่งท้ายรายวิชา Ethics")

    with st.form("lab11_reflection_form"):
        student_id = st.text_input("รหัสนิสิต (ระบุหรือไม่ระบุก็ได้):")
        
        r1 = st.text_area("1. BEFORE: ตอนเริ่มเรียนวิชานี้ ฉันคิดว่า “จริยธรรมของเภสัชกร” คืออะไร?")
        r2 = st.text_area("2. NOW: วันนี้ฉันคิดว่าจริยธรรมของเภสัชกรคืออะไร?")
        r3 = st.text_area("3. NEXT: เมื่อออกไปประกอบวิชาชีพ ฉันอยากรักษาคุณค่าอะไรไว้ แม้ต้องเผชิญแรงกดดัน?")
        r4 = st.text_area("4. 🌟 คำถามสุดท้าย: “ถ้ามีคนถามว่า ‘เภสัชกรที่ดีควรเป็นอย่างไร?’ คุณจะตอบอย่างไรใน 1 ประโยค?”")
        
        sub_ref = st.form_submit_button("ส่ง Final Reflection ปิดรายวิชา")

        if sub_ref and student_id:
            sid_val = "Anonymous" if not student_id else student_id
            combined_ref = f"Before: {r1} | Now: {r2} | Next: {r3} | OneSentence: {r4}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab11 - Final Reflection",
                "Data": f"[{sid_val}] {combined_ref}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab11_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab11_Responses", data=updated)
                    st.success("บันทึก Final Reflection สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_ref:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางรวบรวม Final Reflection ปิดรายวิชาทั้งหมด")
    if conn:
        try:
            df = conn.read(worksheet="Lab11_Responses", ttl=5)
            ref_df = df[df["Step"] == "Lab11 - Final Reflection"]
            if not ref_df.empty:
                st.dataframe(ref_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass