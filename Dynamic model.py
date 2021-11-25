import numpy as np
import matplotlib.pyplot as plt

Yp = 100
pi_p = pi_t = 0.02  # pi_p is past pi and pi_t is target pi
phi = 0.25
vt = 0
a = 1  # alpha
tt_y = 0.5
tt_pi = 0.5
ro = 0.02
e = 0

fig, axs = plt.subplots(1, 3)

# -- Default or manual --
if not (input("Do you want to use the default values? ('y' - yes, else - no) ") == "y"):
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


# -- t_0 base plot --
def plotbasefunc(i):  # function that plots the base supply and demand plots
    # -- DAS initial plot --
    vt = 0
    pi_s = pi_p + phi * (Y - Yp) + vt
    axs[i] = plt.plot(Y, pi_s, 'o', label="DAS")

    # -- DAD initial plot --
    e = 0
    pi_d = pi_t + ((1 + a * tt_y) / (a * tt_pi)) * (Yp - Y) + (1 / (a * tt_pi)) * e
    axs[i] = plt.plot(Y, pi_d, 'o',  label="DAD")


# -- Calling to plot --
axs[0] = plt.figure(0)
plotbasefunc(0)

# -- Asking for shocks --
shockd = float(input("Please enter a Demand shock (0 if none):"))
shocks = float(input("Please enter a Supply shock (0 if none):"))

# -- Plotting the shocks --
for i in 1, 2:
    axs[i] = plt.figure(i)
    plotbasefunc(i)
    # -- Demand Shock calc--
    if shockd != 0:
        e = shockd
        pi_d = pi_t + ((1 + a * tt_y) / (a * tt_pi)) * (Yp - Y) + (1 / (a * tt_pi)) * e
        axs[i] = plt.plot(Y, pi_d, label="DAD-Shocked")

    # -- Supply Shock calc--
    if shocks != 0:
        vt = shocks
        pi_s = pi_p + phi * (Y - Yp) + vt
        axs[i] = plt.plot(Y, pi_s, label="DAS-Shocked")

# -- Initial cross point --
lY = 0
d = 100
for Yi in Y:
    if (abs(Pi_s(Yi) - Pi_d(Yi))) < d:
        d = abs(Pi_s(Yi) - Pi_d(Yi))
        lY = Yi
print("The Intial Cross Point Is: Y=", lY, " pi=", Pi_d(lY))
iY = lY
pi_p = Pi_d(lY)

# -- Moving towards equilibrium --
axs[2] = plt.figure(2)
runs = 0
if e != 0 or vt != 0:
    print("There was a Shock, we'll need to move to an equilibrium")
e = vt = 0
timelimit = int(input("Do you want a time limit to checking the equilibrium? (3 is recommended): "))
while abs(lY - Yp) > 0.01 and runs < timelimit:
    runs = runs + 1
    pi_s = pi_p + phi * (Y - Yp) + vt
    axs[2] = plt.plot(Y, pi_s, label="DAS" + str(runs))
    pi_d = pi_t + ((1 + a * tt_y) / (a * tt_pi)) * (Yp - Y) + (1 / (a * tt_pi)) * e
    axs[2] = plt.plot(Y, pi_d, label="DAD" + str(runs))
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

# -- showing the plot --
show = input("Wanna see the graph? (y,n) ")
if show == "y":
    lx = ry = uy = dy = 0
    if iY >= Yp:
        rx = iY + 0.1
        lx = Yp - 0.1
    else:
        lx = iY - 0.1
        rx = Yp + 0.1
    if Pi_d(iY) >= Pi_d(lY):
        uy = Pi_d(iY) + 0.2
        dy = Pi_d(lY) - 0.2
    else:
        uy = Pi_d(lY) + 0.2
        dy = Pi_d(iY) - 0.2
    for plo in 0, 1, 2:
        plt.figure(plo)
        plt.ylim([dy, uy])
        plt.xlim([lx, rx])
        plt.grid()
        plt.legend()
    plt.show()
