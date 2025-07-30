# Guide for `commands` in `rv.py`

### Format
Every line in `command` is written as:
```
action123 modifier1 modifier2
```
- `action` tells the robot what to do
- `123` is a numerical parameter for the action. Not all actions have them.
- `modifiers` alter the action, like slowing it down.

### Actions
- **Straights**
  - `s123` - go straight 123 cm. Negative is backwards
  - `sd123` - go straight by √2 × 123 cm. Used for diagonals.
- **Turns**
  - `t123` - turn 123° right. Negative is left
  - `l` - left 90°
  - `r` - right 90°
  - `u` - 180°
  - `ld` - left 45°. Used for diagonals
  - `rd` - right 45°. Used for diagonals.

### Modifiers
- `slow` - makes movements slow
- `no-correction` - prevents adjusting the robot by reading the lines on the track with color sensors (straight moves only)