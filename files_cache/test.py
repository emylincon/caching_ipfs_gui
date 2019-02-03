import matplotlib.pyplot as plt
from numpy import pi, linspace, sin, cos, tan
from matplotlib.pylab import subplot, figure


x1 = x2 = linspace(0, 4*pi, 100)
y1 = sin(x1)
y2 = cos(x2)


def plotme():
    figure('yes')
    graph1()
    graph2()
    graph3()
    graph4()
    plt.show()


def graph1():
    subplot(2, 2, 1)
    plt.plot(x1, y1, "b-*")


def graph2():
    subplot(2, 2, 2)
    plt.plot(x2, y2, "r-h")


def graph3():
    subplot(2, 2, 3)
    plt.plot(x1, y1, "g-*")


def graph4():
    subplot(2, 2, 4)
    plt.plot(x2, y2, "r-h")


plotme()
