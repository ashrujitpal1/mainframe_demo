from mainframe_demo.state_manager.story_state import process_business_rule
import logging

logging.basicConfig(level=logging.INFO)

def main():
    # Example business rule
    business_rule = """
        Result value: Modernized Business Rule Definition

        ### Domain Analysis

        The business capabilities extracted from the COBOL program for the Loan Management System can be mapped to the following DDD Subdomains:

        1. **Loan Management**
            * Bounded Context: Loan Account Management
            * Entities:
                + LoanAccount (with attributes: accountNumber, customerName, loanAmount, outstandingAmount, interestRate)
                + Transaction (with attributes: transactionType, transactionAmount)
            * Value Objects:
                + OutstandingAmount
                + InterestRate
        2. **Transaction Processing**
            * Bounded Context: Transaction Management
            * Entities:
                + LoanTransaction (with attributes: accountNumber, transactionType, transactionAmount)
            * Aggregates:
                + LoanAccountAggregate (comprising LoanAccount and its transactions)
        3. **Reporting and Analytics**
            * Bounded Context: Reporting
            * Entities:
                + Report (with attributes: reportDate, loanAccountStatuses)

        ### Entity and Context Mapping

        The mainframe-oriented data structures can be redefined as:

        1. **Loan Account**: Redefined as LoanAccount Entity with attributes accountNumber, customerName, loanAmount, outstandingAmount, interestRate
        2. **Transaction File**: Redefined as Transaction Entity with attributes transactionType, transactionAmount
        3. **Report File**: Redefined as Report Entity with attributes reportDate, loanAccountStatuses

        The COBOL programs or procedures can be mapped to potential Microservices:

        1. **Loan Account Management**: Map to LoanManagementMicroservice (handles creation, update, and retrieval of loan accounts)
        2. **Transaction Processing**: Map to TransactionProcessingMicroservice (handles processing of transactions and updating loan accounts)
        3. **Reporting and Analytics**: Map to ReportingMicroservice (generates reports on loan account statuses)

        ### Microservices Definition

        The microservices boundary for each business capability can be defined as:

        1. **Loan Management**: LoanManagementMicroservice
        2. **Transaction Processing**: TransactionProcessingMicroservice
        3. **Reporting and Analytics**: ReportingMicroservice

        **APIs:**

        1. **Loan Management**
            * `POST /loan-accounts`: Create a new loan account
            * `GET /loan-accounts/{accountNumber}`: Retrieve a loan account by account number
        2. **Transaction Processing**
            * `POST /transactions`: Process a transaction
            * `GET /transactions/{transactionId}`: Retrieve a transaction by ID
        3. **Reporting and Analytics**
            * `GET /reports`: Generate a report on loan account statuses

        ### Technical Requirements

        1. **Database Migration**: Migrate from IMS/VSAM to RDBMS (e.g., PostgreSQL) or NoSQL (e.g., MongoDB)
        2. **Caching Mechanisms**: Implement caching using Redis or Memcached for frequently accessed data
        3. **Event-Driven Architecture**: Use Apache Kafka or RabbitMQ as event store and message broker
        4. **Event-Driven Recommendations**:
            * Identify key business events: Loan Account Creation, Transaction Processing, Report Generation
            * Map these to Domain Events (e.g., `LoanAccountCreated`, `TransactionProcessed`, `ReportGenerated`)
        5. **Integration Considerations**: Use APIs or data pipelines for seamless mainframe-Java integration

        ### Acceptance Criteria

        1. Functional Requirements:
            * Correctly created and updated loan accounts
            * Successfully processed transactions
            * Generated accurate reports on loan account statuses
        2. Non-Functional Requirements:
            * Response time: < 500ms for API calls
            * Throughput: handle >1000 concurrent requests per second
            * Scalability: scale to >10000 instances

        ### Sample Design Blueprint

        ```
        +---------------+
        |  Loan Management  |
        +---------------+
                |
                |  POST /loan-accounts
                v
        +---------------+---------------+
        |  CreateLoanAccount  |
        +---------------+---------------+
                |
                |  GET /loan-accounts/{accountNumber}
                v
        +---------------+---------------+
        |  RetrieveLoanAccount  |
        +---------------+---------------+

        +---------------+
        | Transaction Processing  |
        +---------------+
                |
                |  POST /transactions
                v
        +---------------+---------------+
        |  ProcessTransaction  |
        +---------------+---------------+
                |
                |  GET /transactions/{transactionId}
                v
        +---------------+---------------+
        |  RetrieveTransaction  |
        +---------------+---------------+

        +---------------+
        | Reporting and Analytics  |
        +---------------+
                |
                |  GET /reports
                v
        +---------------+---------------+
        |  GenerateReport  |
        +---------------+---------------+
        ```

        This design blueprint provides a high-level overview of the modernized business rule definition, entity and context mapping, microservices definition, technical requirements, acceptance criteria, and sample design blueprint.
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
