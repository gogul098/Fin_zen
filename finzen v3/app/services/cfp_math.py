import numpy as np

class CFPLogicEngine:
    def __init__(self, user, debts):
        self.user = user
        self.debts = debts

    def run_monte_carlo(self, principal, years=5, simulations=1000):
        if principal <= 0: return 0.0
        mu, sigma = 0.12, 0.20 
        daily_returns = np.random.normal(mu/252, sigma/np.sqrt(252), (simulations, years * 252))
        price_paths = principal * np.cumprod(1 + daily_returns, axis=1)
        final_values = price_paths[:, -1]
        success = np.sum(final_values > principal)
        return round((success / simulations) * 100, 1)

    def calculate_recovery_metrics(self):
        """
        Calculates the exact math required to fix the user's financial health.
        Used for Advisory Mode.
        """
        # 1. Target Safety Net (3 Months Expenses)
        monthly_burn = self.user.monthly_fixed_expenses
        target_fund = monthly_burn * 3
        current_fund = self.user.emergency_fund_cash
        gap = target_fund - current_fund
        
        # 2. Cash Flow Analysis
        monthly_surplus = self.user.monthly_income - self.user.monthly_fixed_expenses
        
        # 3. Time to Recovery
        if monthly_surplus > 0 and gap > 0:
            months_to_fix = round(gap / monthly_surplus, 1)
        elif gap <= 0:
            months_to_fix = 0 # Already safe
        else:
            months_to_fix = 999 # Infinite (Deficit)

        return {
            "safety_gap": gap,
            "monthly_surplus": monthly_surplus,
            "months_to_recover": months_to_fix,
            "target_fund": target_fund
        }

    def run_analysis(self, investment_request_amount=0):
        metrics = {}
        logs = []
        
        # Savings Rate
        net_save = self.user.monthly_income - self.user.monthly_fixed_expenses
        sav_rate = (net_save / self.user.monthly_income) * 100 if self.user.monthly_income > 0 else 0
        metrics["savings_rate"] = round(sav_rate, 1)
        base_risk = 50
        
        # Emergency Fund
        monthly_burn = self.user.monthly_fixed_expenses
        cov = self.user.emergency_fund_cash / monthly_burn if monthly_burn > 0 else 0
        metrics["emergency_coverage"] = round(cov, 1)
        
        if cov < 3:
            base_risk += 35
            logs.append(f"CRITICAL: Emergency Fund only covers {cov} months (Needs 3-6).")

        # Investment Check
        if investment_request_amount > 0:
            if investment_request_amount > self.user.emergency_fund_cash:
                base_risk = 100
                logs.append("Insufficient cash.")
            else:
                prob = self.run_monte_carlo(investment_request_amount)
                if prob < 70: 
                    base_risk += 20
                    logs.append(f"Monte Carlo Warning: {prob}% success probability.")

        final_risk = max(1, min(base_risk, 100))
        metrics["risk_score"] = final_risk
        
        if final_risk <= 40: verdict = "APPROVE"
        elif final_risk <= 75: verdict = "WARNING"
        else: verdict = "REJECT"
        
        metrics["verdict"] = verdict
        metrics["logs"] = logs
        return metrics