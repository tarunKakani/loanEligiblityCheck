from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def calculate_eligibility(loan_amount, income, employment_status, job_type, credit_score, account_balance, account_tenure, past_loan_history, savings_months, mab, collateral_value):
    score = 0
    loan_amount = float(loan_amount)
    income = float(income)
    credit_score = float(credit_score)
    account_balance = float(account_balance)
    account_tenure = float(account_tenure)
    savings_months = float(savings_months)
    mab = float(mab)
    collateral_value = float(collateral_value)

    # Income classification
    if income >= 100000:
        score += 30  # Best
    elif income >= 50000:
        score += 20  # Good
    else:
        score += 10  # Low income, suggest government loans

    # Employment status
    if employment_status.lower() == "full-time":
        score += 20
    elif employment_status.lower() == "part-time":
        score += 10
    else:
        score += 5  # Unemployed

    # Job type
    if job_type.lower() == "salaried":
        score += 20
    elif job_type.lower() == "self-employed":
        score += 10  # Less reliable

    # Credit score
    if credit_score >= 750:
        score += 30
    elif credit_score >= 650:
        score += 20
    else:
        score += 10

    # Account balance vs. loan amount
    if account_balance >= loan_amount * 0.2:
        score += 20
    else:
        score += 10

    # Account tenure
    if account_tenure >= 3:
        score += 10
    elif account_tenure >= 1:
        score += 5

    # Past loan history
    if past_loan_history.lower() in ["good", "none"]:
        score += 10

    # Savings months
    if savings_months >= 3:
        score += 10
    else:
        score += 5

    # Minimum Average Balance
    if mab >= 5000:
        score += 15
    else:
        score += 5

    # Collateral Evaluation
    if collateral_value >= loan_amount * 0.8:
        score += 30
    elif collateral_value >= loan_amount * 0.5:
        score += 20
    else:
        score += 10

    return score

@app.route("/", methods=["GET"])
def main():
    return render_template("main.html")

@app.route("/select-loan", methods=["POST"])
def select_loan():
    loan_type = request.form.get("loan_type")
    if loan_type == "personal":
        return redirect(url_for('index'))
    else:
        return "Loan type not supported yet. Coming soon!"

@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        loan_amount = float(request.form.get("loan_amount", 0) or 0)
        income = float(request.form.get("income", 0) or 0)
        employment_status = request.form.get("employment_status")
        job_type = request.form.get("job_type")
        credit_score = float(request.form.get("credit_score", 0) or 0)
        account_balance = float(request.form.get("account_balance", 0) or 0)
        account_tenure = float(request.form.get("account_tenure", 0) or 0)
        past_loan_history = request.form.get("past_loan_history")
        savings_months = float(request.form.get("savings_months", 0) or 0)
        mab = float(request.form.get("mab", 0) or 0)
        collateral_value = float(request.form.get("collateral_value", 0) or 0)

        eligibility_score = calculate_eligibility(
            loan_amount, income, employment_status, job_type, credit_score, 
            account_balance, account_tenure, past_loan_history, 
            savings_months, mab, collateral_value
        )

        approved = eligibility_score >= 100

        # Suggest government loans if income is too low
        government_suggestion = ""
        if income < 30000:
            government_suggestion = "You might be eligible for government loan schemes like Mudra Yojana or PMEGP."

        return render_template("result.html", score=eligibility_score, approved=approved, government_suggestion=government_suggestion)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
