import matplotlib.pyplot as plt


def Pi_s(Y, pi_p=0.02, phi=0.25, Yp=100, vt=0):
    return pi_p + phi * (Y - Yp) + vt


def Pi_d(Y, pi_t=0.02, a=1, tt_y=0.5, tt_pi=0.5, Yp=100, e=0):
    return pi_t + ((1 + a * tt_y) / (a * tt_pi)) * (Yp - Y) + (1 / (a * tt_pi)) * e


