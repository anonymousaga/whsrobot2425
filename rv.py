# DOWEL OFFSET 7CM
# IF INTIAL SPEED IS OVER 60, TURN UP THE ACCEL TO MAX

targetTime = 69.8

# ACCEL VARS
saccel = 3.6 #3.8 #5.45


# SPEED VARS in cm/s
turnSpeedDefault =  90 #90 #120
maxstraightSpeed = 100 #100 #150
minstraightSpeed = 3


commands="""
s132
u
s100
r
s100
r
s25
t45
sd50
l
sd50
t45
s25
r
s100
u
s200
u
s50
r
s150
r
s50
u
s50
l
s150
l
s49.3
l
s48.4
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


