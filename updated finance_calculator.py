#!/usr/bin/env python3


LINE_DOUBLE = "════════════════════════════════════════════"
LINE_SINGLE = "────────────────────────────────────────────"


def format_indian_currency(amount):
    amount = round(amount, 2)
    integer_part = int(amount)
    decimal_part = int((amount - integer_part) * 100)

    if integer_part == 0:
        indian_format = "0"
    else:
        s = str(integer_part)[::-1]
        result = s[:3]

        for i in range(3, len(s), 2):
            if i + 1 < len(s):
                result += "," + s[i:i+2]
            else:
                result += "," + s[i]

        indian_format = result[::-1]

    return f"₹{indian_format}.{decimal_part:02d}"


def get_valid_input(prompt, input_type=float, min_val=None, max_val=None):
    while True:
        try:
            user_input = input(prompt)

            if input_type == str:
                return user_input.strip()

            value = float(user_input)

            if min_val is not None and value <= min_val:
                print(f"Error: Value must be greater than {min_val}")
                continue

            if max_val is not None and value > max_val:
                print(f"Error: Value must be less than or equal to {max_val}")
                continue

            return value

        except ValueError:
            print("Error: Please enter a valid number")


def collect_employee_data(employee_num=1):
    print(f"\nEnter Employee {employee_num} Financial Information")
    print(LINE_SINGLE)

    employee_name = get_valid_input("Employee name: ", str)
    annual_salary = get_valid_input("Annual salary (₹): ", float, min_val=0)
    tax_percent = get_valid_input("Tax bracket (%): ", float, min_val=0, max_val=50)
    monthly_rent = get_valid_input("Monthly rent (₹): ", float, min_val=0)
    savings_percent = get_valid_input(
        "Savings goal (%): ", float, min_val=0, max_val=100
    )

    return {
        "name": employee_name,
        "annual_salary": annual_salary,
        "tax_percent": tax_percent,
        "monthly_rent": monthly_rent,
        "savings_percent": savings_percent
    }


def calculate_finances(data):
    monthly_salary = data["annual_salary"] / 12
    tax_amount = monthly_salary * (data["tax_percent"] / 100)
    net_salary = monthly_salary - tax_amount
    rent_ratio = (data["monthly_rent"] / net_salary) * 100 if net_salary > 0 else 0
    savings_amount = net_salary * (data["savings_percent"] / 100)
    disposable_income = net_salary - data["monthly_rent"] - savings_amount

    annual_tax = tax_amount * 12
    annual_savings = savings_amount * 12
    annual_rent = data["monthly_rent"] * 12

    disposable_pct = (disposable_income / net_salary) * 100 if net_salary > 0 else 0

    return {
        "monthly_salary": monthly_salary,
        "tax_amount": tax_amount,
        "net_salary": net_salary,
        "rent_ratio": rent_ratio,
        "savings_amount": savings_amount,
        "disposable_income": disposable_income,
        "disposable_pct": disposable_pct,
        "annual_tax": annual_tax,
        "annual_savings": annual_savings,
        "annual_rent": annual_rent
    }


def calculate_health_score(calculations, savings_percent):
    score = 0

    rent_ratio = calculations["rent_ratio"]
    if rent_ratio < 30:
        score += 40
    elif rent_ratio < 50:
        score += 20

    savings_score = min(savings_percent, 30)
    score += savings_score

    disposable_pct = calculations["disposable_pct"]
    disposable_score = min(disposable_pct / 2, 30)
    score += disposable_score

    if score >= 80:
        category = "Excellent"
    elif score >= 60:
        category = "Good"
    elif score >= 40:
        category = "Fair"
    else:
        category = "Poor"

    return round(score), category


def generate_report(employee_data, calculations, health_score, health_category):
    print("\n" + LINE_DOUBLE)
    print("EMPLOYEE FINANCIAL SUMMARY")
    print(LINE_DOUBLE)
    print(f"Employee       : {employee_data['name']}")
    print(f"Annual Salary  : {format_indian_currency(employee_data['annual_salary'])}")
    print(LINE_SINGLE)
    print("Monthly Breakdown:")
    print(f"Gross Salary   : {format_indian_currency(calculations['monthly_salary']):>18}")
    print(f"Tax ({employee_data['tax_percent']}%)    : "
          f"{format_indian_currency(calculations['tax_amount']):>18}")

    net_sal = format_indian_currency(calculations['net_salary'])
    print(f"Net Salary     : {net_sal:>18}")

    rent_str = format_indian_currency(employee_data['monthly_rent'])
    rent_pct = f"({calculations['rent_ratio']:.1f}% of net)"
    print(f"Rent           : {rent_str:>18} {rent_pct}")

    savings_str = format_indian_currency(calculations['savings_amount'])
    print(f"Savings ({employee_data['savings_percent']}%) : {savings_str:>18}")

    disposable = format_indian_currency(calculations['disposable_income'])
    print(f"Disposable     : {disposable:>18}")
    print(LINE_SINGLE)
    print("Annual Projection:")
    print(f"Total Tax      : {format_indian_currency(calculations['annual_tax']):>18}")
    print(f"Total Savings  : {format_indian_currency(calculations['annual_savings']):>18}")
    print(f"Total Rent     : {format_indian_currency(calculations['annual_rent']):>18}")
    print(LINE_SINGLE)
    print(f"Health Score   : {health_score}/100 ({health_category})")
    print(LINE_DOUBLE)


def generate_comparison(emp1_data, emp1_calc, emp1_score,
                        emp2_data, emp2_calc, emp2_score):
    print("\n" + LINE_DOUBLE)
    print("EMPLOYEE COMPARISON")
    print(LINE_DOUBLE)
    print(f"{'Metric':<25} {'Employee 1':>20} {'Employee 2':>20}")
    print(LINE_SINGLE)

    name1 = emp1_data['name'][:20]
    name2 = emp2_data['name'][:20]
    print(f"{'Name':<25} {name1:>20} {name2:>20}")

    sal1 = format_indian_currency(emp1_data['annual_salary'])
    sal2 = format_indian_currency(emp2_data['annual_salary'])
    print(f"{'Annual Salary':<25} {sal1:>20} {sal2:>20}")

    net1 = format_indian_currency(emp1_calc['net_salary'])
    net2 = format_indian_currency(emp2_calc['net_salary'])
    print(f"{'Monthly Net':<25} {net1:>20} {net2:>20}")

    rent1 = f"{emp1_calc['rent_ratio']:.1f}%"
    rent2 = f"{emp2_calc['rent_ratio']:.1f}%"
    print(f"{'Rent Ratio':<25} {rent1:>20} {rent2:>20}")

    sav1 = format_indian_currency(emp1_calc['savings_amount'])
    sav2 = format_indian_currency(emp2_calc['savings_amount'])
    print(f"{'Savings/Month':<25} {sav1:>20} {sav2:>20}")

    disp1 = format_indian_currency(emp1_calc['disposable_income'])
    disp2 = format_indian_currency(emp2_calc['disposable_income'])
    print(f"{'Disposable/Month':<25} {disp1:>20} {disp2:>20}")

    score1 = f"{emp1_score}/100"
    score2 = f"{emp2_score}/100"
    print(f"{'Health Score':<25} {score1:>20} {score2:>20}")
    print(LINE_DOUBLE)

    if emp1_score > emp2_score:
        winner = emp1_data['name']
        diff = emp1_score - emp2_score
        print(f"Winner: {winner} (by {diff} points)")
    elif emp2_score > emp1_score:
        winner = emp2_data['name']
        diff = emp2_score - emp1_score
        print(f"Winner: {winner} (by {diff} points)")
    else:
        print("Result: Both employees have equal financial health!")

    print(LINE_DOUBLE)


def main():
    print("PERSONAL FINANCE CALCULATOR")
    print("Part B: Indian Formatting + Comparison + Health Score")
    print(LINE_DOUBLE)

    employee1_data = collect_employee_data(1)
    employee1_calc = calculate_finances(employee1_data)
    employee1_score, employee1_category = calculate_health_score(
        employee1_calc, employee1_data['savings_percent']
    )

    employee2_data = collect_employee_data(2)
    employee2_calc = calculate_finances(employee2_data)
    employee2_score, employee2_category = calculate_health_score(
        employee2_calc, employee2_data['savings_percent']
    )

    generate_report(employee1_data, employee1_calc,
                    employee1_score, employee1_category)
    generate_report(employee2_data, employee2_calc,
                    employee2_score, employee2_category)

   

    generate_comparison(
        employee1_data, employee1_calc, employee1_score,
        employee2_data, employee2_calc, employee2_score
    )
    print("DEBUG: Entering generate_comparison")


if __name__ == "__main__":
    main()
