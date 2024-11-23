from mainframe_demo.state_manager.story_state import process_business_rule
import logging

logging.basicConfig(level=logging.INFO)

def main():
    # Example business rule
    business_rule = """
    Business Rule: Bank Account Opening System
    Input Validation:

    The system prompts the user to enter mandatory account details:
    A 10-digit Account Number.
    An Account Holder Name (up to 30 characters).
    An Account Type (either "Savings" or "Current").
    An Initial Deposit Amount (in numeric format, e.g., 1000.00).
    All inputs must be provided before the account can be created.
    Account Type Selection:

    The Account Type is determined by the user selection and can only be:
    Savings
    Current
    Account Creation Logic:

    For each account:
    The system collects input data (Account Number, Name, Type, and Initial Deposit).
    The input data is written as a new record into the Account Master File (AccountData.dat).
    Data is written in line-sequential file format, where each record consists of:
    Account Number (10 digits, numeric).
    Account Holder Name (30 characters, alphanumeric).
    Account Type (Savings/Current, alphanumeric).
    Initial Deposit Amount (numeric with two decimal places).
    Iteration Logic:

    The system allows users to open multiple accounts in a single session.
    After creating an account, the user is prompted:
    "Do you want to enter another account? (Y/N)"
    If the user selects Y, the system repeats the account creation process.
    If the user selects N, the system terminates the session.
    File Handling:

    The Account Master File (AccountData.dat):
    Is opened in EXTEND mode, allowing new records to be appended without overwriting existing data.
    Each account record is written to the file upon creation.
    The file is closed immediately after the record is written to ensure data integrity.
    Output:

    A confirmation message, "Account successfully created!", is displayed after each account is added.
    Exit Condition:

    The system ends the session when the user selects N (No) to the prompt for adding another account.
    Expressed as Pseudo-Business Rules
    Validate Input: All fields are mandatory.
    Allow Multiple Accounts: Prompt the user for multiple account creation in one session.
    File Management: Append account details to the AccountData.dat file after each account creation.
    Exit Logic: Allow the user to end the session by choosing not to create additional accounts.
    """
    
    # Process the business rule
    result = process_business_rule(business_rule)
    
    if result["status"] == "success":
        print("\nGenerated User Story:")
        print(result["story"])
    else:
        print("\nError:")
        print(result.get("errors") or result.get("error"))

if __name__ == "__main__":
    main()
