# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt

import numpy as np
from numpy.linalg import svd, inv
T = 200

N = 200
r=50
lam = np.random.randn(N,r)+0.1
f = np.random.randn(T,r)*0.5

X = f@lam.T+np.random.randn(T,N)
gamma = np.r_[1*np.ones((10,1)),np.zeros((N-10,1))]
y = X@gamma+10*np.random.randn(T,1)

u, s, vh = svd(X,full_matrices=False)
fhat = u[:,:r]

bhat = inv(fhat.T@fhat)@fhat.T@y
gammahat = vh[:r,:].T@inv(np.diag(s[:r]))@bhat
yhat = X@gammahat 
np.corrcoef(np.c_[y,yhat].T)

Xhat = u[:,:5]@np.diag(s[:5])@vh[:5,:]
