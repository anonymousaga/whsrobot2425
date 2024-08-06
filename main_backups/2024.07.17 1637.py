### TO BE RUN ON A RASPBERRY PI PICO
## UPLOAD FILE WITH AMPY OR RSHELL
from machine import Pin, Timer, I2C ,reset, freq, PWM, ADC
freq(250000000)

#DOWEL OFFSET 7CM
# IF INTIAL SPEED IS OVER 2, TURN UP THE ACCEL TO MAX
targetTime=1

# TURN CONSTANTS
rturnsteps=16.939
lturnsteps=16.939

# ACCEL VARS
saccel=0.0396 # MAX is 0.0537
saccel_initial=0.0333 # MAX is 0.0411
taccel = 0.0321 # MAX is 0.0409

# SPEED VARS
turnSpeedDefault=0.912 # MAX is 1.289
maxstraightSpeed=3.87
minstraightSpeed=0.09
backwardsMaxSpeed=1.91


commands="""
s40
"""

commands3="""
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

commands3="""
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

commands3="""
u
u
u
u
u
u
u
u
"""



commands3="""
s150
s-150
s150
s-150
s150
s-150
"""




### DO NOT EDIT THESE DURING COMPETITION
startTimeOffset=0.205 # Negative means to decrease the amount of time taken, positive means to increase the amount of time taken
speed_steps_ratio=0.04961
straightsteps=151.129
u_offset=1.000


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
def s(cm,ending):
    global command_number
    global straightSpeed
    global speed_steps_ratio
    AdjustSpeedTimeRealTime() #timing function
    if cm < 0 and straightSpeed > backwardsMaxSpeed:
        straightSpeed=backwardsMaxSpeed
    print('STRAIGHT')
    try:
        display.fill(0)
        display.text('STRAIGHT', 0, 0, 1)
        display.text(f'Speed: {straightSpeed:.2f}', 0, 30, 1)
        display.show()
    except:
        pass
    
    if cm < 0:
        dirPin1.high() 
        dirPin2.high()
        cm *= -1
    else:
        dirPin1.low() 
        dirPin2.low()
    steps=round(cm*straightsteps)
    if command_number == 0:
        saccel_literal=saccel_initial
    else:
        saccel_literal=saccel
    delay=[]
    iAtEnd=int(steps/2)-7
    for i in range(1,round(steps/2)):
        speed=saccel_literal*(i**(1/2))
        if speed > straightSpeed:
            iAtEnd=i
            break
        else:
            delay.append(calcS(speed))
    delay2=delay[::-1]
    presetDelay=calcS(straightSpeed)
    if presetDelay < delay2[0]:
        presetDelay=delay2[0]
    #print(2+steps-iAtEnd-(iAtEnd-1))
    if ending == False:
        for i in range(1,iAtEnd-1):
            step_pin.value(1)
            time.sleep_us(delay[i])
            step_pin.value(0)
            time.sleep_us(delay[i])
        #startTimeConstant=time.ticks_ms()
        for i in range(iAtEnd-1,2+steps-iAtEnd):
            step_pin.value(1)
            time.sleep_us(presetDelay)
            step_pin.value(0)
            time.sleep_us(presetDelay)
        #endTimeConstant=time.ticks_ms()
        for i in range(1,1+steps-(2+steps-iAtEnd)):
            step_pin.value(1)
            time.sleep_us(delay2[i])
            step_pin.value(0)
            time.sleep_us(delay2[i])

    elif ending==True:
        for i in range(1,iAtEnd-1):
            step_pin.value(1)
            time.sleep_us(delay[i])
            step_pin.value(0)
            time.sleep_us(delay[i])
        #startTimeConstant=time.ticks_ms()
        for i in range(iAtEnd-1,(2+steps-iAtEnd)-3600):
            step_pin.value(1)
            time.sleep_us(presetDelay)
            step_pin.value(0)
            time.sleep_us(presetDelay)
        #endTimeConstant=time.ticks_ms()
        led.off()
        for i in range(1,3600):
            step_pin.value(1)
            time.sleep_us(presetDelay)
            step_pin.value(0)
            time.sleep_us(presetDelay)
        #endTimeConstant=time.ticks_ms()
        for i in range(1,1+steps-(2+steps-iAtEnd)):
            step_pin.value(1)
            time.sleep_us(delay2[i])
            step_pin.value(0)
            time.sleep_us(delay2[i])
        
    #speed_steps_ratio=abs((endTimeConstant-startTimeConstant)/((2+steps-iAtEnd)-(iAtEnd-1)+1)-0.0165)/straightSpeed
    #print("ratio: " ,speed_steps_ratio)
    #print("microsec per step: ",((endTimeConstant-startTimeConstant)/((2+steps-iAtEnd)-(iAtEnd-1)+1))-0.0165)
    del delay
    del delay2
    gc.collect()
    command_number +=1 #Shift position to next command

def run_array(arr):
    commandsLength=len(arr)
    for index,command in enumerate(arr):
        command_number=index
        i=command.strip()
        if i.startswith("s"):
            if command_number == commandsLength-1:
                runTheLight=True
            else:
                runTheLight=False
            s(float(i.strip("s")),ending=runTheLight)
            
        elif i == "l" or i == "L":
            t(-90)
        elif i == "r" or i == "R":
            t(90)
        elif i == "u" or i == "U":
            t(180*u_offset)

def turn(degrees,speedLimit):
    global command_number
    global turnTime
    startTurnTime=time.ticks_ms()
    printlcd("TURN")

    if degrees < 0:
        dirPin1.low() 
        dirPin2.high()
        turn_steps=lturnsteps
        degrees *= -1
    else:
        dirPin1.high() 
        dirPin2.low()
        turn_steps=rturnsteps

    steps=round(degrees*turn_steps)
    delay=[]
    iAtEnd=int(steps/2)-7
    for i in range(1,round(steps/2)):
        speed=taccel*(i**(1/2))
        if speed > speedLimit:
            iAtEnd=i
            break
        else:
            delay.append(calcS(speed))
    delay2=delay[::-1]
    presetDelay=calcS(speedLimit)
    if presetDelay < delay2[0]:
        presetDelay=delay2[0]
    for i in range(1,iAtEnd-1):
        step_pin.value(1)
        time.sleep_us(delay[i])
        step_pin.value(0)
        time.sleep_us(delay[i])
    for i in range(iAtEnd-1,2+steps-iAtEnd):
        step_pin.value(1)
        time.sleep_us(presetDelay)
        step_pin.value(0)
        time.sleep_us(presetDelay)
    for i in range(1,1+steps-(2+steps-iAtEnd)):
        step_pin.value(1)
        time.sleep_us(delay2[i])
        step_pin.value(0)
        time.sleep_us(delay2[i])
    del delay
    del delay2
    command_number +=1 #Shift position to next command
    if degrees == 90 or degrees == -90:
        turnTime= (time.ticks_ms()-startTurnTime)/1000
    del startTurnTime
    gc.collect()
    #print("turnTime: ",turnTime)

def t(degrees):
    turn(degrees, turnSpeedDefault)

def calculateTimeLeft(arr,pos):
    global straightSpeed
    global turnTime
    timeLeft = 0
    for index in range (pos,len(arr)):
        i=arr[index].strip()
        if i.startswith("s"):
            cm=abs(float(i.lstrip("s")))
            if cm > 0 or straightSpeed<backwardsMaxSpeed:
                timeLeft += cm*straightsteps*(2*calcS(straightSpeed)+16.5)/1000000  + saccel_delay# extra time for acceleration
            else:
                timeLeft += cm*straightsteps*(2*calcS(backwardsMaxSpeed)+16.5)/1000000  + saccel_delay# extra time for acceleration
        elif i == "l" or i == "L" or i == "r" or i == "R":
            timeLeft += turnTime  # constant time for turns
        elif i == "u" or i == "U": # constant time for U turns
            timeLeft += turnTime*2*u_offset
    
    # This is how it stops between commands
    timeLeft += 0.15 * (len(arr) - pos)
    timeLeft = round(timeLeft,3)
    return timeLeft

def AdjustSpeedTime(targetTimeFunc,arr,pos):
    global straightSpeed
    errorTime=100
    countTries = 0
    while errorTime > 0.05 and countTries <= 6:
        countTries += 1
        timeLeft = calculateTimeLeft(arr,pos)
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
    targetTimeLeft = targetTime - ((time.ticks_ms() - startTime)/1000)
    AdjustSpeedTime(targetTimeLeft,commands,command_number)
    #print((time.ticks_ms() - startTime))




import time
import ssd1306
import gc


print("")
print("")
print("")
straightSpeed=(minstraightSpeed+maxstraightSpeed)/2
turnTime=0.867
commands  = commands.strip().splitlines()
led = Pin(25, Pin.OUT)
step_pin = Pin(11, Pin.OUT)
dirPin1 = Pin(14, Pin.OUT)
dirPin2 = Pin(13, Pin.OUT)
Pin(23,Pin.OUT).high() # Switch PSU to PWM from PSM for better ADC
saccel_delay=round(0.00002909/((saccel)**3) + 0.041,3)
if saccel_delay > 0.8:
    saccel_delay = 0.612
elif saccel_delay < 0.1:
    saccel_delay=0.198
print(f'Saccel Delay: {saccel_delay}')
battNew=ADC(Pin(28, Pin.OUT))
buzzPin=Pin(17,Pin.OUT)
buzzPin.low()
buzzer = PWM(buzzPin)
buzzer.freq(1000)
buzzer.duty_u16(0)

enPin1=Pin(15, Pin.OUT)
enPin1.high()
dirPin1.high()
dirPin2.low()
led.low()
button = Pin(12, Pin.IN, Pin.PULL_UP)
i2c = I2C(1,freq=400000, scl=Pin(3), sda=Pin(2))
try:
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
except:
    print("I2C OLED NOT WORKING!")
command_number=0
voltage=battNew.read_u16()/65536*3.29*6.1-0.05 #3.33
if voltage <= 0:
    voltage = 0
printlcd(f'{voltage:.2f} V')
time.sleep(0.01)

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
            time.sleep(0.15)
            led.off()
            buzzer.freq(1000)
            time.sleep(0.15)
        buzzer.duty_u16(0)
    startTime = time.ticks_ms() - 250
    AdjustSpeedTimeRealTime()

    try:
        display.text(f'Speed: {straightSpeed:.2f}', 0, 15, 1)
        display.text(f'Target: {targetTime}s', 0, 45, 1)
        display.show()
    except:
        pass
    print("Ready to Run")
    while True:
        if button.value() == 0:
            time.sleep(0.02) 
            if button.value() == 0:
                break

    led.on()
    enPin1.low()

    for i in range(1,2000):
        step_pin.value(1)
        time.sleep_us(1)
        step_pin.value(0)
        time.sleep_us(1)
    printlcd("Motors Enabled")
    time.sleep(0.33)


    while True:
        if button.value() == 0:
            time.sleep(0.02)
            if button.value() == 0:
                break
    while button.value() == 0:
        pass
    startTime = time.ticks_ms() + startTimeOffset*(1000) # motor time offset, in nanoseconds
    printlcd("Starting Course")
    # BUZZ (for fun)
    buzzer.duty_u16(1000)
    time.sleep(0.21)
    buzzer.duty_u16(0)


    run_array(commands)

    print("")
    printlcd(f'Time: {(time.ticks_ms() - (startTime-startTimeOffset*1000))/1000:.2f}s')
    # BUZZ (for fun)
    buzzer.freq(750)
    buzzer.duty_u16(1000)
    led.off()
    '''
    for i in range(1,18000):
        step_pin.value(1)
        time.sleep_us(1)
        step_pin.value(0)
        time.sleep_us(1)
    '''
    enPin1.high()
    time.sleep(0.4)
    buzzer.duty_u16(0)
    time.sleep(0.2)
    import song # sing a song cuz why not
except KeyboardInterrupt:
    led.off()
    enPin1.high()
    buzzer.duty_u16(0)
    print("Program Exited")
    display.fill(0)
    display.text("Program Exited", 0, 0, 1)
    display.text("Press RESET", 0, 15, 1)
    display.show()
#reset()

