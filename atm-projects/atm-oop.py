# Importing necessary modules and classes.
import textwrap
import os
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


# Define the User class.
class User:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def make_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)


# Define the Person class that inherits from user.
class Person(User):
    def __init__(self, name, birth_date, cpf, address):
        super().__init__(address)
        self.name = name
        self.birth_date = birth_date
        self.cpf = cpf


# Define the Account class
class Account:
    def __init__(self, number, user):
        self._balance = 0
        self._number = number
        self._branch = "0001"
        self._user = user
        self._history = History()

    @classmethod
    def new_account(cls, user, number):
        # Create a new account for the user and return it.
        return cls(number, user)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def branch(self):
        return self._branch

    @property
    def user(self):
        return self._user

    @property
    def history(self):
        return self._history

    def withdraw(self, amount):
        # Withdraw the amount from the account.
        balance = self.balance
        exceeded_balance = amount > balance

        if exceeded_balance:
            print("\nOperation failed! You don't have enough balance.")
            print("Please check your balance and try again.")
            input("Press <Enter> to continue...")

        elif amount > 0:
            self._balance -= amount
            print("\nYour withdraw was successful.")
            input("Press <Enter> to continue...")
            return True

        else:
            print("\nOperation failed! Please try again.")
            input("Press <Enter> to continue...")

        return False

    def deposit(self, amount):
        # Deposit the amount into the account.
        if amount > 0:
            self._balance += amount
            print(f"\nYour deposit of ${amount:.2f} was successful.")
            input("Press <Enter> to continue...")
        else:
            print("\nOperation failed! Please try again.")
            input("Press <Enter> to continue...")
            return False

        return True


# Define the Checking_Account class that inherits from Account.
class Checking_Account(Account):
    def __init__(self, number, user, limit=500, withdraw_limit=3):
        super().__init__(number, user)
        self._limit = limit
        self._withdraw_limit = withdraw_limit

    def withdraw(self, amount):
        # Withdraw the amount from a checking account.
        withdraw_count = len(
            [transaction for transaction in self.history.transactions
             if transaction["type"] == Withdraw.__name__]
        )

        exceeded_balance = amount > self._limit
        exceeded_withdraw_limit = withdraw_count >= self._withdraw_limit

        if exceeded_balance:
            print("\nOperation failed! You don't have enough limit.")
            input("Press <Enter> to continue...")
        elif exceeded_withdraw_limit:
            print("\nOperation failed! You have exceeded the number of "
                  "withdrawals allowed.")
            input("Press <Enter> to continue...")
        else:
            return super().withdraw(amount)

        return False

    def __str__(self):
        # Provide a string representation of the checking account.
        return f"""\
            Branch:\t{self.branch}\n
            Account:\t\t{self.number}\n
            user:\t{self.user.name}
        """


# Define the History class to track transactions.
class History:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        # Add a transaction to the history.
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "amount": transaction.amount,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


# Define the Transaction class as an abstract base class (ABC).
class Transaction(ABC):
    @property
    @abstractproperty
    def amount(self):
        pass

    @abstractclassmethod
    def register(self, account):
        pass


# Define the Withdraw class that inherits from Transaction.
class Withdraw(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(self, account):
        success_transaction = account.withdraw(self.amount)

        if success_transaction:
            account.history.add_transaction(self)


# Define the Deposit class that inherits from Transaction.
class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(self, account):
        success_transaction = account.deposit(self.amount)

        if success_transaction:
            account.history.add_transaction(self)


# Define the menu function.
def menu():
    menu = """\n
    Welcome to AG Bank!

    Please, select an option:

    [1]\tDeposit
    [2]\tWithdraw
    [3]\tBank Statement
    [4]\tCreate new account
    [5]\tList all accounts
    [6]\tCreate new user
    [0]\tExit

    => """
    return input(textwrap.dedent(menu))


# Define the filter_user function to filter users by CPF.
def filter_user(cpf, users):
    users_filtered = [user for user in users if user.cpf == cpf]
    return users_filtered[0] if users_filtered else None


# Define the recover_account_user function to recover the user's account.
def recover_account_user(user):
    if not user.accounts:
        print("\nUser has no accounts!")
        input("Press <Enter> to continue...")
        return

    return user.accounts[0]


# Define deposit function to deposit money into the account.
def deposit(users):
    cpf = input("\nPlease, enter your CPF: ")
    user = filter_user(cpf, users)

    if not user:
        print("\nUser not found!")
        input("Press <Enter> to continue...")
        return

    amount = float(input("\nEnter the amount to deposit: "))
    transaction = Deposit(amount)

    account = recover_account_user(user)
    if not account:
        return

    user.make_transaction(account, transaction)


# Define withdraw function to withdraw money from the account.
def withdraw(users):
    cpf = input("\nPlease, enter your CPF: ")
    user = filter_user(cpf, users)

    if not user:
        print("\nUser not found!")
        input("Press <Enter> to continue...")
        return

    amount = float(input("\nEnter the amount to withdraw: "))
    transaction = Withdraw(amount)

    account = recover_account_user(user)
    if not account:
        return

    user.make_transaction(account, transaction)


# Define show_bank_statement function to show the user's bank statement.
def show_bank_statement(users):
    cpf = input("\nPlease, enter your CPF: ")
    user = filter_user(cpf, users)

    if not user:
        print("\nUser not found!")
        input("Press <Enter> to continue...")
        return

    account = recover_account_user(user)
    if not account:
        return

    print("\nBank statement:\n")
    transactions = account.history.transactions

    bank_statement = ""
    if not transactions:
        bank_statement = "\nNo transactions made."
        input("Press <Enter> to continue...")
    else:
        for transaction in transactions:
            bank_statement += (
                f"\n{transaction['type']}:\n\t$ {transaction['amount']:.2f}")

    print(bank_statement)
    print(f"\nBalance: {account.balance:.2f}")
    print("\nEnd of bank statement.\n")
    input("Press <Enter> to continue...")
    os.system("cls")


# Define create_user function to create a new user.
def create_user(users):
    cpf = input("\nPlease, enter your CPF: ")
    user = filter_user(cpf, users)

    if user:
        print("\nUser already exists!")
        print("Please, try again with a different CPF.")
        input("\nPress <Enter> to continue...")
        return

    name = input("\nEnter your full name: ")
    birth_date = input("\nEnter your birth date (dd/mm/yyyy): ")
    address = input("\nEnter your address: (street, number, city, state) ")

    user = Person(name=name, birth_date=birth_date, cpf=cpf, address=address)

    users.append(user)

    print("\nUser successfully registered!\n")
    input("Press <Enter> to continue...")


# Define create_account function to create a new account.
def create_account(account_number, users, accounts):
    cpf = input("\nPlease, enter your CPF: ")
    user = filter_user(cpf, users)

    if not user:
        print("\nUser not found! Please, try again.")
        input("Press <Enter> to continue...")
        return

    account = Checking_Account.new_account(
        user=user, number=account_number)
    accounts.append(account)
    user.accounts.append(account)

    print("\nAccount successfully registered!\n")
    input("Press <Enter> to continue...")


# Define list_accounts function to list all accounts.
def list_accounts(accounts):
    for account in accounts:
        print("=" * 50)
        print(textwrap.dedent(str(account)))
    print("List of all accounts:\n")
    input("Press <Enter> to continue...")


# Define the main function to run the program.
def main():
    users = []
    accounts = []

    while True:
        option = menu()
        # os.system is used to clear the screen.
        os.system("cls")

        if option == "1":
            deposit(users)
            os.system("cls")

        elif option == "2":
            withdraw(users)
            os.system("cls")

        elif option == "3":
            show_bank_statement(users)
            os.system("cls")

        elif option == "4":
            account_number = len(accounts) + 1
            create_account(account_number, users, accounts)
            os.system("cls")

        elif option == "5":
            list_accounts(accounts)
            os.system("cls")

        elif option == "6":
            create_user(users)
            os.system("cls")

        elif option == "0":
            print("\nThank you for using AG Bank! See you soon!\n")
            break

        else:
            print("\nInvalid option! Please, try again.")
            input("Press <Enter> to continue...")
            os.system("cls")


# Call the main function.
main()
