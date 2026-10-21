import sys; sys.path.insert(0,"src")
import numpy as np
from gems81.metric import dti_binary, kernel
def test_kernel(): assert kernel(0)==1 and kernel(3)==0 and abs(kernel(1.5)-0.5)<1e-12
def test_dti_perfect():
    t=np.zeros((9,9),bool); t[4,4]=True; assert dti_binary(t.copy(),t)["dti"]>0.999
def test_dti_empty():
    t=np.zeros((9,9),bool); t[4,4]=True; assert dti_binary(np.zeros((9,9),bool),t)["dti"]==0
