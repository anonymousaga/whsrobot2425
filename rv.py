# DOWEL OFFSET 7CM
# IF INTIAL SPEED IS OVER 60, TURN UP THE ACCEL TO MAX

silent = False

targetTime = 72.69

# ACCEL VARS
# SPEED VARS in cm/s
saccel = 4.35 #3.7 #5.45
turnSpeedDefault = 95 #90 #120
maxstraightSpeed = 145 #100 #145


commands="""
s32
r
s100
l
s125
ld
sd35
u
sd35
rd
s50
rd
sd25
r
sd50
ld
s75
r
s50
r
s40
u
s90
l
s40
u
s40
r
s25
rd
sd50
ld
s75
r
s75
rd
sd25
r
sd30
u
sd30
l
sd25
ld
s75
l
s100
r
s50
l
s44
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