# Battleship Game - Beginner Friendly (single ship, loop, quit, win message)

import random


# Step 1: Welcome
print("===================================")
print(" 🚢 Welcome to Battleship Game 🚢 ")
print("===================================\n")

# Step 2: Instructions
print("Instructions:")
print("1. The board is 8x8. Rows: A–H, Columns: 0–7.")
print("2. Type a position like A3 to shoot.")
print("3. Type Q to quit the game at any time.")
print("4. X = Hit, O = Miss.\n")

# Step 3: Create board
board_size = 8
board = [["~"] * board_size for _ in range(board_size)]


# Step 4: Print the board
def print_board(bd):
    """Print column numbers and row letters neatly."""
    print("   " + " ".join(str(i) for i in range(board_size)))
    for r, row in enumerate(bd):
        row_letter = chr(65 + r)  # 65 = 'A'
        print(f"{row_letter}  " + " ".join(row))


# Step 5: Show empty board
print("👉 Here is your ocean board:\n")
print_board(board)

print("\n👉 Next step: we will hide a ship on this board.")

# Step 6: Hide one ship at a random cell
ship_row = random.randint(0, board_size - 1)
ship_col = random.randint(0, board_size - 1)

# Debug (learning only): you can comment this out later
print(
    f"\n[DEBUG] Computer's ship is at: "
    f"{chr(65 + ship_row)}{ship_col}"
)

# Step 7: Game loop (keep asking until hit or quit)
while True:
    print("\n👉 Your turn!")
    guess = input("Enter position (e.g., A3) or Q to quit: ").strip().upper()

    # Quit option
    if guess in ("Q", "QUIT"):
        print("👋 You chose to quit. See you again!")
        break

    # Basic validation
    if len(guess) < 2:
        print("❌ Please type a letter followed by a number, e.g., A3.")
        continue

    row_letter = guess[0]
    digits = guess[1:]

    # Check row letter
    if not ("A" <= row_letter <= chr(65 + board_size - 1)):
        print(f"❌ Row must be A-{chr(65 + board_size - 1)}.")
        continue

    # Check column digits
    if not digits.isdigit():
        print("❌ Column must be a number, e.g., A3 (3 is the column).")
        continue

    col = int(digits)
    if not (0 <= col < board_size):
        print(f"❌ Column out of range. Use 0-{board_size - 1}.")
        continue

    row = ord(row_letter) - 65  # Convert A->0, B->1, ...

  # Prevent player from guessing the same spot twice
    if board[row][col] in ("O", "X"):
        print("⚠️ You already tried that spot. Pick another.")
        continue

    # Check hit or miss
    if row == ship_row and col == ship_col:
        print("🎉 HIT! You sank the battleship! 🚢🔥")
        print("🏆 Congratulations, YOU WIN! Thanks for playing. 🎮")
        board[row][col] = "X"
        print("\n👉 Final board:")
        print_board(board)
        break
    else:
        print("💦 MISS! The ship is still hidden.")
        board[row][col] = "O"

    print("\n👉 Updated board:")
    print_board(board)
