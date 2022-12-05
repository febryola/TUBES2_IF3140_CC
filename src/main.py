#LIBRARY YANG MEMBERIKAN WARNA PADA PROGRAM
from colorama import init #Library untuk memberikan warna pada program
init()
from colorama import Fore, Back, Style
from OCC import *
from Lock import *

def main():
    print(Fore.BLUE+"----------------------------------------------------------------")
    print(Fore.GREEN+"Selamat datang pada simulasi Concurrency Control Kelompok 7 K02!")
    print(Fore.BLUE+"----------------------------------------------------------------"+Fore.RESET)
    input_metode = 0
    while (input_metode < 1 or input_metode > 3):
        print(Fore.YELLOW+"")
        print("Pilih metode yang ingin digunakan :")
        print(Style.RESET_ALL)
        print("1. Simple Locking")
        print("2. Serial Optimistic Concurrency Control (OCC)")
        print("3. Multiversion Concurrency Control (MVCC)")
        print(Fore.BLUE+"")
        input_metode = int(input("Nomor Metode yang ingin digunakan: "))
        print(Style.RESET_ALL)
        if(input_metode < 1 or input_metode > 3):
            print(Fore.RED+"")
            print("Input salah! Silahkan masukkan nomor metode yang ingin digunakan!"+Fore.RESET)

    if input_metode == 1:
        print(Fore.CYAN+"Anda memilih metode Simple Locking\n"+Fore.RESET)
        pilihMetodeInputLock()
    elif input_metode == 2:
        print(Fore.CYAN+"Anda memilih metode Serial Optimistic Concurrency Control (OCC)\n"+Fore.RESET)
        pilihMetodeInputOCC()
    elif input_metode == 3:
        print(Fore.CYAN+"Anda memilih metode Multiversion Concurrency Control (MVCC)\n"+Fore.RESET)

def banner():
    print(Fore.BLUE+"\n\n----------------------------------------------------------------")
    print(Fore.GREEN+"-----------------------Program Selesai--------------------------")
    print(Fore.BLUE+"----------------------------------------------------------------"+Fore.RESET)

if __name__ == "__main__":
    main()
    banner()