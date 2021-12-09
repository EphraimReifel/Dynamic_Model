import matplotlib.pyplot as plt


def Pi_s(Y, pi_p=0.02, phi=0.25, Yp=100, vt=0):     # === Calculating supply inflation
    return pi_p + phi * (Y - Yp) + vt


def Pi_d(Y, pi_t=0.02, a=1, tt_y=0.5, tt_pi=0.5, Yp=100, e=0):  # === Calculating demand inflation
    return pi_t + ((1 + a * tt_y) / (a * tt_pi)) * (Yp - Y) + (1 / (a * tt_pi)) * e


def cross_point(Y):     # === Finding the cross point and returning its Yield (x axis)
    lY = 0
    d = 100
    for Yi in Y:
        if (abs(Pi_s(Yi) - Pi_d(Yi))) < d:
            d = abs(Pi_s(Yi) - Pi_d(Yi))
            lY = Yi
    print("The Intial Cross Point Is: Y=", lY, " pi=", Pi_d(lY))
    iY = lY
    pi_p = Pi_d(lY)
    return lY

