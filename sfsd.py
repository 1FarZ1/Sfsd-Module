from pickle import dumps, loads ## pickle gives the 2 methodes that help u to write binary (wahda t9ra , wahda tktb)

from sys import getsizeof ## sys gices the methode getSizeOf that gives u the size of the files that u give as parameter 


## Variables

global maxStructures ## Max Structures to be Stored In a Single Bloc 

global TLname ## first field

global TFname ## second field

global tnuminscpt ## third field

global Taffil ## fourth field


## i created a Class To try remove the useless bad implementation of engistrement in python (dedicace el hougra)

# class Etudiant:

#     def __init__(self,tnom,tprénom,tnuminscpt):

#         self._tnom=tnom

#         self._tprénom=tprénom

#         self._tnuminscpt=tnuminscpt

#       # getter method

#     def get_tnom(self):

#         return self.tnom

#     # setter method

#     def set_tnom(self, newValue):

#         self.tnom = newValue

# ilyas=Etudiant("ilyas","brihi","2312172")



## Max Structures of a Bloc

maxStructures = 1

## size of 1st field 

TNum = 10

## size of 2nd field 

TLname = 20

## size of 3rd field 

TFname = 20

## size of 4th field 

Taffil = 20



## size of all the Structure

TStudent = TNum + TLname + TFname + Taffil + 1

## fixing our size of Structure

TStructure = '#' * TStudent


## this is our buffer

global buf



##TODO REMOVE THIS 

# """ 

# Dans  la déclaration on définit le typeBloc Tbloc=[0,[Tnreg]*b]

# le premier élément buf[0] c le buf.NB qui est de type entier initialisé à 0

# le deuxième c'est le tableau d'enregistrement de type enregistrement [Tenreg]*b

# """



## Here we are creating our Bloc with its two fields ->  the first field is the number of Structures that the bloc can Contain|Second is the Structures that we Stored in The Bloc

Tbloc = [maxStructures, [TStructure] * maxStructures]



global blocsize



## this Statement will Calculate the size that will be Occuped by The Bloc

blocsize = getsizeof(dumps(Tbloc)) + len(TStructure) * (maxStructures - 1) + (maxStructures - 1)


# print(Tbloc)




## here we are completing the Strings that arent in same size with maxsize of its field with #
def resize_chaine(chaine, MaxSize):

    for _ in range(len(chaine), MaxSize):

        chaine += '#'

    return chaine


# """ la fonction créer c'est l'algorithme de chargement initial d'un fichier T~OF

#     Dans ce cas les blocs sont remplis à 100% si on veut remplir les blocs avec

#     un % donné, on peut juste envoyer à la fonction créer une variable soit par

#     exemple mu et pour tester le si le bloc est plein, au lieu de faire j<b on fait 

#     si j<b*mu (si on veut remplir les blocs à 50%, mu alors = 0.5 )

# """




def créer_fichier():

    fn=input('Entrer le nom du fichier à créer: ')

    j=0

    i=0

    n=0

    buf_tab=[TStructure]*maxStructures 

    buf_nb=0

    try:

        f = open(fn,'wb')

        rep='O'

        while rep in {'O', 'o'}:

            print('Entrer les information de l\'étudiant: ')

            num=input('Enter le numéro d\'inscription : ')

            nom=input('Enter le nom: ')

            prénom=input('Entrer le prénom: ')

            affiliation=input('Entrer l\'affiliation: ')

            num=resize_chaine(num,TNum)

            nom=resize_chaine(nom,TLname)

            prénom=resize_chaine(prénom,TFname)

            affiliation=resize_chaine( affiliation,Taffil)

            etud=num+nom+prénom+affiliation+'0'

            n=n+1

            if (j<maxStructures):

                buf_tab[j]=etud #mettre l'enregitrement dans le tableau  

                buf_nb=buf_nb+1 #augmenter le buf.NB

                j=j+1

            else:

                # mettre le NB et le tableau d'eregistremnt dans une variable buf 

                buf=[buf_nb,buf_tab]

                #ecrire le buf en mémoire centrale

                ecrireBloc(f,i,buf)

                # rénitialiser le tableau d'enregitrement et le Nb

                buf_tab=[TStructure]*maxStructures 

                buf_nb=1

                buf_tab[0]=etud

                j=1

                i=i+1

            rep=input('Avez vous un autre élement à entrer O/N: ')

        buf=[j,buf_tab]

        ecrireBloc(f,i,buf) 

        affecter_entete(f,0,n)

        affecter_entete(f,1,i+1)

    except FileNotFoundError:

        print('impossible d\'ouvrir le fichier en mode d\'écriture ')

# # ces fonctions sont déja expliquées

# def lireBloc(file, i):

#     dp = 2 * getsizeof(dumps(0)) + i * blocsize

#     file.seek(dp, 0);

#     buf = file.read(blocsize)

#     return (loads(buf))

# def ecrireBloc(file, i, bf):

#     dp = 2 * getsizeof(dumps(0)) + i * blocsize

#     file.seek(dp, 0)

#     file.write(dumps(bf));
#     return

# def affecter_entete(file, of, c):

#     dp = of * getsizeof(dumps(0))

#     file.seek(dp, 0)

#     file.write(dumps(c))
#     return

# def entete(file,offset):

#     dp=offset*getsizeof(dumps(0))

#     file.seek(dp,0)

#     c=file.read(getsizeof(dumps(0)))

#     return loads(c)

# def afficher_fichier():

#     fn=input('Entrer le nom du fichier à afficher: ')

#     try:

#         with open(fn,'rb') as f:

#             secondcar=entete(f,1)  

#             print("""

#             RQ: j'ai choisi d'afficher les fichiers supprimés logiquement

#             pour faire la difference entre eux et les fichiers supprimés physiquement

#             """)

#             print(f'votre fichier contient {secondcar} block ')

#             for i in range (secondcar):

#                 buf=lireBloc(f,i)

#                 buf_nb=buf[0] # recupérer le nb          

#                 buf_tab=buf[1] # recupérer le tableau d'enregitrement

#                 print(f'Le contenu du block {i+1} est:\n' )

#                 # pour chaque enregitrement dans le tableau 

#                 for j in range(buf_nb):

#                     print(afficher_enreg(buf_tab[j]))# afficher l'enregitrement

#                 print('\n')                   

#     except Exception:

#         print("erreur")

# def afficher_enreg(e):

#     # recupérer les champs à partir de chaque enregistrement et remplacer les '#' par un espace

#     num = e[:TNum].replace('#', ' ')

#     nom = e[TNum:TLname].replace('#', ' ')

#     prénom = e[TFname:Taffil].replace('#', ' ')

#     affiliation = e[Taffil:-1].replace('#', ' ')

#     return f'{num} {nom} {prénom} {affiliation} {e[-1]}'

# def recherche(fn,elm):

#     buff = 0

#     i = 0

#     try:

#         with open(fn,'rb') as f:

#             nb = entete(f,1)

#             t = False

#             while i < nb and not t: 

#                 buff = lireBloc(f,i)

#                 for j in range(maxStructures):

#                     if buff[1][j][:TNum].replace('#','') == elm:

#                         t = True

#                         print(f"l'element ce trouve dans le bloc {i+1} et l'enregistrement {j+1}")

#                         return (i+1,j+1)

#                 i += 1

#             if not t:

#                 print("l'element doit etre inseree")

#     except Exception:
#         print('erreur')
    

# def insertion(fn):

#     try:

#         with open(fn,'r+b') as f:

#             print('Entrer les information de l\'étudiant: ')

#             num = input('Enter le numéro d\'inscription : ')

#             nom = input('Enter le nom: ')

#             prénom = input('Entrer le prénom: ')

#             affiliation = input('Entrer l\'affiliation: ')

#             num = resize_chaine(num, TNum)

#             nom = resize_chaine(nom, TLname)

#             prénom = resize_chaine(prénom, TFname)

#             affiliation = resize_chaine(affiliation, Taffil)

#             etud = num + nom + prénom + affiliation + '0'

#             nb = entete(f,1)

#             buff = lireBloc(f,nb-1)

#             plein = True

#             for j in range(maxStructures):

#                 if buff[1][j][:TNum].replace('#','') == '':

#                     buff[0] += 1

#                     affecter_entete(f,0,entete(f,0)+1)

#                     buff[1][j] = etud

#                     ecrireBloc(f,nb-1,buff)

#                     plein = False

#             if plein:

#                 buff = Tbloc

#                 buff[0] +=1

#                 buff[1][0] = etud

#                 ecrireBloc(f,nb,buff)

#                 affecter_entete(f,0,entete(f,0)+1)

#                 affecter_entete(f,1,entete(f,1)+1)

#     except Exception:
#         print('error')

# def supression_logique():

#     fn = input('entrez dans quelle fichier vous voulez supprimer logiquement: ')

#     m = input('entrez le matricule que vous voulez supprimer logiquement: ') 

#     try:

#         with open(fn,'r+b') as f:

#             if pos := recherche(fn,m):

#                 i,j = pos[0]-1,pos[1]-1

#                 buff = lireBloc(f,i)

#                 buff[1][j] = f'{buff[1][j][:-1]}1'

#                 ecrireBloc(f,i,buff)

#                 print("l'element a ete supprimer logiquement")

#     except FileNotFoundError:

#         print('file not found')

# def supression_physique():

#     fn = input('entrez dans quelle fichier vous voulez supprimer physiquement: ')

#     m = input('entrez le matricule que vous voulez supprimer physiquement: ') 

#     try:

#         with open(fn,"r+b") as f:

#             nb = entete(f,1)

#             if pos := recherche(fn,m):

#                 i,j = pos[0]-1,pos[1]-1

#                 while i < nb:

#                     if i != nb-1:

#                         buff = lireBloc(f,i)

#                         buff2 = lireBloc(f,i+1)

#                         while j<maxStructures:

#                             if j+1 != maxStructures:

#                                 buff[1][j] = buff[1][j+1]

#                                 # print(f"buff 1{str(buff)}")

#                             else:

#                                 buff[1][j] = buff2[1][0]  

#                                 # print(f"buff 2{str(buff)}")

#                                 # print("buff1"+str(i))

#                                 ecrireBloc(f,i,buff)

#                             j += 1

#                         j = 0

#                     else:

#                         buff = lireBloc(f,i)

#                         while j<maxStructures:

#                             if j+1 != maxStructures:

#                                 buff[1][j] = buff[1][j+1]

#                                 buff[1][j+1] = TStructure

#                                 buff[0] -= 1

#                                 # print("last"+str(i))

#                                 # print(f'last {buff}')

#                                 if buff[1][0].replace('#','') == '':

#                                     affecter_entete(f,1,entete(f,1)-1)

#                                 else:

#                                     ecrireBloc(f,i,buff)

#                             else:

#                                 buff[1][j] = TStructure

#                                 ecrireBloc(f,i,buff)

#                             j+=1

#                     i += 1

#     except FileNotFoundError:

#         print("file not found")

# def fragmentation():

#     fn = input('choisir dans quel fichier vous voulez fragmenter: ')

#     c1 = int(input('entrez la premiere cle: '))

#     c2 = int(input('entrez la deuxieme cle: '))

#     try:

#         with open(fn,'r+b') as f:

#             f1,f2,f3 = open(f'{fn}1','wb'), open(f'{fn}2','wb'),open(f'{fn}3','wb')

#             nb,n1,n2,n3 = entete(f,1),0,0,0

#             i,j = 0,0

#             i1,j1,buff1 = 0,0,[0, [TStructure] * maxStructures]

#             i2,j2,buff2 = 0,0,[0, [TStructure] * maxStructures]

#             i3,j3,buff3 = 0,0,[0, [TStructure] * maxStructures]

#             while i < nb:

#                 buff = lireBloc(f,i)

#                 for j in range(maxStructures):
                    

#                     if buff[1][j].replace('#','') != '':

#                         if int(buff[1][j][:TNum].replace('#','')) < c1:

#                             n1 += 1

#                             if j1 < maxStructures:

#                                 buff1[0] += 1

#                                 buff1[1][j1] = buff[1][j]                   

#                                 j1 += 1

#                             else: 

#                                 ecrireBloc(f1,i1,buff1)  

#                                 i1 += 1

#                                 buff1 = [0, [TStructure] * maxStructures]

#                                 buff1[0] += 1

#                                 buff1[1][0] = buff[1][j]  

#                                 j1 = 1   
                                

#                         elif int(buff[1][j][:TNum].replace('#','')) >= c1 and int(buff[1][j][:TNum].replace('#','')) < c2:

#                             n2 += 1

#                             if j2 < maxStructures:

#                                 buff2[0] += 1

#                                 buff2[1][j2] = buff[1][j]               

#                                 j2 += 1 

#                             else:   

#                                 ecrireBloc(f2,i2,buff2)

#                                 i2 += 1

#                                 buff2 = [0, [TStructure] * maxStructures]

#                                 buff2[0] += 1

#                                 buff2[1][0] = buff[1][j]  

#                                 j2 = 1                        

#                         elif int(buff[1][j][:TNum].replace('#','')) > c2:

#                             n3 += 1

#                             if j3 < maxStructures:

#                                 buff3[0] += 1

#                                 buff3[1][j3] = buff[1][j]

#                                 j3 += 1       

#                             else:   

#                                 ecrireBloc(f3,i3,buff3)

#                                 i3 += 1

#                                 buff3 = [0, [TStructure] * maxStructures]

#                                 buff3[0] += 1

#                                 buff3[1][0] = buff[1][j]  

#                                 j3 = 1                                                      

#                 i +=1

#             ecrireBloc(f1,i1,buff1)

#             ecrireBloc(f2,i2,buff2)

#             ecrireBloc(f3,i3,buff3)

#             affecter_entete(f1,1,i1+1)

#             affecter_entete(f2,1,i2+1)

#             affecter_entete(f3,1,i3+1)

#             affecter_entete(f1,0,n1)

#             affecter_entete(f2,0,n2)

#             affecter_entete(f3,0,n3)

#             f1.close

#             f2.close

#             f3.close

#     except FileNotFoundError:

#         print('file not found')

# def default():

#     return "choix invalid"

# def choix(ch):

#     switcher = {

#         1: créer_fichier,

#         2: afficher_fichier,

#         3: recherche,

#         4: insertion,

#         5: supression_logique,

#         6: supression_physique,

#         7: fragmentation

#     }

#     if ch not in [4,3]:

#         return switcher.get(ch, default)()

#     if ch == 3:

#         fn = input('choisir quel fichier rechercher: ')

#         m = input('entrez le matricule que vous voulez rechercher: ')

#         recherche(fn,m)

#     else:

#         fn = input('choisir dans quel fichier vous voulez inserer un nouvel element: ')
#         insertion(fn) 

# def main():

#     rep = 'O'

#     while (rep == 'O'):

#         print("""Entrer votre choix 

#                  1: créer_fichier

#                  2: afficher_fichier

#                  3: rechercher un element

#                  4: inserer un element

#                  5: supression_logique

#                  6: supression_physique

#                  7: fragmentation""")                

#         ch = int(input())

#         choix(ch)

#         rep = input('Avez vous une autre opération O/N? ')
# main()