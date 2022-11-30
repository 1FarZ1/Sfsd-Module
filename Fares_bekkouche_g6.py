from io import BufferedRWPair ## visualize
from pickle import dumps,loads # read and write
from sys import getsizeof # size of element

## vars

global n
## max structures in a single bloc
global maxStructures


global TLname

global TFname

global tnuminscpt

global Taffil 

global Tdelete

delete="0"


global buf

maxStructures = 3

tnuminscpt = 10
TLname = 20
TFname = 20
Taffil = 20
TStudent = tnuminscpt + TLname + TFname + Taffil + Tdelete
TStructure = TStudent * '#'

Tbloc = [0,[TStructure]*maxStructures] #maxStructures = taille max enreg dans un bloc
global blocsize

blocsize = getsizeof(dumps(Tbloc))+len(TStructure)*(maxStructures-1)+(maxStructures-1)

## here we are completing the Strings that arent in same size with maxsize of its field with #
def resize_chaine(chaine, MaxSize):
    for _ in range(len(chaine), MaxSize):
        chaine += '#'
    return chaine

def affecte_entete(file, of, c):
    dp = of * getsizeof(bytes(0))
    file.seek(dp,0)
    file.write(dumps(c)) #convertir c en binaire
    return

def ecrireBloc(file, i, bf):
    dp = 2 * getsizeof(bytes(0)) + i * blocsize
    file.seek(dp,0)
    file.write(dumps(bf)) #convertir bf en binaire
    return 

def lire_bloc(file, i):
    dp = 2 * getsizeof(bytes(0)) + i * blocsize
    file.seek(dp, 0)
    buf = file.read(blocsize)
    return (loads(buf))

def entete(file, of):
    dp = of * getsizeof(bytes(0))
    file.seek(dp, 0)
    c = file.read(getsizeof(bytes(0)))
    return (loads(c))


def Display_Structure(e):
    num = e[0:tnuminscpt].replace('#','')
    Lname1 = e[tnuminscpt:tnuminscpt+TLname].replace('#','')
    Fname1 = e[tnuminscpt+TLname:tnuminscpt+TLname+TFname].replace('#','')
    afill = e[tnuminscpt+TLname+TFname:len(e)-1].replace('#','')
    delete = e[len(e)-1:]
    return (num+' '+Lname1+' '+Fname1+' '+afill+' '+delete)



def CreateFile():
    f=open(fn,"rb")
    ## i and j to itterate over blocs and Structures
    j=0 ## for Structs
    i=0 ## for blocs
    n=0
    
    
    ## table t3 les buffeur nrigliwh
    buf_tab=[TStructure]*maxStructures 
    buf_nb=0 ## initial Number of Structures in The Buffer
    ## try to in case anything happend and error occurred so we can handle it 
    try:
        
        f = open(fn,'wb')
        ans='Y'
        while ans in {'Y', 'y'}:
            print('Student Information')
            
            
            ## Taking Student Details to Store it in Structures
            num=input('Inscription Number :')
            nom=input('Last Name: ')
            prénom=input('First Name: ')
            affiliation=input('affiliation : ')
            
            ## Resizing the Strings to be in same size with their max size
            num=resize_chaine(num,TNum)
            nom=resize_chaine(nom,TLname)
            prénom=resize_chaine(prénom,TFname)
            affiliation=resize_chaine( affiliation,Taffil)
            
            ## Creating the Structure
            etud=num+nom+prénom+affiliation+'0'
            
            ## how many Structures we have 
            n=n+1
            ## nbdaw nktbo fe lbloc 
            if (j<maxStructures):
                buf_tab[j]=etud #putting Structure in the array
                buf_nb=buf_nb+1 #adding the number of Structures we have in the Buffer
                j=j+1 ## moving into the next Bloc
            else:
                # here we finished the buf_array and itterated over all the structures so now we assign it we the nb into the buf in order to write into the MC
                buf=[buf_nb,buf_tab]
                #Writing the Buf in Central Memory
                ecrireBloc(f,i,buf)
                # starting a new buffer array in order to read the next bloc 
                buf_tab=[TStructure]*maxStructures 
                buf_nb=1
                buf_tab[0]=etud
                j=1
                i=i+1
            ans=input('Do You Want To Enter Another Student ? Y/N: ')
        
        buf=[j,buf_tab]
        ecrireBloc(f,i,buf) 
        affecter_entete(f,0,n)
        affecter_entete(f,1,i+1)
        f.close()
    except FileNotFoundError:
        ## incase the file not found
        print('Sorry But The File Was Not Found ')
        

def Display_File():
    f = open(fn, 'rb')
    secondcar = entete(f, 1)
    print(f'your file has {secondcar} blocs \n')
    for i in range (0, secondcar):
        buf = lire_bloc(f, i)
        buf_nb = buf[0]
        buf_tab = buf[1]
        print(f'the content of bloc {i+1} is : \n')
        for j in range(buf_nb):
            print(Display_Structure(buf_tab[j]))
        print('\n')
    f.close()
    return

def Search():
    f = open (fn, 'rb')
    Key = input("Enter the key : ")
    i = 0 ; Found = False
    while (i<entete(f,1) and Found == False):
        buf = lire_bloc(f, i)
        buf_nb = buf[0]
        buf_tab = buf[1]
        j = 0 
        while(j<buf_nb and Found==False):
            if (int(buf_tab[j][0:tnuminscpt].replace('#','')) == int(Key) and buf_tab[j][TStudent-1:] == '0'):
                Found = True
            else:
                j += 1
        if(not Found ):
            i += 1
    if(Found == True):
        liste = [Found,i,j]
    else:
        liste = [Found,0,0]
    f.close()
    return liste


def Insertion():
   
    l = Search()
    Found = l[0] 
    f = open (fn, 'rb+')
    print('Student Informations ')
    num=input('Inscription Number :')
    nom=input('Last Name: ')
    prénom=input('First Name: ')
    affiliation=input('affiliation : ')
            
    num = resize_chaine(num, tnuminscpt)
    nom = resize_chaine(nom, TLname)
    prenom = resize_chaine(prenom, TFname)
    affiliation = resize_chaine(affiliation, Taffil)
    etud = num + nom + prenom + affiliation + efface
    if (Found == False):
        i = entete(f, 1)
        buf = lire_bloc(f,i-1)
        buf_nb = buf[0]
        buf_tab = buf[1]
        if(buf_nb<maxStructures):
            buf_tab[buf_nb] = etud
            buf_nb += 1
            buf = [buf_nb,buf_tab]
            ecrireBloc(f,i-1,buf)
        else: 
            ecrireBloc(f,i-1,buf)
            buf_tab = [TStructure]*maxStructures
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
        print("Student Already exist !")
    f.close()
    return

def LogicallDelete():  

    f = open (fn, 'rb+')
    l = Search()
    Found = l[0] ; i = l[1] ;  j = l[2]
    if (Found == True):
        buf = lire_bloc(f,i)
        buf_nb = buf[0]
        buf_tab = buf[1]
        buf_tab[j] = buf_tab[j][:(TStudent)-2] + '1'
        buf = [buf_nb, buf_tab]
        ecrireBloc(f,i,buf)
    else:
        print("Student Not Found !")
    f.close()
    return

def suppression_physique():         
    l = Search()
    f = open (fn, 'rb+')
    Found = l[0] ; i = l[1] ; j = l[2] 
    if (Found==True):    
        i1 = entete(f,1)
        buf = lire_bloc(f,i1 - 1)
        buf_nb = buf[0]
        buf_tab = buf[1]
        temp = buf_tab[buf_nb - 1]
        buf_tab[buf_nb - 1] = TStudent * '#'
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
        buf_tab[j] = temp
        ecrireBloc(f,i,buf)
    else:
        print("Student Not Found !") 
    f.close()
    return

def default():
    return "Wrong choice"

def choix(ch):
    switcher = {
        1:CreateFile,
        2:Display_File,
        4:Insertion,
        5:LogicallDelete,
        6:suppression_physique
    }
    return switcher.get(ch, default)()

def main():
    ans = 'y'
    while(ans =='Y' or ans =='y'):
        print("""entrez votre choix : 
              1 : créer_fichier
              2 : affichier_fichier
              3 : Search
              4 : Insertion
              5 : Logicall Delete
              6 : suppression_physique""")
        ch = int(input())
        if(ch != 3):
            choix(ch)
        else:
            l = Search()
            print("the existance of the Student : ",l[0])
            print("bloc number : ",l[1]+1)
            print("Position: ",l[2]+1)
        ans = input('do You want other operations ? (Y/N): ')
    return

global fn
fn = input("name of file: ")
main()
        