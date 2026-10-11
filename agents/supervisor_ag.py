
from agents.banking_ag import BankingAgent
from agents.loan_ag import LoanAgent


class SupervisorAgent:

    def __init__(self):
        self.banking_agent = BankingAgent()
        self.loan_agent = LoanAgent()
    
    def detect_request_type(self, message: str):
        message = message.lower()

        if any(word in message for word in [
            "balance", "how much money", "account balance"
        ]):
            return "balance"

        elif any(word in message for word in [
    "transaction", "transactions", "transactitailon",
    "transcation", "transactional", "spent", "spending"
        ]):
            return "transactions"

        elif any(word in message for word in [
            "emi", "loan", "monthly payment"
        ]):
            return "loan_emi"

        return "unknown"

    def process_request(
        self,
        request_type: str,
        **kwargs
    ):
        if request_type == "balance":
            return self.banking_agent.get_balance(
                kwargs["db"],
                kwargs["account_number"]
            )

        elif request_type == "transactions":
            return self.banking_agent.get_transactions(
                kwargs["db"],
                kwargs["account_number"]
            )

        elif request_type == "loan_emi":
            return self.loan_agent.calculate_emi(
                kwargs["principal"],
                kwargs["annual_interest_rate"],
                kwargs["tenure_months"]
            )

        else:
            return {
                "error": "Unsupported request type",
                "supported_requests": [
                    "balance",
                    "transactions",
                    "loan_emi"
                ]
            }
