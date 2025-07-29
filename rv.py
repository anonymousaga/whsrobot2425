# DOWEL OFFSET 7CM
# IF INTIAL SPEED IS OVER 60, TURN UP THE ACCEL TO MAX

silent = False

targetTime = 60

# ACCEL VARS
# SPEED VARS in cm/s
saccel = 4.3 #4.15 #5.45
turnSpeedDefault = 90 #90 #120
maxstraightSpeed = 145 #100 #145

# TURN VARS
lturnsteps = 15.485
rturnsteps = lturnsteps + 0.062

commands="""
s25
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

commands4= """
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