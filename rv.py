# DOWEL OFFSET 7CM
# IF INTIAL SPEED IS OVER 60, TURN UP THE ACCEL TO MAX

SILENT = True

TARGETTIME = 55.56

# SPEED VARS in cm/s
MAXSTRAIGHTSPEED = 200 #100 #200

# TURN VARS
turnsteps = 27.64
rturnsteps = 27.76
TCS_IMPORT = False

#17.4cm between wheels

commands="""
s70.3
r
s32.6
l
s131.3
s-48.7
l
s82.6
r
s32.6
l
s31.3
s-48.7
l
s32.6
r
s32.6
l
s82.6
l
s32.6
r
s32.6
r
s31.3
s-48.7
r
s32.6
l
s32.6
r
s82.6
r
s132.6
r
s82.6
r
s32.6
r
s31.3
s-48.7
r
s32.6
l
s82.6
l
s32.6
r
s37.3

"""

