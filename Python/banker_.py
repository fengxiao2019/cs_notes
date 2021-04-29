# number of processes
P = 5
# number of resources
R = 3


def calculateNeed(need, maxm, allot):
    # Calculating Need of each P
    for i in range(P):
        for j in range(R):
            # Need of instance = maxm instance -
            # allocated instance
            need[i][j] = maxm[i][j] - allot[i][j]

def is_safe(processes, avail, maxm, allot):
    need = [[0] * R for _ in range(P)]
    calculateNeed(need, maxm, allot)
    finish = [0] * P
    safeSeq = [0] * P
    work = [0] * R
    for i in range(R):
        work[i] = avail[i]


import queue
from multiprocessing import queues
