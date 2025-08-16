
# Battleship Game - Step B (Board Setup)

# Step 1: Welcome message
print("===================================")
print(" 🚢 Welcome to Battleship Game 🚢 ")
print("===================================")

# Step 2 : Instruction for player
print("\nInstructions:")
print("1. This is a Battleship game running in your terminal.")
print("2. You need to find and sink enemy ships.")
print("3. You will enter your guess (row, column).")
print("4. If your guess is correct, you will see 'Hit!', otherwise 'Miss!'.")
print("5. The game ends when all ships are sunk.\n")

# Step 3: Create board
board_size = 8  # set the grid size to 8x8


# Create a 2D list to represent the ocean
# Each cell contains '~' to show water
board = [["~"] * board_size for _ in range(board_size)]

# Step 4: Function to print the board nicely
def print_board(board):
    # Print column numbers at the top
    print("   " + " ".join(str(i) for i in range(board_size)))

    # Print each row with alphabet instead of numbers
    for idx, row in enumerate(board):
        row_letter = chr(65 + idx)  # 65 = 'A', 66 = 'B', etc.
        print(f"{row_letter}  " + " ".join(row))

# Step 5: Show empty board
print("👉 Here is your ocean board:\n")
print_board(board)

print("\n👉 Next step: we will hide a ship on this board.")


