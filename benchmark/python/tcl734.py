import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 24
m = 27
o = 27
n = 24
p = 27
u = 27
gflops = a*m*o*n*p*u*2/1e9
A = np.empty((n,u,o,m,p), order='f', dtype=np.float32)
B = np.empty((a,u), order='f', dtype=np.float32)
C = np.empty((n,p,m,a,o), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "n,u,o,m,p", B, "a,u", beta, C, "n,p,m,a,o" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("nuomp,au->npmao", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC