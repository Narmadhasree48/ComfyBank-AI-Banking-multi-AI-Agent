
from sqlalchemy.orm import Session

from database.models import Customer, Transaction


class BankingAgent:

    def get_balance(self, db: Session, account_number: str):
        customer = db.query(Customer).filter(
            Customer.account_number == account_number
        ).first()

        if not customer:
            return {"error": "Customer not found"}

        transactions = db.query(Transaction).filter(
            Transaction.customer_id == customer.id,
            Transaction.status == "SUCCESS"
        ).all()

        balance = customer.balance

        for transaction in transactions:
            if transaction.transaction_type == "CREDIT":
                balance += transaction.amount
            elif transaction.transaction_type == "DEBIT":
                balance -= transaction.amount

        return {
            "customer_name": customer.name,
            "account_number": customer.account_number,
            "balance": round(balance, 2)
        }

    def get_transactions(self, db: Session, account_number: str):
        customer = db.query(Customer).filter(
            Customer.account_number == account_number
        ).first()

        if not customer:
            return {"error": "Customer not found"}

        transactions = db.query(Transaction).filter(
            Transaction.customer_id == customer.id
        ).all()

        return {
            "transactions": [
                {
                    "type": transaction.transaction_type,
                    "amount": transaction.amount,
                    "description": transaction.description,
                    "status": transaction.status,
                    "date": str(transaction.created_at) if transaction.created_at else "Date unavailable"
                }
                for transaction in transactions
            ]
        }
