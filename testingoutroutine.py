# TO BE RUN ON A RASPBERRY PI PICO
# UPLOAD FILE WITH AMPY OR RSHELL
from machine import freq
freq(300000000)
from machine import Pin, Timer, I2C, reset, freq, PWM, ADC
import gc
import os
import ssd1306
from time import sleep, ticks_ms, sleep_us, time
from math import sqrt
from sys import exit
import _thread
from rv import * #robot vars


# DO NOT EDIT THESE DURING COMPETITION
# Negative means to decrease the amount of time taken, positive means to increase the amount of time taken
startTimeOffset = 0 # in seconds
speed_steps_ratio = 0.04961
straightsteps = 127.088
saccel_initial = saccel - 0.3
taccel = saccel - 0.3
# TURN CONSTANTS
backwardsMaxSpeed = maxstraightSpeed*0.6
rturnsteps = 17.221
lturnsteps = rturnsteps
currentmA = 1250
tmc_uart_en = False
spreadCycleEn = True
ending_led_period = .5 # how long before finish to turn off led at end


if True: # define all functions
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

    def ending_led(delaylength_s):
        if delaylength_s > 0:
            sleep(delaylength_s)
        else:
            print("ending led delay is negative!")
            sleep(0.02)
        led.off()

    def calcS(speedy):
        return round((7756.33/speedy) - 10.157)

    def s(cm, ending=False):
        global command_number
        global straightSpeed
        global runCurrent
        global speed_steps_ratio
        try:
            display.fill(0)
            display.text('STRAIGHT', 0, 0, 1)
            display.text(f'Speed: {straightSpeed:.2f}', 0, 30, 1)
            display.show()
        except:
            pass

        if cm < 0:
            dirfront(dirPin1)
            dirback(dirPin2)
            cm *= -1
        else:
            dirback(dirPin1)
            dirfront(dirPin2)
        steps = round(cm*straightsteps)
        saccel_literal = saccel
        saccel_literal = 25000/saccel_literal
        delay = []
        iAtEnd = int(steps*.496)
        iAtEndinitial = iAtEnd
        presetDelay = calcS(straightSpeed)
        print(presetDelay)
        gc.collect()
        for i in range(1, iAtEndinitial):
            delayi = round(saccel_literal/sqrt(i+2))-2
            if delayi < presetDelay:
                iAtEnd = i
                break
            delay.append(delayi)
        
        try:
            presetDelay = delay[iAtEnd-2]
        except IndexError:
            print("IndexError At presetdelay calc for straight")
            print("iAtEnd ",iAtEnd)
            print("len(delay) ",len(delay))

        #print('AccelSteps: ' + str(int((100*iAtEnd)/(steps/2))), 0, 45, 1)
        #display.show()


           
        range2=range(iAtEnd-1, 2+steps-iAtEnd)
        range3=range((-1*iAtEnd)+2, 0)
        starttime2=ticks_ms()
        for i in range(1, iAtEnd-1):
            step_pin.value(1)
            step_pin.value(0)
            sleep_us(delay[i])
        for i in range2:
            step_pin.value(1)
            step_pin.value(0)
            sleep_us(presetDelay)
        for i in range3:
            step_pin.value(1)
            step_pin.value(0)
            sleep_us(delay[i*-1])
        endtime2=ticks_ms()
        print(str(cm) + f",{ (endtime2 - starttime2) / 1000 },"+ str(saccel) + ',' + str(straightSpeed)+','+str(int((100*iAtEnd)/(steps/2))))


    def run_array(arr):
        commandsLength = len(arr)
        for index, i in enumerate(arr):
            command_number = index
            if i[0]==0:
                if command_number == commandsLength-1:
                    runTheLight = True
                else:
                    runTheLight = False
                s(i[1], ending=runTheLight)
            elif i[0]==1:
                t(i[1])


    def turn(degreeval, speedLimit):
        global command_number
        global turnTime
        startTurnTime = ticks_ms()
        printlcd("TURN")

        if degreeval < 0:
            dirfront(dirPin1)
            dirfront(dirPin2)
            turn_steps = lturnsteps
            degreeval *= -1
        else:
            dirback(dirPin1)
            dirback(dirPin2)
            turn_steps = rturnsteps
        steps = round(degreeval*turn_steps)

        taccel_literal = 25000/taccel
        delay = []
        iAtEnd = int(steps*.411)
        iAtEndinitial = iAtEnd
        presetDelay = calcS(speedLimit)
        gc.collect()
        for i in range(1, iAtEndinitial):
            delayi = round(taccel_literal/sqrt(i+2))-2
            if delayi < presetDelay:
                iAtEnd = i
                break
            delay.append(delayi)
        print(str(steps)+" steps")
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
        command_number += 1  # Shift position to next command
        turnTime = (((ticks_ms()-startTurnTime)/1000)-taccel_delay)/degreeval
        #print("turnTime: ",turnTime)


    def t(degreeval2):
        turn(degreeval2, turnSpeedDefault)

    def straightETA(cm_dist,speed,accel): # accel is unused for now
        return cm_dist/speed + saccel_delay

    def compileCommands(commandvar):
        commandvar = commandvar.strip().splitlines()
        command2 = []
        try:
            for x in commandvar:
                if x=="u":
                    command2.append((1,180))
                elif x=="-u":
                    command2.append((1,-180))
                elif x=="l":
                    command2.append((1,-90))
                elif x=="r":
                    command2.append((1,90))
                elif x=="rd":
                    command2.append((1,45))
                elif x=="ld":
                    command2.append((1,-45))
                elif x.startswith("sd"):
                    command2.append((0,float(x.strip("sd"))*1.414))
                elif x.startswith("s"):
                    command2.append((0,float(x.strip("s"))))
                elif x.startswith("t"):
                    command2.append((1,float(x.strip("t"))))
                elif x.strip()=="":
                    pass # skip blank lines
                else:
                    raise ValueError('command is incorrect')
            return command2, False
        except ValueError as e:
            return [], e


    def calculateTimeLeft(arr, pos):
        global straightSpeed
        global turnTime
        timeLeft = 0
        for index in range(pos, len(arr)):
            i = arr[index]
            if i[0]==0:
                cm = abs(i[1])
                if cm > 0 or straightSpeed < backwardsMaxSpeed:
                    # extra time for acceleration
                    timeLeft += straightETA(cm, straightSpeed, saccel)
                else:
                    # extra time for acceleration
                    timeLeft += straightETA(cm, backwardsMaxSpeed, saccel)
            elif i[0]==1:
                timeLeft +=  (i[1])*turnTime + taccel_delay

        # This is how it stops between commands
        timeLeft += 0.15 * (len(arr) - pos)
        timeLeft = round(timeLeft, 3)
        return timeLeft


    def AdjustSpeedTime(targetTimeFunc, arr, pos):
        global straightSpeed
        errorTime = 100
        countTries = 0
        while errorTime > 0.05 and countTries <= 5:
            countTries += 1

            timeLeft = calculateTimeLeft(arr, pos)
            errorTime = abs(timeLeft - targetTimeFunc)
            errorFactor = timeLeft/targetTimeFunc
            straightSpeed *= errorFactor
            if straightSpeed > maxstraightSpeed or targetTimeFunc <= 0:
                straightSpeed = maxstraightSpeed
            if straightSpeed < minstraightSpeed:
                straightSpeed = minstraightSpeed


    def AdjustSpeedTimeRealTime():
        global commands
        global command_number
        global startTime
        global targetTime
        targetTimeLeft = targetTime - ((ticks_ms() - startTime)/1000)
        AdjustSpeedTime(targetTimeLeft, commands, command_number)
        # print((ticks_ms() - startTime))

    def tmcfuncs():
        if tmc_uart_en == True:
            tmc.setCurrent(currentmA, hold_current_multiplier = 1, hold_current_delay = 10, Vref = 1.325)
            tmc.setSpreadCycle(spreadCycleEn)
            #tmc.setDirection_reg(True)
            #tmc.setVSense(False)
            #tmc.setIScaleAnalog(True) #default
            #tmc.setInterpolation(True)
            #tmc.setMicrosteppingResolution(16)
            #tmc.setInternalRSense(False)

    def lcd_voltage():
        voltage = battNew.read_u16()/65536*3.29*6.1-0.05
        if voltage <= 0:
            voltage = 0
        voltagestr = f'{voltage:.2f} V' 
        if voltage < 6.1:
            undervolt=True
        else:
            undervolt=False
        try:
            display.fill_rect(0, 0,130, 15, 0) # black out wait message
            display.text(voltagestr, 0, 0, 1)
            if undervolt == True:
                display.text('LOW!!!!', 70, 0, 1)
            display.show()
        except:
            pass
        return voltage, undervolt




#_thread.start_new_thread(th_func, ())



saccel_delay = round(0.00002909/((saccel)**3) + 0.041, 3)
if saccel_delay > 0.8:
    saccel_delay = 0.612
elif saccel_delay < 0.1:
    saccel_delay = 0.198

command0,command1, command2, command3, command4, command5, command6, command7, command8, command9 = [0,1,2,3,4,5,6,7,8,9]
del command0,command1, command2, command3, command4, command5, command6, command7, command8, command9
straightSpeed = (minstraightSpeed+maxstraightSpeed)/2
turnTime = 0.0035
taccel_delay = 0.25

led = Pin(25, Pin.OUT)
step_pin = Pin(14, Pin.OUT)
dirPin1 = Pin(11, Pin.OUT)
dirPin2 = Pin(12, Pin.OUT)
Pin(23, Pin.OUT).high()  # Switch PSU to PWM from PSM for better ADC
#saccel_delay = round(0.00002909/((saccel)**3) + 0.041, 3)
#if saccel_delay > 0.8:
#    saccel_delay = 0.612
#elif saccel_delay < 0.1:
#    saccel_delay = 0.198
#print(f'Saccel Delay: {saccel_delay}')
battNew = ADC(Pin(28, Pin.IN))
if silent == True:
    buzzPin = Pin(21, Pin.OUT)  # unused pin to silence buzzer
else:
    buzzPin = Pin(17, Pin.OUT)
buzzPin.low()
buzzer = PWM(buzzPin)
buzzer.freq(1000)
buzzer.duty_u16(0)

enPin1 = Pin(10, Pin.OUT)
enPin1.high()
dirfront(dirPin1)
dirfront(dirPin2)
led.low()
button = Pin(5, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2))
try:
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
except:
    print("I2C OLED NOT WORKING!")

command_number = 0





commands, errorcommands = compileCommands(commands)
if errorcommands != False:
    print("Error: ", errorcommands)
    try:
        display.text('COMMANDS ERROR', 0, 15, 1)
        display.text('PROGRAM EXITED', 0, 30, 1)
        display.show()
    except:
        pass
    exit()
del errorcommands

      




try:
    startTime = ticks_ms() - 250
    AdjustSpeedTimeRealTime()
    voltage, undervoltage = lcd_voltage()
    try:
        display.text(f'Speed: {straightSpeed:.2f}', 0, 15, 1)
        display.text("WAIT 0.5 SEC", 0, 30, 1)
        display.text(f'Target: {targetTime}s', 0, 45, 1)
        display.show()
    except:
        pass


    if tmc_uart_en == True:
        from TMC_2209_StepperDriver import *
        tmc = TMC_2209(18, 19, 20, Pin(9), Pin(8),mtr_id=3) # unused pins
        tmc.setLoglevel(Loglevel.debug)
        tmcfuncs()
    
    gc.collect()

    try:
        display.fill_rect(0, 30,130, 15, 0) # black out wait message
        display.show()
    except:
        pass

    led.on()
    enPin1.low()

    # motor time offset, in nanoseconds
    startTime = ticks_ms() + startTimeOffset*(1000)

    # BUZZ (for fun)
    buzzer.duty_u16(1000)
    sleep(0.21)
    buzzer.duty_u16(0)
    

 # PUT STUFF HERE ################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #cmlist=[1,2,3,4,5,7,9,11,15,20,35.4,40,50]#,140]
    cmlist=[5,25,50,100]
    speedlistfast=[10,20,35,50,75,100,140] #1,2,3,5,7, REDO 11
    cm,saccel,straightSpeed=50,3.8,68
    s(cm)
    #for k in speedlistfast:
    #    straightSpeed = k
    #    for i in [3.9,4.6, 5.35]:
    #        saccel = i
    #        for j in cmlist:
    #            s(j)

    
 
    
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

except KeyboardInterrupt:
    led.off()
    enPin1.high()
    buzzer.duty_u16(0)
    display.fill(0)
    display.text("Program Exited", 0, 0, 1)
    display.text("Press RESET", 0, 15, 1)
    display.show()
# reset()
