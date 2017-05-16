
# coding: utf-8

# In[2]:

type(10)
type(2.718)
type("hello")


# In[3]:

a=[1,2,3,4,5]
print(a)


# In[4]:

len(a)


# In[5]:

a[:-1]


# In[7]:

me={'height':180}


# In[8]:

me['height']


# In[9]:

me['weight']=70


# In[10]:

me['weight']


# In[11]:

print(me)


# In[14]:

hungry = True


# In[15]:

if hungry:
    print("I'm hungry")


# In[16]:

hungry = False


# In[18]:

if hungry:
    print("I'm hungry")
else:
    print("I'm not hungry")
    print("I'm sleepy")        


# In[19]:

for i in[1,2,3]:
    print(i)


# In[20]:

def hello():
    print("Hello world!")


# In[21]:

hello()


# In[22]:

class Man:
    def __init__(self, name):
        self.name = name
        print("initialized!")
        
    def hello(self):
        print("hello, " + self.name + "!")
    
    def goodbye(self):
        print("goodbye " + self.name + "!")


# In[23]:

m = Man("David")
m.hello()


# In[24]:

m.goodbye()


# In[26]:

import numpy as np
x = np.array([1.0, 2.0, 3.0])
print(x)


# In[27]:

type(x)


# In[28]:

y = np.array([4.0, 5.0, 6.0])


# In[29]:

x + y


# In[32]:

x * y


# In[33]:

x / y


# In[35]:

x * 2


# In[36]:

x / 2


# In[40]:

import numpy as np
A = np.array([[1, 2], [3, 4]])
type(A)


# In[41]:

print(A)


# In[43]:

A.shape


# In[44]:

A.dtype


# In[45]:

B = np.array([[5, 6], [7, 8]])


# In[46]:

A * B


# In[47]:

C = np.array([10, 20])


# In[48]:

A * C


# In[49]:

A[1]


# In[50]:

A[1][1]


# In[51]:

X = A.flatten()


# In[52]:

print(X)


# In[53]:

X[np.array([0, 2, 3])]


# In[54]:

X > 3


# In[55]:

X[X > 3]


# In[56]:

import matplotlib.pyplot as plt

x = np.arange(0, 6, 0.1)
y = np.sin(x)


# In[57]:

plt.plot(x, y)
plt.show()


# In[58]:

y2 = np.cos(x)
plt.plot(x, y2)
plt.show()


# In[60]:

plt.plot(x, y, label="sin")
plt.plot(x, y2, linestyle="--", label="cos")
plt.xlabel("x")
plt.ylabel("y")
plt.title('sin & cos')
plt.legend()
plt.show()


# In[64]:

import matplotlib.pyplot as plt
from matplotlib.image import imread

img = imread('4cee3e54-7fa6-4665-a65e-79087a111197_4.jpg')

plt.imshow(img)
plt.show()


# In[ ]:



