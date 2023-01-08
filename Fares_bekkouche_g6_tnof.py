from pickle import dumps, loads ## pickle gives the 2 methodes that help u to write binary (wahda t9ra , wahda tktb)
from sys import getsizeof ## sys gices the methode getSizeOf that gives u the size of the files that u give as parameter 

## Variables
global maxStructures ## Max Structures to be Stored In a Single Bloc 
global TLname ## first field
global TFname ## second field
global tnuminscpt ## third field
global Taffil ## fourth field


## Max Structures of a Bloc
maxStructures = 8
## max size of 1st field 
TNum = 10
## max size of 2nd field 
TLname = 20
## max size of 3rd field 
TFname = 20
## max size of 4th field 
Taffil = 20
## max size of all the Structure
TStudent = TNum + TLname + TFname + Taffil + 1
## fixing our size of Structure
TStructure = '#' * TStudent
## this is our buffer
global buf
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
## this A Function to charge our File With Starting Data , it depend on the percentage that we want to fill with and how to
##TNOF
def CreateFile():
    fn=input('Enter The Name of The File :')
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
    except FileNotFoundError:
        ## incase the file not found
        print('Sorry But The File Was Not Found ')
        
        
def lireBloc(file, i):
    dp = 2 * getsizeof(dumps(0)) + i * blocsize
    file.seek(dp, 0);
    buf = file.read(blocsize)
    return (loads(buf))
def ecrireBloc(file, i, bf):
    dp = 2 * getsizeof(dumps(0)) + i * blocsize
    file.seek(dp, 0)
    file.write(dumps(bf));
    return
def affecter_entete(file, of, c):
    dp = of * getsizeof(dumps(0))
    file.seek(dp, 0)
    file.write(dumps(c))
    return
def entete(file,offset):
    dp=offset*getsizeof(dumps(0))
    file.seek(dp,0)
    c=file.read(getsizeof(dumps(0)))
    return loads(c)
##  here we go block by block and display the content of each structure in the bloc
def Display_File():
    fn=input('Entrer The Name of File To Display')
    ## another Try in case anything happend
    try:
     with open(fn,'rb') as f:
            
            ## the second characeterize(how many blocks are in the file)
            secondcar=entete(f,1)  
            print(f'Your file has {secondcar} blocks ')
            for i in range (secondcar):
                buf=lireBloc(f,i)
                buf_nb=buf[0] # getting the NB(number of structurs in the bloc)     
                buf_tab=buf[1] # getting the structures 
                print(f'The content of block({i+1}) :\n' )
                # for each Structures we had in the array
                for j in range(buf_nb):
                    print(Display_Structure(buf_tab[j]))# afficher l'enregitrement
                print('\n')                   
    except Exception:
        print("An Error has Happend")
        
## here we are displaying the Structure by slicing the desired value we want 
def Display_Structure(Structure):
    num = Structure[:TNum].replace('#', ' ')
    nom = Structure[TNum:TLname].replace('#', ' ')
    prénom = Structure[TFname:Taffil].replace('#', ' ')
    affiliation = Structure[Taffil:-1].replace('#', ' ')
 
    return f'{num} {nom} {prénom} {affiliation} {Structure[-1]}'
## A Function To Search A  particular Element with 
def Search(fn,Key):
    buff = 0
    i = 0
    try:
        with open(fn,'rb') as f:
            nb = entete(f,1)
            Found = False
            while i < nb and not Found: 
                buff = lireBloc(f,i)
                for j in range(maxStructures):
                    if buff[1][j][:TNum].replace('#','') == Key:
                        Found = True
                        print(f"Elemenet Found  in Bloc({i+1}) and Structure({j+1})")
                        print(buff[1][j][TFname:Taffil].replace("#",""))
                        ## Returning The index of Elemenet
                        return (i+1,j+1)
                i += 1
            if not Found:
                print("Element Not Found")
    except Exception:
        print('Error Found')
    
def insertion(fn):
    ## Error Handling
    try:
        ## Opening the file in read and write mode
        with open(fn,'r+b') as f:
            print('Student Informations ')
            num=input('Inscription Number :')
            nom=input('Last Name: ')
            prénom=input('First Name: ')
            affiliation=input('affiliation : ')
            
            ## Resizing the Strings to the max Size
            num = resize_chaine(num, TNum)
            nom = resize_chaine(nom, TLname)
            prénom = resize_chaine(prénom, TFname)
            affiliation = resize_chaine(affiliation, Taffil)
            
            ## Creating the Structure
            etud = num + nom + prénom + affiliation + '0'
            
            ## Getting the characetrization
            nb = entete(f,1)
            buff = lireBloc(f,nb-1)
            buff[0]+1
            Full = True 
            trouve =False
            
            for j in range(maxStructures):
                ## if we find a empty Structure with no key we insert 
                if buff[1][j][:TNum].replace('#','') == '' and not trouve:
                    buff[0] += 1
                    affecter_entete(f,0,entete(f,0)+1)
                    buff[1][j] = etud
                    ecrireBloc(f,nb-1,buff)
                    Full = False
                    trouve=True
            ## if full we enter in  a new bloc
            if Full:
                buff = Tbloc
                buff[0] +=1
                buff[1][0] = etud
                ecrireBloc(f,nb,buff)
                affecter_entete(f,0,entete(f,0)+1)
                affecter_entete(f,1,entete(f,1)+1)
    except Exception:
        print('Error Found')
def DeleteLoGICALLY():
    fn = input('Enter The File U want to delete Logically: ')
    K = input('Enter The Ket  for the One u want to Delete') 
    try:
        ## Opening the file in read and write mode
        with open(fn,'r+b') as f:
            ## we Search
            if pos := Search(fn,K): 
                i,j = pos[0]-1,pos[1]-1
                buff = lireBloc(f,i)
                buff[1][j] = f'{buff[1][j][:-1]}1'
                ecrireBloc(f,i,buff)
                print("Deleted Logically Successfully")
    except FileNotFoundError:
        print('file not found')
def DeletePhysically():
    fn = input('Enter The File U want to delete Physically : ')
    K = input('Enter The Key  for the One u want to Delete Physically') 
    
    
    try:
        with open(fn,"r+b") as f:
            nb = entete(f,1)
            if pos := Search(fn,K):
                i,j = pos[0]-1,pos[1]-1
                ## Decalling 
                while i < nb:
                    if i != nb-1:
                        buff = lireBloc(f,i)
                        buff2 = lireBloc(f,i+1)
                        while j<maxStructures:
                            if j+1 != maxStructures:
                                buff[1][j] = buff[1][j+1]
                              
                            else:
                                buff[1][j] = buff2[1][0]  
                                ecrireBloc(f,i,buff)
                            j += 1
                        j = 0
                    else:
                        buff = lireBloc(f,i)
                        while j<maxStructures:
                            if j+1 != maxStructures:
                                buff[1][j] = buff[1][j+1]
                                buff[1][j+1] = TStructure
                                buff[0] -= 1
                           
                                if buff[1][0].replace('#','') == '':
                                    affecter_entete(f,1,entete(f,1)-1)
                                else:
                                    ecrireBloc(f,i,buff)
                            else:
                                buff[1][j] = TStructure
                                ecrireBloc(f,i,buff)
                            j+=1
                    i += 1
    except FileNotFoundError:
        print("file not found")

        
def default():
    return "Wrong Input"
def Choice(choice):
    
    switcher = {
        1: CreateFile,
        2: Display_File,
        3: Search,
        4: insertion,
        5: DeleteLoGICALLY,
        6: DeletePhysically,
    }
    if choice not in [4,3]:
        return switcher.get(choice, default)()
    if choice == 3:
        fn = input('Choose The File That U Want To Search On ')
        Key = input('Enter The Key for The Element U want to Search ')
        Search(fn,Key)
    else:
        fn = input('Choose the file That u want to Enter A new Element To ')
        insertion(fn) 
def main():
    ans = 'Y'
    while (ans in ["Y","y"]):
        print(""" | Choose |
                 1. créer_fichier
                 2. afficher_fichier
                 3. rechercher un element
                 4. inserer un element
                 5. supression_logique
                 6. supression_physique
             """)                
        choice = int(input())
        Choice(choice)
        ans = input('Do You Want To Do Another Operation Y/n? ')
main()

