import numpy as np
import matplotlib.pyplot as plt

alpha = 1+np.sqrt(5)
x = 0.
y = 0.6
x_0 = x
y_0 = y
k = 6000
j = 0
N = 500 #nombre de pixels
P=[(x,y)]
n = 0
m = 0
x_1 = 0
y_1 = 0
indice = 0
"""""""""""Definition de la matrice"""""""""""
A = np.zeros((N, N), dtype='f')
"""""""Calcul de la trajectoire"""""""""
for i in range(k):
    if(alpha==np.pi or alpha==0):
        x=x+np.cos(alpha)
        P.append((x,y))
        alpha=np.pi-alpha
        j = 1
    elif(alpha==np.pi/2 or alpha==3*np.pi/2):
        y=y+np.sin(alpha)
        P.append((x,y))
        alpha=-alpha
        j = 1
    if (x-y/np.tan(alpha)>0 and x-y/np.tan(alpha)<1 and x-y/np.tan(alpha)!=x and j!=1):
        x=x-y/np.tan(alpha)
        y=0
        alpha=-alpha
    elif (y-x*np.tan(alpha)>0 and y-x*np.tan(alpha)<1 and y-x*np.tan(alpha)!=y and j!=1):
        y=y-x*np.tan(alpha)
        x=0
        if (alpha>=0):
            alpha=np.pi-alpha
        else:
            alpha=-np.pi-alpha
    elif (x+(1-y)/np.tan(alpha)>0 and x+(1-y)/np.tan(alpha)<1 and x+(1-y)/np.tan(alpha)!=x and i!=1):
        x=x+(1-y)/np.tan(alpha)
        y=1
        alpha=-alpha
    elif (y+(1-x)*np.tan(alpha)>0 and y+(1-x)*np.tan(alpha)<1 and y+(1-x)*np.tan(alpha)!=y and i!=1):
        y=y+(1-x)*np.tan(alpha)
        x=1
        if alpha>=0:
            alpha=np.pi-alpha
        else:
            alpha=-np.pi-alpha
    """"Calcul de la repartition"""
    l = abs(int(x*N)-int(x_0*N)) #nbre de verticales
    o = abs(int(y*N)-int(y_0*N)) #nbre d'horizontales
    a = (y-y_0)/float((x-x_0))
    b = y_0 -a*x_0
    if (int(y*N)!=int(y_0*N) and int(x*N)==int(x_0*N)): #solutions suivant les horizontales
        Sol = [[0,0,0] for u in range(o)]
        if(y>y_0):
            for h in range(o):
                y_1 = (int(y_0*N)+h+1)/float(N)
                x_1 = 1/a*(y_1-b)
                Sol[h][0]=x_1
                Sol[h][1]=y_1
                Sol[h][2]=(x_1-x_0)**2+(y_1-y_0)**2 #distance au carre pour les arrondis
        else:
            for h in range(o):
                y_1 = (int(y_0*N)-h)/float(N)
                x_1 = 1/a*(y_1-b)
                Sol[h][0]=x_1
                Sol[h][1]=y_1
                Sol[h][2]=(x_1-x_0)**2+(y_1-y_0)**2
        mini=0
        for h in range(o):
            li=[Sol[u][2] for u in range(len(Sol))]
            indice=li.index(min(li))
            n=int(Sol[indice][1]*N)
            if n==N:
                n=N-1
            m=int(Sol[indice][0]*N)
            if m==N:
                m=N-1
            A[N-1-n][m]=A[N-1-n][m]+np.sqrt(Sol[indice][2])-np.sqrt(mini)
            mini=Sol[indice][2]
            del(Sol[indice])#a refaire, c'est faux
    
    elif(int(y*N)==int(y_0*N) and int(x*N!=x_0*N)): #solutions suivant les verticales
        Sol = [[0,0,0] for u in range(l)]        
        if(x>x_0):
            for h in range(l):
                x_1 = (int(x_0*N)+1+h)/float(N)
                y_1 = a*x_1 + b
                Sol[h][0]=x_1
                Sol[h][1]=y_1
                Sol[h][2]=(x_1-x_0)**2+(y_1-y_0)**2
        else:
            for h in range(l):
                x_1 = (int(N*x_0)-h)/float(N)
                y_1 = a*x_1 + b
                Sol[h][0]=x_1
                Sol[h][1]=y_1
                Sol[h][2]=(x_1-x_0)**2+(y_1-y_0)**2
        mini=0
        for h in range(l):
            li=[Sol[u][2] for u in range(len(Sol))]
            indice=li.index(min(li))
            n=int(Sol[indice][1]*N)
            if n==N:
                n=N-1
            m=int(Sol[indice][0]*N)
            if m==N:
                m=N-1
            A[N-1-n][m]=A[N-1-n][m]+np.sqrt(Sol[indice][2])-np.sqrt(mini)
            mini=Sol[indice][2]
            del(Sol[indice])
    
    elif(int(y*N)!=int(y_0*N) and int(x*N)!=int(x_0*N)): #solutions suivant les verticales et horizontales
        Sol = [[0,0,0] for u in range(o+l)]        
        for h in range(o):
            if(y>y_0):
                y_1 = (int(y_0*N)+1+h)/float(N)
                x_1 = 1/a*(y_1-b)
                Sol[h][0]=x_1
                Sol[h][1]=y_1
                Sol[h][2]=(x_1-x_0)**2+(y_1-y_0)**2
            elif(y<=y_0):
                y_1 = (int(y_0*N)-h)/float(N)
                x_1 = 1/a*(y_1-b)
                Sol[h][0]=x_1
                Sol[h][1]=y_1
                Sol[h][2]=(x_1-x_0)**2+(y_1-y_0)**2
        for h in range(o,o+l,1):
            if(x>x_0):
                x_1 = (int(x_0*N)+1+h-o)/float(N)
                y_1 = a*x_1 + b
                Sol[h][0]=x_1
                Sol[h][1]=y_1
                Sol[h][2]=(x_1-x_0)**2+(y_1-y_0)**2
            elif(x<=x_0):
                x_1 = (int(N*x_0)-h+o)/float(N)
                y_1 = a*x_1 + b
                Sol[h][0]=x_1
                Sol[h][1]=y_1
                Sol[h][2]=(x_1-x_0)**2+(y_1-y_0)**2
        mini=0
        for h in range(o+l):
            li=[Sol[u][2] for u in range(len(Sol))]
            indice=li.index(min(li))
            n=int(Sol[indice][1]*N)
            if n==N:
                n=N-1
            m=int(Sol[indice][0]*N)
            if m==N:
                m=N-1
            A[N-1-n][m]=A[N-1-n][m]+np.sqrt(Sol[indice][2])-np.sqrt(mini)
            mini=Sol[indice][2]
            del(Sol[indice])
        
    x_0 = x
    y_0 = y            
    """else:
        return 'la boule est hors-jeu'"""
    P.append((x,y))

im1 = plt.matshow(A)
plt.colorbar(im1)
plt.show()