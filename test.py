from master.value import Value
import numpy as np
import heapq
import bottleneck
value=Value(1000).linearValue()

sample=np.zeros_like(value)
result=np.zeros_like(value)
c=0
for i in range(200):
    sample = np.zeros_like(value)
    for j in range(1000):
        sample[j]=np.random.normal(value[j],0.4)


    a = heapq.nlargest(10, sample)
    b=min(a)
    c=c+b

c=c/200
print(c)
