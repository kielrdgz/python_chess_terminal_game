```
Terminal-Based Chess Game (Python)

    Terminal-based chess game built entirely using native 
    Python. The engine strictly enforces standard FIDE chess rules, 
    providing a command-line interface where users can play chess 
    matches without any external graphical dependencies.

➤ Content/Features 
    ● Supports En-Passant, Castling, and Pawn-to-Queen-Promotion
    ● Game Modes: PvP (locally/same terminal) or PvE (simple automated 
      opponent)
    ● Side Selection: Choose WHITE or BLACK side or by random assignment
    ● Checks for check, checkmate, and general legal/valid moves

➤ How to Play
1. Download all files and run the main file via:
        python main.py -o <enemyai (PvE) or player (PvP)> -t <choose or random>
    Note: -o (opponent); -t (turn-basis)

2. Choose a chess piece using the available pieces on your side
    Note: pieces with no valid moves will not be shown

3. Enter valid moves 
    Note: Invalid moves are not processed; to exit Move Interface,
    enter -1 (this prompts you to choose a new/different Chess Piece)

4. Castling is achieved by moving the King to its legal destination square
   and promotion triggers automatically when a pawn reaches the opposite end of the board.


```