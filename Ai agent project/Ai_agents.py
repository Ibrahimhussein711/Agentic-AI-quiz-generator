import os
from crewai import Agent, Task, Crew, Process, LLM

# 1. إعداد مفتاح Groq الحقيقي الخاص بك
MY_KEY = "" # ضع مفتاحك هنا

# 2. تعريف الموديل الحديث (Llama 3.3 70B)
# ملاحظة: تم تغيير الاسم ليتوافق مع تحديثات Groq الأخيرة
my_model = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=MY_KEY
)

# 3. تعريف الوكلاء (Agents)
researcher = Agent(
    role='Educational Researcher',
    goal='Research 5 essential facts about {topic}',
    backstory='Expert in academic research and content simplification.',
    llm=my_model,
    verbose=True,
    allow_delegation=False
)

quiz_creator = Agent(
    role='Quiz Designer',
    goal='Create 5 multiple choice questions based on the research',
    backstory='Specialist in creating educational assessments.',
    llm=my_model,
    verbose=True,
    allow_delegation=False
)

reviewer = Agent(
    role='Quality Editor',
    goal='Format the quiz professionally in Markdown',
    backstory='Expert in quality control and formatting.',
    llm=my_model,
    verbose=True,
    allow_delegation=False
)

# 4. تعريف المهام (Tasks)
task1 = Task(
    description='Search for {topic} and provide 5 core facts.',
    agent=researcher,
    expected_output='A bulleted list of 5 facts.'
)

task2 = Task(
    description='Create 5 MCQs (A, B, C, D) with correct answers based on the facts.',
    agent=quiz_creator,
    expected_output='A quiz draft with questions and answers.'
)

task3 = Task(
    description='Format the final quiz perfectly in Markdown.',
    agent=reviewer,
    expected_output='The final formatted quiz.'
)

# 5. تشكيل الفريق
crew = Crew(
    agents=[researcher, quiz_creator, reviewer],
    tasks=[task1, task2, task3],
    process=Process.sequential,
    memory=False 
)

if __name__ == "__main__":
    # مفتاح وهمي فقط لتجاوز قيود المكتبة الداخلية
    os.environ["OPENAI_API_KEY"] = "sk-123456789012345678901234567890123456789012345678"
    
    print("\n--- AI Quiz Generator is starting ---")
    user_topic = input("What topic do you want a quiz for? ")
    
    result = crew.kickoff(inputs={'topic': user_topic})
    
    print("\n\n" + "="*30)
    print("DONE! HERE IS YOUR QUIZ:")
    print("="*30 + "\n")
    print(result)