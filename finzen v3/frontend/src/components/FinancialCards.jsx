import React from 'react';
import { motion } from 'framer-motion';
import { Shield, TrendingUp, Calculator, Building } from 'lucide-react';

export const InsuranceCard = ({ data }) => {
    if (!data) return null;

    return (
        <div className="space-y-4 w-full max-w-sm mt-3">
            {data.map((policy, idx) => (
                <motion.div
                    key={idx}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.1 }}
                    className="bg-finzen-card p-4 rounded-xl border border-blue-500/30 relative overflow-hidden"
                >
                    <div className="absolute top-0 right-0 p-3 opacity-10">
                        <Shield size={60} className="text-blue-500" />
                    </div>
                    <h4 className="font-bold text-lg text-blue-400 mb-1">{policy.type}</h4>
                    <div className="text-2xl font-bold mb-2">₹{(policy.cover_amount / 100000).toFixed(1)} Lakhs</div>
                    <p className="text-sm text-finzen-muted mb-2">{policy.reason}</p>
                    <div className="bg-slate-800/50 p-2 rounded text-xs flex justify-between">
                        <span>Est. Premium:</span>
                        <span className="font-bold text-white">~₹{Math.round(policy.est_premium_monthly)}/mo</span>
                    </div>
                </motion.div>
            ))}
        </div>
    );
};

export const SIPCard = ({ data }) => {
    if (!data) return null;

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-finzen-card p-4 rounded-xl border border-purple-500/30 w-full max-w-sm mt-3"
        >
            <div className="flex items-center gap-2 mb-3 text-purple-400">
                <TrendingUp size={20} />
                <span className="font-bold uppercase tracking-wider text-xs">SIP Projection</span>
            </div>

            <div className="flex justify-between items-end mb-4">
                <div>
                    <p className="text-finzen-muted text-xs">Monthly Inv.</p>
                    <p className="text-xl font-bold">₹{data.monthly}</p>
                </div>
                <div className="text-right">
                    <p className="text-finzen-muted text-xs">Duration</p>
                    <p className="text-xl font-bold">{data.years} Yrs</p>
                </div>
            </div>

            <div className="space-y-2 mb-4">
                <div className="flex justify-between text-sm">
                    <span className="text-finzen-muted">Invested Amount</span>
                    <span className="font-medium">₹{(data.invested / 100000).toFixed(2)}L</span>
                </div>
                <div className="flex justify-between text-lg font-bold text-emerald-400">
                    <span>Est. Returns</span>
                    <span>+₹{(data.gain / 100000).toFixed(2)}L</span>
                </div>
            </div>

            <div className="bg-gradient-to-r from-purple-600 to-indigo-600 p-3 rounded-lg text-center">
                <p className="text-xs text-purple-200 mb-1">Maturity Value</p>
                <p className="text-2xl font-bold text-white">₹{(data.fv / 100000).toFixed(2)} Lakhs</p>
            </div>
        </motion.div>
    );
};

export const TaxCard = ({ data }) => {
    if (!data) return null;

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-finzen-card p-4 rounded-xl border border-orange-500/30 w-full max-w-sm mt-3"
        >
            <div className="flex items-center gap-2 mb-3 text-orange-400">
                <Calculator size={20} />
                <span className="font-bold uppercase tracking-wider text-xs">Tax Estimate (FY25)</span>
            </div>

            <div className="flex justify-between items-center mb-4">
                <span className="text-finzen-muted">Taxable Income</span>
                <span className="font-bold">₹{(data.income / 100000).toFixed(2)}L</span>
            </div>

            <div className="bg-orange-500/10 border border-orange-500/50 p-4 rounded-lg text-center">
                <p className="text-sm text-orange-300 mb-1">Estimated Tax Liability</p>
                <p className="text-3xl font-bold text-orange-500">₹{data.tax.toLocaleString()}</p>
                <p className="text-xs text-finzen-muted mt-2">Regime: {data.regime}</p>
            </div>
        </motion.div>
    );
};

export const PropertyCard = ({ data }) => {
    // Placeholder for property listings
    return (
        <div className="text-finzen-muted text-sm mt-2 italic">
            Property search feature coming soon...
        </div>
    )
}
