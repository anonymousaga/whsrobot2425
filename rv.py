# DOWEL OFFSET 7CM
# IF INTIAL SPEED IS OVER 60, TURN UP THE ACCEL TO MAX

silent = False
targetTime = 62.7

# ACCEL VARS
# SPEED VARS in cm/s
saccel = 4.17 #3.7 #5.45
turnSpeedDefault = 95 #90 #120
maxstraightSpeed = 145 #100 #145


commands="""
s82
l
s40
u
s40
l
s100
l
s50
l
s50
r
s50
l
s50
r
s50
l
s40
u
s40
r
s50
l
s100
r
s150
r
s140
u
s140
l
s150
l
s100
r
s50.7
r
s37
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

