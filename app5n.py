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
if "lab5_page" not in st.session_state:
    st.session_state.lab5_page = 1

# --- Sidebar เมนูด้านซ้าย (12 หน้า) ---
st.sidebar.markdown("### 🎙️ LAB 5 Workflow")

pages_name = {
    1: "Page 1 — Welcome to Lab 5",
    2: "Page 2 — Connect",
    3: "Page 3 — Pre-talk Vote",
    4: "Page 4 — Meet the Professional",
    5: "Page 5 — Ethics Listening Card",
    6: "Page 6 — Ask the Professional",
    7: "Page 7 — Reality vs Classroom",
    8: "Page 8 — Ethical Insight",
    9: "Page 9 — Group Synthesis",
    10: "Page 10 — What Would You Prepare?",
    11: "Page 11 — My Professional Preparation",
    12: "Page 12 — Exit Reflection",
}

current_index = list(pages_name.keys()).index(st.session_state.lab5_page)

selected_page_name = st.sidebar.radio(
    "เลือกหน้า LAB 5:",
    list(pages_name.values()),
    index=current_index,
    key="lab5_menu_selection",
)

for p_num, p_title in pages_name.items():
    if p_title == selected_page_name:
        st.session_state.lab5_page = p_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อด้านบนเพื่อเปลี่ยนหน้ากิจกรรม")


# ==========================================
# Page 1 — Welcome to Lab 5
# ==========================================
if st.session_state.lab5_page == 1:
    st.title("🎙️ Lab 5: เรียนรู้จริยธรรมจากประสบการณ์วิชาชีพ")
    st.markdown("### “จากสิ่งที่เราเรียนรู้ในห้องเรียน สู่การตัดสินใจในโลกการทำงานจริง”")
    st.markdown("---")
    st.info(
        """
        ### 📌 ข้อความแนะนำ:
        “วันนี้ไม่ใช่การค้นหาว่าเภสัชกรต้องเป็นคนสมบูรณ์แบบ แต่เป็นการเรียนรู้ว่าผู้ประกอบวิชาชีพคิด ตัดสินใจ และเรียนรู้จากประสบการณ์อย่างไร”
        """
    )


# ==========================================
# Page 2 — Connect: What Makes Ethics Difficult?
# ==========================================
elif st.session_state.lab5_page == 2:
    st.title("🌉 Page 2 — Connect: What Makes Ethics Difficult?")
    st.markdown("### ชวนคิดก่อนฟังวิทยากร")
    st.warning("“คุณคิดว่าการเป็นเภสัชกรที่มีจริยธรรมในสถานการณ์จริง ยากกว่าการตอบข้อสอบจริยธรรมหรือไม่ เพราะอะไร?”")

    with st.form("lab5_p2_form"):
        student_id = st.text_input("รหัสนิสิต:")
        connect_choice = st.radio(
            "เลือกมุมมองของคุณ:",
            [
                "ยากกว่า",
                "พอ ๆ กัน",
                "ไม่จำเป็นต้องยากกว่า",
                "ขึ้นอยู่กับสถานการณ์"
            ]
        )
        reason_c = st.text_input("เหตุผลสั้น ๆ ประกอบ:")
        sub_p2 = st.form_submit_button("ส่งคำตอบ Connect")

        if sub_p2 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Page2 Connect",
                "Data": f"[{student_id}] Choice: {connect_choice} | Note: {reason_c}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p2:
            st.warning("กรุณากรอกรหัสนิสิต")


# ==========================================
# Page 3 — Pre-talk Vote
# ==========================================
elif st.session_state.lab5_page == 3:
    st.title("🗳️ Page 3 — Pre-talk Vote")
    st.markdown("### “อะไรน่าจะเป็นความท้าทายสำคัญที่สุดในการรักษาจริยธรรมเมื่อทำงานจริง?”")

    with st.form("lab5_p3_form"):
        student_id = st.text_input("รหัสนิสิต:")
        pretalk_choice = st.radio(
            "เลือกความท้าทายที่สำคัญที่สุด:",
            [
                "A. ความรู้หรือประสบการณ์ไม่เพียงพอ",
                "B. ความต้องการของผู้ป่วยหรือผู้รับบริการ",
                "C. แรงกดดันจากผู้บังคับบัญชาหรือองค์กร",
                "D. ผลประโยชน์หรือข้อจำกัดด้านทรัพยากร",
                "E. ความขัดแย้งระหว่างหลักจริยธรรมหลายประการ",
                "F. อื่น ๆ"
            ]
        )
        sub_p3 = st.form_submit_button("ส่ง Pre-talk Vote")

        if sub_p3 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Page3 PretalkVote",
                "Data": f"[{student_id}] Vote: {pretalk_choice[0]}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("บันทึก Pre-talk Vote สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p3:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 ผลโหวต Pre-talk Vote ภาพรวมห้อง")
    if conn:
        try:
            df = conn.read(worksheet="Lab5_Responses", ttl=5)
            p3_df = df[df["Step"] == "Lab5 - Page3 PretalkVote"]
            if not p3_df.empty:
                votes = p3_df["Data"].apply(lambda x: x.split("Vote: ")[1].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
        except:
            pass


# ==========================================
# Page 4 — Meet the Professional
# ==========================================
elif st.session_state.lab5_page == 4:
    st.title("👤 Page 4 — Meet the Professional")
    st.markdown("### ข้อมูลวิทยากรรับเชิญ")
    st.info(
        """
        - **ชื่อและตำแหน่ง:** (อัปเดตตามวิทยากรประจำเซสชัน)  
        - **สถานที่หรือประเภทการปฏิบัติงาน:** โรงพยาบาล / ชุมชน / อุตสาหกรรม  
        - **ประสบการณ์ที่เกี่ยวข้อง:** ประสบการณ์เผชิญหน้าและจัดการกับปัญหาความขัดแย้งทางจริยธรรม  
        """
    )
    st.markdown("---")
    st.markdown("### คำถามนำก่อนฟัง:")
    st.warning("“ระหว่างฟัง คุณจะสังเกตอะไรเพื่อให้เข้าใจเหตุผลเบื้องหลังการตัดสินใจของวิทยากร?”")

    with st.form("lab5_p4_form"):
        student_id = st.text_input("รหัสนิสิต:")
        observe_choice = st.checkbox("ข้อเท็จจริงของสถานการณ์")
        observe_choice2 = st.checkbox("ผู้ที่ได้รับผลกระทบ")
        observe_choice3 = st.checkbox("ทางเลือกที่มี")
        observe_choice4 = st.checkbox("เหตุผลในการตัดสินใจ")
        observe_choice5 = st.checkbox("บทเรียนที่ได้รับ")
        sub_p4 = st.form_submit_button("บันทึกจุดสังเกต")

        if sub_p4 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Page4 ObservePrep",
                "Data": f"[{student_id}] Ready to listen"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p4:
            st.warning("กรุณากรอกรหัสนิสิต")


# ==========================================
# Page 5 — Ethics Listening Card
# ==========================================
elif st.session_state.lab5_page == 5:
    st.title("📋 Page 5 — Ethics Listening Card")
    st.markdown("### เลือกหนึ่งประสบการณ์จากที่วิทยากรถ่ายทอด แล้วบันทึกประเด็นสำคัญ")

    with st.form("lab5_p5_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        
        c1 = st.text_area("1. Situation: เกิดอะไรขึ้น?")
        c2 = st.text_area("2. Ethical Challenge: อะไรทำให้ตัดสินใจยาก?")
        c3 = st.text_area("3. Stakeholders: ใครได้รับผลกระทบ?")
        c4 = st.text_area("4. Decision: วิทยากรตัดสินใจอย่างไร?")
        c5 = st.text_area("5. Reasoning: เหตุผลใดมีความสำคัญ?")
        c6 = st.text_area("6. Lesson: คุณได้เรียนรู้อะไร?")
        
        sub_p5 = st.form_submit_button("ส่ง Ethics Listening Card")

        if sub_p5 and group_name:
            combined_card = f"Sit:{c1}|Chal:{c2}|Stake:{c3}|Dec:{c4}|Reas:{c5}|Lesson:{c6}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Page5 ListeningCard",
                "Data": f"[{group_name}] {combined_card}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("บันทึก Listening Card สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p5:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางรวบรวม Listening Card ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab5_Responses", ttl=5)
            p5_df = df[df["Step"] == "Lab5 - Page5 ListeningCard"]
            if not p5_df.empty:
                st.dataframe(p5_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# Page 6 — Ask the Professional
# ==========================================
elif st.session_state.lab5_page == 6:
    st.title("🙋‍♂️ Page 6 — Ask the Professional")
    st.markdown("### “หากคุณมีโอกาสถามวิทยากรได้หนึ่งคำถาม คุณอยากรู้อะไรเพื่อให้เข้าใจการตัดสินใจทางจริยธรรมในโลกการทำงานจริงมากขึ้น?”")
    st.info("💡 ส่ง 1 คำถามต่อกลุ่ม (เน้นเหตุผล ทางเลือก ข้อจำกัด หรือบทเรียน | ไม่ถามข้อมูลลับหรือชื่อบุคคล)")

    with st.form("lab5_p6_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        question_text = st.text_area("พิมพ์คำถามถึงวิทยากร:")
        sub_p6 = st.form_submit_button("ส่งคำถามถึงวิทยากร")

        if sub_p6 and group_name and question_text:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Page6 QnA",
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
        elif sub_p6:
            st.warning("กรุณากรอกชื่อกลุ่มและคำถาม")

    st.markdown("---")
    st.subheader("📋 รายการคำถามจากกลุ่มทั้งหมด")
    if conn:
        try:
            df = conn.read(worksheet="Lab5_Responses", ttl=5)
            p6_df = df[df["Step"] == "Lab5 - Page6 QnA"]
            if not p6_df.empty:
                st.dataframe(p6_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# Page 7 — Reality vs Classroom
# ==========================================
elif st.session_state.lab5_page == 7:
    st.title("🔄 Page 7 — Reality vs Classroom")
    st.markdown("### เปรียบเทียบประสบการณ์ของวิทยากรกับหลักคิดทางจริยธรรมที่เรียนมา")

    with st.form("lab5_p7_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        q1 = st.text_area("1. อะไรสอดคล้องกับสิ่งที่เรียน?")
        q2 = st.text_area("2. อะไรแตกต่างจากที่คาดไว้?")
        q3 = st.text_area("3. ข้อจำกัดใดในโลกจริงที่ทำให้การตัดสินใจยากขึ้น?")
        
        sub_p7 = st.form_submit_button("ส่งผล Reality vs Classroom")

        if sub_p7 and group_name:
            combined_rc = f"Match: {q1} | Diff: {q2} | Limit: {q3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Page7 RealityVsClass",
                "Data": f"[{group_name}] {combined_rc}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p7:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Reality vs Classroom ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab5_Responses", ttl=5)
            p7_df = df[df["Step"] == "Lab5 - Page7 RealityVsClass"]
            if not p7_df.empty:
                st.dataframe(p7_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# Page 8 — Ethical Insight
# ==========================================
elif st.session_state.lab5_page == 8:
    st.title("💡 Page 8 — Ethical Insight")
    st.markdown("### “จากประสบการณ์ที่ฟัง คุณคิดว่าหลักคิดหรือคุณค่าใดสำคัญที่สุดต่อการตัดสินใจในสถานการณ์นั้น และเพราะอะไร?”")

    insight_options = [
        "ความซื่อสัตย์", "ความรับผิดชอบ", "ความเป็นธรรม",
        "การคำนึงถึงผู้ป่วยหรือผู้รับบริการ", "ความปลอดภัย",
        "การทำงานร่วมกับผู้อื่น", "การปฏิบัติตามมาตรฐานและข้อกำหนด", "อื่น ๆ"
    ]

    with st.form("lab5_p8_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        selected_insights = []
        st.markdown("เลือกคุณค่าหลัก (1-2 ข้อ):")
        for ins in insight_options:
            if st.checkbox(ins, key=f"l5_ins_{ins}"):
                selected_insights.append(ins)
                
        insight_reason = st.text_area("อธิบายเหตุผลโดยอ้างอิงข้อมูลจากประสบการณ์ที่วิทยากรถ่ายทอด:")
        
        sub_p8 = st.form_submit_button("ส่ง Ethical Insight")

        if sub_p8 and group_name:
            if 0 < len(selected_insights) <= 2:
                joined_ins = ", ".join(selected_insights)
                combined_ei = f"Values: {joined_ins} | Reason: {insight_reason}"
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab5 - Page8 Insight",
                    "Data": f"[{group_name}] {combined_ei}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab5_Responses", data=updated)
                        st.success("บันทึกสำเร็จ!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else:
                    st.success("บันทึกจำลองสำเร็จ!")
            else:
                st.warning("กรุณาเลือกคุณค่า 1-2 ข้อเท่านั้น")
        elif sub_p8:
            st.warning("กรุณากรอกชื่อกลุ่ม")


# ==========================================
# Page 9 — Group Synthesis
# ==========================================
elif st.session_state.lab5_page == 9:
    st.title("🎯 Page 9 — Group Synthesis")
    st.markdown("### สรุปสิ่งที่กลุ่มเรียนรู้จากประสบการณ์วิชาชีพ (ส่ง 3 ข้อ)")

    with st.form("lab5_p9_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        syn1 = st.text_area("1. หลักคิดทางจริยธรรมที่ได้เรียนรู้:")
        syn2 = st.text_area("2. ความท้าทายที่ผู้ประกอบวิชาชีพต้องเผชิญ:")
        syn3 = st.text_area("3. แนวทางที่นิสิตสามารถนำไปใช้ในการทำงานจริง:")
        
        sub_p9 = st.form_submit_button("ส่ง Group Synthesis")

        if sub_p9 and group_name:
            combined_syn = f"1.Principle: {syn1} | 2.Challenge: {syn2} | 3.Action: {syn3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Page9 Synthesis",
                "Data": f"[{group_name}] {combined_syn}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p9:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางสรุป Group Synthesis ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab5_Responses", ttl=5)
            p9_df = df[df["Step"] == "Lab5 - Page9 Synthesis"]
            if not p9_df.empty:
                st.dataframe(p9_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# Page 10 — What Would You Prepare?
# ==========================================
elif st.session_state.lab5_page == 10:
    st.title("🎒 Page 10 — What Would You Prepare?")
    st.markdown("### “จากประสบการณ์ที่ฟัง คุณคิดว่าตนเองควรเตรียมความพร้อมเรื่องใดก่อนออกไปปฏิบัติงานจริง?”")

    with st.form("lab5_p10_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        prep1 = st.text_input("สิ่งที่ต้องเรียนรู้เพิ่มเติม:")
        prep2 = st.text_input("ทักษะที่ต้องฝึก:")
        prep3 = st.text_area("วิธีที่ตนเองจะเริ่มเตรียมตัว:")
        
        sub_p10 = st.form_submit_button("ส่งการเตรียมความพร้อม")

        if sub_p10 and group_name:
            combined_prep = f"Learn: {prep1} | Skill: {prep2} | How: {prep3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Page10 Prepare",
                "Data": f"[{group_name}] {combined_prep}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p10:
            st.warning("กรุณากรอกชื่อกลุ่ม")


# ==========================================
# Page 11 — My Professional Preparation
# ==========================================
elif st.session_state.lab5_page == 11:
    st.title("🎯 Page 11 — My Professional Preparation")
    st.markdown("### เขียนแผนพัฒนาตนเองหนึ่งข้อที่เป็นรูปธรรม (รายบุคคล)")
    st.info("ตัวอย่าง: “เมื่อพบสถานการณ์ที่ไม่แน่ใจ ฉันจะ ______ ก่อนตัดสินใจ เพราะ ______” หรือ “ทักษะทางจริยธรรมที่ฉันต้องการฝึกเพิ่มคือ ______ และฉันจะฝึกโดย ______”")

    with st.form("lab5_p11_form"):
        student_id = st.text_input("รหัสนิสิต:")
        my_plan = st.text_area("แผนพัฒนาตนเองของฉัน:")
        sub_p11 = st.form_submit_button("ส่งแผนพัฒนาตนเอง")

        if sub_p11 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Page11 MyPlan",
                "Data": f"[{student_id}] Plan: {my_plan}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p11:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางรวบรวมแผนพัฒนาตนเองของนิสิต")
    if conn:
        try:
            df = conn.read(worksheet="Lab5_Responses", ttl=5)
            p11_df = df[df["Step"] == "Lab5 - Page11 MyPlan"]
            if not p11_df.empty:
                st.dataframe(p11_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# Page 12 — Exit Reflection
# ==========================================
elif st.session_state.lab5_page == 12:
    st.title("🎯 Page 12 — Exit Reflection")
    st.markdown("ตอบรายบุคคล (บันทึกเป็นหลักฐานการเรียนรู้)")

    with st.form("lab5_p12_form"):
        student_id = st.text_input("รหัสนิสิต (ระบุหรือไม่ระบุก็ได้):")
        
        r1 = st.text_area("1. สิ่งที่ทำให้ฉันมองวิชาชีพต่างจากเดิมคือ...")
        r2 = st.text_area("2. บทเรียนทางจริยธรรมที่สำคัญที่สุดสำหรับฉันคือ...")
        r3 = st.text_area("3. สิ่งหนึ่งที่ฉันจะเริ่มเตรียมตัวตั้งแต่วันนี้คือ...")
        
        sub_ref = st.form_submit_button("ส่ง Exit Reflection Lab 5")

        if sub_ref and student_id:
            sid_val = "Anonymous" if not student_id else student_id
            combined_ref = f"Diff: {r1} | Lesson: {r2} | StartToday: {r3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab5 - Exit Reflection",
                "Data": f"[{sid_val}] {combined_ref}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab5_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab5_Responses", data=updated)
                    st.success("บันทึก Exit Reflection สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_ref:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางรวบรวม Exit Reflection (Lab 5)")
    if conn:
        try:
            df = conn.read(worksheet="Lab5_Responses", ttl=5)
            ref_df = df[df["Step"] == "Lab5 - Exit Reflection"]
            if not ref_df.empty:
                st.dataframe(ref_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass