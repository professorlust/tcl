import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 72
m = 72
u = 72
o = 72
n = 72
gflops = a*m*u*o*n*2/1e9
A = np.empty((u,a), order='f', dtype=np.float32)
B = np.empty((o,n,u,m), order='f', dtype=np.float32)
C = np.empty((a,m,n,o), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,a", B, "o,n,u,m", beta, C, "a,m,n,o" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("ua,onum->amno", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC