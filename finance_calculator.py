#!/usr/bin/env python3
"""
Personal Finance Calculator for Employee Benefits Portal.

This module collects employee salary information and generates
a detailed financial summary report.
"""

# Constants for formatting
LINE_DOUBLE = "════════════════════════════════════════════"
LINE_SINGLE = "────────────────────────────────────────────"


def get_valid_input(prompt, input_type=float, min_val=None, max_val=None):
    """
    Get validated input from user.
    
    Args:
        prompt: Message to show user
        input_type: Expected type (float or str)
        min_val: Minimum allowed value (for numbers)
        max_val: Maximum allowed value (for numbers)
    
    Returns:
        Validated user input
    """
    while True:
        try:
            user_input = input(prompt)
            
            if input_type == str:
                return user_input.strip()
            
            # Convert to float for numeric inputs
            value = float(user_input)
            
            # Check minimum value
            if min_val is not None and value <= min_val:
                print(f"Error: Value must be greater than {min_val}")
                continue
            
            # Check maximum value
            if max_val is not None and value > max_val:
                print(f"Error: Value must be less than or equal to {max_val}")
                continue
            
            return value
            
        except ValueError:
            print("Error: Please enter a valid number")


def collect_employee_data():
    """
    Collect all employee financial data from user input.
    
    Returns:
        Dictionary containing employee data
    """
    print("Enter Employee Financial Information")
    print(LINE_SINGLE)
    
    employee_name = get_valid_input("Employee name: ", str)
    annual_salary = get_valid_input("Annual salary (₹): ", float, min_val=0)
    tax_percent = get_valid_input("Tax bracket (%): ", float, min_val=0, max_val=50)
    monthly_rent = get_valid_input("Monthly rent (₹): ", float, min_val=0)
    savings_percent = get_valid_input("Savings goal (%): ", float, min_val=0, max_val=100)
    
    return {
        "name": employee_name,
        "annual_salary": annual_salary,
        "tax_percent": tax_percent,
        "monthly_rent": monthly_rent,
        "savings_percent": savings_percent
    }


def calculate_finances(data):
    """
    Calculate all financial metrics from employee data.
    
    Args:
        data: Dictionary with employee financial data
    
    Returns:
        Dictionary with calculated results
    """
    monthly_salary = data["annual_salary"] / 12
    tax_amount = monthly_salary * (data["tax_percent"] / 100)
    net_salary = monthly_salary - tax_amount
    rent_ratio = (data["monthly_rent"] / net_salary) * 100 if net_salary > 0 else 0
    savings_amount = net_salary * (data["savings_percent"] / 100)
    disposable_income = net_salary - data["monthly_rent"] - savings_amount
    
    # Annual projections
    annual_tax = tax_amount * 12
    annual_savings = savings_amount * 12
    annual_rent = data["monthly_rent"] * 12
    
    return {
        "monthly_salary": monthly_salary,
        "tax_amount": tax_amount,
        "net_salary": net_salary,
        "rent_ratio": rent_ratio,
        "savings_amount": savings_amount,
        "disposable_income": disposable_income,
        "annual_tax": annual_tax,
        "annual_savings": annual_savings,
        "annual_rent": annual_rent
    }


def format_currency(amount):
    """
    Format amount as Indian Rupees with 2 decimal places.
    
    Args:
        amount: Number to format
    
    Returns:
        Formatted currency string
    """
    return f"₹{amount:,.2f}"


def generate_report(employee_data, calculations):
    """
    Generate and display formatted financial report.
    
    Args:
        employee_data: Dictionary with raw employee data
        calculations: Dictionary with calculated values
    """
    print("\n" + LINE_DOUBLE)
    print("EMPLOYEE FINANCIAL SUMMARY")
    print(LINE_DOUBLE)
    print(f"Employee       : {employee_data['name']}")
    print(f"Annual Salary  : {format_currency(employee_data['annual_salary'])}")
    print(LINE_SINGLE)
    print("Monthly Breakdown:")
    print(f"Gross Salary   : {format_currency(calculations['monthly_salary']):>14}")
    print(f"Tax ({employee_data['tax_percent']}%)    : {format_currency(calculations['tax_amount']):>14}")
    print(f"Net Salary     : {format_currency(calculations['net_salary']):>14}")
    
    rent_str = format_currency(employee_data['monthly_rent'])
    rent_pct = f"({calculations['rent_ratio']:.1f}% of net)"
    print(f"Rent           : {rent_str:>14} {rent_pct}")
    
    savings_str = format_currency(calculations['savings_amount'])
    print(f"Savings ({employee_data['savings_percent']}%) : {savings_str:>14}")
    print(f"Disposable     : {format_currency(calculations['disposable_income']):>14}")
    print(LINE_SINGLE)
    print("Annual Projection:")
    print(f"Total Tax      : {format_currency(calculations['annual_tax']):>14}")
    print(f"Total Savings  : {format_currency(calculations['annual_savings']):>14}")
    print(f"Total Rent     : {format_currency(calculations['annual_rent']):>14}")
    print(LINE_DOUBLE)


def main():
    """Main function to run the finance calculator."""
    employee_data = collect_employee_data()
    calculations = calculate_finances(employee_data)
    generate_report(employee_data, calculations)


if __name__ == "__main__":
    main()