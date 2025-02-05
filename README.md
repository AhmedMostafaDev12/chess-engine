# Chess Engine with AI and GUI

## ♟️ Overview
This is a **fully functional Chess Engine** that allows you to play against a **computer AI** or another **human player** using an interactive **GUI**. The AI is powered by the **Minimax algorithm with Alpha-Beta Pruning** to evaluate moves efficiently.

## 🚀 Features
- **Minimax Algorithm with Alpha-Beta Pruning** for optimized AI decision-making
- **Complete Chess Rule Implementation**, including:
  - **Pawn Promotion** ♙➡️♕
  - **En Passant** 🏇
  - **Castling** ♔ ↔️ ♖
- **Smooth GUI** for an engaging gameplay experience
- **Two Game Modes:**
  - **Human vs. Computer** (AI opponent)
  - **Human vs. Human** (Local multiplayer)
- **Object-Oriented Programming (OOP)** for structured and maintainable code

## 🛠️ Project Structure
The project is organized into three main files:

1. **`chessmain.py`** – Handles the **GUI** and interactive gameplay
2. **`chessengine.py`** – Implements **move generation** and **validation**
3. **`AI.py`** – Contains the **AI logic**, including **Minimax with Alpha-Beta Pruning**

## 📦 Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/AhmedMostafaDev12/chess-engine.git
   cd chess-engine
   ```
2. **Install dependencies:**
   ```bash
   pip install pygame
   ```
3. **Run the game:**
   ```bash
   python chessmain.py
   ```

## 🎮 How to Play
- **Start the game** by running `chessmain.py`
- **Choose a mode**: Play against the AI or another human
- **Make moves** by clicking on pieces and selecting valid squares
- **Win by checkmating** the opponent’s king!

## some photos 
![game start](https://github.com/AhmedMostafaDev12/chess-engine/blob/main/Screenshot%202025-02-05%20200000.png)


## 🧠 AI Algorithm
The AI utilizes the **Minimax algorithm** with **Alpha-Beta Pruning**, which:
- Explores future moves recursively
- Prunes unnecessary branches to improve efficiency
- Selects the best move based on board evaluations

## 🏆 Future Improvements
- Implementing **difficulty levels** for AI
- Adding **sound effects** and **animations**
- Online multiplayer support

## 🤝 Contributing
Feel free to **fork this repository** and contribute improvements!





