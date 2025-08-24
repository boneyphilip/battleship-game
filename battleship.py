# Battleship — Emoji Grid, Visual-Width Padding, Centered Headers, Alternating Turns
# ---------------------------------------------------------------------------------
# Two boards side-by-side (Enemy Fleet on left, Your Fleet on right).
# User fires at enemy grid; enemy fires back at random. Game ends when one fleet is sunk.
# Emojis can be double-width in terminals, so wcwidth is used to align columns precisely.

# ========= 1) Imports =========
import os
import random
import re
from colorama import init, Fore, Style
from wcwidth import wcswidth  # measures on-screen (visual) width so emojis align

# Make ANSI colors reset automatically (safe on Windows too)
init(autoreset=True)

# ========= 2) Constants (symbols, labels, layout) =========
# Grid symbols
WATER = "🌊"       # unknown water
MISS  = "💦"       # shot that missed
HIT   = "💥"       # shot that hit
SHIP_CHAR = "🚢"   # player ship (visible on right board)

# Section titles
LEFT_TITLE  = "Enemy Fleet"
RIGHT_TITLE = "Your Fleet"

# Board and layout
BOARD_SIZE = 8                 # rows A–H, columns 1–8
CELL_VISUAL = 3                # visible width of one cell slot (increase to 4 if needed)
GAP_BETWEEN_BOARDS = " " * 10  # gap between the two boards

# ========= 3) ANSI / width helpers =========
# Regex to strip ANSI color codes before measuring width
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

def strip_ansi(s: str) -> str:
    """Remove ANSI codes so width measuring only sees visible characters."""
    return ANSI_RE.sub("", s)

def pad_visual(s: str, width: int) -> str:
    """
    Pad s with spaces so its *visual* width equals width.
    Handles emojis (often width 2) and ignores ANSI color codes.
    """
    vis = wcswidth(strip_ansi(s))
    if vis < 0:  # fallback (should not happen often)
        vis = len(strip_ansi(s))
    return s + " " * max(0, width - vis)

# ========= 4) Tiny UI helpers =========
def strong_yellow(text: str) -> str:
    """Bright yellow (titles)."""
    return Style.BRIGHT + Fore.YELLOW + text + Style.RESET_ALL

def strong_white(text: str) -> str:
    """Bright white (row/column labels)."""
    return Style.BRIGHT + Fore.WHITE + text + Style.RESET_ALL

def clear_screen():
    """Clear terminal to give the feel of one refreshing screen."""
    os.system("cls" if os.name == "nt" else "clear")

# ========= 5) Cell + Board rendering =========
def format_cell(symbol: str) -> str:
    """
    Return one cell padded to CELL_VISUAL columns.
    Using plain emoji (no color) inside cells keeps width consistent.
    """
    return pad_visual(symbol, CELL_VISUAL)

def display_boards(enemy_view, player_board):
    """
    Draw both boards side-by-side:
    - Titles centered over each board block.
    - Column numbers aligned to cell slots.
    - Rows labeled A..H on both sides.
    """
    # "A  " (3 chars) + N cell slots
    board_width = 3 + (BOARD_SIZE * CELL_VISUAL)

    # Titles: center first, then color (so ANSI codes don’t affect centering)
    left_title  = strong_yellow(LEFT_TITLE.center(board_width))
    right_title = strong_yellow(RIGHT_TITLE.center(board_width))
    print(left_title + GAP_BETWEEN_BOARDS + right_title)

    # Column numbers: each number gets the same slot width as a cell
    nums_slots = "".join(format_cell(str(i)) for i in range(1, BOARD_SIZE + 1))
    header_line = "   " + nums_slots  # align with row label area ("A  ")
    print(strong_white(header_line) + GAP_BETWEEN_BOARDS + strong_white(header_line))

    # Rows A..H
    for r in range(BOARD_SIZE):
        row_label = strong_white(chr(65 + r))  # 65→'A'
        left_row  = "".join(format_cell(ch) for ch in enemy_view[r])
        right_row = "".join(format_cell(ch) for ch in player_board[r])
        print(f"{row_label}  {left_row}" + GAP_BETWEEN_BOARDS + f"{row_label}  {right_row}")

# ========= 6) Enemy AI =========
def enemy_take_one_shot(player_board, player_ships, tried):
    """
    Fire one random shot at player board.
    - Avoids repeating positions using 'tried' set.
    - Marks 💥 or 💦 on player board.
    - Removes hit ship from player_ships.
    Returns a short status message.
    """
    while True:
        r = random.randint(0, BOARD_SIZE - 1)
        c = random.randint(0, BOARD_SIZE - 1)
        # skip already attempted or already marked cells
        if (r, c) in tried or player_board[r][c] in (MISS, HIT):
            tried.add((r, c))
            continue
        tried.add((r, c))
        break

    pos = f"{chr(65 + r)}{c + 1}"
    if (r, c) in player_ships:
        player_board[r][c] = HIT
        player_ships.remove((r, c))
        return f"👾 Enemy fires at {pos} — {HIT} Hit!"
    else:
        player_board[r][c] = MISS
        return f"👾 Enemy fires at {pos} — {MISS} Miss."

# ========= 7) Game state (boards + ships) =========
# Enemy board as seen by the player (start unknown water everywhere)
enemy_view   = [[WATER] * BOARD_SIZE for _ in range(BOARD_SIZE)]
# Player board (shows player ships; other cells start as water)
player_board = [[WATER] * BOARD_SIZE for _ in range(BOARD_SIZE)]

NUM_SHIPS = 3  # ships per side

# Hidden enemy ships (set of positions)
enemy_ships = set()
while len(enemy_ships) < NUM_SHIPS:
    enemy_ships.add((random.randint(0, BOARD_SIZE - 1),
                     random.randint(0, BOARD_SIZE - 1)))

# Visible player ships on the right board
player_ships = set()
while len(player_ships) < NUM_SHIPS:
    r = random.randint(0, BOARD_SIZE - 1)
    c = random.randint(0, BOARD_SIZE - 1)
    if (r, c) not in player_ships:
        player_ships.add((r, c))
        player_board[r][c] = SHIP_CHAR

# ========= 8) Intro screen =========
clear_screen()
print("===================================")
print(Style.BRIGHT + Fore.MAGENTA + " 🚢 Welcome to Battleship " + Style.RESET_ALL)
print("===================================\n")
print(Style.BRIGHT + "How to play:" + Style.RESET_ALL)
print("1) Grid is 8x8: rows A–H, columns 1–8.")
print("2) Goal: sink all enemy ships.")
print("3) Type A1, C7, H8 … or Q to quit.")
print(f"4) Symbols: {HIT}=Hit  {MISS}=Miss  {WATER}=Water  {SHIP_CHAR}=Player ship.\n")
input("Press Enter to start... ")
clear_screen()

# ========= 9) Main loop (alternating turns) =========
player_msg = ""            # last message from the user’s shot
enemy_msg  = ""            # last message from enemy shot
enemy_tried = set()        # enemy’s attempted positions (avoid repeats)

while player_ships and enemy_ships:
    clear_screen()
    print("===================================")
    print(Style.BRIGHT + Fore.MAGENTA + " 🚢 Battleship — Alternating Turns " + Style.RESET_ALL)
    print("===================================\n")

    display_boards(enemy_view, player_board)
    if player_msg:
        print("\n" + player_msg)
    if enemy_msg:
        print(enemy_msg)

    # --- user input ---
    guess = input("\nEnter position (e.g., A1) or Q to quit: ").strip().upper()
    if guess == "Q":
        clear_screen()
        print("👋 Game ended by user.")
        break

    # quick validation before converting to row/col indexes
    if len(guess) < 2:
        player_msg = "❌ Format must be a letter followed by a number, e.g., A1."
        continue

    row_letter, digits = guess[0], guess[1:]
    if not ("A" <= row_letter <= chr(65 + BOARD_SIZE - 1)):
        player_msg = f"❌ Row must be A–{chr(65 + BOARD_SIZE - 1)}."
        continue
    if not digits.isdigit():
        player_msg = "❌ Column must be a number, e.g., A1 or B8."
        continue

    col1 = int(digits)
    if not (1 <= col1 <= BOARD_SIZE):
        player_msg = f"❌ Column out of range. Use 1–{BOARD_SIZE}."
        continue

    # convert A..H / 1..8 into 0..7 indexes
    r = ord(row_letter) - 65
    c = col1 - 1

    # block repeated guesses
    if enemy_view[r][c] in (MISS, HIT):
        player_msg = "⚠️ That position was already tried."
        continue

    # apply shot
    if (r, c) in enemy_ships:
        enemy_view[r][c] = HIT
        enemy_ships.remove((r, c))
        player_msg = f"🎯 HIT at {row_letter}{col1}! {HIT}"
    else:
        enemy_view[r][c] = MISS
        player_msg = f"💦 MISS at {row_letter}{col1}. {MISS}"

    # win check (user sank every enemy ship)
    if not enemy_ships:
        break

    # enemy turn
    enemy_msg = enemy_take_one_shot(player_board, player_ships, enemy_tried)
    # loss check (enemy sank every player ship)
    if not player_ships:
        break

# ========= 10) End screen =========
if enemy_ships and not player_ships:
    clear_screen()
    print("===================================")
    print(Style.BRIGHT + Fore.MAGENTA + " 🚢 Battleship — Game Over" + Style.RESET_ALL)
    print("===================================\n")
    display_boards(enemy_view, player_board)
    print("\n💀 All player ships are sunk.")
elif player_ships and not enemy_ships:
    clear_screen()
    print("===================================")
    print(Style.BRIGHT + Fore.MAGENTA + " 🚢 Battleship — Victory!" + Style.RESET_ALL)
    print("===================================\n")
    display_boards(enemy_view, player_board)
    print("\n🏆 All enemy ships are sunk! 🎉")
