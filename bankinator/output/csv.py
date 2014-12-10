from datetime import datetime
from base_output import OutputBase


class WriteOutput(OutputBase):

    def __init__(self):
        OutputBase.__init__(self)

    def write(self, account, account_data):
        today = datetime.today()
        csv_filename = (str(today.year) + '_' + str(today.month) + '_' +
                        str(today.day) + '_' + account['type'] + account['lastno'] +
                        '_transactions.csv')
        csv_file = open(csv_filename, 'w')
        csv_contents = ''
        for line in account_data:
            for data in line:
                csv_contents += data + ';'
            csv_contents += '\n'
        print repr(csv_contents)
        csv_file.write(csv_contents)
        csv_file.close()

        print ('\n' + csv_filename + ' has been writen successfully!')

