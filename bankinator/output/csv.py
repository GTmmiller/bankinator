from datetime import datetime
from string import Template

_fout = Template('$year_$month_$day_$account_name_transactions.csv')


def write(account, account_data):
    today = datetime.today()
    csv_filename = _fout.safe_substitute(year=today.year, month=today.month,
                                         day=today.day,
                                         account_name=account['type'] + account['lastno'])
    csv_file = open(csv_filename, 'w')
    csv_contents = ''

    for line in account_data:
        for data in line:
            csv_contents.append(data + ',')
        csv_contents.append('\n')

    csv_file.write(csv_contents)
    csv_file.close()

