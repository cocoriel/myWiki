
# coding: utf-8

# ### 1st day
# -----------------------------------------------------------------------
# 1. install
#     - pip3 install ipython[all]
#     - pip3 install --upgrade numpy
#     - pip3 install --upgrade matplotlib
#     - pip3 install --upgrade tensorflow-gpu # GPU 버전인경우
#     - pip3 install --upgrade tensorflow     # CPU 버전인경우
#     
# 2. python 경로
#     - C:\Users\user\AppData\Local\Programs\Python\Python36
#     - C:\Program Files\Java\jdk1.8.0_131
# condition and loop

var = 10
if var <  20:
    print('less than 20')
else:
    print('not found')


words = ['this', ' is', 'wonder']
for word in words:
    print(word)

for x in range(10):
    print(x)


# function
def getName():
    '''이름을 print 하는 함수'''
    print('Jinhwa Park')

getName()
help(getName)

def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

nf = factorial(6)
print(nf)

# lambda
t2 = {'FtoK':lambda deg_f:273 + (deg_f - 32) * 5/9, 'CtoK':lambda deg_c:273 + deg_c}

print(t2['FtoK'](32))
print(t2)

# file 입출력
f = open('sometext.txt', 'w')
f.write('hello world')

f.close()

f = open('D:\workspace\sometext.txt', 'r')
print(f.read())
f.close()

# OOP
class Person:
    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def greet(self):
        print("Hello, I am %s." %self.name)

person1 = Person()
person2 = Person()
person1.setName('tea hee kim')
person2.setName('dong won kang')
person1.greet()
person2.greet()

# In[2]:


import numpy as np
from numpy.random import randn
import matplotlib.pyplot as plt


# In[14]:


data = {i: randn() for i in range(7)}


# In[15]:


data


# In[16]:


a = np.array([1,2,3])


# In[17]:


print(type(a))
print(a.shape)


# In[18]:


b = np.array([[1,2,3],[4,5,6]])


# In[24]:


print(type(b))
print(b.shape)


# In[25]:


c = np.arange(32).reshape(8,4)


# In[26]:


c


# In[30]:


a = np.zeros((2,2))
b = np.ones((2,2))
c = np.full((2,2), 7)
d = np.eye(2)
e = np.random.random((2,2))


# In[31]:


a


# In[32]:


b


# In[33]:


c


# In[34]:


d


# In[35]:


e


# In[36]:


a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
a


# - b는 a라는 원본을 참조하고 있음
# - 따라서 b를 수정하면 원본배열 a 역시 수정됨

# In[37]:


b = a[:2, 1:3]
b


# In[40]:


row_r1 = a[1, :]
row_r2 = a[1:2, :]


# In[49]:


print(row_r1) #rank 1인 배열
print(row_r1.shape)


# In[50]:


print(row_r2) #rank 2인 배열
print(row_r2.shape)


# In[43]:


col_r1 = a[:,1]
col_r2 = a[:, 1:2]


# In[46]:


print(col_r1)
print(col_r1.shape)


# In[48]:


print(col_r2)
print(col_r2.shape)


# In[51]:


a = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])


# In[52]:


b = np.array([0,2,0,1])


# In[53]:


a[np.arange(4), b]


# In[55]:


a = np.array([[1,2],[3,4],[5,6]])


# In[56]:


bool_inx = (a > 2)


# In[57]:


bool_inx


# In[58]:


a[bool_inx]


# In[59]:


a[a > 2]


# In[60]:


x = np.array([1,2])
x.dtype


# In[62]:


x = np.array([1.0, 2.0])
x.dtype


# In[63]:


x = np.array([1,2], dtype=np.int64)
x.dtype


# In[3]:


x = np.arange(0, 3 * np.pi, 0.1)
y = np.sin(x)


# In[4]:


plt.plot(x, y)
#plt.show()

plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.title("Sine")
plt.legend(['Sine'])
plt.show()


# In[ ]:




