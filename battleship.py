# Battleship Game — Solo mode with two boards, side-by-side display
# -----------------------------------------------------------------
# What this version does:
# - Shows TWO boards side by side:
#     • Left  : Enemy board (you only see what you have discovered: X/O/~)
#     • Right : Your board (your ships are visible as 'S')
# - You keep guessing until all enemy ships are sunk.
# - This structure prepares us for the next step (adding enemy turns).

import random  # Used for random ship placement


# -------------------------------
# Step 1: Welcome + Instructions
# -------------------------------
print("===================================")
print(" 🚢 Welcome to Battleship Game 🚢 ")
print("===================================\n")

print("Instructions:")
print("1. The grid is 8x8: rows A–H, columns 0–7.")
print("2. You need to find and sink ALL hidden enemy ships.")
print("3. Enter your guess like A3. Type Q anytime to quit.")
print("4. Symbols: X = Hit, O = Miss, ~ = Water (unknown), S = Your ship (on your board).")
print("5. For now, only YOU shoot. (Enemy turn will be added later.)\n")


# -------------------------------
# Step 2: Create Boards
# -------------------------------
board_size = 8  # Grid size 8x8 (rows A-H, columns 0-7)

# enemy_view: what you can see about the enemy board (starts all water "~")
enemy_view = [["~"] * board_size for _ in range(board_size)]

# player_board: your own board (we place your ships here and show them as "S")
player_board = [["~"] * board_size for _ in range(board_size)]


# -------------------------------
# Step 3: Printing Helpers
# -------------------------------
def print_board(bd):
    """Print one board with column numbers and row letters."""
    print("   " + " ".join(str(i) for i in range(board_size)))
    for idx, row in enumerate(bd):
        row_letter = chr(65 + idx)  # 0→A, 1→B, ...
        print(f"{row_letter}  " + " ".join(row))


def display_game_boards(enemy_view, player_board):
    """
    Display enemy board (left) and player board (right) side by side
    with proper alignment. Enemy board shows only what the player
    has discovered so far, while the player board shows their own ships.
    """
    # Column numbers (0 1 2 ...)
    col_numbers = " ".join(str(i) for i in range(board_size))

    # Width of one board block (row label + columns)
    # Example: "A  " (3 chars) + len("0 1 2 3 4 5 6 7")
    block_width = 3 + len(col_numbers)

    # Gap between the two boards
    gap = "   "

    # Header row (columns for both boards)
    left_header = "   " + col_numbers
    right_header = "   " + col_numbers
    print(left_header.ljust(block_width) + gap + right_header)

    # Print rows A..H
    for idx in range(board_size):
        row_letter = chr(65 + idx)
        left_row = f"{row_letter}  " + " ".join(enemy_view[idx])
        right_row = f"{row_letter}  " + " ".join(player_board[idx])

        # Align the left block, then add gap + right block
        print(left_row.ljust(block_width) + gap + right_row)


# -------------------------------
# Step 4: Place Ships (enemy + yours)
# -------------------------------
num_ships = 3  # Number of ships for each side

# Enemy ships (hidden) — you will try to find these
enemy_ships = set()
while len(enemy_ships) < num_ships:
    r = random.randint(0, board_size - 1)
    c = random.randint(0, board_size - 1)
    enemy_ships.add((r, c))

# Your ships (visible as 'S') — placed randomly for now
player_ships = set()
while len(player_ships) < num_ships:
    r = random.randint(0, board_size - 1)
    c = random.randint(0, board_size - 1)
    if (r, c) not in player_ships:
        player_ships.add((r, c))
        player_board[r][c] = "S"

# Debug info (only for learning; remove later for fair play)
debug_enemy = [f"{chr(65 + r)}{c}" for (r, c) in sorted(enemy_ships)]
debug_player = [f"{chr(65 + r)}{c}" for (r, c) in sorted(player_ships)]
print(f"[DEBUG] Enemy ships: {debug_enemy}")
print(f"[DEBUG] Your ships:  {debug_player}")


# -------------------------------
# Step 5: Game Loop (solo shooting)
# -------------------------------
hits = 0  # How many enemy ships have been hit

while hits < num_ships:
    # Show boards side by side
    print("\n=== Enemy (left) vs You (right) ===")
    display_game_boards(enemy_view, player_board)

    # Take player input like "A3"
    guess = input("\nEnter position (e.g., A3) or Q to quit: ").strip().upper()

    # Quit option
    if guess == "Q":
        print("👋 You quit the game. Bye!")
        break

    # Basic validation
    if len(guess) < 2:
        print("❌ Please type a letter followed by a number, e.g., A3.")
        continue

    row_letter = guess[0]
    digits = guess[1:]

    # Check row and column formats
    if not ("A" <= row_letter <= chr(65 + board_size - 1)):
        print(f"❌ Row must be between A and {chr(65 + board_size - 1)}.")
        continue
    if not digits.isdigit():
        print("❌ Column must be a number, e.g., A3.")
        continue

    col = int(digits)
    if not (0 <= col < board_size):
        print(f"❌ Column out of range. Use 0-{board_size - 1}.")
        continue

    row = ord(row_letter) - 65  # Convert A→0, B→1, ...

    # Already guessed this enemy cell?
    if enemy_view[row][col] in ("O", "X"):
        print("⚠️ You already tried this spot. Pick another.")
        continue

    # Hit or miss against enemy ships
    if (row, col) in enemy_ships:
        print("🎯 HIT! You sank part of an enemy ship! 🚢🔥")
        enemy_view[row][col] = "X"
        hits += 1
        enemy_ships.remove((row, col))  # remove the ship cell you found
    else:
        print("💦 MISS! Nothing here.")
        enemy_view[row][col] = "O"

    # Optional: show updated boards again right away
    print("\n👉 Updated boards:")
    display_game_boards(enemy_view, player_board)


# -------------------------------
# Step 6: End of Game
# -------------------------------
if hits == num_ships:
    print("\n=== Final Boards ===")
    display_game_boards(enemy_view, player_board)
    print("🏆 Congratulations, YOU WIN! All enemy ships are sunk! 🎮")
