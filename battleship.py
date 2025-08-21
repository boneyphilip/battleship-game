# Battleship Game 

import random

# Step 1: Welcome message
print("===================================")
print(" 🚢 Welcome to Battleship Game 🚢 ")
print("===================================\n")

# Step 2: Instructions for player
print("Instructions:")
print("1. This is a Battleship game running in your terminal.")
print("2. You need to find and sink the enemy ship.")
print("3. Enter your guess in the format: Letter + Number (e.g., A3).")
print("4. X = Hit (you found the ship), O = Miss (empty water).")
print("5. You can type Q anytime to quit the game.")
print("6. The game ends when you sink the ship.\n")


# Step 3: Create board
board_size = 8
board = [["~"] * board_size for _ in range(board_size)]

# Step 4: Function to print the board
def print_board(bd):
    """Show board with row letters and column numbers."""
    print("   " + " ".join(str(i) for i in range(board_size)))
    for idx, row in enumerate(bd):
        row_letter = chr(65 + idx)  # 65 = A
        print(f"{row_letter}  " + " ".join(row))

# Step 5: Show empty board
print("👉 Here is your ocean board:\n")
print_board(board)

print("\n👉 Next step: we will hide a ship on this board.")

# Step 6: Place a ship randomly
ship_row = random.randint(0, board_size - 1)
ship_col = random.randint(0, board_size - 1)

# Debug info (keep for learning, remove later)
print(f"\n[DEBUG] Ship is hidden at: Row={chr(65 + ship_row)}, Col={ship_col}")

# Step 7: Game loop with turn limit
max_turns = 10  # limit chances
turns_left = max_turns

while turns_left > 0:
    print(f"\n👉 Turns left: {turns_left}")
    guess = input("Enter position (e.g., A3 or Q to quit): ").strip().upper()

    # Quit option
    if guess == "Q":
        print("👋 You quit the game. Bye!")
        break

    # Basic input validation
    if len(guess) < 2:
        print("❌ Please type a letter followed by a number, e.g., A3.")
        continue

    row_letter = guess[0]
    digits = guess[1:]

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
        board[row][col] = "X"
        print("\n👉 Final board:")
        print_board(board)
        print("🏆 Congratulations, YOU WIN! Thanks for playing Battleship. 🎮")
        break
    else:
        if board[row][col] in ["O", "X"]:
            print("⚠️ You already tried this spot.")
        else:
            print("💦 MISS! The ship is still hidden.")
            board[row][col] = "O"

    # Show updated board
    print("\n👉 Updated board:")
    print_board(board)

    # Reduce turns
    turns_left -= 1

# If no turns left → Game Over
if turns_left == 0:
    print("\n😢 Game Over! You ran out of turns.")
    print(f"The hidden ship was at: Row={chr(65 + ship_row)}, Col={ship_col}")
