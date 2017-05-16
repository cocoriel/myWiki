
# coding: utf-8

# In[6]:

def AND(x1, x2):
    w1, w2, theta = 0.5, 0.5, 0.7
    tmp = w1*x1 + w2*x2
    if tmp > theta:
        return 1
    elif tmp <= theta:
        return 0


# In[7]:

AND(0, 0)


# In[8]:

AND(1, 0)


# In[9]:

AND(0, 1)


# In[10]:

AND(1, 1)


# In[14]:

import numpy as np
def AND2(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.7
    tmp = np.sum(w*x) + b
    if tmp > 0:
        return 1
    else:
        return 0


# In[15]:

AND2(1, 1)


# In[16]:

AND2(0, 0)


# In[19]:

def NAND(x1, x2):
    x = np.array([x1, x2])
    w = np.array([-0.5, -0.5])
    b = 0.7
    tmp = np.sum(w*x) + b
    if tmp > 0:
        return 1
    else:
        return 0


# In[20]:

NAND(1,1)


# In[21]:

NAND(1,0)


# In[22]:

NAND(0,1)


# In[23]:

NAND(0,0)


# In[24]:

def OR(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.2
    tmp = np.sum(w*x) + b
    if tmp > 0:
        return 1
    else:
        return 0


# In[25]:

def XOR(x1, x2):
    s1 = NAND(x1, x2)
    s2 = OR(x1, x2)
    y = AND(s1, s2)
    return y


# In[27]:

XOR(0, 0)


# In[28]:

XOR(0, 1)


# In[29]:

XOR(1, 0)


# In[30]:

XOR(1, 1)


# In[ ]:



