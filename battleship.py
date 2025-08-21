# Battleship Game - Step F (Multiple Ships, Beginner-Friendly Version)

import random  # We use this to hide ships at random positions


# Step 1: Welcome message
print("===================================")
print(" 🚢 Welcome to Battleship Game 🚢 ")
print("===================================\n")

# Step 2: Instructions for player
print("Instructions:")
print("1. This is a Battleship game running in your terminal.")
print("2. You need to find and sink ALL hidden enemy ships.")
print("3. You will enter your guess (row + column, e.g., A3).")
print("4. Symbols: X = Hit, O = Miss, ~ = Water (unknown).")
print("5. Type Q anytime to quit the game.\n")


# Step 3: Create board
board_size = 8  # Grid size 8x8 (rows A-H, columns 0-7)

# A 2D list to represent the board, filled with "~" (water)
board = [["~"] * board_size for _ in range(board_size)]


# Step 4: Function to print the board
def print_board(bd):
    """Print the board with column numbers on top and row letters on the side."""
    # Print column numbers (0 1 2 3 ...)
    print("   " + " ".join(str(i) for i in range(board_size)))
    # Print each row with its letter (A, B, C, ...)
    for idx, row in enumerate(bd):
        row_letter = chr(65 + idx)  # Convert row index (0 → A, 1 → B, etc.)
        print(f"{row_letter}  " + " ".join(row))


# Step 5: Place multiple ships randomly
num_ships = 3  # Number of enemy ships hidden

ships = set()  # Using a set so positions are unique
while len(ships) < num_ships:
    r = random.randint(0, board_size - 1)  # random row
    c = random.randint(0, board_size - 1)  # random column
    ships.add((r, c))  # add ship position to the set

# Debug info (only for learning, remove later for fair play)
print(f"[DEBUG] Hidden ships: {ships}")


# Step 6: Game loop
hits = 0  # Track how many ships have been hit
while hits < num_ships:  # Keep looping until all ships are found
    print("\n👉 Current board:")
    print_board(board)

    # Take player input like "A3" or "C7"
    guess = input("Enter position (e.g., A3 or Q to quit): ").strip().upper()

    # Option to quit the game
    if guess == "Q":
        print("👋 You quit the game. Bye!")
        break

    # Input validation (check format)
    if len(guess) < 2:
        print("❌ Please type a letter followed by a number, e.g., A3.")
        continue

    row_letter = guess[0]   # First character is the row (A-H)
    digits = guess[1:]      # Remaining part is the column number (0-7)

    # Check if row is valid
    if not ("A" <= row_letter <= chr(65 + board_size - 1)):
        print(f"❌ Row must be between A and {chr(65 + board_size - 1)}.")
        continue

    # Check if column is a number
    if not digits.isdigit():
        print("❌ Column must be a number, e.g., A3.")
        continue

    col = int(digits)  # Convert column part to integer
    if not (0 <= col < board_size):
        print(f"❌ Column out of range. Use 0-{board_size - 1}.")
        continue

    # Convert row letter to row number (A=0, B=1, etc.)
    row = ord(row_letter) - 65

    # Check if the player already tried this spot
    if board[row][col] in ("O", "X"):
        print("⚠️ You already tried this spot. Pick another.")
        continue

    # Check if guess is a hit or miss
    if (row, col) in ships:
        print("🎯 HIT! You sank part of a battleship! 🚢🔥")
        board[row][col] = "X"  # Mark hit
        hits += 1  # Increase hit count
    else:
        print("💦 MISS! Nothing here.")
        board[row][col] = "O"  # Mark miss


# Step 7: End of game (all ships found)
if hits == num_ships:
    print("\n👉 Final board:")
    print_board(board)
    print("🏆 Congratulations, YOU WIN! All enemy ships are sunk! 🎮")
