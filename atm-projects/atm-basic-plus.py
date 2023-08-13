import textwrap
import os


def menu():
    menu = """\n
    Welcome to AG Bank!

    Please, select an option:

    [1]\tDeposit
    [2]\tWithdraw
    [3]\tBank Statement
    [4]\tCreate new user
    [5]\tCreate new account
    [6]\tList all accounts
    [0]\tExit

    => """
    return int(input(textwrap.dedent(menu)))


def deposit(balance, amount, bank_statement, /):
    if amount > 0:
        balance += amount
        bank_statement += f"\nDeposited:\t\t$ {amount:.2f}\n"
        print("\nSuccess! The operation has been completed.")
        input("Press <Enter> to continue...")
    else:
        print("\nOperation failed! The amount entered is invalid.")
        input("Press <Enter> to continue...")

    return balance, bank_statement


def withdraw(*, balance, amount, bank_statement,
             limit, withdraw_count, withdraw_limit):

    exceeded_balance = amount > balance
    exceeded_limit = amount > limit
    exceeded_withdraw_limit = withdraw_count >= withdraw_limit

    if exceeded_balance:
        print("\nOperation failed! Insufficient funds.")
        input("Press <Enter> to continue...")
    elif exceeded_limit:
        print("\nOperation failed! The amount entered is invalid.")
        input("Press <Enter> to continue...")
    elif exceeded_withdraw_limit:
        print(
            "\nYou have exceeded the number of withdrawals allowed.")
        input("Press <Enter> to continue...")

    elif amount > 0:
        balance -= amount
        bank_statement += f"Withdrawn:\t\t$ {amount:.2f}\n"
        withdraw_count += 1
        print("\nSuccess! The operation has been completed.")
        input("Press <Enter> to continue...")

    else:
        print("\nOperation failed! Please, try again.")
        input("Press <Enter> to continue...")

    return balance, bank_statement


def list_bank_statement(balance, /, *, bank_statement):
    print("\nBank Statement")
    print("No transactions made." if not bank_statement else bank_statement)
    print(f"\nBalance:\t\t$ {balance:.2f}\n")
    print("End of bank statement")
    input("Press <Enter> to continue...")
    os.system("cls")


def create_user(users):
    cpf = input("Please, enter your CPF: ")
    user = filter_user(cpf, users)

    if user:
        print("\nCPF already registered.")
        input("Press <Enter> to continue...")
        return

    name = input("Please, enter your full name: ")
    birth_date = input("Please, enter your birth date (dd-mm-yyyy): ")
    address = input(
        "Please, enter your address (Street, Nº, Neighborhood, City/State): ")

    users.append({"name": name, "birth_date": birth_date,
                  "cpf": cpf, "address": address})
    print("User successfully registered!")
    input("Press <Enter> to continue...")


def create_account(branch, account_number, users):
    cpf = input("Please, enter your CPF: ")
    user = filter_user(cpf, users)

    if user:
        print("\nAccount successfully registered!")
        input("Press <Enter> to continue...")
        return {"branch": branch,
                "account_number": account_number, "user": user}

    print("\nOperation failed! User not found.")
    input("Press <Enter> to continue...")


def list_accounts(accounts):
    for account in accounts:
        line = f"""\
            Branch:\t\t{account['branch']}
            C/C:\t\t{account['account_number']}
            Owner:\t\t{account['user']['name']}
        """
        print("=" * 50)
        print(textwrap.dedent(line))
    input("Press <Enter> to continue...")


def filter_user(cpf, users):
    filtered_users = [user for user in users if user["cpf"] == cpf]
    return filtered_users[0] if filtered_users else None


def main():
    WITHDRAW_LIMIT = 3
    BRANCH = "0001"

    balance = 0
    limit = 500
    bank_statement = ""
    withdraw_count = 0
    users = []
    accounts = []

    while True:
        option = menu()
        os.system("cls")

        if option == 1:
            amount = float(input("Please, enter the amount to be deposited: "))

            balance, bank_statement = deposit(balance, amount, bank_statement)

        elif option == 2:
            amount = float(input("Please, enter the amount to be withdrawn: "))

            balance, bank_statement = withdraw(
                balance=balance,
                amount=amount,
                bank_statement=bank_statement,
                limit=limit,
                withdraw_count=withdraw_count,
                withdraw_limit=WITHDRAW_LIMIT,
            )

        elif option == 3:
            list_bank_statement(balance, bank_statement=bank_statement)

        elif option == 4:
            create_user(users)

        elif option == 5:
            account_number = len(accounts) + 1
            account = create_account(BRANCH, account_number, users)

            if account:
                accounts.append(account)

        elif option == 6:
            list_accounts(accounts)

        elif option == 0:
            print("Thank you for using AG Bank. See you soon!")
            break

        else:
            print("Invalid option. Please, try again.")
            input("Press <Enter> to continue...")


main()
