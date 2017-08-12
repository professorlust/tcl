import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 24
b = 16
m = 16
o = 15
n = 15
p = 15
u = 162
gflops = a*b*m*o*n*p*u*2/1e9
A = np.empty((a,b,u), order='f', dtype=np.float32)
B = np.empty((m,o,n,p,u), order='f', dtype=np.float32)
C = np.empty((b,m,n,o,a,p), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,b,u", B, "m,o,n,p,u", beta, C, "b,m,n,o,a,p" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("abu,monpu->bmnoap", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC