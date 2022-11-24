# IF3140 Manajemen Basis Data

> _Repository ini ditujukan untuk memenuhi Tugas Besar 2 IF3140_

## Deskripsi
Dalam tugas besar Manajemen Basis Data kali ini, kami mengimplementasikan protokol concurrency control dalam bentuk simulasi terhadap kumpulan proses dalam suatu schedule. Berikut ini adalah daftar Concurrency Control Protocol yang kami implementasikan pada tugas besar ini, yaitu:
1. Simple Locking (Exclusive Only)
2. Serial Optimistic Concurrency Control (Validation Based Protocol)
3. Multiversion Timestamp Ordering Concurrency Control (MVCC)

## Requirements
Untuk menjalankan program pastikan Anda telah mendownload dan menginstall hal-hal berikut:
1. Teks editor
2. Python 3

## How To Install
1. Teks Editor yang kami sarankan adalah Visual Studio Code yang panduan download dan installnya dapat dilihat pada tautan berikut ini [vscode](https://www.belajarisme.com/tutorial/install-vscode/#:~:text=Sekarang%20mari%20kita%20install%20VSCode%20dengan%20cara%20berikut,Select%20Star%20Menu%20Folder%20klik%20Next.%20More%20items)
2. Panduan instalasi Python 3 dapat dilihat pada tautan berikut [Python 3](https://www.sebardi.id/2021/05/cara-instal-python-395-di-windows-10.html)

## How To Run
1. Clone repository ini
2. Lalu buka terminal dan lakukan cd src
3. Pada terminal, ketik dan enter command line berikut:
```
$ python main.py
```
5. Inputkan algoritma protokol Concurrency Control yang diinginkan, ketik 1 jika ingin menggunakan simple locking algorithm, ketik 2 jika menggunakan optimistic concurrency control (OCC), dan ketik 3 jika menggunakan multiversion concurrency control algorithm
6. Jika memilih Simple Locking Algorithm,
7. Jika memilih Serial Optimistic Concurrency Control (OCC),
8. Jika memilih Multiversion Concurrency Control (MVCC),

## Contributor
<table>
  <tr >
      <td><b>Nama</b></td>
      <td><b>NIM</b></td>
    </tr>
    <tr >
      <td><b>Fadil Fauzani</b></td>
      <td>13520032</td>
    </tr>
    <tr>
      <td><b>Shadiq Harwiz</b></td>
      <td>13520038</td>
    </tr>
    <tr>
      <td><b>Alifia Rahmah</b></td>
      <td>13520122</td>
    </tr>
    <tr>
      <td><b>Febryola Kurnia Putri</b></td>
      <td>13520140</td>
    </tr>
</table>
