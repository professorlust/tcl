import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 30
c = 32
b = 30
m = 30
n = 30
u = 32
v = 32
gflops = a*c*b*m*n*u*v*2/1e9
A = np.empty((v,c,a,b,u), order='f', dtype=np.float32)
B = np.empty((u,n,m,v), order='f', dtype=np.float32)
C = np.empty((c,n,a,m,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,c,a,b,u", B, "u,n,m,v", beta, C, "c,n,a,m,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vcabu,unmv->cnamb", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC