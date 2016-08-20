Features
========

- Add levels
- Add skills (easy, medium, hard)
- Configurable board size
- Configurably allow monomino, domino, trominoes(, pentominoes, ...?)
- Fullscreen mode?
- AI
- Multiplayer mode

- UI

  * Preview next piece
  * Preserve board aspect with window resize

- Scoring

  * Implement ksirtet's scoring formulas
  * Save high score list to a file
  * highlight top ten or top score in the status bar like ksirtet

- Line removal: add options for

  * Pulse full lines with white
  * Animate line removal

- Shadowing

  * Projection of piece as a shadow below bottom of board (like ksirtet)
  * Shadow piece on the stack of tetrominoes where it would be placed if dropped down

- Keys

  * Implement full set of ksirtet key actions
  * Configurable keybindings

Packaging
=========

- depends on wxPython (should I alternatively or optionally use pyQT or pyGTK?)
- pypi
- ebuild
- deb
- rpm
