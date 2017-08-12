import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 18
c = 18
b = 16
d = 18
m = 240
u = 16
v = 18
gflops = a*c*b*d*m*u*v*2/1e9
A = np.empty((u,v,m), order='f', dtype=np.float32)
B = np.empty((b,d,u,a,v,c), order='f', dtype=np.float32)
C = np.empty((m,a,b,c,d), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,v,m", B, "b,d,u,a,v,c", beta, C, "m,a,b,c,d" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("uvm,bduavc->mabcd", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC