class Transaction(object):

    def __init__(self, id, mulai, selesai, validasi):
        super(Transaction, self).__init__()
        #initiasi output dan transaksi
        self.id = id
        self.mulai = mulai
        self.selesai = selesai
        self.validasi = validasi
        #read variables held by this transaction
        self.readTransaksi = []  
        #write variables held by this transaction
        self.writeTransaksi = []


