import os
import numpy as np
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt


def polyretour(l,x,y,vd,N,eps=10**(-14)):
    Traj=[[0,(x,vd[0]),(y,vd[1])]]
    L=[[l[i]]+[(l[i+1][0]-l[i][0],l[i+1][1]-l[i][1])]+[l[i+1]] for i in range(len(l)-1)]
    L.append([l[-1]]+[(l[0][0]-l[-1][0],l[0][1]-l[-1][1])]+[l[0]])
    for k in range(N):
        T=[]
        for i in range(len(l)):
            x1=float(L[i][1][0])
            x2=float(L[i][1][1])
            if x1*vd[1]-x2*vd[0]!=0:
                x3=x2*L[i][0][0]-x1*L[i][0][1]
                t=(x3-x2*x+x1*y)/(x2*vd[0]-x1*vd[1])
                T.append((t,i))
        Tf=[(t,i) for (t,i) in T if t>eps
            and (vd[0]*t+x-L[i][0][0])*(vd[0]*t+x-L[i][2][0])+(vd[1]*t+y-L[i][0][1])*(vd[1]*t+y-L[i][2][1])<0]
        Tm=[Tf[i][0] for i in range(len(Tf))]
        t=min(Tm)
        i=Tf[Tm.index(t)][1]
        x=vd[0]*t+x
        y=vd[1]*t+y
        x1=float(L[i][1][0])
        x2=float(L[i][1][1])
        a=(x1**2-x2**2)/(x1**2+x2**2)
        b=2*x1*x2/(x1**2+x2**2)
        R=np.array([[a,b],[b,-a]])
        V=np.array(vd)
        if (x,y) in l:
            return 'la boule est hors-jeu'
        else:
            vd=np.dot(R,V)
            vd=vd.tolist()
            Traj.append([t,(x,vd[0]),(y,vd[1])])
    return Traj

def repartlong(n,l,x,y,vd,N,eps=10**(-14)):
    T = polyretour(l,x,y,vd,N,eps=10**(-14))
    M = np.zeros((2**n,2**n))
    
    for k in range(len(T)-1):
        x1,y1,x2,y2,v=T[k][1][0],T[k][2][0],\
                       T[k+1][1][0],T[k+1][2][0],\
                       [T[k][1][1],T[k][2][1]]
        I=[(round(x1,14),round(y1,14)),(round(x2,14),round(y2,14))]
        i=int(2**n*x1)
        j=int(2**n*x2)
        mi,ma=min(i,j),max(i,j)
        ab=range(mi+1,ma+1) 
    
    #vd1!=0 et vd2!=0 sinon trivial
        I=I+[(o/2.0**n,round(y1+(o/2.0**n-x1)*v[1]/v[0],14)) for o in ab]
        i=int(2**n*y1)
        j=int(2**n*y2)
        mi,ma=min(i,j),max(i,j)
        ordo=range(mi+1,ma+1)
        I=I+[(round(x1+(o/2.0**n-y1)*v[0]/v[1],14),o/2.0**n) for o in ordo]
        I=set(I)
        I=list(I)
        I.sort()
        for k2 in range(len(I)-1):
            d=np.sqrt((I[k2+1][0]-I[k2][0])**2+(I[k2+1][1]-I[k2][1])**2)
            (xm,ym)=((I[k2+1][0]+I[k2][0])/2.0,(I[k2+1][1]+I[k2][1])/2.0)
            j,i=int(2**n*xm),int(2**n*ym)
            M[2**n-1-i,j] = M[2**n-1-i,j] + d
            print(M[2**n-1-i,j])
            
    return M
    
def repartretour(n,l,x,y,vd,N,eps=10**(-14)):
    T=polyretour(l,x,y,vd,N,eps)
    M=np.zeros((2**n,2**n))
    for k in range(len(T)-1):
        x1,y1,x2,y2,v=T[k][1][0],T[k][2][0],\
                       T[k+1][1][0],T[k+1][2][0],\
                       [T[k][1][1],T[k][2][1]]
        I=[(round(x1,14),round(y1,14)),(round(x2,14),round(y2,14))]
        i=int(2**n*x1)
        j=int(2**n*x2)
        mi,ma=min(i,j),max(i,j)
        ab=range(mi+1,ma+1)
#vd1!=0 et vd2!=0 sinon trivial
        I=I+[(o/2.0**n,round(y1+(o/2.0**n-x1)*v[1]/v[0],14)) for o in ab]
        i=int(2**n*y1)
        j=int(2**n*y2)
        mi,ma=min(i,j),max(i,j)
        ordo=range(mi+1,ma+1)
        I=I+[(round(x1+(o/2.0**n-y1)*v[0]/v[1],14),o/2.0**n) for o in ordo]
        I=set(I)
        I=list(I)
        I.sort()
        for k2 in range(len(I)-1):
            d=np.sqrt((I[k2+1][0]-I[k2][0])**2+(I[k2+1][1]-I[k2][1])**2)
            (xm,ym)=((I[k2+1][0]+I[k2][0])/2.0,(I[k2+1][1]+I[k2][1])/2.0)
            j,i=int(2**n*xm),int(2**n*ym)
            if j==2**n:
                j=j-1                
            M[2**n-1-i,j]=M[2**n-1-i,j]+d
    return M
    
def numeri(n,l,x,y,vd,N,eps=10**(-14)):
    M=repartretour(n,l,x,y,vd,N,eps)
    M=M.tolist()
    S=sum([ sum (j) for j in M ])
    d=0
    for i in M :
        for j in i :
            d+=np.abs(4**n*j - S)
    return d/(S*4.0**n)

#entree = input('n,x,y,vd,N?')
#n,x,y,vd,N = entree.split(';')
#N = int(N)
#n = int(n)
#x = float(x)
#y = float(y)
#vx,vy = vd.split(',')
#vx = float(vx)
#vy = float(vy)
#vd = (vx,vy)
n = 7
N = 100
x = 0.
y = 0.3
vd = [4,2]
l = [(0,0),(0,1),(1,1),(1,0),(0,0)]


densite = repartlong(n,l,x,y,vd,N,eps=10**(-14))

plt.matshow(densite)
#plt.colorbar()
plt.savefig('coralie.png')
print(densite, type(densite))