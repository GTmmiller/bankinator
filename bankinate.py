import pkgutil
import sys
import bankinator.bank
import bankinator.output
import getpass


def ignore_base_walk(module_base_path):
    # Check available modules. Ignore modules with base in the name
    modules = []
    for importer, modname, ispkg in pkgutil.walk_packages(path=module_base_path.__path__,
                                                          prefix=module_base_path.__name__+'.',
                                                          onerror=lambda x: None):
        if 'base_' not in modname:
            modules.append(modname)
    return modules


def module_selector(module_list, module_type):
    print '\nYou have ' + str(len(module_list)) + ' ' + module_type + ' module(s) to choose from.\n'

    for index, module in enumerate(module_list):
        print ('[ ' + str(index) + ' ] ' + module)

    input_module = raw_input('\nSelect a ' + module_type + ' module: ')
    return __import__(module_list[int(input_module)], fromlist=[module_type.capitalize()])

bank_modules = ignore_base_walk(bankinator.bank)
output_modules = ignore_base_walk(bankinator.output)

bank_module = module_selector(bank_modules, 'bank')
output_module = module_selector(output_modules, 'output')

bank_class = getattr(bank_module, 'Bank')
output_class = getattr(output_module, 'WriteOutput')

bank = bank_class()
output = output_class()

try:
    username = raw_input('\nEnter your username: ')
    password = getpass.getpass('Enter your password: ')
    homepage = bank.authenticate(username, password)
except:
    raise

try:
    (account, raw_data) = bank.navigate(homepage)
except:
    raise

try:
    account_data = bank.parse(account, raw_data)
except:
    raise

try:
    output.write(account_data[0], account_data[1])
except:
    raise
finally:
    sys.exit()
