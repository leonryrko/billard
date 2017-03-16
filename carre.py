import os
import numpy as np
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt


os.getenv("PORT", "8080")
os.getenv("IP", "0.0.0.0")


carre = [[0,1,1,0,0],[0,0,1,1,0]] # a généraliser encore aux polygones
x = np.random.random()
y = 0. # départ d'un bord pour raisons d'affichage
V = [(np.random.random(),np.random.random())]
T = [0.0] # ensemble des durées entre deux rebonds consécutifs
Pt_Int = [(x,y)] # ensemble des points de rebond
grille_finesse = 2**6
Grille = np.zeros((grille_finesse,grille_finesse))
Somme = []


i = 0
while i < 10 :
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
    
    #repartition
    for col in range(grille_finesse):
        for rng in range(grille_finesse):
            for n in range(grille_finesse):
                k = 1./grille_finesse
                grille_index = (grille_finesse-1-rng,col)
                if np.sqrt((x+n*k*t*vx-k*col)**2+(y+n*k*t*vy-k*rng)**2) < k/2.:
                    #Grille[grille_index] += abs(np.sqrt((x+k*vx-k*col)**2+(y+k*vy-k*rng)**2))
                    #Grille[grille_index] += 1
                    Grille[grille_index] += abs(vy/vx)*k
         

        
    x = x + t*vx
    y = y + t*vy
    Pt_Int.append((abs(round(x,14)),abs(round(y,14))))
    
    if round(x,14) == 1. or round(x,14) == 0.:
        V.append((-vx,vy))
    elif round(y,14) == 1. or round(y,14) == 0.: 
        V.append((vx,-vy))
    else:
        print("There is a problem","\n")
        
    #equirepartition
    somme = 0.
    for g in Grille:
        for k in g:
            #print(type(g), type(k))
            somme += np.abs(k*(grille_finesse^2) - np.sum(Grille))
            #print(somme)
    Somme.append(somme/(np.sum(Grille)*float(4^grille_finesse)))
    #print(np.sum(somme)/np.sum(Grille)/float(grille_finesse^2))
        
    
    i = i+1


Grille = Grille + np.ones((grille_finesse,grille_finesse))
#Grille = [np.log(l) for l in Grille]
print(Grille,"\n")



X_pt_int = []
Y_pt_int = []
for i in Pt_Int[:] :
    X_pt_int.append(i[0])
    Y_pt_int.append(i[1])
    
print(Somme, type(Somme), max(Somme))    

plt.plot(carre[0],carre[1], 'k-', X_pt_int, Y_pt_int, 'r-')
plt.savefig('display1.png') # Any filename will do
plt.matshow(Grille, fignum=100, cmap=plt.cm.gray)
plt.axis('off')
plt.savefig('display2.png') # Any filename will do
plt.clf()
plt.plot(range(len(Somme)),Somme,'ko')
plt.axis([0, len(Somme), 0, int(max(Somme))+1])
plt.savefig('display3.png')