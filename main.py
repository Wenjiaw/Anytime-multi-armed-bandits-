from master.value import Value
from master.ATLUCB import AT_LUCB
from master.uniform import uniform
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (10, 8)
n=1000
m=10
interation=150000
sigma=0.5
alpha=0.99
linear=Value.linearValue(n)
polynpmial=Value.polynomialValue(n)
sparse=Value.sparseValue(n)


linear10=AT_LUCB(n,interation,sigma,alpha,1,m,linear)
minlinear10=linear10.undate()[0]
sumlinear10=linear10.undate()[1]



plt.figure(1)

plt.title('Linear m=10', fontweight='bold')
plt.xlabel('t')
plt.ylabel('min')
plt.plot(minlinear10,'b-',color='r',label='AT-LUCB')


plt.legend()
plt.xlim(0,interation)
plt.ylim(0,1)
plt.show()
