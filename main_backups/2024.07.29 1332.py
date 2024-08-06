# TO BE RUN ON A RASPBERRY PI PICO
# UPLOAD FILE WITH AMPY OR RSHELL
from machine import freq
freq(250000000)
from machine import Pin, Timer, I2C, reset, freq, PWM, ADC
import gc
import ssd1306
from time import sleep, ticks_ms, sleep_us, time
from math import sqrt


# DOWEL OFFSET 7CM
# IF INTIAL SPEED IS OVER 2, TURN UP THE ACCEL TO MAX
targetTime = 1.3

# TURN CONSTANTS
rturnsteps = 17.18
lturnsteps = rturnsteps

# ACCEL VARS
saccel = 6.475
saccel_initial = 4.9
taccel = 4.9

# SPEED VARS
turnSpeedDefault = 1.85
maxstraightSpeed = 2.43
minstraightSpeed = 0.04
backwardsMaxSpeed = 1


command4s= """
s32
r
s50
l
s200
l
s100
"""
commands4 = """
s32
r
s50
l
s100
l
s50
r
s50
r
s50
l
s50
l
s150
l
s50
l
s50
r
s50
r
s50
l
s100
l
s50
l
s50
l
s50
r
s50
r
s50
l
s50
l
s50
r
s50
r
s150
r
s50
r
s50
l
s50
l
s50
r
s50
r
s40
u
s40
l
s50
l
s50
r
s50
r
s50
l
s50
l
s150
l
s50
l
s50
r
s50
r
s50
l
s99.7
l
s11.3
"""

commands4 = """
r
r
r
r
r
r
r
r
r
r
r
r
"""

commands = """
l
l
l
l
l
l
l
l
l
l
l
l
"""

commands6 = """
u
u
u
u
u
u
u
u
"""


commands3 = """
s150
s-150
s150
s-150
s150
s-150
"""


# DO NOT EDIT THESE DURING COMPETITION
# Negative means to decrease the amount of time taken, positive means to increase the amount of time taken
startTimeOffset = 0.205
speed_steps_ratio = 0.04961
straightsteps = 127.088
u_offset = 1.000
currentmA = 1250
silent = True
tmc_uart_en = True
spreadCycleEn = True


def dirfront(dirPin):
    dirPin.low()


def dirback(dirPin):
    dirPin.high()


def printlcd(text):
    try:
        display.fill(0)
        display.text(text, 0, 0, 1)
        display.show()
    except:
        pass
    print(text)


def calcS(speedy):
    return round((124.944/speedy) - 10.157)


def s(cm, ending):
    global command_number
    global straightSpeed
    global runCurrent
    global speed_steps_ratio
    AdjustSpeedTimeRealTime()  # timing function
    if cm < 0 and straightSpeed > backwardsMaxSpeed:
        straightSpeed = backwardsMaxSpeed
    print('STRAIGHT')
    try:
        display.fill(0)
        display.text('STRAIGHT', 0, 0, 1)
        display.text(f'Speed: {straightSpeed:.2f}', 0, 30, 1)
        display.show()
    except:
        pass

    if cm < 0:
        dirfront(dirPin1)
        dirfront(dirPin2)
        cm *= -1
    else:
        dirback(dirPin1)
        dirback(dirPin2)
    steps = round(cm*straightsteps)
    if command_number == 0:
        saccel_literal = saccel_initial
    else:
        saccel_literal = saccel
    saccel_literal = 25000/saccel_literal
    delay = []
    iAtEnd = int(steps*.411)
    iAtEndinitial = iAtEnd
    presetDelay = calcS(straightSpeed)
    gc.collect()
    for i in range(1, iAtEndinitial):
        delayi = round(saccel_literal/sqrt(i+1))
        if delayi < presetDelay:
            iAtEnd = i
            break
        delay.append(delayi)
    print(iAtEnd)
    print(len(delay))
    presetDelay = delay[iAtEnd-2]
    try:
        display.text('AccelSteps%: ' +
                     str(int((100*iAtEnd)/(steps/2))), 0, 45, 1)
        display.show()
    except:
        pass
    del saccel_literal
    del iAtEndinitial
    del delayi
    del cm
    # delay2=delay[::-1]
    # if presetDelay < delay2[0]:
    #    presetDelay=delay2[0]
    # print(2+steps-iAtEnd-(iAtEnd-1))
    if ending == False:
        for i in range(1, iAtEnd-1):
            step_pin.value(1)
            # sleep_us(delay[i])
            step_pin.value(0)
            sleep_us(delay[i])
        # startTimeConstant=ticks_ms()
        for i in range(iAtEnd-1, 2+steps-iAtEnd):
            step_pin.value(1)
            # sleep_us(presetDelay)
            step_pin.value(0)
            sleep_us(presetDelay)
        # endTimeConstant=ticks_ms()
        for i in range((-1*iAtEnd)+2, 0):
            step_pin.value(1)
            # sleep_us(delay2[i])
            step_pin.value(0)
            sleep_us(delay[i*-1])

    elif ending == True:
        for i in range(1, iAtEnd-1):
            step_pin.value(1)
            # sleep_us(delay[i])
            step_pin.value(0)
            sleep_us(delay[i])
        # startTimeConstant=ticks_ms()
        for i in range(iAtEnd-1, (2+steps-iAtEnd)-3600):
            step_pin.value(1)
            # sleep_us(presetDelay)
            step_pin.value(0)
            sleep_us(presetDelay)
        # endTimeConstant=ticks_ms()
        led.off()
        for i in range(1, 3600):
            step_pin.value(1)
            # sleep_us(presetDelay)
            step_pin.value(0)
            sleep_us(presetDelay)
        # endTimeConstant=ticks_ms()
        for i in range((-1*iAtEnd)+2, 0):
            step_pin.value(1)
            # sleep_us(delay[i])
            step_pin.value(0)
            sleep_us(delay[i*-1])

    # speed_steps_ratio=abs((endTimeConstant-startTimeConstant)/((2+steps-iAtEnd)-(iAtEnd-1)+1)-0.0165)/straightSpeed
    # print("ratio: " ,speed_steps_ratio)
    # print("microsec per step: ",((endTimeConstant-startTimeConstant)/((2+steps-iAtEnd)-(iAtEnd-1)+1))-0.0165)
    del delay
    gc.collect()
    command_number += 1  # Shift position to next command


def run_array(arr):
    commandsLength = len(arr)
    for index, command in enumerate(arr):
        command_number = index
        i = command.strip()
        if i.startswith("s"):
            if command_number == commandsLength-1:
                runTheLight = True
            else:
                runTheLight = False
            s(float(i.strip("s")), ending=runTheLight)

        elif i == "l" or i == "L":
            t(-90)
        elif i == "r" or i == "R":
            t(90)
        elif i == "u" or i == "U":
            t(180*u_offset)
        elif i == "-u" or i == "-U":
            t(-180*u_offset)


def turn(degrees, speedLimit):
    global command_number
    global turnTime
    startTurnTime = ticks_ms()
    printlcd("TURN")

    if degrees < 0:
        dirback(dirPin2)
        dirfront(dirPin1)
        turn_steps = lturnsteps
        degrees *= -1
    else:
        dirfront(dirPin2)
        dirback(dirPin1)
        turn_steps = rturnsteps
    presetDelay = calcS(speedLimit)
    steps = round(degrees*turn_steps)

    taccel_literal = 25000/taccel
    delay = []
    iAtEnd = int(steps*.411)
    iAtEndinitial = iAtEnd
    presetDelay = calcS(straightSpeed)
    for i in range(1, iAtEndinitial):
        delayi = round(taccel_literal/sqrt(i+1))-2
        if delayi < presetDelay:
            iAtEnd = i
            break
        delay.append(delayi)
    print(iAtEnd)
    print(len(delay))
    presetDelay = delay[iAtEnd-2]
    delay2 = delay[::-1]

    if presetDelay < delay2[0]:
        presetDelay = delay2[0]
    for i in range(1, iAtEnd-1):
        step_pin.value(1)
        # sleep_us(delay[i])
        step_pin.value(0)
        sleep_us(delay[i])
    for i in range(iAtEnd-1, 2+steps-iAtEnd):
        step_pin.value(1)
        # sleep_us(presetDelay)
        step_pin.value(0)
        sleep_us(presetDelay)
    for i in range(1, 1+steps-(2+steps-iAtEnd)):
        step_pin.value(1)
        # sleep_us(delay2[i])
        step_pin.value(0)
        sleep_us(delay2[i])
    del delay
    del delay2
    command_number += 1  # Shift position to next command
    if degrees == 90 or degrees == -90:
        turnTime = (ticks_ms()-startTurnTime)/1000
    del startTurnTime
    gc.collect()
    # print("turnTime: ",turnTime)


def t(degrees):
    turn(degrees, turnSpeedDefault)


def calculateTimeLeft(arr, pos):
    global straightSpeed
    global turnTime
    timeLeft = 0
    for index in range(pos, len(arr)):
        i = arr[index].strip()
        if i.startswith("s"):
            cm = abs(float(i.lstrip("s")))
            if cm > 0 or straightSpeed < backwardsMaxSpeed:
                # extra time for acceleration
                timeLeft += cm*straightsteps * \
                    (2*calcS(straightSpeed)+16.5)/1000000 + saccel_delay
            else:
                # extra time for acceleration
                timeLeft += cm*straightsteps * \
                    (2*calcS(backwardsMaxSpeed)+16.5)/1000000 + saccel_delay
        elif i == "l" or i == "L" or i == "r" or i == "R":
            timeLeft += turnTime  # constant time for turns
        elif i == "u" or i == "U":  # constant time for U turns
            timeLeft += turnTime*2*u_offset

    # This is how it stops between commands
    timeLeft += 0.15 * (len(arr) - pos)
    timeLeft = round(timeLeft, 3)
    return timeLeft


def AdjustSpeedTime(targetTimeFunc, arr, pos):
    global straightSpeed
    errorTime = 100
    countTries = 0
    while errorTime > 0.05 and countTries <= 6:
        countTries += 1
        timeLeft = calculateTimeLeft(arr, pos)
        errorTime = abs(timeLeft - targetTimeFunc)
        errorFactor = timeLeft/targetTimeFunc
        straightSpeed *= errorFactor

        if straightSpeed > maxstraightSpeed or targetTimeFunc <= 0:
            straightSpeed = maxstraightSpeed
        if straightSpeed < minstraightSpeed:
            straightSpeed = minstraightSpeed
    '''
    if countTries >= 15:
        print("WARNING: AdjustSpeedTime exceeded 15 tries, errorTime = ", str(round(errorTime,4)),"s")
    print("straightSpeed:", str(straightSpeed))
    print("timeLeft:", str(round(timeLeft,2)))
    print("targetTimeLeft:", str(round(targetTimeFunc,2)))
    '''


def AdjustSpeedTimeRealTime():
    global commands
    global command_number
    global startTime
    global targetTime
    targetTimeLeft = targetTime - ((ticks_ms() - startTime)/1000)
    AdjustSpeedTime(targetTimeLeft, commands, command_number)
    # print((ticks_ms() - startTime))


import _thread
#_thread.start_new_thread(th_func, ())
print("")
print("")
print("")


straightSpeed = (minstraightSpeed+maxstraightSpeed)/2
turnTime = 0.867
commands = commands.strip().splitlines()
led = Pin(25, Pin.OUT)
step_pin = Pin(11, Pin.OUT)
dirPin1 = Pin(14, Pin.OUT)
dirPin2 = Pin(13, Pin.OUT)
Pin(23, Pin.OUT).high()  # Switch PSU to PWM from PSM for better ADC
saccel_delay = round(0.00002909/((saccel)**3) + 0.041, 3)
if saccel_delay > 0.8:
    saccel_delay = 0.612
elif saccel_delay < 0.1:
    saccel_delay = 0.198
print(f'Saccel Delay: {saccel_delay}')
battNew = ADC(Pin(28, Pin.IN))
if silent == True:
    buzzPin = Pin(21, Pin.OUT)  # unused pin to silence buzzer
else:
    buzzPin = Pin(17, Pin.OUT)
buzzPin.low()
buzzer = PWM(buzzPin)
buzzer.freq(1000)
buzzer.duty_u16(0)

enPin1 = Pin(15, Pin.OUT)
enPin1.high()
dirfront(dirPin1)
dirfront(dirPin2)
led.low()
button = Pin(12, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2))
try:
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
except:
    print("I2C OLED NOT WORKING!")
command_number = 0
voltage = battNew.read_u16()/65536*3.29*6.1-0.05  # 3.33
if voltage <= 0:
    voltage = 0
printlcd(f'{voltage:.2f} V')




try:
    startTime = ticks_ms() - 250
    AdjustSpeedTimeRealTime()
    try:
        display.text(f'Speed: {straightSpeed:.2f}', 0, 15, 1)
        display.text("WAIT 0.5 SEC", 0, 30, 1)
        display.text(f'Target: {targetTime}s', 0, 45, 1)
        display.show()
    except:
        pass

    if voltage < 6.1:
        buzzer.duty_u16(1000)
        try:
            display.text('LOW!!!!', 70, 0, 1)
            display.show()
        except:
            pass
        print('LOW VOLTAGE!')
        for i in range(3):
            led.on()
            buzzer.freq(500)
            sleep(0.15)
            led.off()
            buzzer.freq(1000)
            sleep(0.15)
        buzzer.duty_u16(0)

    def tmcfuncs():
        if tmc_uart_en == True:
            tmc.setCurrent(currentmA, hold_current_multiplier = 1, hold_current_delay = 10, Vref = 2.05)
            tmc.setSpreadCycle(spreadCycleEn)
            #tmc.setDirection_reg(True)
            #tmc.setVSense(False)
            #tmc.setIScaleAnalog(True) #default
            #tmc.setInterpolation(True)
            #tmc.setMicrosteppingResolution(16)
            #tmc.setInternalRSense(False)
    if tmc_uart_en == True:
        from tmc.TMC_2209_StepperDriver import *
        tmc = TMC_2209(18, 19, 20, Pin(9), Pin(8),mtr_id=3) # unused pins
        tmc.setLoglevel(Loglevel.debug)
        tmcfuncs()

    try:
        display.text("#############", 0, 30, 1)
        display.show()
    except:
        pass

    while True:
        if button.value() == 0:
            sleep(0.02)
            if button.value() == 0:
                break

    led.on()
    enPin1.low()

    for i in range(1, 2000):
        step_pin.value(1)
        sleep_us(1)
        step_pin.value(0)
        sleep_us(1)
    printlcd("Motors Enabled")
    sleep(0.33)

    while True:
        if button.value() == 0:
            sleep(0.02)
            if button.value() == 0:
                break
    while button.value() == 0:
        pass
    # motor time offset, in nanoseconds
    startTime = ticks_ms() + startTimeOffset*(1000)
    printlcd("Starting Course")

    # BUZZ (for fun)
    buzzer.duty_u16(1000)
    sleep(0.21)
    buzzer.duty_u16(0)

    run_array(commands)

    print("")
    printlcd(
        f'Time: {(ticks_ms() - (startTime-startTimeOffset*1000))/1000:.2f}s')
    # BUZZ (for fun)
    buzzer.freq(750)
    buzzer.duty_u16(1000)
    led.off()
    '''
    for i in range(1,18000):
        step_pin.value(1)
        sleep_us(1)
        step_pin.value(0)
        sleep_us(1)
    '''
    enPin1.high()
    sleep(0.4)
    buzzer.duty_u16(0)
    sleep(0.2)
    if silent == False:
        import song  # sing a song cuz why not
except KeyboardInterrupt:
    led.off()
    enPin1.high()
    buzzer.duty_u16(0)
    print("Program Exited")
    display.fill(0)
    display.text("Program Exited", 0, 0, 1)
    display.text("Press RESET", 0, 15, 1)
    display.show()
# reset()
