import streamlit as st
import random

# Initialize session state for score and problem
if 'correct' not in st.session_state:
    st.session_state.correct = 0
    st.session_state.total = 0
    st.session_state.num1 = random.randint(10, 99)
    st.session_state.num2 = random.randint(10, 99)
    st.session_state.operator = random.choice(['+', '-', '*', '/'])
    st.session_state.correct_answer = None  # Initialize as None

# Function to generate a new problem and set correct answer
def generate_problem():
    st.session_state.num1 = random.randint(10, 99)
    st.session_state.num2 = random.randint(10, 99)
    st.session_state.operator = random.choice(['+', '-', '*', '/'])
    
    # Calculate correct answer
    if st.session_state.operator == '+':
        st.session_state.correct_answer = st.session_state.num1 + st.session_state.num2
    elif st.session_state.operator == '-':
        st.session_state.correct_answer = st.session_state.num1 - st.session_state.num2
    elif st.session_state.operator == '*':
        st.session_state.correct_answer = st.session_state.num1 * st.session_state.num2
    else:  # Division: Ensure whole number result
        st.session_state.correct_answer = st.session_state.num1 // st.session_state.num2
        st.session_state.num1 = st.session_state.correct_answer * st.session_state.num2  # Adjust num1

# Set correct answer for initial problem
if st.session_state.correct_answer is None:
    generate_problem()

# Layout: Two columns (left for problem, right for score)
col1, col2 = st.columns([3, 1])

# Left column: Problem and input
with col1:
    st.title("Math Game")
    # Display the problem
    problem = f"{st.session_state.num1} {st.session_state.operator} {st.session_state.num2} = "
    st.write(f"**Solve**: {problem}")

    # User input for answer
    user_answer = st.text_input("Your answer:", key="answer_input")
    
    # Submit button
    if st.button("Submit"):
        if user_answer:
            try:
                user_answer = float(user_answer)
                st.session_state.total += 1
                # Check if answer is correct
                if abs(user_answer - st.session_state.correct_answer) < 0.01:  # Allow small float errors for division
                    st.session_state.correct += 1
                    st.success("Correct!")
                else:
                    st.error(f"Wrong! The correct answer was {st.session_state.correct_answer}")
                # Generate new problem after submission
                generate_problem()
            except ValueError:
                st.error("Please enter a valid number!")
        else:
            st.warning("Please enter an answer!")

# Right column: Score display
with col2:
    st.subheader("Score")
    st.write(f"Correct: {st.session_state.correct}")
    st.write(f"Total: {st.session_state.total}")
    if st.session_state.total > 0:
        accuracy = (st.session_state.correct / st.session_state.total) * 100
        st.write(f"Accuracy: {accuracy:.2f}%")