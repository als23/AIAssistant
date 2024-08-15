# import os

import openai
import streamlit as st


# client = openai.Client(
#     api_key = os.getenv("OPENAI_API_KEY")
# )

# Получение API ключа из secrets
api_key = st.secrets["openai"]["openai_api_key"]

# Инициализация клиента с использованием API ключа
client = openai.Client(api_key=api_key)

SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.

Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу
Потом представь результат в виде оценки от 1 до 10.
""".strip()

def request_gpt(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1000,
        temperature=0,
    )
    return response.choices[0].message.content


st.title('CV Scoring App')

job_description = st.text_area("Enter the job description")

cv = st.text_area("Enter the CV")

if st.button("Score CV"):
    with st.spinner("Scoring CV..."):
        user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv}"
        response = request_gpt(SYSTEM_PROMPT, user_prompt)
        # response = request_gpt('Score the CV based on the job description', f'Job description: {job_description}\nCV: {cv}')
    st.write(response)