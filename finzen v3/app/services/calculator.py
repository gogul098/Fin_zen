class TaxCalculator:
    @staticmethod
    def calculate_tax(income, regime="new"):
        """
        Simple Indian Tax Calculation (FY 2024-25 estimation)
        """
        tax = 0
        slabs = []
        
        if regime == "new":
            # New Regime Slabs (Standard Deduction 75k assumed for FY25 forecast, using 50k current for safety)
            # 0-3L: 0
            # 3-7L: 5%
            # 7-10L: 10%
            # 10-12L: 15%
            # ... simplified logical steps
            
            taxable_income = max(0, income - 50000) # Standard Deduction
            
            if taxable_income <= 300000:
                return 0, "No Tax"
                
            # Quick estimation logic
            if taxable_income <= 700000:
                 # Rebate u/s 87A applies if taxes < 25k (approx 7L limit)
                 return 0, "Rebate u/s 87A Applied"
            
            # Simple progressive logic for estimation
            remaining = taxable_income
            
            # 0-3L
            remaining -= 300000
            
            # 3L-6L (5%)
            slab_amount = min(remaining, 300000)
            tax += slab_amount * 0.05
            remaining -= slab_amount
            
            # 6L-9L (10%)
            if remaining > 0:
                slab_amount = min(remaining, 300000)
                tax += slab_amount * 0.10
                remaining -= slab_amount
                
            # 9L-12L (15%)
            if remaining > 0:
                slab_amount = min(remaining, 300000)
                tax += slab_amount * 0.15
                remaining -= slab_amount
                
            # 12L-15L (20%)
            if remaining > 0:
                slab_amount = min(remaining, 300000)
                tax += slab_amount * 0.20
                remaining -= slab_amount
                
            # >15L (30%)
            if remaining > 0:
                tax += remaining * 0.30
                
        else:
             # Old Regime (Complex, ignoring for MVP demo simplicity or implementing flat logic)
             # return a rough estimate
             tax = income * 0.20 # Dummy fallback
             
        # Cess 4%
        tax += tax * 0.04
        return round(tax, 2), "New Regime Estimate"

class SIPCalculator:
    @staticmethod
    def calculate_future_value(monthly_investment, rate, years):
        i = rate / 100 / 12
        n = years * 12
        fv = monthly_investment * ((((1 + i)**n) - 1) / i) * (1 + i)
        return round(fv, 2)

class InsuranceAdvisor:
    @staticmethod
    def suggest_coverage(age, annual_income, dependents=2):
        suggestions = []
        
        # Term Life
        cover_multiplier = 20 if age < 35 else 15
        term_cover = annual_income * cover_multiplier
        suggestions.append({
            "type": "Term Life",
            "cover_amount": term_cover,
            "reason": f"{cover_multiplier}x Annual Income",
            "est_premium_monthly": term_cover * 0.0002 # Rough estimation rule
        })
        
        # Health
        base_health = 500000 + (dependents * 200000)
        suggestions.append({
            "type": "Health Insurance",
            "cover_amount": base_health,
            "reason": f"Base 5L + 2L per dependent",
            "est_premium_monthly": base_health * 0.003 # Rough estimation
        })
        
        return suggestions
