# Battleship Game - Step D (A3 input + validation + one-shot result)

import random


# Step 1: Welcome message
print("===================================")
print(" 🚢 Welcome to Battleship Game 🚢 ")
print("===================================\n")

# Step 2: Instructions for player
print("Instructions:")
print("1. This is a Battleship game running in your terminal.")
print("2. You need to find and sink enemy ships.")
print("3. You will enter your guess (row, column).")
print("4. If your guess is correct, you will see 'Hit!', "
      "otherwise 'Miss!'.")
print("5. The game ends when all ships are sunk.\n")

# Step 3: Create board
board_size = 8  # set the grid size to 8x8

# Create a 2D list to represent the ocean ("~" = water)
board = [["~"] * board_size for _ in range(board_size)]


# Step 4: Function to print the board nicely
def print_board(bd):
    """Pretty print the board with column numbers and row letters."""
    # Print column numbers at the top
    print("   " + " ".join(str(i) for i in range(board_size)))

    # Print each row with alphabet instead of numbers
    for idx, row in enumerate(bd):
        row_letter = chr(65 + idx)  # 65 = 'A', 66 = 'B', etc.
        print(f"{row_letter}  " + " ".join(row))


# Step 5: Show empty board
print("👉 Here is your ocean board:\n")
print_board(board)

print("\n👉 Next step: we will hide a ship on this board.")

# Step 6: Place a ship randomly
ship_row = random.randint(0, board_size - 1)
ship_col = random.randint(0, board_size - 1)

# (For debugging: we can print the hidden ship position)
# ⚠️ Later we will remove this, for now keep it for learning
print(
    f"\n[DEBUG] Computer's ship is hidden at: "
    f"Row={chr(65 + ship_row)}, Col={ship_col}"
)

# Step 7: Game loop for guessing
while True:
    print("\n👉 Now it's your turn to find the ship!")

    # Input like "A3" or "c5"
    guess = input("Enter position (e.g., A3): ").strip().upper()

    # Basic validation
    if len(guess) < 2:
        print("❌ Please type a letter followed by a number, e.g., A3.")
        continue  # skip rest and ask again

    row_letter = guess[0]
    digits = guess[1:]  # remaining characters (e.g., "3")

    # Check row letter range (A to A+board_size-1)
    if not ("A" <= row_letter <= chr(65 + board_size - 1)):
        print(f"❌ Row must be A-{chr(65 + board_size - 1)}.")
        continue
    elif not digits.isdigit():
        print("❌ Column must be a number, e.g., A3 (3 is the column).")
        continue

    col = int(digits)
    if not (0 <= col < board_size):
        print(f"❌ Column out of range. Use 0-{board_size - 1}.")
        continue

    row = ord(row_letter) - 65

    # Check guess vs hidden ship
    if row == ship_row and col == ship_col:
        print("🎉 HIT! You sank the battleship! 🚢🔥")
        board[row][col] = "X"  # mark hit
        print("\n👉 Final board:")
        print_board(board)
        break  # game ends
    else:
        if board[row][col] in ["O", "X"]:
            print("⚠️ You already tried this spot!")
        else:
            print("💦 MISS! The ship is still hidden.")
            board[row][col] = "O"  # mark miss

    # Show board after guess
    print("\n👉 Updated board:")
    print_board(board)
