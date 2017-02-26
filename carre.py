import os
import numpy as np
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt


os.getenv("PORT", "8080")
os.getenv("IP", "0.0.0.0")


carre = [[0,1,1,0,0],[0,0,1,1,0]] # a généraliser encore aux polygones
x_init = np.random.random()
y_init = 0. # départ d'un bord pour raisons d'affichage
V = [(np.random.random(),np.random.random())]
T = [0.0] # ensemble des durées entre deux rebonds consécutifs
Pt_Int = [(x_init,y_init)] # ensemble des points de rebond
grille_finesse = 2**6
Grille = np.ones((grille_finesse,grille_finesse))

i = 0
while i < 100 :
    print(i)
    x = Pt_Int[len(Pt_Int)-1][0]
    y = Pt_Int[len(Pt_Int)-1][1]
    vx = V[len(V)-1][0]
    vy = V[len(V)-1][1]

    I = []
    t_bas = - y/vy
    t_haut = (1. - y)/vy
    t_droit = (1. - x)/vx
    t_gauche = - x/vx
    I = [round(t_haut,14), round(t_gauche,14), round(t_droit,14), round(t_bas,14)]

    I = [l for l in I if l > 0.] ### and 0. <= round(x + t*vx,14) - np.sign(round(x + t*vx,14)) * 10**(-14) <= 1. and 0. <= round(y + t*vy, 14) - np.sign(round(x + t*vx,14)) * 10**(-14) <= 1.]

    print(I)
    t = min(I)
    T.append(t)
    
    for h in range(grille_finesse):
        for j in range(grille_finesse):
            for n in range(grille_finesse):
                k = 1./grille_finesse
                grille_index = (grille_finesse-1-j,h)
                if np.sqrt((x+n*k*t*vx-k*h)**2+(y+n*k*t*vy-k*j)**2) < k/2.:
                    Grille[grille_index] += abs(np.sqrt(8*k**2)*vy/vx*(np.sqrt((x+k*t*vx-k*h)**2+(y+k*t*vy-k*j)**2) - k/2.))
                    #Grille[grille_index] += 1
        

        
    x = x + t*vx
    y = y + t*vy
    Pt_Int.append((abs(round(x,14)),abs(round(y,14))))
    
    if round(x,14) == 1. or round(x,14) == 0.:
        V.append((-vx,vy))
    elif round(y,14) == 1. or round(y,14) == 0.: 
        V.append((vx,-vy))
    else:
        print("There is a problem","\n")
        
    
    i = i+1

#Grille = [np.log(l) for l in Grille]
print(Grille,"\n")



X_pt_int = []
Y_pt_int = []
for i in Pt_Int[:] :
    X_pt_int.append(i[0])
    Y_pt_int.append(i[1])
    
    

plt.plot(carre[0],carre[1], 'k-', X_pt_int, Y_pt_int, 'r-')
plt.savefig('display1.png') # Any filename will do
plt.matshow(Grille, fignum=100, cmap=plt.cm.gray)
plt.axis('off')
plt.savefig('display2.png') # Any filename will do