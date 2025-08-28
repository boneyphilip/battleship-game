# Battleship — Framed Boards (Fixed Side-by-Side)
# Emoji Grid, Alternating Turns
# -----------------------------------------------------------------
# Two boards display: Enemy Fleet (left) and Your Fleet (right).
# Player fires at the enemy grid; enemy fires back at random.
# Game ends when one fleet is fully sunk.
#
# Visual notes:
# - Emoji can be double-width, so wcwidth is used for alignment.
# - Boards are always printed side-by-side (no responsive/stacked mode).
# - Boards are framed with box-drawing characters; titles are centered.

# ========= 1) Imports =========
import os
import re
import random
from colorama import init, Fore, Style
from wcwidth import wcswidth  # measures on-screen width so emoji align

# Configure color handling (safe on Windows)
init(autoreset=True)

# ========= 2) Constants (symbols, labels, layout) =========
WATER = "🌊"        # unknown water
MISS = "💦"         # shot that missed
HIT = "💥"          # shot that hit
SHIP_CHAR = "🚢"    # player ship (visible on right board)

LEFT_TITLE = "Enemy Fleet"
RIGHT_TITLE = "Your Fleet"

BOARD_SIZE = 8                 # rows A–H, columns 1–8
CELL_VISUAL = 3                # visible width of one cell slot
GAP_BETWEEN_BOARDS = " " * 8   # spaces between framed boards

# ========= 3) ANSI / width helpers =========
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")  # strip ANSI codes


def strip_ansi(s: str) -> str:
    """Return s with ANSI codes removed (keeps width math accurate)."""
    return ANSI_RE.sub("", s)


def pad_visual(s: str, width: int) -> str:
    """
    Pad s with spaces so its visible width equals width.

    Handles emoji width and ignores ANSI color codes when measuring.
    """
    vis = wcswidth(strip_ansi(s))
    if vis < 0:
        vis = len(strip_ansi(s))
    return s + " " * max(0, width - vis)


# ========= 4) Small UI helpers =========
def strong_yellow(text: str) -> str:
    """Bright yellow text."""
    return Style.BRIGHT + Fore.YELLOW + text + Style.RESET_ALL


def strong_white(text: str) -> str:
    """Bright white text."""
    return Style.BRIGHT + Fore.WHITE + text + Style.RESET_ALL


def clear_screen():
    """Clear terminal to simulate a single refreshing screen."""
    os.system("cls" if os.name == "nt" else "clear")


# ========= 5) Framing helpers =========
TL, TR, BL, BR = "┌", "┐", "└", "┘"
H, V = "─", "│"


def title_bar(text: str, inner_width: int) -> str:
    """
    Build a top border with a centered title, e.g.:

    ┌──── Enemy Fleet ────────────┐
    """
    label = f" {text} "
    spare = inner_width - len(strip_ansi(label))
    left = max(0, spare // 2)
    right = max(0, spare - left)
    return TL + (H * left) + label + (H * right) + TR


def horizontal_bar(inner_width: int) -> str:
    """Bottom border, e.g.: └──────────────┘"""
    return BL + (H * inner_width) + BR


# ========= 6) Cell + board rendering =========
def format_cell(symbol: str) -> str:
    """Return one cell padded to CELL_VISUAL columns."""
    return pad_visual(symbol, CELL_VISUAL)


def build_board_block(title_text: str,
                      grid_rows: list[list[str]]) -> list[str]:
    """
    Build a single framed board (title + header + rows + bottom).

    Returns a list of text lines representing that board.
    """
    inner_width = 3 + (BOARD_SIZE * CELL_VISUAL)
    lines = []

    lines.append(title_bar(title_text, inner_width))

    nums = "".join(format_cell(str(i)) for i in range(1, BOARD_SIZE + 1))
    header = "   " + nums
    lines.append(V + strong_white(header) + V)

    for r in range(BOARD_SIZE):
        row_label = strong_white(chr(65 + r))
        row_cells = "".join(format_cell(ch) for ch in grid_rows[r])
        content = f"{row_label}  {row_cells}"
        content = pad_visual(content, inner_width)
        lines.append(V + content + V)

    lines.append(horizontal_bar(inner_width))
    return lines


def display_boards(enemy_view: list[list[str]],
                   player_board: list[list[str]]) -> None:
    """Print both framed boards side-by-side (fixed layout)."""
    left_block = build_board_block(LEFT_TITLE, enemy_view)
    right_block = build_board_block(RIGHT_TITLE, player_board)

    for lft, rgt in zip(left_block, right_block):
        print(lft + GAP_BETWEEN_BOARDS + rgt)


# ========= 7) Enemy AI =========
def enemy_take_one_shot(player_board, player_ships, tried):
    """
    Fire one random shot at the player board.

    - Avoid repeating positions using `tried`.
    - Mark 💥 or 💦 on the player board.
    - Remove a ship position on hit.

    Returns a short status message.
    """
    global total_enemy_shots

    while True:
        r = random.randint(0, BOARD_SIZE - 1)
        c = random.randint(0, BOARD_SIZE - 1)
        if (r, c) in tried or player_board[r][c] in (MISS, HIT):
            tried.add((r, c))
            continue
        tried.add((r, c))
        break

    pos = f"{chr(65 + r)}{c + 1}"
    total_enemy_shots += 1
    if (r, c) in player_ships:
        player_board[r][c] = HIT
        player_ships.remove((r, c))
        return f"👾 Enemy fires at {pos} — {HIT} Hit!"
    player_board[r][c] = MISS
    return f"👾 Enemy fires at {pos} — {MISS} Miss."


# ========= 8) Game state =========
enemy_view = [[WATER] * BOARD_SIZE for _ in range(BOARD_SIZE)]
player_board = [[WATER] * BOARD_SIZE for _ in range(BOARD_SIZE)]

NUM_SHIPS = 3

enemy_ships = set()
while len(enemy_ships) < NUM_SHIPS:
    enemy_ships.add(
        (random.randint(0, BOARD_SIZE - 1),
         random.randint(0, BOARD_SIZE - 1))
    )

player_ships = set()
while len(player_ships) < NUM_SHIPS:
    r = random.randint(0, BOARD_SIZE - 1)
    c = random.randint(0, BOARD_SIZE - 1)
    if (r, c) not in player_ships:
        player_ships.add((r, c))
        player_board[r][c] = SHIP_CHAR


# ========= 8A) Welcome screen =========
def ascii_command_title():
    """Big header that feels like a command console."""
    print(Style.BRIGHT + Fore.CYAN + "═" * 80 + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.CYAN)
    print(
        "█▄▄ ▄▀█ ▀█▀ ▀█▀ █   █▀▀ █▀ █ █ █ █▀█ █▀   █▀▀ █▀█ █▀▄▀█ "
        "█▀▄▀█ ▄▀█ █▄░█ █▀▄"
    )
    print(
        "█▄█ █▀█ ░█░ ░█░ █▄▄ ██▄ ▄█ █▀█ █ █▀▀ ▄█   █▄▄ █▄█ █░▀░█ "
        "█░▀░█ █▀█ █░▀█ █▄▀"
    )
    print(
        Fore.YELLOW + "     B A T T L E S H I P   C O M M A N D"
        + Style.RESET_ALL
    )
    print(Fore.CYAN + "═" * 80 + Style.RESET_ALL)


def ascii_ship_art():
    """Compact battleship ASCII (tinted lightly for a steel look)."""
    ship = r"""
⠀⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠰⠶⢿⡶⠦⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣀⣿⣿⣿⣿⣿⣿⡇⢀⠀⢀⡀⠀⣀⣀⣠⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠉⠻⠿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣶⣶⣾⣧⣤⣴⣆⣀⢀⣤⡄⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
    colored = []
    for line in ship.splitlines():
        out = []
        for ch in line:
            if ch in "#*+=-:/\\":
                out.append(Fore.CYAN + ch + Style.RESET_ALL)
            elif ch in "_|":
                out.append(Fore.WHITE + ch + Style.RESET_ALL)
            else:
                out.append(ch)
        colored.append("".join(out))
    print("\n".join(colored))


def mission_briefing():
    """Professional, game-like instruction panel."""
    briefing = [
        "MISSION BRIEFING:",
        "",
        "Welcome, Commander. A hostile fleet has breached these waters.",
        "The tactical grid is 8×8 sectors (rows A–H, columns 1–8).",
        "Any sector may hide empty waves… or an enemy hull.",
        "",
        "Orders:",
        " • Enter strike coordinates such as A1, C7, or H8.",
        " • Each strike will update the radar:",
        "     💥  Direct hit on an enemy ship",
        "     💦  Shot splashed into the sea",
        "     🌊  Uncharted waters (not yet targeted)",
        "     🚢  Player fleet positions (only on the right radar)",
        "",
        "Rules of Engagement:",
        " • Turns alternate — one shot per side.",
        " • Victory: sink the entire enemy fleet.",
        " • Defeat: lose all ships in the player fleet.",
        "",
        "Maintain accuracy. Conserve ammunition. Hold the line.",
    ]
    width = max(len(line) for line in briefing) + 4
    top = "┌" + "─" * width + "┐"
    bot = "└" + "─" * width + "┘"

    print()
    print(Fore.YELLOW + top + Style.RESET_ALL)
    for line in briefing:
        print("│ " + line.ljust(width - 2) + " │")
    print(Fore.YELLOW + bot + Style.RESET_ALL)


def show_welcome_screen():
    """Full welcome screen: title, ship art, briefing, and start prompt."""
    clear_screen()
    ascii_command_title()
    ascii_ship_art()
    mission_briefing()
    print(
        Style.BRIGHT + Fore.GREEN
        + "\n▶ Press Enter to assume command and begin battle! ◀"
        + Style.RESET_ALL
    )
    input()
    clear_screen()


# ========= 9) Intro screen =========
show_welcome_screen()

# ========= 10) Main loop =========
player_msg = ""          # last message from player shot
enemy_msg = ""           # last message from enemy shot
enemy_tried = set()      # coordinates already attempted by enemy
total_player_shots = 0
total_enemy_shots = 0

while player_ships and enemy_ships:
    clear_screen()
    print("===================================")
    print(
        Style.BRIGHT + Fore.MAGENTA
        + " 🚢 Battleship — Alternating Turns "
        + Style.RESET_ALL
    )
    print("===================================\n")

    display_boards(enemy_view, player_board)

    legend = (
        f"{HIT}=Hit  {MISS}=Miss  {WATER}=Water  {SHIP_CHAR}=Player ship"
    )
    enemy_left = len(enemy_ships)
    player_left = len(player_ships)
    enemy_bar = " ".join([SHIP_CHAR] * enemy_left) if enemy_left else "—"
    player_bar = " ".join([SHIP_CHAR] * player_left) if player_left else "—"

    print("\n" + strong_white("Legend: ") + legend)
    print(
        strong_white("Status: ")
        + f"Enemy ships: {enemy_left} [{enemy_bar}]   "
        + f"Player ships: {player_left} [{player_bar}]   "
        + f"Shots — Player: {total_player_shots}  "
        + f"Enemy: {total_enemy_shots}"
    )

    if player_msg:
        print("\n" + player_msg)
    if enemy_msg:
        print(enemy_msg)

    # --- Player turn ---
    print("\n" + strong_yellow("— Player Turn —"))
    guess = input("Enter position (e.g., A1) or Q to quit: ").strip().upper()
    if guess == "Q":
        clear_screen()
        print("👋 Game ended by user.")
        break

    if len(guess) < 2:
        player_msg = (
            "❌ Format must be a letter followed by a number, e.g., A1."
        )
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

    r = ord(row_letter) - 65
    c = col1 - 1

    if enemy_view[r][c] in (MISS, HIT):
        player_msg = "⚠️ That position was already tried."
        continue

    total_player_shots += 1
    if (r, c) in enemy_ships:
        enemy_view[r][c] = HIT
        enemy_ships.remove((r, c))
        player_msg = f"🎯 HIT at {row_letter}{col1}! {HIT}"
    else:
        enemy_view[r][c] = MISS
        player_msg = f"💦 MISS at {row_letter}{col1}. {MISS}"

    if not enemy_ships:
        break

    # --- Enemy turn ---
    enemy_msg = (
        strong_yellow("— Enemy Turn —") + "\n"
        + enemy_take_one_shot(player_board, player_ships, enemy_tried)
    )

    if not player_ships:
        break


# ========= 11) End screen =========
if enemy_ships and not player_ships:
    clear_screen()
    print("===================================")
    print(
        Style.BRIGHT + Fore.MAGENTA
        + " 🚢 Battleship — Game Over"
        + Style.RESET_ALL
    )
    print("===================================\n")
    display_boards(enemy_view, player_board)
    print("\n💀 All player ships are sunk.")

elif player_ships and not enemy_ships:
    clear_screen()
    print("===================================")
    print(
        Style.BRIGHT + Fore.MAGENTA
        + " 🚢 Battleship — Victory!"
        + Style.RESET_ALL
    )
    print("===================================\n")
    display_boards(enemy_view, player_board)
    print("\n🏆 All enemy ships are sunk! 🎉")
