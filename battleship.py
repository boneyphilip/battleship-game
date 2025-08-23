# Battleship Game — Solo mode with two boards, side-by-side, columns 1..N
# ----------------------------------------------------------------------
# What this version does:
# - Shows TWO boards side by side:
#     • Left  : Enemy board (you only see what you have discovered: X/O/~)
#     • Right : Your board (your ships are visible as 'S')
# - Columns are labeled 1..board_size (more natural for humans).
# - You type guesses like A1, C7, H8 (NOT A0).
# - Internally we still use 0-based indexing, so we convert (col-1).
# - Screen refreshes each turn so the view looks “live”.
# - This structure prepares us to add Enemy turns later.

import os      # for clearing the console screen (live feel)
import random  # for random ship placement


# -------------------------------
# Small helper to clear the screen
# -------------------------------
def clear_screen():
    """Clear the terminal so the game looks like it updates in place."""
    # Windows uses 'cls'; macOS/Linux use 'clear'
    os.system("cls" if os.name == "nt" else "clear")


# -------------------------------
# Step 1: Welcome + Instructions
# -------------------------------
print("===================================")
print(" 🚢 Welcome to Battleship Game 🚢 ")
print("===================================\n")

print("Instructions:")
print("1) The grid is 8x8: rows A–H, columns 1–8 (NOT starting at 0).")
print("2) Your goal is to find and sink ALL hidden enemy ships.")
print("3) Enter guesses like A1, C7, H8. Type Q anytime to quit.")
print("4) Symbols: X = Hit, O = Miss, ~ = Water (unknown), S = Your ship (on your board).")
print("5) For now, only YOU shoot. (Enemy turn will be added later.)\n")

input("Press Enter to start... ")
clear_screen()


# -------------------------------
# Step 2: Create Boards
# -------------------------------
board_size = 8  # Grid size 8x8 (rows A-H, columns 1-8 for display)

# enemy_view: what you can see about the enemy board (starts all water "~")
enemy_view = [["~"] * board_size for _ in range(board_size)]

# player_board: your own board (we place your ships here and show them as "S")
player_board = [["~"] * board_size for _ in range(board_size)]


# -------------------------------
# Step 3: Printing Helpers
# -------------------------------
def print_board(bd):
    """
    Print one board with:
    - Column numbers starting from 1 (human-friendly).
    - Row letters A..H on the left.
    """
    # Column numbers: "1 2 3 ... board_size"
    print("   " + " ".join(str(i) for i in range(1, board_size + 1)))
    # Each row: "A  ~ ~ ~ ~ ~ ~ ~ ~"
    for idx, row in enumerate(bd):
        row_letter = chr(65 + idx)  # Convert index 0..7 to 'A'..'H'
        print(f"{row_letter}  " + " ".join(row))


def display_game_boards(enemy_view, player_board):
    """
    Display enemy board (left) and player board (right) side by side,
    aligned neatly. Enemy board shows only what you have discovered
    so far; your board shows your ships.
    """
    # Column numbers string for one board, using 1..N
    col_numbers = " ".join(str(i) for i in range(1, board_size + 1))

    # Width of one printed board block:
    #  - "A  " (3 chars) + len(col_numbers)
    block_width = 3 + len(col_numbers)

    # Gap between the two boards
    gap = "   "

    # Titles (roughly centered over each board)
    left_title = "ENEMY (what you know)"
    right_title = "YOU (your ships)"
    print(left_title.ljust(block_width) + gap + right_title)

    # Header line: column numbers for both boards
    left_header = "   " + col_numbers
    right_header = "   " + col_numbers
    print(left_header.ljust(block_width) + gap + right_header)

    # Rows A..H for both boards
    for idx in range(board_size):
        row_letter = chr(65 + idx)
        left_row = f"{row_letter}  " + " ".join(enemy_view[idx])
        right_row = f"{row_letter}  " + " ".join(player_board[idx])
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

# Debug info (for learning only). Shows friendly A1-based positions.
debug_enemy = [f"{chr(65 + r)}{c + 1}" for (r, c) in sorted(enemy_ships)]
debug_player = [f"{chr(65 + r)}{c + 1}" for (r, c) in sorted(player_ships)]
print(f"[DEBUG] Enemy ships: {debug_enemy}")
print(f"[DEBUG] Your ships:  {debug_player}")
input("\n(Dev note) Press Enter to hide debug and start playing...")
clear_screen()


# -------------------------------
# Step 5: Game Loop (solo shooting)
# -------------------------------
hits = 0              # How many enemy ships have been hit so far
last_message = ""     # Last feedback text (Hit/Miss/Validation) shown under boards

while hits < num_ships:
    # Refresh the view at the start of each turn
    clear_screen()

    # Header + boards
    print("===================================")
    print(" 🚢 Battleship — Solo Mode (Prep for Versus)")
    print("===================================\n")
    display_game_boards(enemy_view, player_board)

    # Show the last action/result under the boards (if any)
    if last_message:
        print("\n" + last_message)

    # Ask for the next guess (A1..H8 or Q)
    guess = input("\nEnter position (e.g., A1) or Q to quit: ").strip().upper()

    # Quit option
    if guess == "Q":
        clear_screen()
        print("👋 You quit the game. Bye!")
        break

    # Basic format validation: need at least 2 chars (e.g., 'A1')
    if len(guess) < 2:
        last_message = "❌ Please type a letter followed by a number, e.g., A1."
        continue

    row_letter = guess[0]
    digits = guess[1:]  # the numeric part (1..board_size as text)

    # Validate row letter is within A..(A + board_size - 1)
    if not ("A" <= row_letter <= chr(65 + board_size - 1)):
        last_message = f"❌ Row must be between A and {chr(65 + board_size - 1)}."
        continue

    # Validate column is numeric and within 1..board_size
    if not digits.isdigit():
        last_message = "❌ Column must be a number, e.g., A1 or B8."
        continue

    # Convert to int, but remember the display is 1-based (so we subtract 1)
    col_1based = int(digits)
    if not (1 <= col_1based <= board_size):
        last_message = f"❌ Column out of range. Use 1–{board_size}."
        continue

    # Convert to zero-based column index for internal board access
    col = col_1based - 1

    # Convert row letter to zero-based row index (A→0, B→1, ...)
    row = ord(row_letter) - 65

    # Prevent shooting the same enemy cell twice
    if enemy_view[row][col] in ("O", "X"):
        last_message = "⚠️ You already tried that spot. Pick another."
        continue

    # Resolve hit or miss against enemy ships
    if (row, col) in enemy_ships:
        enemy_view[row][col] = "X"
        hits += 1
        enemy_ships.remove((row, col))
        last_message = f"🎯 HIT at {row_letter}{col_1based}! Enemy ship damaged! 🚢🔥"
    else:
        enemy_view[row][col] = "O"
        last_message = f"💦 MISS at {row_letter}{col_1based}. Nothing there."


# -------------------------------
# Step 6: End of Game
# -------------------------------
if hits == num_ships:
    clear_screen()
    print("===================================")
    print(" 🚢 Battleship — Solo Mode (Prep for Versus)")
    print("===================================\n")
    display_game_boards(enemy_view, player_board)
    print("\n🏆 Congratulations, YOU WIN! All enemy ships are sunk! 🎮")
