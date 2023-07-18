balance = 0
limit = 500
bank_statement = ""
withdrawal_count = 0
WITHDRAWAL_LIMIT = 3

menu = """

Welcome to AG Bank!

Please, select an option:

[1] Deposit
[2] Withdraw
[3] Bank Statement
[0] Exit

=> """

while True:

    option = input(menu)

    if option == "1":
        amount = float(input("Enter the deposit amount: "))

        if amount > 0:
            balance += amount
            bank_statement += f"Deposit: $ {amount:.2f}\n"
            print("Success! The operation has been completed.")
            input("Press <Enter> to continue...")
        else:
            print("Operation failed! The amount entered is invalid.")
            input("Press <Enter> to continue...")

    elif option == "2":
        amount = float(input("Enter the withdrawal amount: "))

        exceeded_balance = amount > balance

        exceeded_limit = amount > limit

        exceeded_withdrawals = withdrawal_count >= WITHDRAWAL_LIMIT

        if exceeded_balance:
            print("Operation failed! You have insufficient balance.")

        elif exceeded_limit:
            print("Operation failed! The withdrawal amount exceeds the limit.")

        elif exceeded_withdrawals:
            print("Operation failed! Maximum number of withdrawals exceeded.")

        elif amount > 0:
            balance -= amount
            bank_statement += f"Withdrawal: $ {amount:.2f}\n"
            withdrawal_count += 1
            print("Success! The operation has been completed.")
            input("Press <Enter> to continue...")

        else:
            print("Operation failed! The amount entered is invalid.")

    elif option == "3":
        print("\nBank Statement\n")
        print("No transactions made."
              if not bank_statement else bank_statement)
        print(f"\nBalance: $ {balance:.2f}\n")
        input("Press <Enter> to continue...")

    elif option == "0":
        print("Your session has been successfully concluded.")
        break

    else:
        print("Invalid operation. Please, try again.")
        input("Press <Enter> to continue...")
