
# packages
import numpy as np
import scipy as sp
from scipy import linalg as la
import contextlib
import scipy.linalg as sla

def Df(g,y,d=1e-4):
    """
    approximate derivative via finite-central-differences 

    input:
    g - function - g : R^n -> R^m
    y - n array
    (optional)
    d - scalar - finite differences displacement parameter

    output:
    Dg(y) - m x n - approximation of Jacobian of g at y
    """
    # given $g:\mathbb{R}^n\rightarrow\mathbb{R}^m$:
    # $$D_y g(y)e_j \approx \frac{1}{2\delta}(g(y+\delta e_j) - g(y - \delta e_j)),\ \delta\ll 1$$
    e = np.identity(len(y))
    Dyg = []
    for j in range(len(y)):
        Dyg.append((.5/d)*(g(y+d*e[j]) - g(y-d*e[j])))
    return np.array(Dyg).T

def forward_euler(f,t,x0=[],t0=0.,dt=1e-4,ut=None,
                  ux=None,utx=None,return_u=False):
    """
    simulate x' = f(x,u) using forward Euler algorithm

    input:
        f : R x X x U --> X - vector field
        X - state space (must be vector space)
        U - control input set
        t - scalar - final simulation time
        x - initial condition; element of X

    (optional:)
        t0 - scalar - initial simulation time
        dt - scalar - stepsize parameter
        return_u - bool - whether to return u_

        (only one of:)
        ut : R --> U
        ux : X --> U
        utx : R x X --> U

    output:
        t_ - N array - time trajectory
        x_ - N x X array - state trajectory
        (if return_u:)
        u_ - N x U array - state trajectory
    """
    t_,x_,u_ = [t0],[x0],[]
  
    inputs = sum([1 if u is not None else 0 for u in [ut,ux,utx]])
    assert inputs <= 1, "more than one of ut,ux,utx defined"

    if inputs == 0:
        assert not return_u, "no input supplied"
    else:
        if ut is not None:
            u = lambda t,x : ut(t)
        elif ux is not None:
            u = lambda t,x : ux(x)
        elif utx is not None:
            u = lambda t,x : utx(t,x)

    while t_[-1]+dt < t:
        if inputs == 0:
            _t,_x = t_[-1],x_[-1]
            dx = f(t_[-1],x_[-1]) * dt
        else:
            _t,_x,_u = t_[-1],x_[-1],u(t_[-1],x_[-1])
            dx = f(_t,_x,_u) * dt
            u_.append( _u )

        x_.append( _x + dx )
        t_.append( _t + dt )

    if return_u:
        return np.asarray(t_),np.asarray(x_),np.asarray(u_)
    else:
        return np.asarray(t_),np.asarray(x_)

def psi(f,t,x,t0=0.,dt=1e-4,ut=None,ux=None,utx=None):
    """
    simulate x' = f(x,u) using forward Euler algorithm, return final state

    input:
    f : R x X x U --> X - vector field
    X - state space (must be vector space)
    U - control input set
    t - scalar - final simulation time
    x - initial condition; element of X

    (optional:)
    t0 - scalar - initial simulation time
    dt - scalar - stepsize parameter

    (only one of:)
    ut : R --> U
    ux : X --> U
    utx : R x X --> U
    output:
      x(t) - X array - final state 
    """
    t_,x_ = forward_euler(f,t,x,t0=t0,dt=dt,ut=ut,ux=ux,utx=utx)
    return x_[-1]

def controllability(A,B):
    """
    controllability matrix of the pair (A,B)

    input:
        A - n x n 
        B - n x m

    output:
        C - n x (n*m) 
    """
    assert A.shape[0] == A.shape[1] # A is n x n
    assert A.shape[0] == B.shape[0] # B is n x m
    C = [B]
    for n in range(A.shape[0]):
        C.append( np.dot(A, C[-1]) )
    return np.hstack(C)

def controllable(A,B,eps=1e-3):
    """
    test controllability of the pair (A,B) for the LTI system  x' = A x + B u

    input:
        A - n x n 
        B - n x m
        (optional)
        eps - threshold on singular values of controllability matrix

    output:
        bool - controllable (with threshold eps)
    """
    C = controllability(A,B)
    _,s,_ = np.linalg.svd(C)
    return np.all( s > eps )

def observability(A,C):
    """
    observability matrix of the pair (A,C)

    input:
        A - n x n 
        C - m x n

    output:
        O - (n*m) x n
    """
    assert A.shape[0] == A.shape[1] # A is n x n
    assert A.shape[0] == C.shape[1] # C is m x n
    return controllability(A.T,C.T).T

def observable(A,C,eps=1e-3):
    """
    test observability of the pair (A,C) 
    for the LTI system  x' = A x, y = C x

    input:
        A - n x n 
        C - m x n
        (optional)
        eps - threshold on singular values of observability matrix

    output:
        bool - observable (with threshold eps)
    """
    O = observability(A,C)
    _,s,_ = np.linalg.svd(O)
    return np.all( s > eps )

@contextlib.contextmanager
def temp_seed(seed):
    state = np.random.get_state()
    np.random.seed(seed)
    try:
        yield
    finally:
        np.random.set_state(state)
        
def PSD(n,sqrt=False, seed=None):
    """
      compute random positive semidefinite matrix

      input:
        n - int - dimension of matrix
        (optional)
        sqrt - bool - whether to return S such that Q = np.dot( S.T, S)

      output:
        Q - n x n - Q = Q^T,  spec Q \subset R^+
    """
    if seed!=None:
        np.random.seed(seed)
    H = np.random.randn(n,n)
    d,u = np.linalg.eig(H + H.T)
    S = np.dot( u, np.dot( np.diag( np.sqrt( d*np.sign(d) ) ), u.T ) )
    if sqrt:
        return np.dot(S.T, S), S
    else:
        return np.dot(S.T, S)
    
    
def isPSD(P, verbose=True):
    if np.allclose(P,P.T, rtol=1e-3) and np.all(np.linalg.eig(P)[0]>0):
        print('is PD?  :   True')
        if verbose:
            print('eigs(P) :  ', np.linalg.eig(P)[0])
    else: print('is PD?  :   False')
    return np.allclose(P,P.T, rtol=1e-3) and np.all(np.linalg.eig(P)[0]>0)
        
        
def isCTRB(C, n):
    if np.linalg.matrix_rank(C)==n:
        print('is CC?   :   True')
    else: print('is CC?   :   False')
    print("rank(C): ", np.linalg.matrix_rank(C))
        
def isOBSV(O, n):
    if np.linalg.matrix_rank(O)==n:
        print('is CO   :   True')
    else: 
        print('is CO?   :   False')
    print("rank(O): ", np.linalg.matrix_rank(O))
        
## this is a simple function to implement the PBH test

def PBH(A,B):
    '''PBH test
    input: dynamics A, nxn array
    output: true if rank(sI-A|B)=n for all s in spec(A)
            false otherwise
    '''
    print(np.all(np.array([np.linalg.matrix_rank(np.hstack((s*np.eye(A.shape[0])-A, B)))
                           -A.shape[0] for s in np.linalg.eig(A)[0]])<=1e-4))
    
def lyapCtr(A,B, verbose=False):
    Q=-B@B.T
    W=sla.solve_lyapunov(A.T,Q)
    if verbose:
        print("W:\n",W)
        print("")
    print("is controllable? : ", isPSD(W))
    
def getCtrMat(A,B):
    n=A.shape[0]
    Wc_=B
    for i in range(n-1):
        A_=np.copy(A)
        for j in range(i): A_=A_@A
        Wc_=np.hstack((Wc_, A_@B))
    return Wc_

## this is a simple function to implement the PBH test

def detect(A, C, verbose=False):
    '''PBH test
    input: dynamics A, nxn array
    output: true if rank(sI-A|B)=n for all s in spec(A)
            false otherwise
    '''
    v=[]
    n=np.shape(A)[0]
    for e in np.linalg.eig(A)[0]:
        if np.real(e)>=0:
            v.append(np.linalg.matrix_rank(np.vstack((e*np.eye(A.shape[0])-A, C))))
    isdetect=np.all(np.asarray(v)==n)
    if verbose:
        print("is detectable?: ", isdetect)
    return isdetect

    #print(np.all(np.array([np.linalg.matrix_rank(np.hstack((s*np.eye(A.shape[0])-A, B)))-A.shape[0] for s in np.linalg.eig(A)[0]])<=1e-4))

            
def getObsMat(A,C):
    n=A.shape[0]
    O_=C
    for i in range(n-1):
        A_=np.copy(A)
        for j in range(i): A_=A_@A
        O_=np.vstack((O_, C@A_))
    return O_


def feuler(f, T=None ,x0=[], dt=1e-3,MAXITERS=None, t0=0):
    '''
        T  :  final time
        f  :  dynamics, (t,x) --> R^n
        x  :  state, in R^n
        dt :  stepsize
        x0 :  initial state, in R^n
        
        (optional)
        MAXITERS : if you want to specify iterations, you can
        t0 : initial time
    '''
    n=len(x0)
    if T==None and MAXITERS!=None:
        T=MAXITERS*dt
    elif MAXITERS==None and T!=None:
        MAXITERS=int(T/dt)
    else:
        raise Exception('MAXITERS or T should be defined.')


    x=[x0]
    t=[t0]
    for i in range(MAXITERS-1):
        x.append(x[-1]+dt*f(t[-1],x[-1]))
        t.append(t[-1]+dt)
    return np.asarray(t),np.asarray(x).reshape(MAXITERS,n)