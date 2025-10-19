# Robot Pico — Competition runner for Raspberry Pi Pico 2

A compact MicroPython project to control a two-stepper robot (line-follow/dowel tasks) using a Raspberry Pi Pico.

## Summary

- Controls stepper motors via GPIO and optional TMC2209 UART driver.
- Reads two TCS34725 color sensors for line/dowel detection and corrections.
- Uses an SSD1306 I2C OLED for status and a small buzzer/speaker for beeps.

## Quick start

1. Copy the project to your Raspberry Pi Pico filesystem (use Thonny, rshell, ampy, or similar).
2. Edit `rv.py` to set the `commands` string for your course.
3. Power the robot, connect OLED and TCS sensors to the I2C buses (see pin assignments in `main.py`).
4. Reset the Pico; the program will load and run the course.

## Important files

- `main.py` — Main robot control program (movement, sensor reading, command parsing).
- `rv.py` — Example command list and configuration used by `main.py`.
- `TMC_2209_StepperDriver.py` and `TMC_2209_uart.py` — Optional TMC2209 UART control / helper classes.
- `tcs34725.py` — Driver for TCS34725 color sensors.
- `ssd1306.py` — SSD1306 OLED driver (I2C).

## Pin summary (as used in `main.py`)

- STEP: GPIO14
- DIR: GPIO11, GPIO15
- ENABLE: GPIO10
- OLED (I2C): I2C(1) SCL=GPIO3 SDA=GPIO2
- OLED2 (I2C): I2C(0) SCL=GPIO13 SDA=GPIO12
- TCS sensors: I2C buses above

## Notes & tips

- Timing and accelerations are tuned for the team's hardware; adjust `straightsteps`, `turnsteps`, and speed constants if behavior differs.
- For best performance during a run, avoid making heavy changes to `main.py`; tweak `rv.py` commands instead.
