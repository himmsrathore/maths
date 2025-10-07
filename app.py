import streamlit as st
import random

# Initialize session state
if 'correct' not in st.session_state:
    st.session_state.correct = 0  # Total correct answers
    st.session_state.total = 0    # Total attempts
    st.session_state.level = 1    # Start at Level 1
    st.session_state.correct_in_level = 0  # Correct answers in current level
    st.session_state.num1 = random.randint(10, 99)
    st.session_state.num2 = random.randint(10, 99)
    st.session_state.operator = random.choice(['+', '-'])  # Level 1: only + and -
    st.session_state.correct_answer = None
    st.session_state.correct_to_advance = 5  # Number of correct answers to level up

# Function to get level parameters
def get_level_params(level):
    if level == 1:
        return ['+', '-'], (10, 99), 0.01  # Operators, number range, tolerance
    elif level == 2:
        return ['+', '-', '*'], (10, 99), 0.01
    elif level == 3:
        return ['+', '-', '*', '/'], (10, 99), 0.01
    elif level >= 4:
        max_num = 99 + (level - 3) * 100  # Increase range: 199, 299, ..., 999
        tolerance = max(0.001, 0.01 / (level - 2))  # Tighter tolerance
        return ['+', '-', '*', '/'], (10, max_num), tolerance

# Function to generate a new problem
def generate_problem():
    operators, (min_num, max_num), _ = get_level_params(st.session_state.level)
    st.session_state.num1 = random.randint(min_num, max_num)
    st.session_state.num2 = random.randint(min_num, max_num)
    st.session_state.operator = random.choice(operators)
    
    # Calculate correct answer
    if st.session_state.operator == '+':
        st.session_state.correct_answer = st.session_state.num1 + st.session_state.num2
    elif st.session_state.operator == '-':
        st.session_state.correct_answer = st.session_state.num1 - st.session_state.num2
    elif st.session_state.operator == '*':
        st.session_state.correct_answer = st.session_state.num1 * st.session_state.num2
    else:  # Division: Ensure whole number result
        st.session_state.correct_answer = st.session_state.num1 // st.session_state.num2
        st.session_state.num1 = st.session_state.correct_answer * st.session_state.num2

# Set correct answer for initial problem
if st.session_state.correct_answer is None:
    generate_problem()

# Layout: Two columns (left for problem, right for score)
col1, col2 = st.columns([3, 1])

# Left column: Problem and input
with col1:
    st.title("Math Game")
    # Display level and instructions
    st.write(f"**Level {st.session_state.level}**: Solve {st.session_state.correct_to_advance - st.session_state.correct_in_level} more to level up!")
    
    # Display problem in large font
    problem = f"{st.session_state.num1} <span style='font-size:60px'>{st.session_state.operator}</span> {st.session_state.num2} = "
    st.markdown(f"<h2 style='font-size:40px'>{problem}</h2>", unsafe_allow_html=True)

    # User input for answer
    user_answer = st.text_input("Your answer:", key=f"answer_input_{st.session_state.total}")

    # Submit button
    if st.button("Submit"):
        if user_answer:
            try:
                user_answer = float(user_answer)
                st.session_state.total += 1
                # Get tolerance for current level
                _, _, tolerance = get_level_params(st.session_state.level)
                # Check if answer is correct
                if abs(user_answer - st.session_state.correct_answer) < tolerance:
                    st.session_state.correct += 1
                    st.session_state.correct_in_level += 1
                    st.success("Correct!")
                    # Check for level-up
                    if st.session_state.correct_in_level >= st.session_state.correct_to_advance:
                        if st.session_state.level < 10:
                            st.session_state.level += 1
                            st.session_state.correct_in_level = 0
                            st.balloons()  # Celebration animation
                            st.write(f"🎉 Leveled up to Level {st.session_state.level}!")
                        else:
                            st.write("🎉 Max Level (10) Reached! Keep playing!")
                    generate_problem()  # Auto-generate new problem
                else:
                    st.error(f"Wrong! The correct answer was {st.session_state.correct_answer}")
            except ValueError:
                st.error("Please enter a valid number!")
        else:
            st.warning("Please enter an answer!")

    # Refresh button
    if st.button("Refresh Problem"):
        generate_problem()

# Right column: Score and level display
with col2:
    st.subheader("Score")
    st.write(f"Level: {st.session_state.level}")
    st.write(f"Correct: {st.session_state.correct}")
    st.write(f"Total: {st.session_state.total}")
    if st.session_state.total > 0:
        accuracy = (st.session_state.correct / st.session_state.total) * 100
        st.write(f"Accuracy: {accuracy:.2f}%")