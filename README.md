🚢 Battleship Game (Python Terminal Edition)

This is a Python-based command-line Battleship game where the user plays against the computer (enemy).
The game uses an emoji-based grid display and runs in alternating turns until one side’s fleet is completely destroyed.

The project was developed as part of the Python Essentials Portfolio Project (Full Stack Software Development Diploma).
It demonstrates fundamental Python programming skills: loops, conditionals, functions, data structures, error handling, and external library usage.

🎯 Project Purpose

User Goal: To play a fun, logic-based Battleship game in the terminal, with clear feedback and a visually engaging grid system.

Developer Goal: To design and implement a working Python application that demonstrates programming constructs, input validation, data handling, version control, and documentation.

🛠️ Features
✅ Core Features

Two boards displayed side by side:

Enemy Fleet → shows only what the user discovers (hits 💥 and misses 💦).

Your Fleet → shows the user’s own ships (🚢), hits, and misses.

Alternating turns: The user takes a shot, then the enemy takes one.

Random ship placement for both fleets, ensuring replayability.

Emoji-based grid symbols for better visuals:

🌊 = Water (unknown)

💦 = Miss

💥 = Hit

🚢 = User ship (visible only on the right board)

Input validation:

Rejects invalid inputs (e.g., "Z9", "11A").

Warns if a guess is repeated.

Prevents firing outside the grid.

Clear game messages:

Feedback after every turn (hit/miss).

Victory/defeat message when game ends.

Quit option by typing Q.

🌟 Extra Features

Centered titles above each board: Enemy Fleet and Your Fleet.

Aligned grid display even when using emojis, by handling visual widths (wcwidth).

Color-coded messages using colorama:

Hits (💥) in red.

Misses (💦) in blue.

Titles in yellow.

Row/column labels in white.

Replayability: Ships are hidden in random positions each run.

🧰 Technologies Used

Python 3 — core programming language.

colorama
 — provides colored terminal output across platforms.

wcwidth
 — ensures emoji symbols align correctly in grids by measuring visual width.

Git & GitHub — version control and project management.

▶️ How to Run the Project
1. Clone the repository
git clone https://github.com/boneyphilip/battleship-game.git
cd battleship-game

2. Install dependencies

Make sure Python 3 is installed. Then run:

pip install -r requirements.txt

3. Run the game
py battleship.py


(or python3 battleship.py depending on system)

📖 Instructions for Playing

The game starts by displaying two 8×8 grids:

Enemy Fleet (hidden ships, revealed as you hit/miss).

Your Fleet (shows user ships 🚢).

Ships are placed randomly on both sides.

On each turn:

Enter a guess like A1, C7, or H8.

Results appear immediately on the grid.

After the user’s turn, the enemy fires at the user’s fleet.

The game continues until:

All enemy ships are sunk → Victory 🏆

All user ships are sunk → Defeat 💀

At any time, type Q to quit the game.

🔍 Testing & Validation

Input testing:

Invalid row input (e.g., Z5) → error message shown.

Invalid column input (e.g., A9) → error message shown.

Repeated guesses (e.g., A1 twice) → warning shown.

Game logic:

Ships placed randomly each run, verified over multiple plays.

Both win and loss conditions tested manually.

Linting:

Code passes PEP8
 style checks.

User experience:

Game tested in Windows PowerShell and VS Code terminal.

Emoji alignment validated using wcwidth.

🗂️ Project Development (Git Workflow)

Development tracked with Git & GitHub.

Each feature/fix committed with a clear descriptive message, e.g.:

Add alternating turns between player and enemy

Fix emoji grid alignment with wcwidth

Improve input validation and error messages

Commits kept small and meaningful to show progression.

🚀 Future Improvements

Allow the user to choose grid size (e.g., 6×6, 10×10).

Enable manual ship placement by the user.

Add turn counter or scoring system.

Support multiple ship sizes (like the classic Battleship game).

Deploy to PythonAnywhere or Replit for easier access.

👨‍💻 Credits

colorama → for terminal text coloring.

wcwidth → for emoji width alignment.

General game logic and structure coded independently by the developer for assessment.

📦 Deployment Notes

Currently, the game runs locally.
For deployment to a cloud platform:

Upload repository to GitHub.

Link with PythonAnywhere or Replit.

Ensure requirements.txt is included with:

colorama
wcwidth

✅ Assessment Criteria Mapping

LO1–LO3: Python loops, functions, lists, sets, and error handling implemented.

LO4: README clearly explains the program.

LO5: Errors tested and handled gracefully (invalid input, repeats).

LO6: Libraries (colorama, wcwidth) used appropriately.

LO7: Data model → 2D lists (boards) + sets (ships).

LO8: GitHub commits document development.

LO9: Deployment instructions provided.

📜 Plagiarism Statement
This project is an original work developed for the Diploma in Full Stack Software Development.
All external libraries used (colorama, wcwidth) are properly credited.
The project follows academic integrity guidelines and Code Institute’s assessment requirements.