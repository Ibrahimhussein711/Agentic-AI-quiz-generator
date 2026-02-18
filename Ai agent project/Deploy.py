import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM

# 1. إعدادات الصفحة
st.set_page_config(page_title="AI Quiz Generator", page_icon="📝")

st.title("🤖 AI Agentic Quiz Generator")
st.write("This app uses 3 AI agents to research and create a quiz for you.")

# 2. القائمة الجانبية لإعدادات المفاتيح
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Groq API Key:", type="password")
    st.info("Get your key from [console.groq.com](https://console.groq.com)")
    
    # اختيار الموديل
    model_choice = st.selectbox("Choose Model:", 
                                ["groq/llama-3.3-70b-versatile", "groq/llama-3.1-8b-instant"])

# 3. واجهة المستخدم الرئيسية
topic = st.text_input("Enter the topic for your quiz:", placeholder="e.g. History of Rome")

if st.button("Generate Quiz"):
    if not api_key:
        st.error("Please provide a Groq API Key!")
    elif not topic:
        st.warning("Please enter a topic first!")
    else:
        # البدء في تنفيذ الـ Agents
        with st.spinner("🤖 Agents are collaborating... This may take 30-60 seconds."):
            try:
                # إعداد الموديل وخدعة OpenAI
                os.environ["OPENAI_API_KEY"] = "sk-dummy-key"
                my_llm = LLM(model=model_choice, api_key=api_key)

                # تعريف الوكلاء (Agents)
                researcher = Agent(
                    role='Educational Researcher',
                    goal=f'Identify 5 core educational facts about {topic}',
                    backstory='You are an expert academic researcher.',
                    llm=my_llm,
                    allow_delegation=False
                )

                quiz_creator = Agent(
                    role='Quiz Designer',
                    goal=f'Create 5 MCQs based on the facts provided',
                    backstory='Specialist in designing educational assessments.',
                    llm=my_llm,
                    allow_delegation=False
                )

                reviewer = Agent(
                    role='Quality Editor',
                    goal='Review and format the final quiz in professional Markdown',
                    backstory='Expert in quality control and clear formatting.',
                    llm=my_llm,
                    allow_delegation=False
                )

                # تعريف المهام (Tasks)
                t1 = Task(description=f'Search for 5 key facts about {topic}.', agent=researcher, expected_output='A list of 5 facts.')
                t2 = Task(description='Create 5 MCQs with A,B,C,D options and answers.', agent=quiz_creator, expected_output='A quiz draft.')
                t3 = Task(description='Finalize the quiz in Markdown format.', agent=reviewer, expected_output='The final formatted quiz.')

                # تشكيل الفريق
                crew = Crew(
                    agents=[researcher, quiz_creator, reviewer],
                    tasks=[t1, t2, t3],
                    process=Process.sequential,
                    memory=False
                )

                # تشغيل الفريق
                result = crew.kickoff()

                # عرض النتيجة النهائية
                st.success("✅ Quiz Created Successfully!")
                st.markdown("---")
                st.markdown(result.raw)
                
                # خيار التحميل
                st.download_button(label="Download Quiz as File", data=result.raw, file_name="quiz.md")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")