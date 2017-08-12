import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 16
c = 16
b = 16
d = 16
m = 15
n = 16
u = 16
v = 16
gflops = a*c*b*d*m*n*u*v*2/1e9
A = np.empty((u,n,m,v), order='f', dtype=np.float32)
B = np.empty((v,b,a,d,u,c), order='f', dtype=np.float32)
C = np.empty((n,c,a,b,d,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,n,m,v", B, "v,b,a,d,u,c", beta, C, "n,c,a,b,d,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("unmv,vbaduc->ncabdm", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC