import streamlit as st
from simpleai.search import CspProblem, backtrack

# Streamlit app title
st.title("Cryptarithmetic Puzzle Solver")

def solve_cryptarithmetic_puzzle(word1, word2, result):
    # Convert input words to uppercase
    word1 = word1.upper()
    word2 = word2.upper()
    result = result.upper()

    # Get all unique letters in the puzzle
    letters = set(word1 + word2 + result)

    # Define variable domains (0-9 for each letter)
    domains = {letter: list(range(10)) for letter in letters}

    # Define the constraint that each letter must have a unique value
    def constraint_unique(variables, values):
        return len(values) == len(set(values))

    # Define the constraint for the addition operation
    def constraint_addition(variables, values):
        w1_value = int("".join(str(values[letter])) for letter in word1)
        w2_value = int("".join(str(values[letter])) for letter in word2)
        result_value = int("".join(str(values[letter])) for letter in result)
        return w1_value + w2_value == result_value

    constraints = [
        (list(letters), constraint_unique),          # Unique values for each letter
        ((word1, word2, result), constraint_addition) # Addition constraint
    ]

    # Create the CSP problem
    problem = CspProblem(list(letters), domains, constraints)

    # Solve the puzzle
    solution = backtrack(problem)

    return solution

# Input for the puzzle
word1 = st.text_input("Enter the first word:")
word2 = st.text_input("Enter the second word:")
result = st.text_input("Enter the result word:")

if st.button("Solve Puzzle"):
    # Solve the puzzle
    solution = solve_cryptarithmetic_puzzle(word1, word2, result)

    if solution:
        st.success("Solution found:")
        for letter, digit in solution.items():
            st.write(f"{letter}: {digit}")
    else:
        st.error("No solution found.")
