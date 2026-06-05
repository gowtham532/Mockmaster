import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="MockMaster", layout="wide")


# ---------------------------
# READ PDF
# ---------------------------
def read_pdf(uploaded_file):
    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


# ---------------------------
# EXTRACT QUESTIONS
# ---------------------------
def extract_questions(text):

    pattern = r'(Q\d+\..*?)(?=Q\d+\.|\Z)'

    blocks = re.findall(pattern, text, re.S)

    questions = []

    for block in blocks:

        lines = [x.strip() for x in block.split("\n") if x.strip()]

        if len(lines) < 5:
            continue

        question = lines[0]

        options = []

        for line in lines[1:]:

            if re.match(r'^[A-D]\.', line):
                options.append(line)

        if len(options) == 4:

            questions.append({
                "question": question,
                "options": options
            })

    return questions


# ---------------------------
# EXTRACT ANSWERS
# ---------------------------
def extract_answers(text):

    answers = {}

    matches = re.findall(
        r'(\d+)\s*[\.\:\-\)]\s*([A-D])',
        text,
        re.I
    )

    for qno, ans in matches:
        answers[int(qno)] = ans.upper()

    return answers


# ---------------------------
# UI
# ---------------------------
st.title("📘 MockMaster")
st.subheader("Upload Question PDF and Answer PDF")

question_pdf = st.file_uploader(
    "Upload Questions PDF",
    type=["pdf"]
)

answer_pdf = st.file_uploader(
    "Upload Answer PDF",
    type=["pdf"]
)

if question_pdf and answer_pdf:

    question_text = read_pdf(question_pdf)
    answer_text = read_pdf(answer_pdf)

    questions = extract_questions(question_text)
    st.write("Questions Found:", len(questions))
    answer_key = extract_answers(answer_text)

    st.success(f"{len(questions)} Questions Loaded")
    st.success(f"{len(answer_key)} Answers Loaded")

    if len(questions) == 0:
        st.error("No questions detected from PDF.")
        st.text_area(
            "Extracted Text",
            question_text[:10000],
            height=400
        )
        st.stop()

    user_answers = {}

    for i, q in enumerate(questions, start=1):

        st.markdown(f"## Q{i}")

        st.write(q["question"])

        user_answers[i] = st.radio(
            "Choose Answer",
            q["options"],
            key=f"q_{i}"
        )

        st.divider()

    if st.button("Submit Test"):

        score = 0

        st.header("Results")

        for i in range(1, len(questions) + 1):

            selected = user_answers.get(i)

            if not selected:
                continue

            user_letter = selected[0].upper()

            correct_answer = answer_key.get(i)

            if user_letter == correct_answer:

                score += 1

                st.success(
                    f"Q{i} ✓ Correct"
                )

            else:

                st.error(
                    f"Q{i} ✗ Incorrect"
                )

            st.write(
                f"Your Answer: {user_letter}"
            )

            st.write(
                f"Correct Answer: {correct_answer}"
            )

            st.write("---")

        st.success(
            f"Final Score: {score}/{len(questions)}"
        )