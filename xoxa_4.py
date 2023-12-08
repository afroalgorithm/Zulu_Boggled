import tkinter as tk
import random
import string
import time

# List of words for the Boggle game
words = ['umama', 'xoxa', 'umuntu', 'usisi', 'hamba', 'woza', 'gijima', 'khuluma', 'sawubona', 'inkosikazi', 'ubaba', 'ukuthi', 'ngoba', 'futhi']

# Function to generate a 9x9 grid of letters based on words and random letters
def generate_grid(words_list):
    grid = [['' for _ in range(9)] for _ in range(9)]

    # Place letters from words list
    for word in words_list:
        word_length = len(word)
        if word_length <= 81:  # Increase grid size to accommodate longer words
            direction = random.choice([(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)])
            dx, dy = direction
            x, y = random.randint(0, 8), random.randint(0, 8)
            x_end, y_end = x + dx * (word_length - 1), y + dy * (word_length - 1)
            if 0 <= x_end < 9 and 0 <= y_end < 9:
                valid = True
                for i in range(word_length):
                    if grid[x + i * dx][y + i * dy] != '' and grid[x + i * dx][y + i * dy] != word[i]:
                        valid = False
                        break
                if valid:
                    for i in range(word_length):
                        grid[x + i * dx][y + i * dy] = word[i]

    # Fill remaining cells with random letters
    for i in range(9):
        for j in range(9):
            if grid[i][j] == '':
                grid[i][j] = random.choice(string.ascii_lowercase)

    return grid

# Function to validate word within the grid
def validate_word():
    global score
    word = entry.get().lower()
    if word in found_words:
        result_label.config(text=f"You've already found '{word}'!")
    elif word not in words:
        result_label.config(text=f"'{word}' is not a valid word.")
    elif not is_valid_word(word):
        result_label.config(text=f"'{word}' cannot be formed from adjacent letters.")
    else:
        found_words.append(word)
        score += len(word)  # Increase score based on word length
        result_label.config(text=f"Word '{word}' found! Score: {score}")

# Function to check if the word can be formed from adjacent letters
def is_valid_word(word):
    def search_from_cell(x, y, idx):
        if x < 0 or x >= 9 or y < 0 or y >= 9 or visited[x][y] or word[idx] != grid[x][y]:
            return False
        if idx == len(word) - 1:
            return True
        
        visited[x][y] = True
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if search_from_cell(x + dx, y + dy, idx + 1):
                    visited[x][y] = False
                    return True
        visited[x][y] = False
        return False

    for i in range(9):
        for j in range(9):
            visited = [[False for _ in range(9)] for _ in range(9)]
            if search_from_cell(i, j, 0):
                return True
    return False

# Function to update the timer label
def update_timer():
    global time_remaining
    minutes = time_remaining // 60
    seconds = time_remaining % 60
    timer_label.config(text=f"Time Left: {minutes:02d}:{seconds:02d}")
    if time_remaining > 0:
        time_remaining -= 1
        root.after(1000, update_timer)
    else:
        result_label.config(text=f"Time's up! Final Score: {score}")

# Create the main window
root = tk.Tk()
root.title("Mthuli Buthelezi")

# Generate a grid of letters based on words and random letters
grid = generate_grid(words)

# Display the grid of letters
for i in range(9):
    for j in range(9):
        label = tk.Label(root, text=grid[i][j], font=("Helvetica", 16), width=3, height=1, borderwidth=1, relief="solid")
        label.grid(row=i, column=j)

# Create an entry for word input
entry = tk.Entry(root, font=("Helvetica", 12))
entry.grid(row=9, columnspan=9)

# Create a button to validate the word
validate_button = tk.Button(root, text="Hlola Igama", command=validate_word)
validate_button.grid(row=10, columnspan=9)

# Create a label to display the result
result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.grid(row=11, columnspan=9)

# Create a label for the timer
time_remaining = 120  # Two minutes
timer_label = tk.Label(root, text="Isikhathi Esisele: 02:00", font=("Helvetica", 12))
timer_label.grid(row=12, columnspan=9)

# Variable to keep track of the score
score = 0

# Start the countdown timer
update_timer()

# List to store found words
found_words = []

root.mainloop()
