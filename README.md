<pre align="center">

██████   █████  ████████ ████████ ██      ███████ ███████ ██   ██ ██ ██████  ███████ 
██   ██ ██   ██    ██       ██    ██      ██      ██      ██   ██ ██ ██   ██ ██      
██████  ███████    ██       ██    ██      █████   ███████ ███████ ██ ██████  ███████ 
██   ██ ██   ██    ██       ██    ██      ██           ██ ██   ██ ██ ██           ██ 
██████  ██   ██    ██       ██    ███████ ███████ ███████ ██   ██ ██ ██      ███████ 
                                                                                     
                                                                                      



*Battleships Game – Python Terminal Edition*  

⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠰⠶⢿⡶⠦⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣀⣿⣿⣿⣿⣿⣿⡇⢀⠀⢀⡀⠀⣀⣀⣠⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠉⠻⠿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣶⣶⣾⣧⣤⣴⣆⣀⢀⣤⡄⠀⠀⣀⡀⠀

</pre>

---

## Battleships Game – Python Terminal Edition

This is a **Python-based Battleships game** built for the terminal.  
The player battles against the computer with alternating turns until one fleet is destroyed.  

This project was developed as part of the **Python Essentials Portfolio Project** (Full Stack Software Development Diploma).  
It demonstrates core Python skills: loops, functions, lists, input validation, error handling, and use of external libraries.

---

## 🎯 Project Purpose

- **User Goal**: Play a fun, logic-based Battleships game with interactive feedback.  
- **Developer Goal**: Implement a Python project showing clear logic, error handling, and visual engagement in the terminal.  

---

## 🛠️ Features

### Core Features
- Two side-by-side boards:
  - **Enemy Fleet** → shows only discovered hits 💥 and misses 💦  
  - **Your Fleet** → shows your ships 🚢 plus hits & misses  
- Turn-based play: player and computer alternate shots.  
- Random ship placement for replayability.  
- Input validation prevents invalid or repeated guesses.  
- Victory / defeat messages when the game ends.  

### Visual Enhancements
- **Color-coded feedback** with `colorama`:  
  - Hits → Red 💥  
  - Misses → Blue 💦  
  - Fleet names → Yellow  
- **Emoji-based grid display** with `wcwidth` for alignment.  
- **Mission briefing screen** with typing effect.  
- **ASCII Battleship art and gradient title** on welcome screen.  

---

## 📖 How to Play

1. Clone the repository:  
   ```bash
   git clone https://github.com/boneyphilip/battleship-game.git
   cd battleship-game

2. Install dependencies:

   pip install -r requirements.txt


3. Run the game:

   python3 battleship.py

--------------------------------------------------------------------------
   📸 Screenshots

👉 (Replace these placeholders with actual images from your game output)

- Welcome Screen
  
   ![Welcome Screen](docs/images/welcome.png)

- Mission Briefing

  ![Mission Briefing](docs/images/briefing.png)

- Game Board Example

  ![Game Board](docs/images/board.png)

------------------------------------------------------------------------

  🧪 Testing & Validation

- Input validation tested:

   - Invalid coordinates (e.g., Z5, 11A) rejected.

   - Repeated guesses flagged.

   - Out-of-range inputs blocked.

- Gameplay tested:

  - Both win and loss conditions verified.

  - Ships placed randomly each run.

- Style:

  - Code checked with PEP8/Flake8, no major warnings.

- UX tested on:

   - VS Code terminal

   - Windows PowerShell

   - Replit console

   - PythonAnywhere

-------------------------------------------------------------------

🗂️ Technologies Used

   - Python 3 — core language

   - Colorama — colored terminal text

   - Wcwidth — ensures emojis align in grid

   - Git & GitHub — version control

--------------------------------------------------------------------

🚀 Deployment

Run locally

   - Clone repo

   - Install dependencies (pip install -r requirements.txt)

   - Run with python3 battleship.py

Run online

   - Linked with Replit for instant play in browser.

   - Deployed on PythonAnywhere for cloud execution.

----------------------------------------------------------------------

👨‍💻 Credits

  - Colorama → terminal text coloring.

  - Wcwidth → emoji width alignment.

  - ASCII Battleship art sourced from community ASCII art templates.

  - Game logic designed independently by the developer.

----------------------------------------------------------------------

📜 Plagiarism Statement

   This project is an original work developed for the Diploma in Full Stack Software Development.
   All external resources (Colorama, Wcwidth) are credited.
  
