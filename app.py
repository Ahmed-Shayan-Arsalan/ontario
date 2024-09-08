import streamlit as st
import random
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq

# API key and model initialization
groq_api_key = "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"
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant")

# Define prompts for agents (3rd-grade, 6th-8th grade, 9th grade, 10th grade)
question_generation_prompt_3rd = """
You are a question generator for 3rd-grade math. Generate 5 unique math questions DO NOT WRITE ANYTHING ELSE, JUST THE QUESTIONS. DO NOT REPEAT ANY QUESTIONS, DO NOT GIVE MCQS.
"""
question_generation_prompt_6th_8th = """
You are a question generator for 6th-8th grade students. You work on these questions Number Sense and Numeration: Understanding numbers, operations, and the relationships among them.
Measurement: Understanding and applying concepts of length, area, volume, capacity, mass, time, and temperature.
Geometry and Spatial Sense: Understanding properties of shapes, symmetry, transformations, and spatial reasoning.
Patterning and Algebra: Understanding patterns, relationships, and algebraic expressions.
Data Management and Probability: Collecting, organizing, displaying, and analyzing data; understanding and applying probability. Generate 5 unique math questions, DO NOT WRITE ANYTHING ELSE, JUST THE QUESTIONS. DO NOT REPEAT ANY QUESTIONS, DO NOT GIVE MCQS.
"""
question_generation_prompt_9th = """
You are a question generator for 9th grade students. You work on these questions: 
- Number Sense and Numeration: Linear Relations: Understanding and solving linear equations and inequalities.
- Measurement and Geometry: Exploring properties of geometric figures and relationships between them.
Generate 5 unique math questions. DO NOT WRITE ANYTHING ELSE, JUST THE QUESTIONS. DO NOT REPEAT ANY QUESTIONS, DO NOT GIVE MCQS.
"""
question_generation_prompt_10th = """
You are a question generator for 10th grade students. You work on these questions: 
Exploring quadratic equations, graphs, and their applications.
Generate exactly 5 unique math questions. DO NOT WRITE ANYTHING ELSE, JUST THE QUESTIONS. DO NOT REPEAT ANY QUESTIONS, DO NOT GIVE MCQS.
"""
question_generation_prompt_12th = """
You are a question generator for 12th grade students. You work on these questions: 
Advanced Functions (Grade 12): Deeper exploration of complex functions and their applications.
Calculus and Vectors (Grade 12): Introduction to the fundamentals of calculus and vector algebra.
Generate exactly 5 unique math questions. DO NOT WRITE ANYTHING ELSE, JUST THE QUESTIONS. DO NOT REPEAT ANY QUESTIONS, DO NOT GIVE MCQS.
"""

complexity_increase_prompt = """
You are a complexity enhancer. Take the following math questions and make them more challenging by adding additional steps, deeper concepts, or more complex numbers.
DO NOT WRITE ANYTHING ELSE, JUST THE QUESTIONS. DO NOT REPEAT ANY QUESTIONS
Questions: {questions}
"""

question_formatting_prompt = """
You are a document formatter. Separate the generated questions and store them in a document variable.
Questions: {questions}
"""

answer_check_prompt = """
You are an answer checker. Check if the provided answer is correct for the following question.
Question: {question}
Your Answer: {user_answer}
Please respond with "true" if the answer is correct and "false" if it is incorrect.
"""

feedback_prompt = """
You are a feedback provider. Provide feedback based on the user's answer.
Question: {question}
Your Answer: {user_answer}
Is Correct: {is_correct}
If the answer is correct, provide a congratulatory remark. If incorrect, provide the correct answer and encourage the user.
"""

# Create the question generation agents
question_agent_3rd = Agent(
    role="Math Question Generator",
    goal="Generate 5 unique math questions for 3rd graders. DO NOT WRITE ANYTHING ELSE, JUST THE QUESTIONS. DO NOT REPEAT ANY QUESTIONS, DO NOT GIVE MCQS",
    backstory=question_generation_prompt_3rd,
    allow_delegation=False,
    verbose=True,
    llm=llm
)

question_agent_6th_8th = Agent(
    role="Math Question Generator",
    goal="Generate 5 unique math questions for 6th-8th graders. DO NOT WRITE ANYTHING ELSE, JUST THE QUESTIONS. DO NOT REPEAT ANY QUESTIONS, DO NOT GIVE MCQS",
    backstory=question_generation_prompt_6th_8th,
    allow_delegation=False,
    verbose=True,
    llm=llm
)

question_agent_9th = Agent(
    role="Math Question Generator",
    goal="Generate 5 unique math questions for 9th graders. DO NOT WRITE ANYTHING ELSE, JUST THE QUESTIONS. DO NOT REPEAT ANY QUESTIONS, DO NOT GIVE MCQS",
    backstory=question_generation_prompt_9th,
    allow_delegation=False,
    verbose=True,
    llm=llm
)

question_agent_10th = Agent(
    role="Math Question Generator",
    goal="Generate exactly 5 unique math questions for 10th graders. DO NOT WRITE ANYTHING ELSE, JUST THE QUESTIONS. DO NOT REPEAT ANY QUESTIONS, DO NOT GIVE MCQS",
    backstory=question_generation_prompt_10th,
    allow_delegation=False,
    verbose=True,
    llm=llm
)

question_agent_12th = Agent(
    role="Math Question Generator",
    goal="Generate exactly 5 unique math questions for 12th graders. DO NOT WRITE ANYTHING ELSE, JUST THE QUESTIONS. DO NOT REPEAT ANY QUESTIONS, DO NOT GIVE MCQS",
    backstory=question_generation_prompt_12th,
    allow_delegation=False,
    verbose=True,
    llm=llm
)

complexity_agent = Agent(
    role="Complexity Enhancer",
    goal="Increase the complexity of the generated math questions.",
    backstory=complexity_increase_prompt,
    allow_delegation=False,
    verbose=True,
    llm=llm
)

document_agent = Agent(
    role="Document Formatter",
    goal="Format and store the generated questions in a document variable.",
    backstory=question_formatting_prompt,
    allow_delegation=False,
    verbose=True,
    llm=llm
)

answer_check_agent = Agent(
    role="Answer Checker",
    goal="Check if the user's answer is correct.",
    backstory=answer_check_prompt,
    allow_delegation=False,
    verbose=True,
    llm=llm
)

feedback_agent = Agent(
    role="Feedback Provider",
    goal="Provide feedback based on the user's answer.",
    backstory=feedback_prompt,
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# Streamlit app
def main():
    st.set_page_config(page_title="Ontario Math Arithmetic Test", page_icon="🧮", layout="wide")
    st.title("Ontario Math Arithmetic Test")

    # Session state initialization
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'feedbacks' not in st.session_state:
        st.session_state.feedbacks = []
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'quiz_complete' not in st.session_state:
        st.session_state.quiz_complete = False
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    # Sidebar for grade selection and quiz start
    with st.sidebar:
        st.header("Quiz Settings")
        grade_level = st.selectbox("Select Grade Level", [3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        start_quiz = st.button("Start Quiz")

        if start_quiz:
            with st.spinner("Generating questions..."):
                st.session_state.questions = generate_questions(grade_level)
            st.session_state.current_question = 0
            st.session_state.answers = []
            st.session_state.feedbacks = []
            st.session_state.score = 0
            st.session_state.quiz_complete = False
            st.session_state.submitted = False
            st.rerun()

    # Main quiz interface
    if st.session_state.questions:
        if not st.session_state.quiz_complete:
            question = st.session_state.questions[st.session_state.current_question]
            st.subheader(f"Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}")
            st.write(question)

            user_answer = st.text_input("Your Answer", key=f"answer_{st.session_state.current_question}")

            # Display feedback if submitted
            if st.session_state.submitted:
                st.write(f"**Feedback:** {st.session_state.feedbacks[st.session_state.current_question]}")
                st.write(f"**Your Answer:** {st.session_state.answers[st.session_state.current_question]}")

            col1, col2 = st.columns(2)

            with col1:
                if not st.session_state.submitted:
                    if st.button("Submit Answer"):
                        with st.spinner("Checking answer..."):
                            is_correct, feedback = check_answer(question, user_answer)
                        st.session_state.answers.append(user_answer)
                        st.session_state.feedbacks.append(feedback)
                        st.session_state.submitted = True
                        if is_correct:
                            st.session_state.score += 1
                        st.rerun()

            with col2:
                if st.session_state.submitted:
                    if st.button("Next"):
                        if st.session_state.current_question < len(st.session_state.questions) - 1:
                            st.session_state.current_question += 1
                            st.session_state.submitted = False
                        else:
                            st.session_state.quiz_complete = True
                        st.rerun()

        else:
            st.header("Quiz Complete!")
            score_percentage = (st.session_state.score / len(st.session_state.questions)) * 100
            st.subheader(f"Your Score: {score_percentage:.2f}%")
            
            if score_percentage >= 75:
                st.success("Congratulations! You have passed the Ontario math arithmetic test.")
            else:
                st.error("Unfortunately, you have not passed the Ontario math arithmetic test.")

            # Display results in an expandable section
            with st.expander("See Detailed Results"):
                for i, (question, answer, feedback) in enumerate(zip(st.session_state.questions, st.session_state.answers, st.session_state.feedbacks)):
                    st.write(f"**Question {i+1}:** {question}")
                    st.write(f"**Your Answer:** {answer}")
                    st.write(f"**Feedback:** {feedback}")
                    st.write("---")

            if st.button("Restart Quiz"):
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()

# Function to generate questions based on grade level
def generate_questions(grade_level):
    if grade_level in [3, 4, 5]:
        selected_question_agent = question_agent_3rd
    elif grade_level in [6, 7, 8]:
        selected_question_agent = question_agent_6th_8th
    elif grade_level == 9:
        selected_question_agent = question_agent_9th
    elif grade_level in [10, 11]:
        selected_question_agent = question_agent_10th
    elif grade_level == 12:
        selected_question_agent = question_agent_12th

    question_task = Task(
        description="Generate 5 unique math questions.",
        agent=selected_question_agent,
        expected_output="A list of 5 unique math questions"
    )

    crew = Crew(
        agents=[selected_question_agent],
        tasks=[question_task],
        verbose=2
    )

    question_result = crew.kickoff()
    questions = [q.strip() for q in question_result.strip().split("\n") if q.strip()]

    if grade_level in [9, 10, 12]:
        complexity_task = Task(
            description=complexity_increase_prompt.format(questions="\n".join(questions)),
            agent=complexity_agent,
            expected_output="A list of 5 more complex math questions"
        )

        crew = Crew(
            agents=[complexity_agent],
            tasks=[complexity_task],
            verbose=2
        )

        complex_question_result = crew.kickoff()
        questions = [q.strip() for q in complex_question_result.strip().split("\n") if q.strip()]

    return questions[:5]  # Ensure we have exactly 5 questions

# Function to check answer and provide feedback
def check_answer(question, user_answer):
    answer_check_task = Task(
        description=answer_check_prompt.format(question=question, user_answer=user_answer),
        agent=answer_check_agent,
        expected_output="True or False"
    )

    crew = Crew(
        agents=[answer_check_agent],
        tasks=[answer_check_task],
        verbose=2
    )

    answer_check_result = crew.kickoff()
    is_correct = answer_check_result.strip().lower() == "true"

    feedback_task = Task(
        description=feedback_prompt.format(question=question, user_answer=user_answer, is_correct=is_correct),
        agent=feedback_agent,
        expected_output="Feedback on the user's answer"
    )

    crew = Crew(
        agents=[feedback_agent],
        tasks=[feedback_task],
        verbose=2
    )

    feedback_result = crew.kickoff()
    feedback = feedback_result.strip()

    return is_correct, feedback

if __name__ == "__main__":
    main()
