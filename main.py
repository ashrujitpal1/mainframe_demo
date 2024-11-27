from mainframe_demo.state_manager.story_state import process_business_rule
import logging

logging.basicConfig(level=logging.INFO)

def main():
    # Example business rule
    business_rule = """
        The following business rules are extracted from the COBOL program for the Loan Management System, tailored to a modern development perspective:

        1. Loan Account Management
        Loan Account Creation:

        Each loan account must have a unique Loan Account Number, a Customer Name, an Initial Loan Amount, and an Interest Rate.
        Loan accounts are categorized by status: Active, Closed.
        Loan Account Update:

        When a loan account is processed:
        If the status is Active, calculate and update the Outstanding Loan Amount with interest.
        Accounts with a balance of zero or less after repayment are marked as Closed.
        2. Input Validation
        All loan account details and transaction records must meet the following criteria:
        Loan Account Number: Unique, numeric, 10 digits.
        Customer Name: Alphanumeric, up to 30 characters.
        Interest Rate: Numeric, with up to two decimal places.
        Transaction Amount: Numeric, with up to two decimal places.
        Transactions must have a valid Transaction Type:
        DISBURSEMENT or REPAYMENT.
        3. Interest Calculation
        Formula:
        Updated Outstanding Amount = Outstanding Amount + (Outstanding Amount × Interest Rate / 100)
        Interest is added to the Outstanding Loan Amount only for active loans during processing.
        4. Loan Transactions
        Disbursement:
        Adds the transaction amount to the Outstanding Loan Amount of the specified loan account.
        Repayment:
        Subtracts the transaction amount from the Outstanding Loan Amount of the specified loan account.
        If the Outstanding Loan Amount becomes zero or negative, the loan account status is updated to Closed.
        Transactions are only applied to loan accounts with a matching Loan Account Number.
        5. File Handling
        Loan Account File:
        Stores loan account details including account number, customer name, loan amount, outstanding amount, interest rate, and status.
        Opened in line-sequential mode to ensure data integrity.
        Transaction File:
        Stores transaction records including account number, transaction type, and transaction amount.
        Processed sequentially to update loan accounts.
        Report File:
        Generates a loan management report summarizing account statuses after processing.
        6. Multi-Account Processing
        The system processes multiple loan accounts sequentially:
        Reads loan account records.
        Applies transactions from the Transaction File.
        After processing each transaction, the Loan Account File is updated immediately to prevent data loss or corruption.
        7. Reporting
        The system generates a Loan Management Report summarizing the results:
        Includes details of all processed accounts, outstanding balances, and their statuses.
        A header and separator are included for better readability.
        8. Error Handling
        If a transaction refers to an invalid or missing account number:
        Display an error message: "Account Not Found: [Account Number]".
        Invalid transaction types or missing details are flagged as errors and ignored.
        9. System Termination
        The system gracefully closes all files after processing.
        Displays a success message: "Loan Management System Terminated Successfully. 
    """
    
    # Process the business rule
    result = process_business_rule(business_rule)
    
    if result["status"] == "success":
        print("\nGenerated User Story:")
        print(result)
    else:
        print("\nError:")
        print(result.get("errors") or result.get("error"))

if __name__ == "__main__":
    main()
