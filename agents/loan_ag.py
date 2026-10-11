
class LoanAgent:

    def calculate_emi(
        self,
        principal: float,
        annual_interest_rate: float,
        tenure_months: int
    ):
        if principal <= 0 or tenure_months <= 0:
            return {"error": "Principal and tenure must be positive"}

        if annual_interest_rate < 0:
            return {"error": "Interest rate cannot be negative"}

        monthly_rate = annual_interest_rate / (12 * 100)

        if monthly_rate == 0:
            emi = principal / tenure_months
        else:
            factor = (1 + monthly_rate) ** tenure_months
            emi = principal * monthly_rate * factor / (factor - 1)

        total_payment = emi * tenure_months

        return {
            "principal": round(principal, 2),
            "annual_interest_rate": annual_interest_rate,
            "tenure_months": tenure_months,
            "monthly_emi": round(emi, 2),
            "total_interest": round(total_payment - principal, 2),
            "total_payment": round(total_payment, 2)
        }
