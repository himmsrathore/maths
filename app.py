import streamlit as st
import random
import time
from datetime import datetime
import pandas as pd  # Moved to top to avoid NameError

# Initialize session state
if 'correct' not in st.session_state:
    st.session_state.correct = 0
    st.session_state.total = 0
    st.session_state.level = 1
    st.session_state.correct_in_level = 0
    st.session_state.problems = []  # List to store problem history
    st.session_state.start_time = None
    st.session_state.num1 = random.randint(10, 99)
    st.session_state.num2 = random.randint(10, 99)
    st.session_state.operator = random.choice(['+', '-'])
    st.session_state.correct_answer = None
    st.session_state.correct_to_advance = 5

# Function to get level parameters
def get_level_params(level):
    if level == 1:
        return ['+', '-'], (10, 99), 0.01
    elif level == 2:
        return ['+', '-', '*'], (10, 99), 0.01
    elif level == 3:
        return ['+', '-', '*', '/'], (10, 99), 0.01
    elif level >= 4:
        max_num = 99 + (level - 3) * 100
        tolerance = max(0.001, 0.01 / (level - 2))
        return ['+', '-', '*', '/'], (10, max_num), tolerance

# Function to generate a new problem (no negative results)
def generate_problem():
    operators, (min_num, max_num), _ = get_level_params(st.session_state.level)
    st.session_state.num1 = random.randint(min_num, max_num)
    st.session_state.num2 = random.randint(min_num, max_num)
    st.session_state.operator = random.choice(operators)
    
    # Ensure no negative results for subtraction
    if st.session_state.operator == '-':
        if st.session_state.num1 < st.session_state.num2:
            st.session_state.num1, st.session_state.num2 = st.session_state.num2, st.session_state.num1
    
    # Calculate correct answer
    if st.session_state.operator == '+':
        st.session_state.correct_answer = st.session_state.num1 + st.session_state.num2
    elif st.session_state.operator == '-':
        st.session_state.correct_answer = st.session_state.num1 - st.session_state.num2
    elif st.session_state.operator == '*':
        st.session_state.correct_answer = st.session_state.num1 * st.session_state.num2
    else:  # Division: Ensure whole number result
        st.session_state.correct_answer = random.randint(1, max_num // min_num)
        st.session_state.num2 = random.randint(min_num, max_num)
        st.session_state.num1 = st.session_state.correct_answer * st.session_state.num2
        if st.session_state.num1 > max_num:
            st.session_state.num1 = st.session_state.correct_answer * min_num
    
    # Start timer for new problem
    st.session_state.start_time = time.time()

# Set correct answer for initial problem
if st.session_state.correct_answer is None:
    generate_problem()

# Layout: Two columns (left for problem, right for score)
col1, col2 = st.columns([3, 1])

# Left column: Problem and input
with col1:
    st.title("Math Game")
    # Display level and instructions
    remaining = st.session_state.correct_to_advance - st.session_state.correct_in_level
    st.write(f"**Level {st.session_state.level}**: Solve {remaining} more to level up!")
    
    # Display current time spent on problem
    if st.session_state.start_time:
        current_time = time.time()
        time_spent = current_time - st.session_state.start_time
        st.write(f"⏱️ Time on current problem: {time_spent:.1f} seconds")
    
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
                
                # Calculate time spent
                end_time = time.time()
                time_spent = end_time - st.session_state.start_time if st.session_state.start_time else 0
                
                # Get tolerance for current level
                _, _, tolerance = get_level_params(st.session_state.level)
                
                # Check if answer is correct
                is_correct = abs(user_answer - st.session_state.correct_answer) < tolerance
                
                # Record problem in history
                problem_record = {
                    'problem': f"{st.session_state.num1} {st.session_state.operator} {st.session_state.num2}",
                    'correct_answer': st.session_state.correct_answer,
                    'user_answer': user_answer,
                    'is_correct': is_correct,
                    'time_spent': time_spent,
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                }
                st.session_state.problems.append(problem_record)
                
                if is_correct:
                    st.session_state.correct += 1
                    st.session_state.correct_in_level += 1
                    st.success(f"Correct! ({time_spent:.1f}s)")
                    
                    # Check for level-up
                    if st.session_state.correct_in_level >= st.session_state.correct_to_advance:
                        if st.session_state.level < 10:
                            st.session_state.level += 1
                            st.session_state.correct_in_level = 0
                            st.balloons()
                            st.write(f"🎉 Leveled up to Level {st.session_state.level}!")
                        else:
                            st.write("🎉 Max Level (10) Reached! Keep playing!")
                else:
                    st.error(f"Wrong! Correct answer: {st.session_state.correct_answer} ({time_spent:.1f}s)")
                
                generate_problem()
                
            except ValueError:
                st.error("Please enter a valid number!")
        else:
            st.warning("Please enter an answer!")

    # Refresh button
    if st.button("Refresh Problem"):
        if st.session_state.start_time:
            time_spent = time.time() - st.session_state.start_time
            problem_record = {
                'problem': f"{st.session_state.num1} {st.session_state.operator} {st.session_state.num2}",
                'correct_answer': st.session_state.correct_answer,
                'user_answer': None,
                'is_correct': False,
                'time_spent': time_spent,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.problems.append(problem_record)
        generate_problem()

# Right column: Score and problem history table
with col2:
    st.subheader("Score")
    st.write(f"Level: {st.session_state.level}")
    st.write(f"Correct: {st.session_state.correct}")
    st.write(f"Total: {st.session_state.total}")
    if st.session_state.total > 0:
        accuracy = (st.session_state.correct / st.session_state.total) * 100
        st.write(f"Accuracy: {accuracy:.2f}%")
    
    # Problem history table
    if st.session_state.problems:
        st.subheader("Problem History")
        df_data = []
        for i, prob in enumerate(st.session_state.problems[-10:], 1):
            status = "✅" if prob['is_correct'] else "❌"
            answer = prob['user_answer'] if prob['user_answer'] is not None else "Skipped"
            df_data.append({
                'Problem': prob['problem'],
                'Answer': answer,
                'Time': f"{prob['time_spent']:.1f}s",
                'Status': status
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, height=300)
    else:
        st.write("No problems solved yet")