import streamlit as st
import pdfplumber

st.set_page_config(page_title="MockMaster", layout="wide")

st.title("📘 MockMaster")
st.subheader("Upload PDF and Generate Mock Test")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    text = ""

    # Read PDF
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    st.success("PDF uploaded successfully!")

    lines = text.split("\n")

    questions = []
    current_question = None
    options = []

    # Extract Questions
    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith("Q") and "." in line:

            if current_question:
                questions.append({
                    "question": current_question,
                    "options": options
                })

            current_question = line
            options = []

        elif (
            line.startswith("A)")
            or line.startswith("B)")
            or line.startswith("C)")
            or line.startswith("D)")
        ):
            options.append(line)

    # Add Last Question
    if current_question:
        questions.append({
            "question": current_question,
            "options": options
        })

    st.success(f"Questions Found: {len(questions)}")

    # ANSWER KEY
    correct_answers = {
        0: "C) 29",
        1: "B) 12",
        2: "C) 36",
        3: "B) 135",
        4: "B) 1",
        5: "C) 2",
        6: "D) 22",
        7: "A) 5",
        8: "C) 24",
        9: "A) 81",
        10: "A) School",
        11: "A) Cut",
        12: "B) Den",
        13: "B) Glove",
        14: "A) Hunger",
        15: "B) Cat",
        16: "C) Cold",
        17: "A) Bird",
        18: "B) Hear",
        19: "C) Air",
        20: "B) Babur",
        21: "C) Gandhi",
        22: "B) 1757",
        23: "B) Shah Jahan",
        24: "C) 1942",
        25: "C) Chandragupta Maurya",
        26: "B) Agra",
        27: "B) Chanakya",
        28: "A) 1526",
        29: "B) Humayun",
        30: "D) Both A and C",
        31: "B) Sings",
        32: "C) Brave",
        33: "A) They",
        34: "C) Softly",
        35: "B) Boy",
        36: "A) Beautiful",
        37: "B) Fly",
        38: "A) We",
        39: "C) Correctly"
    }

    user_answers = {}

    # Show Questions
    for i, q in enumerate(questions):

        st.markdown(f"### {q['question']}")

        user_answers[i] = st.radio(
            "Choose Answer",
            q["options"],
            key=f"q{i}"
        )

        st.divider()

    # Submit Button
    if st.button("Submit Test"):

        score = 0
        wrong_questions = []

        for i, user_answer in user_answers.items():

            if i in correct_answers:

                if user_answer == correct_answers[i]:
                    score += 1

                else:
                    wrong_questions.append({
                        "question": questions[i]["question"],
                        "your_answer": user_answer,
                        "correct_answer": correct_answers[i]
                    })

        st.success(f"Your Score: {score}/{len(questions)}")

        st.write(f"✅ Correct Answers: {score}")
        st.write(f"❌ Wrong Answers: {len(wrong_questions)}")

        if wrong_questions:

            st.subheader("📋 Review Wrong Answers")

            for item in wrong_questions:

                st.error(item["question"])

                st.write(
                    f"**Your Answer:** {item['your_answer']}"
                )

                st.write(
                    f"**Correct Answer:** {item['correct_answer']}"
                )

                st.divider()