from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 2: Professional Ethics & Decision-Making",
    page_icon="⚖️",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab2_step" not in st.session_state:
    st.session_state.lab2_step = 1

# --- Sidebar เมนูด้านซ้าย ---
st.sidebar.markdown("### ⚖️ LAB 2 Workflow")

steps_name = {
    1: "Activity 1: Warm-up",
    2: "Activity 2: Everyday Dilemma",
    3: "Activity 3: WHY?",
    4: "Activity 4: Change One Factor",
    5: "Activity 5: Small Group Discussion",
    6: "Activity 6: Ethical Tension Map",
    7: "Activity 7: Re-Vote",
    8: "Activity 8: Bridge to Prof. Ethics",
    9: "Activity 9: Final Reflection",
    10: "Activity 10: Instructor Debrief",
}

current_index = list(steps_name.keys()).index(st.session_state.lab2_step)

selected_step_name = st.sidebar.radio(
    "เลือกกิจกรรม LAB 2:",
    list(steps_name.values()),
    index=current_index,
    key="lab2_menu_selection",
)

for s_num, s_title in steps_name.items():
    if s_title == selected_step_name:
        st.session_state.lab2_step = s_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อกิจกรรมด้านบนเพื่อเปลี่ยนหน้า")


# ==========================================
# 1. Activity 1 — Warm-up
# ==========================================
if st.session_state.lab2_step == 1:
    st.title("🧩 Activity 1 — Warm-up")
    st.markdown("### “คุณเคยทำสิ่งที่รู้ว่า ‘ไม่ค่อยถูกต้อง’ เพราะไม่อยากมีปัญหากับคนอื่นหรือไม่?”")

    with st.form("lab2_act1_form"):
        student_id = st.text_input("รหัสนิสิต (หรือระบุ Anonymous):")
        choice = st.radio("เลือกคำตอบ:", ["เคย", "ไม่เคย", "ไม่แน่ใจ"])
        
        st.markdown("---")
        st.markdown("**คำถามสะท้อนคิด:** “อะไรทำให้บางครั้งเราทำสิ่งที่ขัดกับสิ่งที่เราคิดว่าถูก?”")
        comment_text = st.text_area("พิมพ์ความเห็นของคุณ (เช่น ความกดดันจากสังคม, ความสัมพันธ์, ความกลัว, ฯลฯ):")
        
        sub1 = st.form_submit_button("ส่งคำตอบ Warm-up")

        if sub1 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Act 1 Warmup",
                "Data": f"[{student_id}] Vote: {choice} | Comment: {comment_text}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึกคำตอบสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub1:
            st.warning("กรุณากรอกรหัสนิสิตก่อนส่งคำตอบ")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผล Vote (Activity 1)")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            act1_df = df[df["Step"] == "Lab2 - Act 1 Warmup"]
            if not act1_df.empty:
                votes = act1_df["Data"].apply(lambda x: x.split("|")[0].replace("Vote: ", "").strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
            else:
                st.info("ยังไม่มีข้อมูลผลโหวต")
        except:
            pass


# ==========================================
# 2. Activity 2 — Everyday Ethical Dilemma
# ==========================================
elif st.session_state.lab2_step == 2:
    st.title("📋 Activity 2 — Everyday Ethical Dilemma")
    st.error(
        "**สถานการณ์:** คุณอยู่ในกลุ่มทำงาน และพบว่าเพื่อนคนหนึ่งไม่ได้ช่วยทำงาน แต่ต้องการให้ใส่ชื่อในผลงานกลุ่มด้วย เพราะเพื่อนบอกว่า “ครั้งนี้มีเหตุจำเป็นจริง ๆ”"
    )

    with st.form("lab2_act2_form"):
        student_id = st.text_input("รหัสนิสิต:")
        choice_d2 = st.radio(
            "คุณจะทำอย่างไร?",
            [
                "A. ใส่ชื่อให้ เพราะเป็นเพื่อน",
                "B. ไม่ใส่ชื่อ เพราะไม่ได้ทำงาน",
                "C. คุยกับเพื่อนก่อนแล้วหาทางออก",
                "D. ขึ้นอยู่กับรายละเอียดของสถานการณ์",
                "E. อื่น ๆ"
            ]
        )
        sub_d2 = st.form_submit_button("ยืนยันคำตอบ Dilemma")

        if sub_d2 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Act 2 Dilemma",
                "Data": f"[{student_id}] {choice_d2}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึกผลโหวตสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_d2:
            st.warning("กรุณากรอกรหัสนิสิตก่อนส่งคำตอบ")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผลโหวต Activity 2")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            d2_df = df[df["Step"] == "Lab2 - Act 2 Dilemma"]
            if not d2_df.empty:
                st.bar_chart(d2_df["Data"].value_counts())
            else:
                st.info("ยังไม่มีข้อมูลผลโหวต")
        except:
            pass


# ==========================================
# 3. Activity 3 — WHY?
# ==========================================
elif st.session_state.lab2_step == 3:
    st.title("🧠 Activity 3 — WHY?")
    st.markdown("### “เหตุผลสำคัญที่สุดที่ทำให้คุณเลือกคำตอบนี้คืออะไร?”")

    with st.form("lab2_act3_form"):
        student_id = st.text_input("รหัสนิสิต:")
        reason_choice = st.selectbox(
            "เลือกเหตุผลหลัก:",
            [
                "ความยุติธรรม", "ความรับผิดชอบ", "ความสัมพันธ์กับเพื่อน",
                "ผลกระทบต่อกลุ่ม", "ความซื่อสัตย์", "การให้โอกาสผู้อื่น",
                "กฎ/ระเบียบ", "ผลประโยชน์ของส่วนรวม", "อื่น ๆ"
            ]
        )
        comment_why = st.text_area("ช่องแสดงความคิดเห็นเพิ่มเติม:")
        sub_r3 = st.form_submit_button("ส่งเหตุผล")

        if sub_r3 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Act 3 Why",
                "Data": f"[{student_id}] Reason: {reason_choice} | Comment: {comment_why}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึกเหตุผลสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_r3:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงเหตุผล (Horizontal Bar Chart)")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5.0)
            r3_df = df[df["Step"] == "Lab2 - Act 3 Why"]
            if not r3_df.empty:
                reasons = r3_df["Data"].apply(lambda x: x.split("|")[0].replace("Reason: ", "").strip() if "Reason: " in x else x)
                st.bar_chart(reasons.value_counts())
            else:
                st.info("ยังไม่มีข้อมูลเหตุผล")
        except:
            pass

    st.markdown("---")
    st.info("📌 **คำถามอภิปราย:** “ถ้าคุณกับเพื่อนเลือกคำตอบต่างกัน แสดงว่าใครคิดถูก?” (ไม่เฉลย ใช้เปิดประเด็นถกเถียง)")


# ==========================================
# 4. Activity 4 — CHANGE ONE FACTOR
# ==========================================
elif st.session_state.lab2_step == 4:
    st.title("⚡ Activity 4 — CHANGE ONE FACTOR (Pre-Vote)")
    st.markdown("โหวตก่อนอภิปรายในแต่ละ Scenario ที่มีการเปลี่ยนแปลงเงื่อนไข")

    scenario_choice = st.selectbox(
        "เลือก Scenario สำหรับโหวต:",
        [
            "Scenario A: เพื่อนไม่ได้ทำงาน แต่ขอใส่ชื่อเพราะมีเหตุจำเป็น",
            "Scenario B: เพื่อนไม่ได้ทำงาน เพราะต้องดูแลสมาชิกในครอบครัวที่ป่วย",
            "Scenario C: เพื่อนไม่ได้ทำงาน แต่ผลงานของเขาในส่วนอื่นช่วยให้กลุ่มประสบความสำเร็จ",
            "Scenario D: เพื่อนไม่ได้ทำงาน และไม่มีเหตุจำเป็น แต่เป็นเพื่อนสนิทของคุณ"
        ]
    )

    with st.form("lab2_act4_form"):
        student_id = st.text_input("รหัสนิสิต:")
        vote_a4 = st.radio("คุณจะตัดสินใจอย่างไรสำหรับ Scenario นี้?", ["ใส่ชื่อ", "ไม่ใส่ชื่อ", "ขึ้นอยู่กับบริบทเพิ่มเติม"])
        sub_a4 = st.form_submit_button("ส่งผลโหวต Scenario (Pre-Vote)")

        if sub_a4 and student_id:
            scen_tag = scenario_choice.split(":")[0]
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": f"Lab2 - Act 4 ({scen_tag})",
                "Data": f"[{student_id}] {vote_a4}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success(f"บันทึก Pre-Vote {scen_tag} สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a4:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 เปรียบเทียบผล Pre-Vote แต่ละ Scenario (A / B / C / D)")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            scen_df = df[df["Step"].str.contains("Lab2 - Act 4", na=False)]
            if not scen_df.empty:
                pivot_data = scen_df.pivot_table(index="Data", columns="Step", aggfunc="size", fill_value=0)
                st.bar_chart(pivot_data)
            else:
                st.info("ยังไม่มีข้อมูล Pre-Vote ของ Scenario")
        except:
            pass


# ==========================================
# 5. Activity 5 — Small Group Discussion
# ==========================================
elif st.session_state.lab2_step == 5:
    st.title("👥 Activity 5 — Small Group Discussion")
    st.warning("ร่วมมือกันอภิปรายในกลุ่มย่อย และบันทึกคำตอบ 5 ข้อด้านล่างนี้")

    with st.form("lab2_act5_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        q1 = st.text_area("1. อะไรคือ “ประเด็นทางจริยธรรม” ของสถานการณ์นี้?")
        q2 = st.text_area("2. ใครคือผู้มีส่วนได้ส่วนเสีย?")
        q3 = st.text_area("3. คุณค่าใดกำลังขัดแย้งกัน?")
        q4 = st.text_area("4. ข้อมูลอะไรที่เรายังไม่รู้และอาจมีผลต่อการตัดสินใจ?")
        q5 = st.text_area("5. กลุ่มของคุณจะตัดสินใจอย่างไร?")
        sub_a5 = st.form_submit_button("ส่งสรุปผลการอภิปรายกลุ่ม")

        if sub_a5 and group_name:
            combined = f"Q1: {q1} | Q2: {q2} | Q3: {q3} | Q4: {q4} | Decision: {q5}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Act 5 Discussion",
                "Data": f"[{group_name}] {combined}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึกสรุปกลุ่มสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a5:
            st.warning("กรุณาระบุชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางรวมคำตอบกลุ่มย่อย (Activity 5)")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            p5_df = df[df["Step"] == "Lab2 - Act 5 Discussion"]
            if not p5_df.empty:
                st.dataframe(p5_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูลกลุ่มย่อย")
        except:
            pass


# ==========================================
# 6. Activity 6 — Ethical Tension Map
# ==========================================
elif st.session_state.lab2_step == 6:
    st.title("🗺️ Activity 6 — Ethical Tension Map")
    st.markdown("### ค้นหาคู่คุณค่าที่ขัดแย้งกันหลักในสถานการณ์นี้")

    with st.form("lab2_act6_form"):
        student_id = st.text_input("รหัสนิสิต / หรือชื่อกลุ่ม:")
        tension_choice = st.radio(
            "คู่คุณค่าใดเป็น ‘ความขัดแย้งหลัก’ ของสถานการณ์นี้?",
            [
                "ความซื่อสัตย์ ↕ ความสัมพันธ์",
                "ความยุติธรรม ↕ การให้โอกาส",
                "กฎระเบียบ ↕ ความเห็นอกเห็นใจ"
            ]
        )
        sub_a6 = st.form_submit_button("ส่งการเลือก Ethical Tension")

        if sub_a6 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Act 6 Tension Map",
                "Data": f"[{student_id}] {tension_choice}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึกข้อมูล Tension Map สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a6:
            st.warning("กรุณากรอกรหัสนิสิตหรือชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📊 สรุปความขัดแย้งของคุณค่า (Values in Tension)")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            t_df = df[df["Step"] == "Lab2 - Act 6 Tension Map"]
            if not t_df.empty:
                st.bar_chart(t_df["Data"].value_counts())
            else:
                st.info("ยังไม่มีข้อมูล Tension Map")
        except:
            pass


# ==========================================
# 7. Activity 7 — Re-Vote
# ==========================================
elif st.session_state.lab2_step == 7:
    st.title("🔄 Activity 7 — Re-Vote (Post-Vote)")
    st.markdown("โหวตหลังอภิปราย แยกตาม Scenario A, B, C, D พร้อมวิเคราะห์เหตุผลการเปลี่ยนแปลง")

    revote_scenario = st.selectbox(
        "เลือก Scenario สำหรับ Re-Vote:",
        [
            "Scenario A: เพื่อนไม่ได้ทำงาน แต่ขอใส่ชื่อเพราะมีเหตุจำเป็น",
            "Scenario B: เพื่อนไม่ได้ทำงาน เพราะต้องดูแลสมาชิกในครอบครัวที่ป่วย",
            "Scenario C: เพื่อนไม่ได้ทำงาน แต่ผลงานของเขาในส่วนอื่นช่วยให้กลุ่มประสบความสำเร็จ",
            "Scenario D: เพื่อนไม่ได้ทำงาน และไม่มีเหตุจำเป็น แต่เป็นเพื่อนสนิทของคุณ"
        ]
    )

    with st.form("lab2_act7_form"):
        student_id = st.text_input("รหัสนิสิต:")
        vote_post = st.radio("การตัดสินใจหลังอภิปราย (Post-Vote):", ["ใส่ชื่อ", "ไม่ใส่ชื่อ", "ขึ้นอยู่กับบริบทเพิ่มเติม"])
        
        st.markdown("---")
        reason_change = st.selectbox(
            "“อะไรทำให้คุณเปลี่ยนหรือไม่เปลี่ยนความคิดเห็น?”",
            [
                "ได้ข้อมูลใหม่", "เห็นมุมมองของเพื่อน", "มองเห็นผู้มีส่วนได้ส่วนเสียมากขึ้น",
                "เห็นคุณค่าที่ขัดแย้งกันชัดขึ้น", "ยังคิดเหมือนเดิม", "อื่น ๆ"
            ]
        )
        sub_a7 = st.form_submit_button("ส่งผล Re-Vote")

        if sub_a7 and student_id:
            scen_tag = revote_scenario.split(":")[0]
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": f"Lab2 - Act 7 Post ({scen_tag})",
                "Data": f"[{student_id}] Vote: {vote_post} | Reason: {reason_change}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success(f"บันทึก Re-Vote ของ {scen_tag} สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a7:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟเปรียบเทียบผลโหวต ก่อนอภิปราย (Pre) และ หลังอภิปราย (Post)")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            scen_tag_curr = revote_scenario.split(":")[0]
            
            pre_df = df[df["Step"] == f"Lab2 - Act 4 ({scen_tag_curr})"]
            post_df = df[df["Step"] == f"Lab2 - Act 7 Post ({scen_tag_curr})"]
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.markdown(f"**Pre-Vote ({scen_tag_curr})**")
                if not pre_df.empty:
                    st.bar_chart(pre_df["Data"].value_counts())
                else:
                    st.info("ยังไม่มีข้อมูล Pre-Vote")
            with col_p2:
                st.markdown(f"**Post-Vote ({scen_tag_curr})**")
                if not post_df.empty:
                    post_votes = post_df["Data"].apply(lambda x: x.split("|")[0].replace("Vote: ", "").strip() if "Vote: " in x else x)
                    st.bar_chart(post_votes.value_counts())
                else:
                    st.info("ยังไม่มีข้อมูล Post-Vote")
        except:
            pass


# ==========================================
# 8. Activity 8 — Bridge to Professional Ethics
# ==========================================
elif st.session_state.lab2_step == 8:
    st.title("🌉 Activity 8 — Bridge to Professional Ethics")
    st.markdown("### “ถ้าสถานการณ์เดียวกันนี้เกิดขึ้นในวิชาชีพเภสัชกรรม จะมีอะไรเพิ่มเข้ามาจากการตัดสินใจในชีวิตประจำวัน?”")

    with st.form("lab2_act8_form"):
        student_id = st.text_input("รหัสนิสิต:")
        prof_answer = st.text_area("พิมพ์ความคิดเห็นของคุณแบบ Open-ended:")
        sub_a8 = st.form_submit_button("ส่งคำตอบ Bridge")

        if sub_a8 and student_id and prof_answer:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Act 8 Bridge",
                "Data": f"[{student_id}] {prof_answer}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึกข้อมูลสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a8:
            st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")

    st.markdown("---")
    st.subheader("📌 อาจารย์สรุป 4 มิติทางวิชาชีพ (Instructor Summary)")
    st.markdown(
        """
        1. **PERSON:** ฉันคิดอย่างไร?
        2. **OTHER PEOPLE:** ใครได้รับผลกระทบ?
        3. **RULES:** มีกฎหมาย/กฎ/มาตรฐานอะไรเกี่ยวข้อง?
        4. **PROFESSION:** ความรับผิดชอบในฐานะวิชาชีพเพิ่มอะไรเข้ามา?
        """
    )
    
    # ช่องสรุป 4 มิติทางวิชาชีพของอาจารย์
    with st.form("instructor_4dims_form"):
        instructor_summary_text = st.text_area("ช่องสรุปประเด็น 4 มิติวิชาชีพ (สำหรับอาจารย์บันทึกสรุปหน้าห้อง):")
        sub_sum = st.form_submit_button("บันทึกสรุป 4 มิติ")

        if sub_sum and instructor_summary_text:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Act 8 Instructor Summary",
                "Data": f"[Instructor 4-Dims] {instructor_summary_text}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึกสรุป 4 มิติทางวิชาชีพสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")

    st.markdown("---")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            b_df = df[df["Step"] == "Lab2 - Act 8 Bridge"]
            if not b_df.empty:
                st.markdown("#### คำตอบของนิสิตทั้งหมด:")
                st.dataframe(b_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีคำตอบ Open-ended ของนิสิต")
        except:
            pass


# ==========================================
# 9. Final Reflection
# ==========================================
elif st.session_state.lab2_step == 9:
    st.title("🎯 Final Reflection (Lab 2)")

    with st.form("lab2_reflection_form"):
        student_id = st.text_input("รหัสนิสิต (ไม่บังคับ / ระบุ Anonymous ได้):")
        q1 = st.text_area("1. สิ่งที่คุณคิดว่ายากที่สุดในการตัดสินใจทางจริยธรรมคืออะไร?")
        q2 = st.text_area("2. หลังจากกิจกรรมวันนี้ คุณจะคิดต่างจากเดิมอย่างไรเมื่อเจอสถานการณ์ที่มีความขัดแย้งทางคุณค่า?")
        sub_ref = st.form_submit_button("ส่งแบบสะท้อนความคิด")

        if sub_ref and q1 and q2:
            sid_val = "Anonymous" if not student_id else student_id
            combined = f"Q1: {q1} | Q2: {q2}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Final Reflection",
                "Data": f"[{sid_val}] {combined}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึก Reflection สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกสำเร็จ!")
        elif sub_ref:
            st.warning("กรุณาตอบคำถามทั้งสองข้อ")


# ==========================================
# 10. Instructor Debrief
# ==========================================
elif st.session_state.lab2_step == 10:
    st.title("👨‍🏫 Instructor Debrief & Summary")
    st.markdown("### แนวทางการสรุปสำหรับอาจารย์ (ใช้คำถาม 5 ข้อ)")
    st.markdown(
        """
        1. **เราตัดสินใจจากอะไร?**
        2. **ข้อมูลที่เพิ่มขึ้นทำให้การตัดสินใจเปลี่ยนหรือไม่?**
        3. **ใครได้รับผลกระทบ?**
        4. **คุณค่าใดกำลังขัดแย้งกัน?**
        5. **เมื่อเข้าสู่วิชาชีพ เงื่อนไขอะไรจะเพิ่มเข้ามา?**
        """
    )
    st.info("💡 **Key Takeaway:** ไม่จำเป็นต้องสรุปว่า “คำตอบที่ถูกคืออะไร” ในทุกสถานการณ์ แต่เน้นกระบวนการคิดและตระหนักรู้ทางจริยธรรม")
    
    st.markdown("---")
    st.subheader("📝 บันทึกสรุปภาพรวมสำหรับผู้สอน (Instructor Summary)")
    with st.form("debrief_summary_form"):
        instructor_notes = st.text_area("พิมพ์สรุปผลการอภิปรายในห้องเรียน หรือประเด็นสำคัญที่ได้จากคลาสนี้:")
        sub_note = st.form_submit_button("บันทึกสรุปผลผู้สอน")

        if sub_note and instructor_notes:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Instructor Debrief",
                "Data": f"[Instructor] {instructor_notes}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึกสรุปผลผู้สอนลง Google Sheets สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")