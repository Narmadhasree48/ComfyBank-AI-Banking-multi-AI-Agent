
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Query
from agents.supervisor_ag import SupervisorAgent
from pydantic import BaseModel, Field
from database.models import Customer
from backend.auth import pwd_context
import math

from database.db import SessionLocal
from backend.auth import (
    login_user,
    create_access_token,
    verify_access_token,
    oauth2_scheme
)
from database.models import Transaction, Customer
class ChatRequest(BaseModel):
    message: str
    principal: float | None = None
    annual_interest_rate: float | None = None
    tenure_months: int | None = None

class RegisterRequest(BaseModel):

    customer_name: str = Field(min_length=2, max_length=100)
    account_number: str = Field(min_length=8, max_length=20)
    phone: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=8, max_length=72)
    ifsc_code: str = Field(min_length=4, max_length=15)
class ResetPasswordRequest(BaseModel):
    account_number: str
    new_password: str = Field(min_length=8, max_length=72)

class TransferRequest(BaseModel):
    receiver_account: str = Field(min_length=8, max_length=20)
    amount: float = Field(gt=0)

app = FastAPI(title="AI Banking Assistant")

supervisor = SupervisorAgent()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/demo/reset-password")
def reset_demo_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.account_number == request.account_number
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.password_hash = pwd_context.hash(
        request.new_password
    )

    try:
        db.commit()
        return {
            "message": "Demo password reset successful"
        }
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Password reset failed"
        )

@app.post("/demo/add-balance/{account_number}")
def add_demo_balance(
    account_number: str,
    amount: float = Query(gt=0, le=100000),
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.account_number == account_number
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.balance += amount

    try:
        db.commit()
        db.refresh(customer)
        return {
            "message": "Demo balance added",
            "account_number": customer.account_number,
            "balance": round(customer.balance, 2)
        }
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to add demo balance"
        )

@app.get("/")
def home():
    return {"message": "Bank API--->is okayrunning"}


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    customer = login_user(
        db,
        form_data.username,  # Phone number
        form_data.password
    )

    if not customer:
        raise HTTPException(
            status_code=401,
            detail="Invalid phone number or password"
        )

    access_token = create_access_token(customer.account_number)

    return {
    "access_token": access_token,
    "token_type": "bearer",
    "account_number": customer.account_number
}


@app.get("/transactions/{account_number}")
def get_transactions(
    account_number: str,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    token_account = verify_access_token(token)

    if token_account != account_number:
        raise HTTPException(
        status_code=403,
        detail="You cannot access another account"
    )
    customer = db.query(Customer).filter(
        Customer.account_number == account_number
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    transactions = db.query(Transaction).filter(
        Transaction.customer_id == customer.id
    ).all()
    return {
    "customer_name": customer.name,
    "transactions": [
        {
            "date": (
                transaction.created_at.strftime("%d-%m-%Y %I:%M %p")
                if transaction.created_at
                else "Date unavailable"
            ),
            "type": transaction.transaction_type,
            "amount": transaction.amount,
            "description": transaction.description,
            "status": transaction.status,
            "date": str(transaction.created_at) if transaction.created_at else "Date unavailable"
        }
        for transaction in transactions
    ]
}


@app.get("/balance/{account_number}")
def get_balance(
    account_number: str,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    token_account = verify_access_token(token)

    if token_account != account_number:
        raise HTTPException(
            status_code=403,
            detail="You cannot access another account"
        )

    customer = db.query(Customer).filter(
        Customer.account_number == account_number
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "customer_name": customer.name,
        "account_number": customer.account_number,
        "balance": round(customer.balance, 2)
    }


@app.get("/loan-emi")
def calculate_loan_emi(
    principal: float = Query(gt=0),
    annual_interest_rate: float = Query(ge=0),
    tenure_months: int = Query(gt=0)
):
    monthly_rate = annual_interest_rate / (12 * 100)

    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        factor = (1 + monthly_rate) ** tenure_months

        emi = (
            principal
            * monthly_rate
            * factor
            / (factor - 1)
        )

    total_payment = emi * tenure_months
    total_interest = total_payment - principal

    return {
        "principal": round(principal, 2),
        "annual_interest_rate": annual_interest_rate,
        "tenure_months": tenure_months,
        "monthly_emi": round(emi, 2),
        "total_interest": round(total_interest, 2),
        "total_payment": round(total_payment, 2)
    }
    
@app.get("/agent/loan-emi")
def agent_loan_emi(
    principal: float = Query(gt=0),
    annual_interest_rate: float = Query(ge=0),
    tenure_months: int = Query(gt=0)
):
    return supervisor.process_request(
        "loan_emi",
        principal=principal,
        annual_interest_rate=annual_interest_rate,
        tenure_months=tenure_months
    )

@app.get("/agent/balance/{account_number}")
def agent_balance(
    account_number: str,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    token_account = verify_access_token(token)

    if token_account != account_number:
        raise HTTPException(
            status_code=403,
            detail="You cannot access another account"
        )

    return supervisor.process_request(
        "balance",
        db=db,
        account_number=account_number
    )


@app.post("/agent/chat")
def agent_chat(
    request: ChatRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    token_account = verify_access_token(token)

    request_type = supervisor.detect_request_type(
        request.message
    )

    if request_type == "balance":
        result = supervisor.process_request(
            "balance",
            db=db,
            account_number=token_account
        )

    elif request_type == "transactions":
        result = supervisor.process_request(
            "transactions",
            db=db,
            account_number=token_account
        )

    
    elif request_type == "loan_emi":
        if (
            request.principal is None
            or request.annual_interest_rate is None
            or request.tenure_months is None
        ):
            return {
                "message": (
                    "Please provide principal, annual interest "
                    "rate, and tenure in months."
                )
            }

        result = supervisor.process_request(
            "loan_emi",
            principal=request.principal,
            annual_interest_rate=request.annual_interest_rate,
            tenure_months=request.tenure_months
        )

        return {
            "detected_request": request_type,
            "result": result
        }


    else:
        return {
            "message": "I can help with account balance, transactions, and loan EMI."
        }

    return {
        "detected_request": request_type,
        "result": result
    }

@app.post("/transfer")
def transfer_money(
    request: TransferRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    sender_account = verify_access_token(token)

    if sender_account == request.receiver_account:
        raise HTTPException(
            status_code=400,
            detail="Cannot transfer to your own account"
        )

    sender = db.query(Customer).filter(
        Customer.account_number == sender_account
    ).first()

    receiver = db.query(Customer).filter(
        Customer.account_number == request.receiver_account
    ).first()

    if not sender or not receiver:
        raise HTTPException(
            status_code=404,
            detail="Sender or receiver account not found"
        )

    if request.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero"
        )

    if sender.balance < request.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    try:
        sender.balance -= request.amount
        receiver.balance += request.amount

        db.add_all([
            Transaction(
                customer_id=sender.id,
                transaction_type="DEBIT",
                amount=request.amount,
                description=f"Transfer to {receiver.account_number}",
                status="SUCCESS"
            ),
            Transaction(
                customer_id=receiver.id,
                transaction_type="CREDIT",
                amount=request.amount,
                description=f"Transfer from {sender.account_number}",
                status="SUCCESS"
            )
        ])

        db.commit()

        return {
            "message": "Transfer successful",
            "amount": request.amount,
            "receiver_account": receiver.account_number,
            "remaining_balance": round(sender.balance, 2)
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Transfer failed"
        )

@app.post("/register")
def register_customer(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing_customer = db.query(Customer).filter(
        (Customer.account_number == request.account_number)
        | (Customer.phone == request.phone)
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=409,
            detail="Account number or phone number already registered"
        )

    customer = Customer(
        name=request.customer_name,
        account_number=request.account_number,
        phone=request.phone,
        ifsc_code=request.ifsc_code,
        password_hash=pwd_context.hash(request.password),
        balance=0.0
    )

    try:
        db.add(customer)
        db.commit()
        db.refresh(customer)

        return {
            "message": "Customer registered successfully",
            "account_number": customer.account_number
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )

