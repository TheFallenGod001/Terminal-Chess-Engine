# Terminal Chess Engine

A terminal-based chess game written in Python with move validation, piece logic, and two input modes. Play in the terminal using standard coordinates or arrow keys with a snapping feature.

## Features

* Full chess piece move logic (King, Queen, Rook, Bishop, Knight, Pawn)
* Turn-based gameplay (white vs black)
* Move validation with piece-blocking logic
* Danger zone calculation (squares attacked by opponent pieces)
* King protection (can't move into check)
* Terminal UI with Unicode chess pieces and color-coded squares
* Two input modes: coordinates or keyboard navigation
* Keyboard "snapping" — press an arrow key twice quickly to jump to the next piece in that direction

## How to Play

```bash
pip install rich keyboard

python chess.py
```

### Standard Input Mode

Enter positions as comma-separated coordinates: `row,column` where rows are 1-8 (top to bottom) and columns are 1-8 (left to right).

```
Enter position to choose(comma separated): 2,4
```

Squares light up as you navigate:
* **Blue** — your currently selected square
* **Green** — valid moves for that piece
* **Red** — opponent pieces you can capture

Press `q` to switch to keyboard mode.

### Keyboard Mode

Use arrow keys to move around the board:
* **LEFT / RIGHT** — move horizontally
* **UP / DOWN** — move vertically
* **Double-tap an arrow** (within 0.25s) — "snap" to the next piece of your color in that direction
* **q** — switch back to standard input mode

The snapping feature is handy for quickly jumping across the board without clicking through every square.

## Code Structure

**`chess_pieces` class:** 
Handles individual piece move generation. Each piece type (K, Q, R, B, N, pawn) has its own movement logic. The `moves()` method takes current position and lists of friendly/enemy positions, returns all legal destinations accounting for blocked paths and captures.

**`Square` class:**
Represents one board square. Tracks whether it's empty or occupied, the piece on it, and styling (normal, chosen, valid moves, elimination/capture).

**`Board` class:**
The main game board (8×8). Manages:
* Piece positions and piece lists for each side
* Turn tracking
* Move validation via `choose()` (select a piece and show valid moves)
* Danger zone scanning (which squares are under attack)
* Snapping logic via `snap()` (find the next piece in a given direction)
* Display via the `rich` library

## Piece Move Logic

* **King** — 1 square in any direction, avoids danger zones
* **Queen** — combines Rook + Bishop
* **Rook** — straight lines (up/down/left/right), stops when blocked
* **Bishop** — diagonals, stops when blocked
* **Knight** — L-shaped (2+1), ignores pieces between start and end
* **Pawn** — forward one square (two on first move), captures diagonally

The move generation handles:
* Board boundaries (1-8 for both axes)
* Friendly piece blocking (can't land on own pieces)
* Enemy piece blocking (rooks/bishops/queens stop, pawns/knights ignore)
* Captures (landing on enemy pieces)

## Board State

The board is initialized with standard chess starting positions (pieces on rows 1-2 for white, 7-8 for black). A few starting pawns are removed as test cases — you can uncomment or modify this in `Board.__init__()`.

Positions are stored as tuples: `(row, column)` where both range 1-8.

## Known Issues / TODOs

* Move-blocking logic has some bugs (particularly in rook/bishop movement when using `a1`, `a2`, `a3`, `a4` flags)
* No check/checkmate detection beyond danger zone for the king
* No en passant, castling, or pawn promotion
* No move history or undo
* No way to actually move a piece (only validation/display of legal moves)
* `dangerZones` parameter sometimes `None` instead of empty list — should handle this better

## Dependencies

* `rich` — terminal UI and styling
* `keyboard` — keyboard input handling (requires elevated privileges on some systems)

## Next Steps

To make this a fully playable game:
1. Implement actual piece movement (currently you can only select pieces and see valid moves)
2. Add check/checkmate detection
3. Implement special moves (castling, en passant, pawn promotion)
4. Add a move history for undoing
5. Fix the move-blocking logic bugs
6. Consider adding a simple AI opponent
