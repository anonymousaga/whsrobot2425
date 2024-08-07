# DOWEL OFFSET 7CM
# IF INTIAL SPEED IS OVER 60, TURN UP THE ACCEL TO MAX

targetTime = 11

# ACCEL VARS
saccel = 5.45 #3.8 #5.45


# SPEED VARS in cm/s
turnSpeedDefault =  120 #90 #120
maxstraightSpeed = 150 #100 #150
minstraightSpeed = 3


commands="""
s32
r
s50
l
s75
ld
sd50
r
sd50
l
sd25
ld
s100
ld
sd25
l
sd50
r
sd50
ld
s75
l
s50
l
s50
l
s50
r
s25
rd
sd50
l
sd50
r
sd25
rd
s100
rd
sd25
r
sd50
l
sd50
r
s48
u
s48
l
sd50
r
sd50
l
sd25
ld
s100
ld
sd25
l
sd50
r
sd50
ld
s75
l
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


