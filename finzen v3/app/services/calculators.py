class FinancialCalculator:
    @staticmethod
    def loan_emi(principal, annual_rate, tenure_years):
        p = principal
        r = (annual_rate / 100) / 12
        n = tenure_years * 12
        if r == 0: return p / n
        return round((p * r * ((1 + r) ** n)) / (((1 + r) ** n) - 1), 2)

    @staticmethod
    def sip_future_value(monthly_investment, annual_rate, years):
        p = monthly_investment
        i = (annual_rate / 100) / 12
        n = years * 12
        fv = p * ((((1 + i) ** n) - 1) / i) * (1 + i)
        return round(fv, 2)

    @staticmethod
    def retirement_corpus_need(current_monthly_expense, inflation_rate, years_to_retire, years_in_retire, return_rate):
        r_inf = inflation_rate / 100
        fv_expense_annual = (current_monthly_expense * ((1 + r_inf) ** years_to_retire)) * 12
        r_inv = return_rate / 100
        real_rate = (1 + r_inv) / (1 + r_inf) - 1
        
        if real_rate == 0:
            corpus = fv_expense_annual * years_in_retire
        else:
            corpus = fv_expense_annual * (1 - (1 + real_rate) ** (-years_in_retire)) / real_rate
        return round(corpus, 2)