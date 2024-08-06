# TO BE RUN ON A RASPBERRY PI PICO
# UPLOAD FILE WITH AMPY OR RSHELL
import gc
import ssd1306
from time import sleep, ticks_ms, sleep_us
from machine import Pin, Timer, I2C, reset, freq, PWM, ADC, UART
from math import sqrt
freq(250000000)

# DOWEL OFFSET 7CM
# IF INTIAL SPEED IS OVER 2, TURN UP THE ACCEL TO MAX
targetTime = 1
silent = True

# TURN CONSTANTS
rturnsteps = 17.18
lturnsteps = rturnsteps

# ACCEL VARS
saccel = 5.423
saccel_initial = 4.81
taccel = 4.86

# SPEED VARS
turnSpeedDefault = 1.62
maxstraightSpeed = 2.45
minstraightSpeed = 0.04
backwardsMaxSpeed = 1
runCurrent = 32  # between 1 and 32
holdCurrent = runCurrent  # between 1 and 32


I_scale_analog = 1
internal_Rsense = 0  # default 0
en_spreadcycle = 0
shaft = 1
index_otpw = 1  # default 0
index_step = 0
pdn_disable = 1
mstep_reg_select = 0
multistep_filt = 0  # default 1
test_mode = 0

tmc_id=3

commands = """
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
s100
l
s7.5
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

commands3 = """
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
currentmA = 800


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
    iAtEnd = int(steps*.45)
    iAtEndinitial = iAtEnd
    presetDelay = calcS(straightSpeed)
    gc.collect()
    for i in range(1, iAtEndinitial):
        delayi = round(saccel_literal/sqrt(i+4))-10
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
    iAtEnd = int(steps*.45)
    iAtEndinitial = iAtEnd
    presetDelay = calcS(straightSpeed)
    for i in range(1, iAtEndinitial):
        delayi = round(taccel_literal/sqrt(i+30))-10
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

###############################


def compute_crc8_atm(datagram, initial_value=0):
    crc = initial_value
    # Iterate bytes in data
    for byte in datagram:
        # Iterate bits in byte
        for _ in range(0, 8):
            if (crc >> 7) ^ (byte & 0x01):
                crc = ((crc << 1) ^ 0x07) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
            # Shift to next bit
            byte = byte >> 1
    return crc


def read_reg(mtr_id, reg):
    global uart2
    x = [0x55, 0, 0, 0]
    x[1] = mtr_id
    x[2] = reg
    x[3] = compute_crc8_atm(x[:-1])
    y = uart2.write(bytes(x))
    if y != len(x):
        print("Err in read")
        return False
        sleep(.01)
    if uart2.any():
        # read what it self send and trash it (RX and TX one line)
        y = uart2.read(4)
        y = uart2.read()
    else:
        y = 0
        sleep(.000005)
    return (y)


def write_reg(mtr_id, reg, val):
    global uart2
    x = [0x55, 0, 0, 0, 0, 0, 0, 0]
    x[1] = mtr_id
    x[2] = reg | 0x80
    x[3] = 0xFF & (val >> 24)
    x[4] = 0xFF & (val >> 16)
    x[5] = 0xFF & (val >> 8)
    x[6] = 0xFF & val
    x[7] = compute_crc8_atm(x[:-1])
    y = uart2.write(bytes(x))
    if y != len(x):
        print("Err in write")
        return False
        sleep(.01)
    if uart2.any():
        y = uart2.read()  # read what it self send and trash it (RX and TX one line)
        sleep(.000002)


def write_gconf():
    write_reg(tmc_id, GCONF, ((multistep_filt*256 + 512*test_mode)+(I_scale_analog + 2*internal_Rsense + 4 * en_spreadcycle + 8*shaft + 16*index_otpw + 32*index_step + 64*pdn_disable + 128*mstep_reg_select)))
    #pass

def write_current():
    write_reg(tmc_id, IHOLD_IRUN, (65536+(holdCurrent-1)+(runCurrent-1)*256))
    #pass

# TMC2209 registermap
GCONF = 0x00
GSTAT = 0x01
IFCNT = 0x02
SLAVECONF = 0x03
OTP_PROG = 0x04
OTP_READ = 0x05
IOIN = 0x06
FACTORY_CONF = 0x07
IHOLD_IRUN = 0x10
TPOWER_DOWN = 0x11
TSTEP = 0x12
TPWMTHRS = 0x13
TCOOLTHRS = 0x14
VACTUAL = 0x22
SGTHRS = 0x40
SG_RESULT = 0x41
COOLCONF = 0x42
MSCNT = 0x6A
MSCURACT = 0x6B
CHOPCONF = 0x6C
DRV_STATUS = 0x6F
PWMCONF = 0x70
PWM_SCALE = 0x71
PWM_AUTO = 0x72


# import _thread


print("")
print("")
print("")


uart2 = UART(1, baudrate=115200,  bits=8, parity=None,
             stop=1, tx=Pin(8), rx=Pin(9))

write_gconf()
sleep(0.05)
write_gconf()
a=read_reg(tmc_id,GCONF)
print(a)
sleep(0.05)
write_current()
sleep(0.05)


# uart = UART(1, 9600)                         # init with given baudrate
# uart.init(9600, bits=8, parity=None, stop=1,rx=21, tx=20) # init with given parameters
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
battNew = ADC(Pin(28, Pin.OUT))
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
sleep(0.01)

try:
    if voltage < 6.3:
        buzzer.duty_u16(1000)
        try:
            display.text(' LOW VOLTAGE!', 0, 30, 1)
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
    startTime = ticks_ms() - 250
    AdjustSpeedTimeRealTime()

    try:
        display.text(f'Speed: {straightSpeed:.2f}', 0, 15, 1)
        display.text("WAIT 0.5 SEC", 0, 30, 1)
        display.text(f'Target: {targetTime}s', 0, 45, 1)
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
    en_spreadcycle = 1
    write_gconf()
    write_current()
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
