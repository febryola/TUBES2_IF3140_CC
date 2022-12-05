#Library untuk memberikan warna pada program
from colorama import init 
init()
from colorama import Fore, Back

class Transaction:
    def __init__(self, id):
        self.id = id
        self.listTransaction = []
        self.listAllTransaction = []
        self.waitTransactionExlusiveLockFrom = ""
        self.indexwaitTransactionExlusiveLockFrom = ""

class ExlusivceClock:
    def __init__(self, data):
        self.data = data
        self.whoTransactionGetExlusiveLock = ""

def validasiTransaksi(transaction) -> bool:
    if ( ( len(transaction.listTransaction) == 1 ) and ( transaction.listTransaction[0][0] == "C" ) )  :
        return True

def getIndexListExlusiveLock(data, listExlusiveLock):
    for i in range (len(listExlusiveLock)) :
        if ( listExlusiveLock[i].data == data) :
            return (i)

def exclusiveLockRelease(idTransaction, listExclusiveLock, listUrutanSchedule) :
    for i in range (len(listExclusiveLock)) :
        if (listExclusiveLock[i].whoTransactionGetExlusiveLock == idTransaction) :
            listUrutanSchedule.append("UL" + idTransaction + "("  + listExclusiveLock[i].data + ")")
            print("==> Exclusive Lock " + listExclusiveLock[i].data + " on transaction " + idTransaction + " release")
            listExclusiveLock[i].whoTransactionGetExlusiveLock = ""
    return (listUrutanSchedule)

def moveQueueToSchedule(queueOperasi, listSchedule, listAbortTransaction) :
    tempListSchedule = []
    for i in range (len(queueOperasi)):
        if (queueOperasi[i] not in listAbortTransaction) :
            tempListSchedule.append(queueOperasi[i])
    for i in range (len(listSchedule)) :
        if (listSchedule[i] not in listAbortTransaction) :
            tempListSchedule.append(listSchedule[i])
    del listSchedule
    del queueOperasi
    listSchedule = []
    queueOperasi = []
    for i in range (len(tempListSchedule)) :
        listSchedule.append(tempListSchedule[i])
    del tempListSchedule
    return(queueOperasi, listSchedule)

def eliminationTransactionDeadLock(listSchedule, listAbortTransaction):
    tempListSchedule = []
    for j in range (len(listSchedule)) :
        if (listSchedule[j] not in listAbortTransaction):
            tempListSchedule.append(listSchedule[j])
    del listSchedule
    listSchedule = []
    for j in range (len(tempListSchedule)) :
        listSchedule.append(tempListSchedule[j])
    del tempListSchedule
    return(listSchedule)

def checkExlusiveLock(listExclusiveLock, indexExlusiveLock, listTransaksi, id, idStr, listSchedule, queueOperasi, data, listQueueData, listQueueTransaction, listUrutanSchedule, isUseWoundWaitSchema, listUrutanTransaksi, listAbortTransaction, listOfListAbortTransaction) :
    if listExclusiveLock[indexExlusiveLock].whoTransactionGetExlusiveLock == "" and listTransaksi[id].listTransaction[0] == listSchedule[0] :
        if ( listTransaksi[id].waitTransactionExlusiveLockFrom != "" ) :
            listTransaksi[id].waitTransactionExlusiveLockFrom = ""
            listTransaksi[id].indexwaitTransactionExlusiveLockFrom = ""
        listExclusiveLock[indexExlusiveLock].whoTransactionGetExlusiveLock = idStr
        print("==> Give Exclusive Lock " + data + " to T" + idStr)
        listUrutanSchedule.append("XL" + idStr + "(" + data + ")")
        listUrutanSchedule.append(listSchedule[0])
        del listSchedule[0]
        del listTransaksi[id].listTransaction[0]
        print("==> Success")
    elif listExclusiveLock[indexExlusiveLock].whoTransactionGetExlusiveLock == idStr and listTransaksi[id].listTransaction[0] == listSchedule[0] :
        if ( listTransaksi[id].waitTransactionExlusiveLockFrom != "") :
            listTransaksi[id].waitTransactionExlusiveLockFrom = ""
            listTransaksi[id].indexwaitTransactionExlusiveLockFrom = ""
        listUrutanSchedule.append(listSchedule[0])
        del listSchedule[0]
        del listTransaksi[id].listTransaction[0]
        print("==> Success")
    else :
        if ( listTransaksi[id].waitTransactionExlusiveLockFrom == "") :
            listTransaksi[id].waitTransactionExlusiveLockFrom = data
            listTransaksi[id].indexwaitTransactionExlusiveLockFrom = listExclusiveLock[indexExlusiveLock].whoTransactionGetExlusiveLock
        print("==> Transaction " + idStr + " is waiting for Exclusive Lock " + listTransaksi[id].waitTransactionExlusiveLockFrom + " which is in Transaction "+ listTransaksi[id].indexwaitTransactionExlusiveLockFrom + ". " + listSchedule[0] + " get into the queue...")
        queueOperasi.append(listSchedule[0])
        if ( data not in listQueueData ) :
            listQueueData.append(data)
        if ( idStr not in listQueueTransaction) :
            listQueueTransaction.append(idStr)
        del listSchedule[0]

        # Cek apakah transaksi tua meminta lock kepada transaksi yang muda dari nya
        isOldAskYoung = False
        susOld = idStr
        urutanSusOld = 0
        susYoung = ""
        urutanSusYoung = 0
        for i in range (len(listExclusiveLock)) :
            if (listExclusiveLock[i].data == listTransaksi[id].waitTransactionExlusiveLockFrom) :
                susYoung = listExclusiveLock[i].whoTransactionGetExlusiveLock
        
        for i in range (len(listUrutanTransaksi)) :
            if (str(listUrutanTransaksi[i]) == susOld):
                urutanSusOld = i
            if (str(listUrutanTransaksi[i]) == susYoung):
                urutanSusYoung = i
        
        if (urutanSusOld < urutanSusYoung) :
            isOldAskYoung = True
        else :
            isOldAskYoung = False
        
        if (isUseWoundWaitSchema == True and isOldAskYoung == True ) :
            if ( len(listAbortTransaction) != 0 ) :
                listOfListAbortTransaction.append(listAbortTransaction)
                del listAbortTransaction
                listAbortTransaction = []

            print("!!!Do Wound-Wait Scheme!!!")
            print("Aborting T", end="")
            idTransactionPrevent = int(susYoung)
            id = idTransactionPrevent - 1
            listUrutanSchedule.append("A" + str(idTransactionPrevent))

            #Transaksi yang di-abort masuk ke dalam listAbortTransaction
            for j in range (len(listTransaksi[id].listAllTransaction)):
                listAbortTransaction.append(listTransaksi[id].listAllTransaction[j])

            # Fase pembebasan exclusive lock yang ada pada transaki tersebut
            for j in range ( len(listExclusiveLock) ):
                if (listExclusiveLock[j].whoTransactionGetExlusiveLock == str(idTransactionPrevent)) :
                    listUrutanSchedule.append("UL" + str(idTransactionPrevent) + "(" + listExclusiveLock[j].data + ")")
                    print("==> Exclusive Lock " + listExclusiveLock[j].data + " on transaction " + str(idTransactionPrevent) + " release")
                    listExclusiveLock[j].whoTransactionGetExlusiveLock = ""

            # Fase eliminasi transaksi yang di-deadlock
            if ( len(queueOperasi) > 0 ) :
                queueOperasi, listSchedule = moveQueueToSchedule(queueOperasi, listSchedule, listAbortTransaction)
            else :
                listSchedule = eliminationTransactionDeadLock(listSchedule, listAbortTransaction)
            
            # Fase penghapusan list
            del listQueueData
            listQueueData = []
                

    return(listExclusiveLock, listSchedule, listTransaksi, queueOperasi, listQueueData, listQueueTransaction, listUrutanSchedule, listUrutanTransaksi, listAbortTransaction, listOfListAbortTransaction)

def LockTransaction(listSchedule, totalTransaksi, isUseWoundWaitSchema):
    print(Fore.BLUE+"-------------------------------------------------------"+Fore.RESET)
    print(Fore.RED +"---------------------Simple Locking--------------------"+Fore.RESET)
    print(Fore.BLUE+"-------------------------------------------------------"+Fore.RESET)

    # Fase Inisialisasi
    # Inisialisasi kamus
    isDeadLock = False
    queueOperasi = []
    listExclusiveLock = []
    listData = []
    listTransaksi = []
    listQueueData = []
    listUrutanTransaksi = []
    listUrutanSchedule = []
    listQueueTransaction = []
    listAbortTransaction = []
    listOfListAbortTransaction = []

    # Inisialisasi list transaksi
    for i in range (totalTransaksi):
        transaksi = Transaction(i+1)
        listTransaksi.append(transaksi)

    # Inisialisasi list data yang akan ditransaksi
    print("Berikut Urutan Transaksi")
    for i in range (len(listSchedule)) :
        idTransaksi = 0

        #Kalau schedulenya berupa commit
        if (len(listSchedule[i]) == 2) : 
            idTransaksi = int(listSchedule[i][1]) - 1
        elif ( len(listSchedule[i]) == 3 ) :
            idTransaksi = (int( listSchedule[i][1] + listSchedule[i][2] )) - 1

        #Kalau schedulenya berupa write dan read
        if ( len(listSchedule[i]) == 5 ) :
            idTransaksi = int(listSchedule[i][1]) - 1

            if listSchedule[i][3] not in listData :
                exlusiveClock = ExlusivceClock(listSchedule[i][3])
                listExclusiveLock.append(exlusiveClock)
                listData.append(listSchedule[i][3])

            if ((idTransaksi + 1) not in listUrutanTransaksi):
                listUrutanTransaksi.append(idTransaksi + 1)
                print("Transaksi", idTransaksi + 1)
        elif ( len(listSchedule[i]) == 6 ) :
            idTransaksi = (int( listSchedule[i][1] + listSchedule[i][2] )) - 1

            if listSchedule[i][4] not in listData :
                exlusiveClock = ExlusivceClock(listSchedule[i][4])
                listExclusiveLock.append(exlusiveClock)
                listData.append(listSchedule[i][4])
            
            if ((idTransaksi + 1) not in listUrutanTransaksi):
                listUrutanTransaksi.append(idTransaksi + 1)
                print("Transaksi", idTransaksi + 1)

        (listTransaksi[idTransaksi].listTransaction).append(listSchedule[i])
        (listTransaksi[idTransaksi].listAllTransaction).append(listSchedule[i])

    print()
    # Fase operasi
    while ( len(listSchedule) > 0 ):
        i = 0

        # Kasus commit
        if (listSchedule[i][0] == "C"):
            idTransaction = 0
            idTransactionStr = ""

            print(Fore.BLUE+Back.WHITE+"Commit"+Fore.RESET + Back.RESET+" ", end="")
            print("transaksi T", end="")

            if ( len(listSchedule[i]) == 2 ):
                idTransaction = int(listSchedule[i][1]) - 1
                idTransactionStr = listSchedule[i][1]
                print(idTransactionStr)
            elif ( len(listSchedule[i]) == 3 ):
                idTransaction = int( listSchedule[i][1] + listSchedule[i][2] ) - 1
                idTransactionStr = (listSchedule[i][1] + listSchedule[i][2])
                print(idTransactionStr)
            
            # Fase Validasi
            hasilValidasi = validasiTransaksi(listTransaksi[idTransaction])
            
            if (hasilValidasi == True):
                print("==> Success...")

                # Fase pembebasan exclusive lock yang ada pada transaki tersebut
                listUrutanSchedule = exclusiveLockRelease(idTransactionStr, listExclusiveLock, listUrutanSchedule)
                
                # Fase penghapusan transaksi yang berhasil di-commit dari listTransaksi dan listSchedule
                del listTransaksi[idTransaction].listTransaction
                listUrutanSchedule.append(listSchedule[i])
                del listSchedule[i]
                
                # Fase pemindahan queueOperasi ke listSchedule
                if ( len(queueOperasi) > 0 ) :
                    queueOperasi, listSchedule = moveQueueToSchedule(queueOperasi, listSchedule, listAbortTransaction)

                # Fase penghapusan transaksi yang telah berhasil di-commit dari listUrutanTransaksi
                for j in range (len(listUrutanTransaksi)) :
                    if listUrutanTransaksi[j] == (idTransaction + 1) :
                        del listUrutanTransaksi[j]
                        break
                
            else:
                print("==> Pending...")
                
                # Fase pemindahan transaksi itu ke queueOperasi
                queueOperasi.append(listSchedule[i])
                
                # Hapus transaksi itu dari listSchedule
                del listSchedule[i]

        # Kasus Read atau Write
        elif (listSchedule[i][0] == "R" or listSchedule[i][0] == "W"):
            
            if(len(listSchedule[i]) == 5):
                id = int( listSchedule[i][1] ) - 1
                idStr = listSchedule[i][1]
                data = listSchedule[i][3]
                indexExlusiveLock = getIndexListExlusiveLock(data, listExclusiveLock)

                if (listSchedule[i][0] == "R"):
                    print(Fore.YELLOW+Back.WHITE+"Read"+Fore.RESET + Back.RESET+" ", end="")
                else: #(listSchedule[i][0] == "W")
                    print(Fore.RED+Back.WHITE+"Write"+Fore.RESET + Back.RESET+" ", end="")
                
                print(data, "pada T", end="")
                print(idStr)
                
                #Cek exclusive lock sedang dipegang transaksi apa dan apakah terdapat transaksi sebelum si transaksi tersebut 
                listExclusiveLock, listSchedule, listTransaksi, queueOperasi, listQueueData, listQueueTransaction, listUrutanSchedule, listUrutanTransaksi, listAbortTransaction, listOfListAbortTransaction = checkExlusiveLock(listExclusiveLock, indexExlusiveLock, listTransaksi, id, idStr, listSchedule, queueOperasi, data, listQueueData, listQueueTransaction, listUrutanSchedule, isUseWoundWaitSchema, listUrutanTransaksi, listAbortTransaction, listOfListAbortTransaction)

            elif(len(listSchedule[i]) == 6):
                id = (int( listSchedule[i][1] + listSchedule[i][2] )) - 1
                idStr = listSchedule[i][1] + "" + listSchedule[i][2]
                data = listSchedule[i][4]
                indexExlusiveLock = getIndexListExlusiveLock(data, listExclusiveLock)

                if (listSchedule[i][0] == "R"):
                    print(Fore.YELLOW+Back.WHITE+"Read"+Fore.RESET + Back.RESET+" ", end="")
                else: #(listSchedule[i][0] == "W")
                    print(Fore.RED+Back.WHITE+"Write"+Fore.RESET + Back.RESET+" ", end="")
                
                print(data,"pada T", end="")
                print(idStr)
                    
                #Cek exclusive lock sedang dipegang transaksi apa dan apakah terdapat transaksi sebelum si transaksi tersebut 
                listExclusiveLock, listSchedule, listTransaksi, queueOperasi, listQueueData, listQueueTransaction, listUrutanSchedule, listUrutanTransaksi, listAbortTransaction, listOfListAbortTransaction = checkExlusiveLock(listExclusiveLock, indexExlusiveLock, listTransaksi, id, idStr, listSchedule, queueOperasi, data, listQueueData, listQueueTransaction, listUrutanSchedule, isUseWoundWaitSchema, listUrutanTransaksi, listAbortTransaction, listOfListAbortTransaction)

        #Cek jika ternyata terjadi proses saling menunggu yang menyebabkan deadlock
        if ( len(listData) == len(listQueueData) and len(listUrutanTransaksi) == len(listQueueTransaction) and len(listQueueData) > 1 and len(listQueueTransaction) > 1 and len(listSchedule) != 0 and isUseWoundWaitSchema == False) :
            print("!!!Deadlock detected!!!")
            del listSchedule
            listSchedule = []
            isDeadLock = True
            break

        #Fase menjalankan transaksi yang telah diabort
        if ( len(listSchedule) == 0 and len(listAbortTransaction) != 0 ) :
            print("!!!Executing aborted transactions!!!")
            listOfListAbortTransaction.append(listAbortTransaction)
            if (len(listOfListAbortTransaction) > 0) :
                for i in range (len(listOfListAbortTransaction)) :
                    del listAbortTransaction
                    listAbortTransaction = []
                    for j in range (len(listOfListAbortTransaction[i])):
                        listAbortTransaction.append((listOfListAbortTransaction[i])[j])
                    #Cari id transaksi yang di abort
                    id = 0
                    if ( len(listAbortTransaction[0]) == 5 or len(listAbortTransaction[0]) == 2):
                        id = int(listAbortTransaction[0][1]) - 1
                    elif ( len(listAbortTransaction[0]) == 6 or len(listAbortTransaction[0]) == 3):
                        id = int(listAbortTransaction[0][1] + listAbortTransaction[0][2]) - 1
                    del listTransaksi[id].listTransaction
                    listTransaksi[id].listTransaction = []
                    for i in range (len(listTransaksi[id].listAllTransaction)) :
                        (listTransaksi[id].listTransaction).append(listTransaksi[id].listAllTransaction[i])                
                    for j in range (len(listAbortTransaction)) :
                        listSchedule.append(listAbortTransaction[j])
                    del listAbortTransaction
                    listAbortTransaction = []
            else :
                #Cari id transaksi yang di abort
                id = 0
                if ( len(listAbortTransaction[0]) == 5 or len(listAbortTransaction[0]) == 2):
                    id = int(listAbortTransaction[0][1]) - 1
                elif ( len(listAbortTransaction[0]) == 6 or len(listAbortTransaction[0]) == 3):
                    id = int(listAbortTransaction[0][1] + listAbortTransaction[0][2]) - 1
                del listTransaksi[id].listTransaction
                listTransaksi[id].listTransaction = []
                for i in range (len(listTransaksi[id].listAllTransaction)) :
                    (listTransaksi[id].listTransaction).append(listTransaksi[id].listAllTransaction[i])                
                for j in range (len(listAbortTransaction)) :
                    listSchedule.append(listAbortTransaction[j])
                del listAbortTransaction
                listAbortTransaction = []

    if (len(listSchedule) == 0 and len(queueOperasi) == 0 and isDeadLock == False) :
        print("\nBerikut Urutan Schedule")
        for i in range (len(listUrutanSchedule)) :
            print(listUrutanSchedule[i], end="")
            print("; ", end="")
        print("\n")
        return True
    else :
        return False

def formatting(listSchedule):
    for i in range (len(listSchedule)):
        kata = listSchedule[i]
        hurufPertama = kata[0]

        if (hurufPertama != "R"):
            if (hurufPertama != "W"):
                if (hurufPertama != "C"):
                    return False

        if (hurufPertama == "R" or hurufPertama == "W"):
            if (len(kata) == 5) :
                if not(kata[1].isnumeric()):
                    return False
                if kata[2]!="(" or kata[-1]!=")":
                    return False
                if not(kata[-2].isalpha()):
                    return False
            elif (len(kata) == 6):
                if not(kata[1].isnumeric()):
                    return False
                if not(kata[2].isnumeric()) :
                    return False
                if kata[3]!="(" or kata[-1]!=")":
                    return False
                if not(kata[-2].isalpha()):
                    return False
            else:
                return False
        else :
            if not(kata[1].isnumeric()):
                return False

    return True

def executeLock(isUseWoundWaitSchema):
    print(Fore.BLUE+"-------------------------------------------------------"+Fore.RESET)
    print(Fore.RED +"----------------Starting Simple Locking----------------"+Fore.RESET)
    print(Fore.BLUE+"-------------------------------------------------------"+Fore.RESET)
    print(Fore.CYAN+"Masukkan jumlah transaksi : "+Fore.RESET, end="")
    totalTransaksi = int(input())
    listSchedule = []
    print(Fore.CYAN+"Masukkan total schedule : "+Fore.RESET, end="")
    totalSchedule  = int(input())
    
    print(Fore.BLUE+"-------------------------------------------------------"+Fore.RESET)
    print(Fore.YELLOW +"Format Schedule : 'R1(X)', 'W1(X)', 'C1'"+Fore.RESET)
    print(Fore.BLUE+"-------------------------------------------------------"+Fore.RESET)
    for i in range (totalSchedule ) :
        print("Schedule", (i+1),": ",end="")
        x = str(input())
        listSchedule.append(x)

    if not(formatting(listSchedule)):
        print(Fore.RED+"Format yang Anda Masukkan Salah!!!"+Fore.RESET)

    if (LockTransaction(listSchedule, totalTransaksi, isUseWoundWaitSchema)):
        print(Fore.BLUE+"Validasi Transaksi Sukses Dilakukan"+Fore.RESET)
    else :
        print(Fore.RED+"Validasi Transaksi Gagal Dilakukan"+Fore.RESET)

def pilihMetodeInputLock():

    isUseWoundWaitSchema = False
    inputMetode = 0
    while (inputMetode < 1 or inputMetode > 2):
        print(Fore.BLUE+"Apakah menggunakan Wound-Wait Scheme? : "+Fore.RESET)
        print("1. Ya")
        print("2. Tidak")
        print(Fore.YELLOW+"Masukkan Pilihan Anda : "+Fore.RESET, end="")
        inputMetode = int(input())
        if(inputMetode < 1 or inputMetode > 2):
            print(Fore.RED+"")
            print("Input salah! Silahkan masukkan nomor metode yang ingin digunakan!"+Fore.RESET)

    if (inputMetode == 1):
        isUseWoundWaitSchema = True
    elif (inputMetode == 2):
        isUseWoundWaitSchema = False

    inputMetode = 0
    while (inputMetode < 1 or inputMetode > 2):
        print(Fore.BLUE+"Pilih Metode Input : "+Fore.RESET)
        print("1. Input Manual")
        print("2. Input File")
        print(Fore.YELLOW+"Masukkan Pilihan Anda : "+Fore.RESET, end="")
        inputMetode = int(input())
        if(inputMetode < 1 or inputMetode > 2):
            print(Fore.RED+"")
            print("Input salah! Silahkan masukkan nomor metode yang ingin digunakan!"+Fore.RESET)

    if (inputMetode == 1):
        executeLock(isUseWoundWaitSchema)
    elif (inputMetode == 2):
        print("Masukkan nama file (Pastikan file sudah ada di folder test) : ", end="")
        filename = str(input())
        file = open("../test/" + filename, "r")
        content = file.read()
        arrString = content.split('\n')
    

        totalTransaksi = int(arrString[0])
        totalSchedule = int(len(arrString)-2)
        listSchedule = []
        
        for i in range (totalSchedule):
            x = str(arrString[i+2])
            print("Schedule", (i+1),": ",x)
            listSchedule.append(x)

        if (LockTransaction(listSchedule, totalTransaksi, isUseWoundWaitSchema)):
            print(Fore.BLUE+"Validasi Transaksi Sukses Dilakukan"+Fore.RESET)   
        else :
            print(Fore.RED+"Validasi Transaksi Gagal Dilakukan"+Fore.RESET)
