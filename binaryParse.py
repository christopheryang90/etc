import struct
from collections import defaultdict

class payments:

    def __init__(self, input_file):        
        with open(input_file,"rb") as data_file:
            self.data = data_file.read()
        self.head = struct.unpack("!4sbi",self.data[:9])
        self.records_data = self.data[9:]
        self.user_balance = defaultdict(float)
        self.total_debit = 0
        self.total_credit = 0
        self.autopay_start_count = 0
        self.autopay_end_count = 0
        self.record_count = 0
        while self.record_count < self.head[2]:
            self.read_next()

        
    def read_next(self):
        record_type = self.records_data[0]
        if record_type == '\x00': #Debit
            record =  struct.unpack("!biqd",self.records_data[:21])
            self.total_debit += record[3]
            self.user_balance[record[2]] += record[3]
            new_records = self.records_data[21:]
            self.records_data = new_records
        elif record_type == '\x01': #Credit
            record =  struct.unpack("!biqd",self.records_data[:21])
            self.total_credit += record[3]
            self.user_balance[record[2]] += record[3]
            new_records = self.records_data[21:]
            self.records_data = new_records
        elif record_type == '\x02': #StartAutopay
            record =  struct.unpack("!biq",self.records_data[:13])
            self.autopay_start_count += 1
            new_records = self.records_data[13:]
            self.records_data = new_records
        elif record_type == '\x03': #EndAutopay
            record =  struct.unpack("!biq",self.records_data[:13])
            self.autopay_end_count += 1
            new_records = self.records_data[13:]
            self.records_data = new_records
        else :raise ValueError("unknown record type enum")
        self.record_count += 1


def main():
    txn=payments("txnlog.dat")
    print "Total amount in dollars of debits is: $", txn.total_debit   
    print "Total amount in dollars of credits is: $", txn.total_credit
    print txn.autopay_start_count, "autopays started"
    print txn.autopay_end_count, "autopays ended"
    print "balance of user ID 2456938384156277127 is: $", txn.user_balance[2456938384156277127]
    
if __name__ == "__main__":
    main()



