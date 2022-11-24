from Transaction import Transaction 
#Library untuk memberikan warna pada program
from colorama import init 
init()
from colorama import Fore, Back, Style
import time

def validasiTransaksi(idTransaksi, listTransaksi) -> bool:
    for i in listTransaksi:
        if (i.validasi == None):
            continue
        if (i.id == idTransaksi.id):
            continue
        if(i.validasi < idTransaksi.validasi):
            if(i.selesai < idTransaksi.mulai):
                pass
            elif((idTransaksi.mulai < i.selesai) and (i.selesai < idTransaksi.validasi)):
                for list in i.writeTransaksi:
                    if list in idTransaksi.readTransaksi:
                        return False
            else:
                return False
    return True

def OCCTransaction(schedule, totalTransaksi):
    print(Fore.BLUE+"-------------------------------------------------------"+Fore.RESET)
    print(Fore.RED+"---------Serial Optimistic Concurrency Control---------"+Fore.RESET)
    print(Fore.BLUE+"-------------------------------------------------------"+Fore.RESET)

    # Inisialisasi list transaksi
    daftarTransaksi = []
    for i in range (totalTransaksi):
        transaksi = Transaction(i+1,None,None,None)
        daftarTransaksi.append(transaksi)

    # Fase Read
    for i in range (len(schedule)):
        if (schedule[i][0] == "C"):
            print(Fore.BLUE+Back.WHITE+"Commit"+Fore.RESET + Back.RESET+" ", end="")
            print("transaksi T", end="")
            print(schedule[i][1])
            id = int(schedule[i][1]) - 1
            time.sleep(0.1)
            daftarTransaksi[id].validasi = time.time()
            # Fase Validasi
            hasilValidasi = validasiTransaksi(daftarTransaksi[id], daftarTransaksi)
            # Fase Write
            if (hasilValidasi):
                time.sleep(0.1)
                daftarTransaksi[id].selesai = time.time()
                print(f"===> Transaksi T{id+1} sukses dilakukan")
            else:
                print(f"===> Transaksi T{id+1} gagal dilakukan")
                print(f"Transaksi T{id+1} aborted")
                return False

        elif (schedule[i][0] == "R" or schedule[i][0] == "W"):
            id = int(schedule[i][1]) - 1
            # Ketika timestamp transaksi belum dimulai
            if (daftarTransaksi[id].mulai == None):
                # Inisiasi waktu mulai transaksi
                time.sleep(0.1)
                daftarTransaksi[id].mulai = time.time()
            
            if(len(schedule[i]) == 5):
                if (schedule[i][0] == "R"):
                    
                    print(Fore.YELLOW+Back.WHITE+"Read"+Fore.RESET + Back.RESET+" ", end="")
                    print(schedule[i][3], "pada transaksi T", end="")
                    print(schedule[i][1])
                    daftarTransaksi[id].readTransaksi.append(schedule[i][2])
                else:
                    print(Fore.RED+Back.WHITE+"Write"+Fore.RESET + Back.RESET+" ", end="")
                    print(schedule[i][3], "pada transaksi T", end="")
                    print(schedule[i][1])
                    daftarTransaksi[id].writeTransaksi.append(schedule[i][2])
            elif(len(schedule[i]) == 6):
                if (schedule[i][0] == "R"):
                    print(Fore.YELLOW+Back.WHITE+"Read"+Fore.RESET + Back.RESET+" ", end="")
                    print(schedule[i][4],"pada transaksi T", end="")
                    print(schedule[i][1])
                    daftarTransaksi[id].readTransaksi.append(schedule[i][1])
                else:
                    print(Fore.RED+Back.WHITE+"Write"+Fore.RESET + Back.RESET+" ", end="")
                    print(schedule[i][4],"pada transaksi T", end="")
                    print(schedule[i][1])
                    daftarTransaksi[id].writeTransaksi.append(schedule[i][1])
    return True

def formatting(schedule):
    for i in range (len(schedule)):
        kata = schedule[i]
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

def executeOCC():
    print(Fore.BLUE+"-------------------------------------------------------"+Fore.RESET)
    print(Fore.RED +"----Starting Serial Optimistic Concurrency Control-----"+Fore.RESET)
    print(Fore.BLUE+"-------------------------------------------------------"+Fore.RESET)
    print(Fore.CYAN+"Masukkan jumlah transaksi : "+Fore.RESET, end="")
    totalTransaksi = int(input())
    schedule = []
    print(Fore.CYAN+"Masukkan total schedule : "+Fore.RESET, end="")
    totalSchedule  = int(input())
    
    print(Fore.BLUE+"-------------------------------------------------------"+Fore.RESET)
    print(Fore.YELLOW +"Format Schedule : 'R1(X)', 'W1(X)', 'C1'"+Fore.RESET)
    print(Fore.BLUE+"-------------------------------------------------------"+Fore.RESET)
    for i in range (totalSchedule ) :
        print("Schedule", (i+1),": ",end="")
        x = str(input())
        schedule.append(x)

    if not(formatting(schedule)):
        print(Fore.RED+"Format yang Anda Masukkan Salah!!!"+Fore.RESET)

    if (OCCTransaction(schedule, totalTransaksi)):
        print(Fore.BLUE+"Validasi Transaksi Sukses Dilakukan"+Fore.RESET)
    else :
        print(Fore.RED+"Validasi Transaksi Gagal Dilakukan"+Fore.RESET)

def pilihMetodeInputOCC():
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
        executeOCC()
    elif (inputMetode == 2):
        print("Masukkan nama file (Pastikan file sudah ada di folder test) : ", end="")
        filename = str(input())
        file = open("../test/" + filename, "r")
        content = file.read()
        arrString = content.split('\n')
    

        totalTransaksi = int(arrString[0])
        totalSchedule = int(len(arrString)-2)
        schedule = []
        
        for i in range (totalSchedule):
            x = str(arrString[i+2])
            print("Schedule", (i+1),": ",x)
            schedule.append(x)

        if (OCCTransaction(schedule, totalTransaksi)):
            print(Fore.BLUE+"Validasi Transaksi Sukses Dilakukan"+Fore.RESET)   
        else :
            print(Fore.RED+"Validasi Transaksi Gagal Dilakukan"+Fore.RESET)
