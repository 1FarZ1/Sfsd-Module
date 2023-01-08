def fragmentation():
    fn = input('choose the file to devide into 2 files ')
    key1 = int(input('First Key '))
    key2 = int(input('Second Key'))
    try:
        with open(fn,'r+b') as f:
            f1= open(f'{fn}1','wb')
            f2=open(f'{fn}2','wb')
            f3=open(f'{fn}3','wb')
            nb = entete(f,1)
            
            ## number of elements
            n1=0
            n2=0
            n3=0
            
            i,j = 0,0
            i1,j1= 0,0
            i2,j2=0,0
            i3,j3 = 0,0
            buff1=[0, [TStructure] * maxStructures]
            buff2 = [0, [TStructure] * maxStructures]
            buff3=[0, [TStructure] * maxStructures]
            while i < nb:
                buff = lireBloc(f,i)
                for j in range(maxStructures):
                    
                    if buff[1][j].replace('#','') != '':
                        if int(buff[1][j][:TNum].replace('#','')) < key1:
                     
                            if j1 < maxStructures:
                                buff1[0] += 1
                                buff1[1][j1] = buff[1][j]                   
                                j1 += 1
                            else: 
                                ecrireBloc(f1,i1,buff1)  
                                i1 += 1
                                buff1 = [0, [TStructure] * maxStructures]
                                buff1[0] += 1
                                buff1[1][0] = buff[1][j]  
                                j1 = 1   
                                
                        elif int(buff[1][j][:TNum].replace('#','')) >= key1 and int(buff[1][j][:TNum].replace('#','')) < key2:
                            n2 += 1
                            if j2 < maxStructures:
                                buff2[0] += 1
                                buff2[1][j2] = buff[1][j]               
                                j2 += 1 
                            else:   
                                ecrireBloc(f2,i2,buff2)
                                i2 += 1
                                buff2 = [0, [TStructure] * maxStructures]
                                buff2[0] += 1
                                buff2[1][0] = buff[1][j]  
                                j2 = 1                        
                        elif int(buff[1][j][:TNum].replace('#','')) > key2:
                            n3 += 1
                            if j3 < maxStructures:
                                buff3[0] += 1
                                buff3[1][j3] = buff[1][j]
                                j3 += 1       
                            else:   
                                ecrireBloc(f3,i3,buff3)
                                i3 += 1
                                buff3 = [0, [TStructure] * maxStructures]
                                buff3[0] += 1
                                buff3[1][0] = buff[1][j]  
                                j3 = 1                                                      
                i +=1
                
            ecrireBloc(f1,i1,buff1)
            ecrireBloc(f2,i2,buff2)
            ecrireBloc(f3,i3,buff3)
            affecter_entete(f1,1,i1+1)
            affecter_entete(f2,1,i2+1)
            affecter_entete(f3,1,i3+1)
            affecter_entete(f1,0,n1)
            affecter_entete(f2,0,n2)
            affecter_entete(f3,0,n3)
            f1.close()
            f2.close()
            f3.close()
    except FileNotFoundError:
        print('file not found')
        