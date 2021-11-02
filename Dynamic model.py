import numpy as np
import matplotlib.pyplot as plt

Yp = 100
pi_p = pi_t = 0.02  # pi_p is pi past and pi_t is pi target
phi = 0.25
vt = 0
a = 1  # alpha
tt_y = 0.5
tt_pi = 0.5
ro = 0.02
e = 0

fig, ax = plt.subplots(figsize=(12, 8))
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# -- Default or manual --
if not (input("Do you want to use the default values? (y,n) ") == "y"):
    Yp = float(input("Insert potential Yield (default = 100): "))
    pi_p = float(input("Insert previous inflation (default = 0.02): "))
    pi_t = float(input("Insert target inflation (default = 0.02): "))
    phi = float(input("Insert philips curve slope (default = 0.25): "))
    ro = float(input("Insert natural real interest rate (default = 0.02): "))
    a = float(input("Insert the yield's sensitivity to differences between the real and natural interest (default = "
                    "1): "))
    tt_y = float(input("Insert the interest's reaction to the yield not being equal to the potential yield (default = "
                       "0.5): "))
    tt_pi = float(input("Insert the inflation's reaction to the inflation not being equal to the target inflation ("
                        "default = 0.5): "))

# -- Defining functions --
def Pi_s(Y):
    return pi_p + phi * (Y - Yp) + vt


def Pi_d(Y):
    return pi_t + ((1 + a * tt_y) / (a * tt_pi)) * (Yp - Y) + (1 / (a * tt_pi)) * e


Y = np.arange(0, 200, 0.001)

# -- DAS initial plot --
pi_s = pi_p + phi * (Y - Yp) + vt
plt.plot(Y, pi_s, label="DAS")

# -- DAD initial plot --
pi_d = pi_t + ((1 + a * tt_y) / (a * tt_pi)) * (Yp - Y) + (1 / (a * tt_pi)) * e
plt.plot(Y, pi_d, label="DAD")

# -- Demand Shock --
shock = float(input("Please enter a demand shock (0 if none):"))
if shock != 0:
    e = shock
    pi_d = pi_t + ((1 + a * tt_y) / (a * tt_pi)) * (Yp - Y) + (1 / (a * tt_pi)) * e
    plt.plot(Y, pi_d, label="DAD-Shocked")

# -- Supply Shock --
shock = float(input("Please enter a Supply shock (0 if none):"))
if shock != 0:
    vt = shock
    pi_s = pi_p + phi * (Y - Yp) + vt
    plt.plot(Y, pi_s, label="DAS-Shocked")

# -- Initial cross point --
lY = 0
d = 100
for Yi in Y:
    if (abs(Pi_s(Yi) - Pi_d(Yi))) < d:
        d = abs(Pi_s(Yi) - Pi_d(Yi))
        lY = Yi
print("The Intial Cross Point Is: Y=", lY, " pi=", Pi_d(lY))
pi_p = Pi_d(lY)

# -- Moving towards equilibrium --
runs = 0
if e != 0 or vt != 0:
    print("There was a Shock, we'll need to move to an equilibrium")
e = 0
vt = 0
timelimit = int(input("Do you want a time limit? (3 is recommended): "))
while abs(lY - Yp) > 0.01 and runs < timelimit:
    runs = runs + 1
    pi_s = pi_p + phi * (Y - Yp) + vt
    plt.plot(Y, pi_s, label="DAS" + str(runs))
    pi_d = pi_t + ((1 + a * tt_y) / (a * tt_pi)) * (Yp - Y) + (1 / (a * tt_pi)) * e
    plt.plot(Y, pi_d, label="DAD" + str(runs))
    d = 100
    for Yi in Y:
        if (abs(Pi_s(Yi) - Pi_d(Yi))) < d:
            d = abs(Pi_s(Yi) - Pi_d(Yi))
            lY = Yi

# -- Final Cross point --
for Yi in Y:
    if (abs(Pi_s(Yi) - Pi_d(Yi))) < d:
        d = abs(Pi_s(Yi) - Pi_d(Yi))
        lY = Yi
print("The Final Cross Point Is: Y=", lY, " pi=", Pi_d(lY), " and it took me ", runs, " time periods")

show = input("Wanna see the graph? (y,n) ")
if show == "y":
    plt.ylim([0, 0.6])
    plt.xlim([97.5, 102.5])
    plt.grid()
    plt.legend()
    plt.show()
    plt.pause(0.8)
