# DOWEL OFFSET 7CM
# IF INTIAL SPEED IS OVER 40, TURN UP THE ACCEL TO MAX

silent = False
targetTime = 56.5

# ACCEL VARS
# SPEED VARS in cm/s
saccel = 5 #4 #5.45
turnSpeedDefault = 80 #80 #110
maxstraightSpeed = 100
minstraightSpeed = 3


commands="""
s32
l
s50
r
s50
u
s50
l
s100
l
s100
l
s50
l
s50
u
s50
l
s50
r
s50
r
s150
l
s50
l
s50
u
s50
r
s50
r
s150
l
s50
l
s100
r
s100
l
s50
u
s50
r
s100
l
s100
r
s49.1
r
s40.7
"""

commands4 = """
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
s89
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

commands8= """
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


