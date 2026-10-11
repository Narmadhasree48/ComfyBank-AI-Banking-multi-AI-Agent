
from database.db import SessionLocal
from database.models import Customer, Transaction, Loan
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_database():
    db = SessionLocal()

    try:
        customer = db.query(Customer).filter_by(
            account_number="123456789012"
        ).first()

        if customer:
            print("Demo customer already exists!")
            return

        customer = Customer(
            name="Narmadha ",
            account_number="123456789012",
            ifsc_code="DEMO0001234",
            phone="9876543210",
            password_hash=pwd_context.hash("Bank@123")
        )

        db.add(customer)
        db.flush()

        db.add_all([
            Transaction(
                customer_id=customer.id,
                transaction_type="CREDIT",
                amount=15000,
                description="Demo salary credit",
                status="SUCCESS"
            ),
            Transaction(
                customer_id=customer.id,
                transaction_type="DEBIT",
                amount=1200,
                description="Shopping payment",
                status="SUCCESS"
            ),
            Loan(
                customer_id=customer.id,
                loan_type="Personal Loan",
                principal_amount=100000,
                interest_rate=10.5,
                tenure_months=24
            )
        ])

        db.commit()
        print("Demo banking data created successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
