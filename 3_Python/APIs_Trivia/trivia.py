# How to Install:
# Open your terminal or command prompt and run the following commands:
# pip install requests
# pip install tabulate
# ==============================================================================

# Import necessary modules
import requests
import random
import html
from tabulate import tabulate  # Used for nicely formatted tables
import os

# Use functions with returns to make code reusable
def get_api_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the API: {e}")
        return None  # Return None to signify failure


# 1. Setup and Get All Categories for the user to view
print("\nWelcome! Connecting to the Open Trivia Database...")

categories_url = "https://opentdb.com/api_category.php"
categories_data = get_api_data(categories_url)


# Check if the API call was successful before proceeding.
if not categories_data:
    print("Could not load categories. Please check your internet connection and try again.")
else:
    # Use a data structure (list of dictionaries)
    categories = categories_data["trivia_categories"]


    # 2. User Choices
    print("\nHere are the available categories:")
    print(tabulate(categories, headers="keys", tablefmt="fancy_outline"))


    category_choice = input("\nWhat is your chosen category? Please input the category ID from the table: ")
    no_questions = int(input("How many questions would you like? (max 50): "))


    # 3. Fetch The Chosen Questions
    print("\nFetching your questions...")
    questions_url = f"https://opentdb.com/api.php?amount={no_questions}&category={category_choice}&type=multiple"
    questions_data = get_api_data(questions_url)

    if not questions_data or not questions_data["results"]:
        print("Error: Could not fetch questions. The category might be empty or the API is temporarily down.")
    else:
        questions = questions_data["results"]


      # 4. Quiz Loop
        score = 0                   # starting score
        results_log = []            # A list to store results

        # 'Enumerate' function gives us a counter and the item - I started this with a 'counter' variable, but then found this out
        for counter, q in enumerate(questions, 1):
            question_text = html.unescape(q['question']) # this cleans up the formatting - I was getting weird characters without it
            correct_answer = html.unescape(q['correct_answer'])
            incorrect_answers = [html.unescape(ans) for ans in q['incorrect_answers']]

            # Combining correct and incorrect answers into one list
            answers = incorrect_answers + [correct_answer] # correct answer is a string, not a list
            random.shuffle(answers) # shuffles it so correct answer isn't always last

            # String multiplication for formatting
            print("-" * 30) # visually separates the text
            print(f"Question {counter}: {question_text}")
            for i, answer in enumerate(answers, 1):
                print(f"  {i}. {answer}")

            # Get and validate user's answer
            user_input = input("Your answer (1-4): ")
            user_answer_index = int(user_input) - 1 # -1 because indexing starts at 0
            user_answer_text = answers[user_answer_index]

            # Check answer and update score using an if/else
            if user_answer_text == correct_answer:
                print("✅ Correct!\n")
                score += 1
                is_correct = True # this is for the saved file
            else:
                print(f"❌ Sorry, the correct answer was: '{correct_answer}'\n")
                is_correct = False


      # Store the result for the final file
            results_log.append({
                "question": question_text,
                "your_answer": user_answer_text,
                "correct_answer": correct_answer,
                "was_correct": is_correct
            })


        # 5. Display Final Score and Save to File
        print("-" * 30)
        print("Quiz Complete!")
        print(f"Your final score is: {score} / {no_questions}")

        # Write your final results to a file
        filename = "quiz_results.txt"
        with open(filename, "w") as f:
            f.write("--- Your Trivia Quiz Results ---\n\n")

            # Find the full name of the chosen category to write to the file - user only added ID
            chosen_category_name = "Unknown Category"
            for cat in categories:
                if str(cat['id']) == category_choice:
                    chosen_category_name = cat['name']
                    break

            # Slice the category name to a max of 20 chars for nicer formatting
            short_category_title = chosen_category_name[:20]

            f.write(f"Category: {short_category_title}\n")
            f.write(f"Final Score: {score} / {no_questions}\n\n")
            f.write("--- Question Breakdown ---\n")

            for result in results_log:
                status = "Correct" if result["was_correct"] else "Incorrect"
                f.write(f"\nQuestion: {result['question']}\n")
                f.write(f"  Your Answer: {result['your_answer']} ({status})\n")
                if not result['was_correct']:
                    f.write(f"  Correct Answer: {result['correct_answer']}\n")

        # Use another inbuilt function (os.path.abspath)
        absolute_path = os.path.abspath(filename)
        print(f"\nDetailed results have been saved to: '{absolute_path}'\n\nThank you for playing!")