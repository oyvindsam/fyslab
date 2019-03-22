"""
Bevegelsen til kulen gjennom banen er beskrevet av ligning (6).
Dette er en førsteordens differensialliging som vi vil løse nummerisk med Eulers metode yn+1=yn+hf(tn,yn).(15)
Denne brukes for å finne nestey-verdi,yn+1,
ved å adderenåværendey-verdi og stigningstalletf(tn,yn)(den deriver-te av y) multiplisert med en liten steglengde h.
Vi vil førstløse ligningen for kulens hastighetvmed ligningenvn+1=vn+h ̇v.(16)2
Deretter løser vi for kulens x posisjon ved å sette verdieneforvvi fant over
inn i ligningenxn+1=xn+hvxn,(17)hvorvxner hastighet i x-retning.
I et gitt punkt(x,y)vildenne komponenten være lik|v|cosα(x)
"""

import numpy as np
import matplotlib as plt

x0=0
y0=1
xf=10
n=101
deltax=(xf-x0)/(n-1)

x=np.linspace(x0,xf,n)

y=np.zeros([n])
y[0]=y0
for i in range  (1,n):
    y[i] = deltax*(-y[i-1] + np.sin(x[i-1])) + y[i-1]

for i in range(n):
    print(x[i],y[i])

plt.plot(x,y,'o')
plt.xlabel("Value of x")
plt.ylabel("Value of y")
plt.title("Approximate solution with Forward Euler's Method")
plt.show()