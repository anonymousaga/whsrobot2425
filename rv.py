# DOWEL OFFSET 7CM
# IF INTIAL SPEED IS OVER 60, TURN UP THE ACCEL TO MAX

silent = False
targetTime = 62.6

# ACCEL VARS
# SPEED VARS in cm/s
saccel = 3.8 #3.8 #5.45
turnSpeedDefault =  90 #90 #120
maxstraightSpeed = 100 #100 #150
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
s50
r
s43
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


