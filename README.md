<div align="center">
  <img src="images/logo.svg" width="60%" alt="StockFish-Vision"/>
</div>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [1. Introduction](#1-introduction)
- [2. Disclaimer](#2-disclaimer)
- [3. Features](#3-features)
- [4. Architecture \& Workflow](#4-architecture--workflow)
  - [4.1 Module 1: Chessboard Recognition](#41-module-1-chessboard-recognition)
  - [4.2 Module 2: Move Extraction](#42-module-2-move-extraction)
  - [4.3 Module 3: Stockfish Integration](#43-module-3-stockfish-integration)
  - [4.4 Module 4: GUI / UX Layer](#44-module-4-gui--ux-layer)
- [5. Installation](#5-installation)
- [6. License](#6-license)

---

## 1. Introduction

**StockFish-Vision** is a Python-based project that leverages **Computer Vision** and **Stockfish Engine** to analyze 2D chessboards (e.g., from chess.com screenshots), recognize board state (FEN), and suggest optimal next moves automatically.

---

## 2. Disclaimer

- This project is intended **solely for educational, analytical, and research purposes**.
- It **must not be used in online rated matches or competitive play**.  
- Using external assistance during games may violate the terms of service of chess platforms (e.g., [Chess.com Fair Play Policy](https://www.chess.com/legal/fair-play)) and could result in account bans or other penalties.

> Use this tool responsibly — to **learn**, **explore strategy**, and **improve your understanding** of chess.

---

## 3. Features

- [**DONE**] Recognize chess pieces on 2D board screenshots using OpenCV Template Matching.
- [**DONE**] Generate valid FEN strings directly from board images.
- [**UPDATING**] Stockfish engine integration (upcoming).
- [**UPDATING**] Automatic move detection from screen changes.
- [**UPDATING**] Simple GUI/UX overlay for desktop users.

---

## 4. Architecture & Workflow

### 4.1 Module 1: Chessboard Recognition

This module loads an input chessboard image (e.g., a screenshot from chess.com), splits it into 8×8 cells, and classifies each cell using template matching to detect which piece (if any) is present.

- **Tech Stack:** `OpenCV`, `NumPy`
- **Key Output:** FEN string representing the board state
- **Key Script:** `src/match_template.py`
- **Templates Directory:** `templates/` with piece variants on both light and dark backgrounds.

### 4.2 Module 2: Move Extraction

> Status: Updating...

This module will detect the last move made by comparing two sequential board states or leveraging board annotations (arrows, highlights).

### 4.3 Module 3: Stockfish Integration

> Status: Updating...

This module will connect to the Stockfish chess engine to calculate the best move from the current FEN.

### 4.4 Module 4: GUI / UX Layer

> Status: Updating...

The UX layer will overlay suggested moves directly on the screen (optional) or in a pop-up window, depending on user configuration.

---

## 5. Installation

To ensure the computer vision model works accurately, please configure your chess interface (e.g., Chess.com) as follows:

- **Piece Style (Theme):** `Classic`
- **Board Style:** `Blue`
- **Turn off Coordinates:**  Disable board coordinates (letters/numbers) to avoid misclassification.
- **Chessboard:** Download by share feature of Chess.com

> These settings are optimized to match the trained templates in the `templates/` folder.  
> Other themes or styles **may cause recognition errors**.

>  We're actively working to **diversify and expand the template set** to support more styles and layouts in future updates.

python main.py --image ./images/board_3.png --debug --output ./fen_output.txt

---

## 6. License
This project is licensed under the MIT License. See the LICENSE file for more details.
