import numpy as np
from numpy.linalg import inv

# check the scaling factor of F
with open('moonmon_460um.txt') as f:
    lines = f.readlines()[7:7+3]
    C = []
    for line in lines:
        C.append([float(l)*1e-12 for l in line.split()[1:]])

C = np.array(C)
C = C[1:3,1:3]
print('C = ', C)

# Constants
e = 1.602e-19
h = 6.626e-34
hbar = h / (2 * np.pi)

# M = np.array([[1, 1, 0], [1, -1, 0], [0, 0, 1]])
M = np.array([[1, 1], [1, -1]])
K = np.matmul(inv(M.T), np.matmul(C, inv(M)))
Kinv = inv(K)

print('Kinv = ', Kinv)
print('Kinv[1,1] = ', Kinv[1,1])

Ec = e**2/2*Kinv[1,1]
print('Ec (Joules) = ', Ec)

Ec = 0.350#Ec/h*10**-9
print('Ec (GHz) = ', Ec)

Ej = Ec*50
print('Ej (GHz) = ', Ej)

omage = np.sqrt(8.0*Ec*Ej)
print('omage (GHz) = ', omage)