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
Fq = h/(2*e)
Ec_Ej_ratio = 50
deltaAl = 190e-6*1.602176634e-19 #eV

print('delta Al = ', deltaAl)

# M = np.array([[1, 1, 0], [1, -1, 0], [0, 0, 1]])
M = np.array([[1, 1], [1, -1]])
K = np.matmul(inv(M.T), np.matmul(C, inv(M)))
Kinv = inv(K)

print('Kinv = ', Kinv)
print('Kinv[1,1] = ', Kinv[1,1])

Ec = e**2/2*Kinv[1,1]
print('Ec (Joules) = ', Ec)

Ec_f = Ec/h*10**-9 #0.350#
print('Ec (GHz) = ', Ec_f)

Ej = Ec*Ec_Ej_ratio
print('Ej (Joules) = ', Ej)

Ej_f = Ec_f*Ec_Ej_ratio
print('Ej (GHz) = ', Ej_f)

omaga = np.sqrt(8.0*Ec_f*Ej_f)-Ec_f
print('omaga (GHz) = ', omaga)

Ic = Ej*2*np.pi/Fq
print('Ic (A) = ', Ic)

Rj = np.pi*deltaAl/(Ic*2*e)
print('Rj (Ohm) = ', Rj)