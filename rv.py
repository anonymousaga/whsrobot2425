# DOWEL OFFSET 7CM
# IF INTIAL SPEED IS OVER 60, TURN UP THE ACCEL TO MAX

targetTime = 55.1

# ACCEL VARS
saccel = 3.8 #5.5


# SPEED VARS in cm/s
turnSpeedDefault =  90 #120
maxstraightSpeed = 100 #150
minstraightSpeed = 3


commands = """
s32
r
s100
l
s125
t-135
sd75
rd
s75
r
s75
rd
sd30
u
sd30
ld
s75
r
s50
r
s93
"""

commands5 = """
s32
l
s50
r
s200
ld
s2
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

commands5= """
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


