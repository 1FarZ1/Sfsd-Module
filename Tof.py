from io import BufferedRWPair
from pickle import dumps,loads
from sys import getsizeof


global n
global b
global tnom
global tprenom
global tnum
global taffiliation 
global tefface

b = 3
tefface = 1
efface = '0'
tnum = 10
tnom = 20
tprenom = 20
taffiliation = 20
tetud = tnum + tnom + tprenom + taffiliation + tefface
tnreg = tetud * '#'
global buf
tbloc = [0,[tnreg]*b] #b = taille max enreg dans un bloc
global blocsize
blocsize = getsizeof(dumps(tbloc))+len(tnreg)*(b-1)+(b-1)

def resize_chaine(chaine, maxtaille):
    for i in range (len(chaine), maxtaille):
        chaine = chaine + '#'
    return chaine 

def creer_fichier():
    j = 0 ; i = 0 ; n = 0
    buf_tab = [tnreg]*b
    buf_nb = 0
    try :
        f= open(fn, 'wb')
    except:
        print("impossible d\'ouvrir le fichier en mode d\'écriture")
    rep = 'O'
    while(rep == 'o' or rep =='O'):
        print("entrez les informations de l\'étudiant : ")
        num = input("entrez le numéro d\'inscription : ")
        nom = input("entrez le nom : ")
        prenom = input("entrez le  prenom : ")
        affiliation = input("entrez l\'affiliation : ")
        num = resize_chaine(num, tnum)
        nom = resize_chaine(nom, tnom)
        prenom = resize_chaine(prenom, tprenom)
        affiliation = resize_chaine(affiliation, taffiliation)
        etud = num + nom + prenom + affiliation + efface
        n = n + 1 # n = nombre max des enreg dans le fichier
        if(j<b):
            buf_tab[j]=etud
            buf_nb += 1
            j += 1
        else:
            buf = [buf_nb, buf_tab]
            ecrireBloc(f, i, buf)
            buf_tab = [tnreg]*b
            buf_nb = 1
            buf_tab[0] = etud
            j = 1 
            i += 1
        rep = input("avez vous un autre element a entrer (O/N) : ")
    buf =[j, buf_tab]
    ecrireBloc(f, i, buf) 
    affecte_entete(f, 0, n)           
    affecte_entete(f, 1, i+1)
    f.close()
    return
        
def affecte_entete(f, of, c):
    dp = of * getsizeof(bytes(0))
    f.seek(dp,0)
    f.write(dumps(c)) #convertir c en binaire
    return

def ecrireBloc(f, i, bf):
    dp = 2 * getsizeof(bytes(0)) + i * blocsize
    f.seek(dp,0)
    f.write(dumps(bf)) #convertir bf en binaire
    return 

def lire_bloc(f, i):
    dp = 2 * getsizeof(bytes(0)) + i * blocsize
    f.seek(dp, 0)
    buf = f.read(blocsize)
    return (loads(buf))

def entete(f, of):
    dp = of * getsizeof(bytes(0))
    f.seek(dp, 0)
    c = f.read(getsizeof(bytes(0)))
    return (loads(c))

def affichage():
    f = open(fn, 'rb')
    secondcar = entete(f, 1)
    print(f'votre fichier contient {secondcar} block \n')
    for i in range (0, secondcar):
        buf = lire_bloc(f, i)
        buf_nb = buf[0]
        buf_tab = buf[1]
        print(f'le contenu du block {i+1} est : \n')
        for j in range(buf_nb):
            print(afficher_enreg(buf_tab[j]))
        print('\n')
    f.close()
    return

def afficher_enreg(e):
    num = e[0:tnum].replace('#','')
    nom = e[tnum:tnum+tnom].replace('#','')
    prenom = e[tnum+tnom:tnum+tnom+tprenom].replace('#','')
    affiliation = e[tnum+tnom+tprenom:len(e)-1].replace('#','')
    efface = e[len(e)-1:]
    return (num+' '+nom+' '+prenom+' '+affiliation+' '+efface)

def recherche():
    f = open (fn, 'rb')
    cle = input("entrez la clé : ")
    i = 0 ; trouv = False
    while (i<entete(f,1) and trouv == False):
        buf = lire_bloc(f, i)
        buf_nb = buf[0]
        buf_tab = buf[1]
        j = 0 
        while(j<buf_nb and trouv==False):
            if (int(buf_tab[j][0:tnum].replace('#','')) == int(cle) and buf_tab[j][tetud-1:] == '0'):
                trouv = True
            else:
                j += 1
        if(not trouv ):
            i += 1
    if(trouv == True):
        liste = [trouv,i,j]
    else:
        liste = [trouv,0,0]
    f.close()
    return liste

def insertion():
    print("<-- L'insertion d'un élement -->")
    l = recherche()
    trouv = l[0] 
    f = open (fn, 'rb+')
    print("entrez les informations de l\'étudiant pour l'insertion : ")
    num = input("entrez le numéro d\'inscription : ")
    nom = input("entrez le nom : ")
    prenom = input("entrez le  prenom : ")
    affiliation = input("entrez l\'affiliation : ")
    num = resize_chaine(num, tnum)
    nom = resize_chaine(nom, tnom)
    prenom = resize_chaine(prenom, tprenom)
    affiliation = resize_chaine(affiliation, taffiliation)
    etud = num + nom + prenom + affiliation + efface
    if (trouv == False):
        i = entete(f, 1)
        buf = lire_bloc(f,i-1)
        buf_nb = buf[0]
        buf_tab = buf[1]
        if(buf_nb<b):
            buf_tab[buf_nb] = etud
            buf_nb += 1
            buf = [buf_nb,buf_tab]
            ecrireBloc(f,i-1,buf)
        else: 
            ecrireBloc(f,i-1,buf)
            buf_tab = [tnreg]*b
            buf_nb = 0
            buf_tab[0] = etud
            buf_nb += 1
            buf = [buf_nb,buf_tab]
            affecte_entete(f, 1, i+1)
            ecrireBloc(f, i, buf)        
        n = entete(f, 0)
        n += 1 
        affecte_entete(f, 0, n) 
    else :
        print("L'élément existe déjà !")
    f.close()
    return

def suppression_logique():  
    print("<-- suppression logique d'un élement -->")       
    f = open (fn, 'rb+')
    l = recherche()
    trouv = l[0] ; i = l[1] ;  j = l[2]
    if (trouv == True):
        buf = lire_bloc(f,i)
        buf_nb = buf[0]
        buf_tab = buf[1]
        buf_tab[j] = buf_tab[j][:(tetud)-2] + '1'
        buf = [buf_nb, buf_tab]
        ecrireBloc(f,i,buf)
    else:
        print("L'élement n\'existe pas !")
    f.close()
    return

def suppression_physique():        
    print("<-- suppression physique d'un élement -->")    
    l = recherche()
    f = open (fn, 'rb+')
    trouv = l[0] ; i = l[1] ; j = l[2] 
    if (trouv==True):    
        i1 = entete(f,1)
        buf = lire_bloc(f,i1 - 1)
        buf_nb = buf[0]
        buf_tab = buf[1]
        enreg_tmp = buf_tab[buf_nb - 1]
        buf_tab[buf_nb - 1] = tetud * '#'
        buf_nb -= 1
        if (buf_nb == 0):
            i1 -= 1
            affecte_entete(f,1,i1)
        else : 
            buf = [buf_nb,buf_tab]
            ecrireBloc(f,i1-1,buf)
        buf = lire_bloc(f,i)
        buf_nb = buf[0]
        buf_tab = buf[1]
        buf_tab[j] = enreg_tmp
        ecrireBloc(f,i,buf)
    else:
        print("L\'element n\'existe pas !") 
    f.close()
    return

def default():
    return "choix invalid"

def choix(ch):
    switcher = {
        1:creer_fichier,
        2:affichage,
        4:insertion,
        5:suppression_logique,
        6:suppression_physique
    }
    return switcher.get(ch, default)()

def main():
    rep = 'O'
    while(rep =='O' or rep =='o'):
        print("""entrez votre choix : 
              1 : créer_fichier
              2 : affichier_fichier
              3 : recherche
              4 : insertion
              5 : suppression_logique
              6 : suppression_physique""")
        ch = int(input())
        if(ch != 3):
            choix(ch)
        else:
            print("<-- recherche d'un clé -->")
            l = recherche()
            print("L'existance de L'élément : ",l[0])
            print("Bloc numéro : ",l[1]+1)
            print("La position dans le bloc : ",l[2]+1)
        rep = input('avez vous une autre operation (O/N): ')
    return

global fn
#fn = input("entrez le nom du fichier : ")
fn = 'FichierTNOF.txt'
main()
        