# DOWEL OFFSET 7CM
# IF INTIAL SPEED IS OVER 60, TURN UP THE ACCEL TO MAX

silent = False
targetTime = 70.581

# ACCEL VARS
# SPEED VARS in cm/s
saccel = 3.7 #3.7 #5.45
turnSpeedDefault = 90 #90 #120
maxstraightSpeed = 145 #100 #145


commands="""
s122
u
s90
r
s75
rd
sd25
r
sd50
l
sd50
r
sd25
t45
s65
u
s190
u
s50
r
s125
rd
sd30
u
sd30
t-45
s125
l
s51.8
l
s49.7
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

