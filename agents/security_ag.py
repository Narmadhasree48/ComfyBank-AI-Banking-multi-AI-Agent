
from sqlalchemy.orm import Session

from database.models import Customer
from backend.auth import login_user


class SecurityAgent:

    def verify_login(
        self,
        db: Session,
        account_number: str,
        password: str
    ):
        customer = login_user(
            db,
            account_number,
            password
        )

        if not customer:
            return {
                "verified": False,
                "message": "Invalid account number or password"
            }

        return {
            "verified": True,
            "message": "Login verification successful",
            "customer_name": customer.name
        }

    def verify_account(
        self,
        db: Session,
        account_number: str,
        phone: str,
        last_four_digits: str
    ):
        customer = db.query(Customer).filter(
            Customer.account_number == account_number
        ).first()

        if not customer:
            return {"verified": False, "message": "Account verification failed"}

        if customer.phone != phone:
            return {"verified": False, "message": "Account verification failed"}

        if customer.account_number[-4:] != last_four_digits:
            return {"verified": False, "message": "Account verification failed"}

        return {
            "verified": True,
            "message": "Account details verified"
        }
