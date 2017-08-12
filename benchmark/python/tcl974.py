import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 24
b = 32
m = 864
u = 30
w = 32
v = 30
gflops = a*b*m*u*w*v*2/1e9
A = np.empty((b,u,a,v,w), order='f', dtype=np.float32)
B = np.empty((w,u,m,v), order='f', dtype=np.float32)
C = np.empty((a,b,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "b,u,a,v,w", B, "w,u,m,v", beta, C, "a,b,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("buavw,wumv->abm", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC