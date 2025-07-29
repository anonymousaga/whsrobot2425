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
import tcs34725

# initialize variables to defaults if they dont exist
silent = False
targetTime = 60
saccel = 4.2
turnSpeedDefault=95
maxstraightSpeed=145
lturnsteps = 15.5
rturnsteps = lturnsteps


# DO NOT EDIT THESE DURING COMPETITION
startTimeOffset = 0 # in seconds;  Negative means to decrease the amount of time taken, positive means to increase the amount of time taken
speed_steps_ratio = 0.04961
straightsteps = 127.088
saccel_initial = saccel
taccel = saccel - 0.3
if taccel < 3.8:
    taccel = 3.8
minstraightSpeed = 3
slowSpeed = 50
backwardsMaxSpeed = maxstraightSpeed*0.6
tmc_uart_en = True
spreadCycleEn = False
currentmA = 925 # combined current for both motors
ending_led_period = 0.75 # how long before finish to turn off led at end

from rv import * #robot vars

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

    def printlcd2(text):
        try:
            display2.fill(0)
            display2.text(text, 0, 0, 1)
            display2.show()
        except:
            pass
        print(text)

    def ending_led(timer=None):
        led.off()

    def calcS(speedy):
        return round((7756.33/speedy) - 10.157)

    def s(cm, ending=False, s_correction=True,t_correction=True, slow=False):
        global command_number
        global straightSpeed
        global slowSpeed
        global last_val_middle
        global last_tiltangle
        global last_val_middle2
        global run_tcs
        global stepcount
        global speed_steps_ratio
        AdjustSpeedTimeRealTime()  # timing function
        if cm < 0 and straightSpeed > backwardsMaxSpeed:
            straightSpeed = backwardsMaxSpeed
        if slow == True and straightSpeed > slowSpeed:
            straightSpeed = slowSpeed
        print("STRAIGHT")
        try:
            display.fill(0)
            display.text('STRAIGHT', 0, 0, 1)
            display.text(f'CM: {cm:.0f}', 0, 15, 1)
            display.text(f'SPEED: {straightSpeed:.0f}', 0, 30, 1)
            display.show()
        except:
            pass

        if cm < 0:
            dirfront(dirPin1)
            dirback(dirPin2)
            cm = -cm
        else:
            dirback(dirPin1)
            dirfront(dirPin2)
        steps = round(cm*straightsteps)
        if command_number == 0:
            saccel_literal = saccel_initial
        else:
            saccel_literal = saccel
        saccel_literal = 25000/saccel_literal
        delay = []
        stepcount = 0
        last_val_middle = 0
        last_val_middle2 = 0
        last_tiltangle = 0
        iAtEnd = int(steps*.496)
        iAtEndinitial = iAtEnd
        presetDelay = calcS(straightSpeed)
        gc.collect()
        if saccel > 4.8:
            offsetval = 3
        else:
            offsetval = 0
        for i in range(1, iAtEndinitial):
            delayi = int(saccel_literal/sqrt(i+offsetval))-2
            if delayi < presetDelay:
                iAtEnd = i
                break
            delay.append(delayi)
        print(str(steps)+" steps")
        try:
            presetDelay = delay[iAtEnd-2]
        except IndexError:
            print("IndexError At presetdelay calc for straight")
            print("iAtEnd ",iAtEnd)
            print("len(delay) ",len(delay))
        try:
            display.text('ACCEL%: ' + str(round((100*iAtEnd)/(steps/2))), 0, 45, 1)
            display.show()
        except:
            pass
        if ending==True:
            Timer(-1).init(mode=Timer.ONE_SHOT, period=int((straightETA(cm, straightSpeed, saccel)-ending_led_period)*1000), callback=ending_led)
        range2=range(iAtEnd-1, 2+steps-iAtEnd)
        range3=range((-iAtEnd)+2, 0)
        if s_correction == True or t_correction == True:
            _thread.start_new_thread(tcs_scan, (None,))
        starttime2=ticks_ms()
        for i in range(1, iAtEnd-1):
            step_pin.value(1)
            step_pin.value(0)
            stepcount += 1
            sleep_us(delay[i])
        for i in range2:
            step_pin.value(1)
            step_pin.value(0)
            stepcount += 1
            sleep_us(presetDelay)
        for i in range3:
            step_pin.value(1)
            step_pin.value(0)
            stepcount += 1
            sleep_us(delay[-i])
        endtime2=ticks_ms()
        print(f"Elapsed Time: { (endtime2 - starttime2) / 1000 } seconds")
        run_tcs = False  # stop the tcs34725 sensor
        if True:  # all the tcs34725 sensors code
            try:
                middle_edge = []
                middle_edge2 = []
                diffvals = 0
                last_val_middle = 0
                last_val_middle2 = 0
                for index,i in enumerate(rising_edge):
                    x=(rising_edge[index]+falling_edge[index])/(2*straightsteps)
                    middle_edge.append(x)
                    last_val_middle = round(x-cm+25+1.5,2) #sensors are 1.5cm in front of wheels
                    print("Distance at step, sensor 1: ", last_val_middle, "cm")
                for index,i in enumerate(rising_edge2):
                    x=(rising_edge2[index]+falling_edge2[index])/(2*straightsteps)
                    middle_edge2.append(x)
                    last_val_middle2 = round(x-cm+25+1.5,2) # sensors are 1.5cm in front of wheels
                    print("Distance at step, sensor 2: ", last_val_middle2, "cm")
                last_val_middle_avg = round((last_val_middle + last_val_middle2) / 2,2)
                if last_val_middle_avg != 0 and last_val_middle2 != 0:
                    diffvals = last_val_middle - last_val_middle2
                else:
                    diffvals = 0
                last_tiltangle=-1*round((360/(2*3.14159))*math.atan(diffvals/9.2),1) # 9.2cm is the horizontal distance between the two sensors
                last_tiltangle += 3 # add 3 degrees right offset, sensors arent perfectly aligned
                if t_correction == True and abs(last_tiltangle) >= 1:
                    print(f'Tilt adjust: {last_tiltangle:.0f}deg')
                    t(last_tiltangle)
                if s_correction == True:
                    if abs(last_val_middle_avg) > .1:
                        print(f'Straight adjust: {last_val_middle_avg:.1f}cm')
                        if ending==True:
                            s(last_val_middle_avg-8,s_correction=False,t_correction=False)
                        else:
                            s(last_val_middle_avg,s_correction=False,t_correction=False)
                #print("diffvals ",diffvals)

            
            except Exception as e:
                print("Error parsing TCS34725 data: ", e)
        command_number += 1


    def run_array(arr):
        commandsLength = len(arr)
        for index, i in enumerate(arr):
            command_number = index
            if i[0]==0:
                if command_number == commandsLength-1:
                    runTheLight = True
                else:
                    runTheLight = False
                
                slowvar = False
                t_correctionvar = True
                s_correctionvar = True
                for modifier in i[2]:
                    if modifier == 1:
                        slowvar = True
                    elif modifier == 2:
                        t_correctionvar = False
                        s_correctionvar = False
                s(i[1], ending=runTheLight, slow=slowvar, s_correction=s_correctionvar, t_correction=t_correctionvar)
            elif i[0]==1:
                slowvar = False
                for modifier in i[2]:
                    if modifier == 1:
                        slowvar = True
                t(i[1], slow=slowvar)

    def tcs_scan(randomarg=None):
        global stepcount
        global rising_edge
        global rising_edge2
        global tcsensor
        global tcsensor2
        global falling_edge
        global falling_edge2
        global run_tcs
        run_tcs = True
        rising_edge = []
        falling_edge = []
        rising_edge2 = []
        falling_edge2 = []
        consecutive_high = 0
        consecutive_low = 0
        consecutive_high2 = 0
        consecutive_low2 = 0
        is_high = False
        is_high2 = False
        while run_tcs:
            try:
                # Read both sensors independently
                reading1 = tcsensor.read()
                reading2 = tcsensor2.read()

                # Process sensor 1
                if reading1[0] > 3500:
                    if not is_high:
                        consecutive_high += 1
                    if consecutive_high >= 1:
                        rising_edge.append(stepcount)
                        is_high = True
                        consecutive_high = 0
                    consecutive_low = 0
                else:
                    if is_high:
                        consecutive_low += 1
                    if consecutive_low >= 1:
                        falling_edge.append(stepcount)
                        is_high = False
                        consecutive_low = 0
                    consecutive_high = 0

                # Process sensor 2 independently 
                if reading2[0] > 3500:
                    if not is_high2:
                        consecutive_high2 += 1
                    if consecutive_high2 >= 1:
                        rising_edge2.append(stepcount)
                        is_high2 = True
                        consecutive_high2 = 0
                    consecutive_low2 = 0
                else:
                    if is_high2:
                        consecutive_low2 += 1
                    if consecutive_low2 >= 1:
                        falling_edge2.append(stepcount)
                        is_high2 = False
                        consecutive_low2 = 0
                    consecutive_high2 = 0
            except Exception as e:
                print("TCS Read Error: ", e)
                break

    def clear(): # clear main.py file to allow re-uploading in emergency
        os.remove('main.py')

    def t(degreeval, slow=False):
        global command_number
        global turnTime
        startTurnTime = ticks_ms()
        if slow == True:
            turnSpeed = slowSpeed
        else:
            turnSpeed=turnSpeedDefault
        print("TURN")
        try:
            display.fill(0)
            display.text('TURN', 0, 0, 1)
            display.text(f'DEGREES: {degreeval:.0f}', 0, 15, 1)
            display.text(f'SPEED: {turnSpeed:.0f}', 0, 30, 1)
            display.show()
        except:
            pass

        if degreeval < 0:
            dirfront(dirPin1)
            dirfront(dirPin2)
            turn_steps = lturnsteps
            degreeval = -degreeval
        else:
            dirback(dirPin1)
            dirback(dirPin2)
            turn_steps = rturnsteps
        steps = round(degreeval*turn_steps)

        taccel_literal = 25000/taccel
        delay = []
        iAtEnd = int(steps*.496)
        iAtEndinitial = iAtEnd
        presetDelay = calcS(turnSpeed)
        gc.collect()
        if taccel > 4.5:
            offsetval = 1
        else:
            offsetval = 0
        for i in range(1, iAtEndinitial):
            delayi = int(taccel_literal/sqrt(i+offsetval))-2
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


    def straightETA(cm_dist,speed,accel): # accel is unused for now
        return cm_dist/speed + 0.43 + 0.00483546*(speed+30)

    def compileCommands(commandvar):
        commandvar = commandvar.strip().splitlines()
        command2 = []
        modifier_lookup = {
            "slow": 1,
            "no-correction": 2,
        }
        try:
            for xfull in commandvar:
                xarr = xfull.split(" ")
                x = xarr[0].strip()

                # Process additional modifiers after the command
                modifiers = [modif.strip() for modif in xarr[1:]]
                modifiers_numeric = []
                for modi in modifiers:
                    try:
                        modifiers_numeric.append(modifier_lookup[modi])
                    except KeyError:
                        print(f"Unknown modifier: '{modi}', skipping.")
                
                if x=="u":
                    command2.append((1,180,modifiers_numeric))
                elif x=="-u":
                    command2.append((1,-180,modifiers_numeric))
                elif x=="l":
                    command2.append((1,-90,modifiers_numeric))
                elif x=="r":
                    command2.append((1,90,modifiers_numeric))
                elif x=="rd":
                    command2.append((1,45,modifiers_numeric))
                elif x=="ld":
                    command2.append((1,-45,modifiers_numeric))
                elif x.startswith("sd"):
                    command2.append((0,float(x.strip("sd"))*1.4142,modifiers_numeric)) # square root of 2
                elif x.startswith("s"):
                    command2.append((0,float(x.strip("s")),modifiers_numeric))
                elif x.startswith("t"):
                    command2.append((1,float(x.strip("t")),modifiers_numeric))
                elif x=="":
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


    def lcd_voltage():
        voltage = battNew.read_u16()/65536*3.33*6.2
        if voltage <= 0:
            voltage = 0
        voltagestr = f'{voltage:.2f} V' 
        if voltage < 6.1:
            undervolt=True
        else:
            undervolt=False
        try:
            display2.fill_rect(0, 0,130, 15, 0) # black out wait message
            display2.text(voltagestr, 0, 0, 1)
            if undervolt == True:
                display2.text('LOW!!!!', 70, 0, 1)
            display2.show()
        except:
            pass
        return voltage, undervolt




#_thread.start_new_thread(th_func, ())
print("")
print("")
print("")

#saccel_delay = round(0.00002909/((saccel)**3) + 0.041, 3)
#if saccel_delay > 0.8:
#    saccel_delay = 0.612
#elif saccel_delay < 0.1:
#    saccel_delay = 0.198


command0,command1, command2, command3, command4, command5, command6, command7, command8, command9 = [0,1,2,3,4,5,6,7,8,9]
del command0,command1, command2, command3, command4, command5, command6, command7, command8, command9
straightSpeed = (minstraightSpeed+maxstraightSpeed)/2
turnTime = 0.0035
taccel_delay = 0.25

led = Pin(25, Pin.OUT)
step_pin = Pin(14, Pin.OUT)
dirPin1 = Pin(11, Pin.OUT)
dirPin2 = Pin(15, Pin.OUT)
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

speakerPin = Pin(6, Pin.OUT)
speakerPin.low()

enPin1 = Pin(10, Pin.OUT)
enPin1.high()
dirfront(dirPin1)
dirfront(dirPin2)
led.low()
button = Pin(5, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2))
i2c2 = I2C(0, freq=400000, scl=Pin(13), sda=Pin(12))
try:
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
except:
    print("I2C OLED1 NOT WORKING!")

try:
    display2 = ssd1306.SSD1306_I2C(128, 64, i2c2)
except:
    print("I2C OLED2 NOT WORKING!")


try:
    stepcount = 0
    rising_edge = []
    falling_edge = []
    run_tcs = False
    tcsensor = tcs34725.TCS34725(i2c)
    tcsensor.integration_time(2.4)  # Set integration time to 2.4 ms
    tcsensor.gain(4)  # Set gain to 4x
    print("TCS Sensor 1 ID: ",tcsensor.sensor_id())  # Print sensor ID to verify connection
except Exception as e:
    print("TCS34725 Sensor 1 not found or not working! ",e)

try:
    rising_edge2 = []
    falling_edge2 = []
    tcsensor2 = tcs34725.TCS34725(i2c2)
    tcsensor2.integration_time(2.4)  # Set integration time to 2.4 ms
    tcsensor2.gain(4)  # Set gain to 4x
    print("TCS Sensor 2 ID: ",tcsensor2.sensor_id())  # Print sensor ID to verify connection
except Exception as e:
    print("TCS34725 Sensor 2 not found or not working! ",e)
command_number = 0


try:
    commands, errorcommands = compileCommands(commands)
    if errorcommands != False:
        print("Error: ", errorcommands)
        try:
            display.text('COMMANDS ERROR!!', 0, 50, 1)
        except:
            pass
        raise KeyboardInterrupt()


    startTime = ticks_ms() - 250
    AdjustSpeedTimeRealTime()
    voltage, undervoltage = lcd_voltage()
    print(str(voltage) + " V")
    try:
        display.text(f'Speed: {straightSpeed:.2f}', 0, 15, 1)
        display.text("WAIT 0.5 SEC", 0, 30, 1)
        display.text(f'Target: {targetTime}s', 0, 45, 1)
        display.show()
    except:
        pass

    if undervoltage == True:
        print("LOW VOLTAGE!")
        buzzer.duty_u16(1000)
        for i in range(3):
            led.on()
            buzzer.freq(500)
            sleep(0.15)
            led.off()
            buzzer.freq(1000)
            sleep(0.15)
        buzzer.duty_u16(0)
    del undervoltage
    del voltage

    if tmc_uart_en == True:
        try:
            from TMC_2209_StepperDriver import *
            tmc = TMC_2209(18, 19, 20, Pin(9), Pin(8),mtr_id=3) # unused pins
            tmc.setLoglevel(Loglevel.debug)
            tmc.setVSense(False)
            tmc.setInterpolation(True)
            tmc.setMicrosteppingResolution(16)
            tmc.setInternalRSense(False)
            tmc.setIScaleAnalog(False)
            tmc.setCurrent(currentmA, Vref = 2.1) # POTENTIOMETERS MUST BE AT MAX VREF (~2.3V)
            tmc.setSpreadCycle(spreadCycleEn)
            tmc.setDirection_reg(False)
        except Exception as e:
            printlcd("TMC UART FAILED")
            display.text('NOT RUNNING!!!', 0, 30, 1)
            display.show()
            buzzer.duty_u16(1000)
            for i in range(5):
                led.on()
                buzzer.freq(400)
                sleep(0.3)
                led.off()
                buzzer.freq(800)
                sleep(0.15)
            buzzer.duty_u16(0)
            while True:
                sleep(1)

    
    gc.collect()

    try:
        display.fill_rect(0, 30,130, 15, 0) # black out wait message
        display.show()
    except:
        pass
    countled = 0
    while True:
        if countled == 12500:
            lcd_voltage()
            countled = 0
        sleep_us(2)
        if button.value() == 0:
            sleep_us(25) # debounce 25ms
            if button.value() == 0:
                break
        countled += 1
    
    led.on()
    enPin1.low()

    for i in range(1, 2000):
        step_pin.value(1)
        sleep_us(10)
        step_pin.value(0)
        sleep_us(10)
    sleep(0.17)
    printlcd("Motors Enabled")

    while True:
        if countled == 12500:
            lcd_voltage()
            countled = 0
        sleep_us(2)
        if button.value() == 0:
            sleep_us(25) # debounce 25ms
            if button.value() == 0:
                break
        countled += 1
    
    while button.value() == 0:
        sleep_us(2)   # wait until button is fully released

    del countled
    # motor time offset, in nanoseconds
    startTime = ticks_ms() + startTimeOffset*(1000)
    printlcd("Starting Course")

    # BUZZ (for fun)
    buzzer.duty_u16(1000)
    sleep(0.21)
    buzzer.duty_u16(0)

    if silent == False:
        speakerPin.high()
    
    run_array(commands)
    #if abs(last_val_middle) > .1:
    #    printlcd(f'ADJ {last_val_middle:.1f}cm')
    #    #s(last_val_middle)
    #if abs(last_tiltangle) > 1:
    #    printlcd(f'TILT {last_tiltangle:.0f}deg')
    #    t(last_tiltangle)
    print("")
    printlcd(
        f'Time: {(ticks_ms() - (startTime-startTimeOffset*1000))/1000:.2f}s')
    try:
        display2.fill(0)
        display2.show()
    except:
        pass
    speakerPin.low() # turn off the sound
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
        import random
        tones = {
        "B0": 31,
        "C1": 33,
        "CS1": 35,
        "D1": 37,
        "DS1": 39,
        "E1": 41,
        "F1": 44,
        "FS1": 46,
        "G1": 49,
        "GS1": 52,
        "A1": 55,
        "AS1": 58,
        "B1": 62,
        "C2": 65,
        "CS2": 69,
        "D2": 73,
        "DS2": 78,
        "E2": 82,
        "F2": 87,
        "FS2": 93,
        "G2": 98,
        "GS2": 104,
        "A2": 110,
        "AS2": 117,
        "B2": 123,
        "C3": 131,
        "CS3": 139,
        "D3": 147,
        "DS3": 156,
        "E3": 165,
        "F3": 175,
        "FS3": 185,
        "G3": 196,
        "GS3": 208,
        "A3": 220,
        "AS3": 233,
        "B3": 247,
        "C4": 262,
        "CS4": 277,
        "D4": 294,
        "DS4": 311,
        "E4": 330,
        "F4": 349,
        "FS4": 370,
        "G4": 392,
        "GS4": 415,
        "A4": 440,
        "AS4": 466,
        "B4": 494,
        "C5": 523,
        "CS5": 554,
        "D5": 587,
        "DS5": 622,
        "E5": 659,
        "F5": 698,
        "FS5": 740,
        "G5": 784,
        "GS5": 831,
        "A5": 880,
        "AS5": 932,
        "B5": 988,
        "C6": 1047,
        "CS6": 1109,
        "D6": 1175,
        "DS6": 1245,
        "E6": 1319,
        "F6": 1397,
        "FS6": 1480,
        "G6": 1568,
        "GS6": 1661,
        "A6": 1760,
        "AS6": 1865,
        "B6": 1976,
        "C7": 2093,
        "CS7": 2217,
        "D7": 2349,
        "DS7": 2489,
        "E7": 2637,
        "F7": 2794,
        "FS7": 2960,
        "G7": 3136,
        "GS7": 3322,
        "A7": 3520,
        "AS7": 3729,
        "B7": 3951,
        "C8": 4186,
        "CS8": 4435,
        "D8": 4699,
        "DS8": 4978
        }

        rickAstley = (random.randint(0,100000) < 69420)
        if rickAstley:
            song = ['D4','E4','G4','E4','B4','P','B4','P','A4','P','P','D4','E4','G4','E4','A4','P','A4','P','G4'] #Im gonna give you up
        else:
            song = ['C5', 'AS4', 'P', 'GS4', 'P', 'G4', 'P', 'DS4', 'F4', 'P', 'C5', 'P', 'F5'] #Jaspers song
        def playtone(frequency):
            buzzer.duty_u16(1000)
            buzzer.freq(frequency)

        def bequiet():
            buzzer.duty_u16(0)

        def playsong(mysong):
            for i in range(len(mysong)):
                if (mysong[i] == "P"):
                    bequiet()
                    if rickAstley:
                        sleep(0.04)
                else:
                    playtone(tones[mysong[i]])
                sleep(0.15)
            bequiet()
        playsong(song)
    while True:
        lcd_voltage()
        sleep(.75)
except KeyboardInterrupt:
    led.off()
    enPin1.high()
    speakerPin.low()
    buzzer.duty_u16(0)
    print("Program Exited")
    if errorcommands == False: # leave the command error message on the display
        display.fill(0)
    display.text("Program Exited", 0, 0, 1)
    display.text("Press RESET", 0, 15, 1)
    display.show()
    display2.fill(0)
    display2.show()
# reset()
# I dont know why he puit the song in but remember, A bird does not sing because it has somthing to say, it sings becuase it has a song. 
# Your critique, Izyan Syed
#play this video, https://www.youtube.com/watch?v=dQw4w9WgXcQ