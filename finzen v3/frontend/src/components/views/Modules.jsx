import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Shield, Home, Briefcase, Calculator } from 'lucide-react';
import { InsuranceCard, SIPCard, TaxCard } from '../FinancialCards';

// --- STOCKS VIEW ---
export const StocksView = () => {
    const [stocks, setStocks] = useState([]);
    const [buying, setBuying] = useState(null);

    useEffect(() => {
        axios.get('http://localhost:8001/recommendations/stock').then(res => setStocks(res.data));
    }, []);

    const handleBuy = async (symbol) => {
        setBuying(symbol);
        try {
            const res = await axios.post('http://localhost:8001/trade', {
                user_id: 1,
                symbol: symbol,
                amount: 100 // Default to $100 for simplicity
            });
            alert("✅ " + res.data.message);
        } catch (e) {
            alert("❌ " + (e.response?.data?.detail || "Trade Failed"));
        }
        setBuying(null);
    };

    return (
        <div className="p-6 space-y-6 h-full overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <Briefcase className="text-emerald-400" /> Market Recommendations
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {stocks.map((stock, idx) => (
                    <motion.div key={idx} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: idx * 0.1 }}
                        className="bg-finzen-card p-4 rounded-xl border border-slate-700/50 hover:border-emerald-500/50 transition-colors">
                        <div className="flex justify-between items-start mb-2">
                            <div>
                                <h3 className="font-bold text-lg">{stock.symbol}</h3>
                                <p className="text-sm text-finzen-muted">{stock.name}</p>
                            </div>
                            <button
                                onClick={() => handleBuy(stock.symbol)}
                                disabled={buying === stock.symbol}
                                className="bg-emerald-500/20 text-emerald-400 px-3 py-1 rounded text-xs font-bold hover:bg-emerald-500/40 transition-colors disabled:opacity-50 cursor-pointer">
                                {buying === stock.symbol ? "⏳" : "BUY"}
                            </button>
                        </div>
                        <div className="flex justify-between items-end mt-4">
                            <span className="text-2xl font-bold">₹{stock.price}</span>
                            <span className="text-xs text-finzen-muted">{stock.reason}</span>
                        </div>
                    </motion.div>
                ))}
            </div>
        </div>
    );
};

// --- PROPERTY VIEW ---
export const PropertiesView = () => {
    const [location, setLocation] = useState('Mumbai');
    const [properties, setProperties] = useState([]);
    const [loading, setLoading] = useState(false);
    const [budgetExceeded, setBudgetExceeded] = useState(false);

    // Mock Budget for demo (e.g., ₹50 Lakhs limit)
    const MAX_BUDGET_INR = 5000000;

    const searchProperties = async () => {
        setLoading(true);
        setBudgetExceeded(false);
        try {
            const res = await axios.get(`http://localhost:8001/recommendations/property?location=${location}`);
            const data = Array.isArray(res.data) ? res.data : [];

            // Check Affordability
            if (data.length === 0 || data.every(p => p.price_inr > MAX_BUDGET_INR)) {
                setBudgetExceeded(true);
                // Optionally clear properties to force empty state, or keep them to show what they missed
                // setProperties([]); 
            }

            setProperties(data);
        } catch (e) {
            console.error(e);
            setProperties([]);
        }
        setLoading(false);
    };

    // Auto-load on mount
    useEffect(() => { searchProperties(); }, []);

    return (
        <div className="p-6 space-y-6 h-full overflow-y-auto relative">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <Home className="text-blue-400" /> Real Estate Search
            </h2>
            <div className="flex gap-2 mb-6">
                <input
                    value={location} onChange={(e) => setLocation(e.target.value)}
                    className="bg-slate-800 p-2 rounded-lg border border-slate-700 flex-1 text-white"
                    placeholder="Enter City..."
                />
                <button onClick={searchProperties} disabled={loading} className="bg-blue-600 px-4 py-2 rounded-lg text-white font-bold">
                    {loading ? "Searching..." : "Search"}
                </button>
            </div>

            {/* Affordability Popup Warning */}
            {budgetExceeded && (
                <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}
                    className="bg-red-500/20 border border-red-500/50 text-red-100 p-4 rounded-xl mb-6 flex items-start gap-4 backdrop-blur-sm">
                    <span className="text-2xl">⚠️</span>
                    <div>
                        <h4 className="font-bold">Affordability Warning</h4>
                        <p className="text-sm">Based on your current FinZen profile, there are no listings in <b>{location}</b> that fit your budget (Under ₹{(MAX_BUDGET_INR / 100000).toFixed(0)} Lakhs). Consider adjusting your target location or saving more towards your goals!</p>
                    </div>
                </motion.div>
            )}

            <div className="grid grid-cols-1 gap-4">
                {/* Check if properties is a list, if not handle error */}
                {Array.isArray(properties) && properties.length > 0 ? properties.map((prop, idx) => (
                    <motion.div key={idx} initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                        className="bg-finzen-card p-4 rounded-xl border border-slate-700/50 flex flex-col md:flex-row gap-4">
                        <div className="w-full md:w-32 h-32 bg-slate-700 rounded-lg animate-pulse"></div>
                        <div className="flex-1">
                            <h3 className="font-bold text-lg">{prop.name || "Property Name"}</h3>
                            <p className="text-finzen-muted">{prop.location}</p>
                            <div className="mt-2 text-xl font-bold text-emerald-400">₹{(prop.price_inr / 100000).toFixed(1)} Lakhs</div>
                            <div className="mt-2 flex gap-2">
                                <span className="bg-slate-800 px-2 py-1 rounded text-xs">{prop.type}</span>
                            </div>
                        </div>
                    </motion.div>
                )) : <div className="text-red-400">Failed to load listings.</div>}
            </div>
        </div>
    );
};

// --- PLANNING VIEW ---
export const PlanningView = () => {
    // Mock Data for View Only
    const sipData = { monthly: 5000, years: 10, rate: 12, fv: 1161695, invested: 600000, gain: 561695 };
    const taxData = { income: 1200000, tax: 82500, regime: "New Regime" };

    return (
        <div className="p-6 space-y-6 h-full overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <Calculator className="text-purple-400" /> Financial Planning
            </h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                    <h3 className="text-lg font-semibold mb-2">SIP Calculator</h3>
                    <SIPCard data={sipData} />
                </div>
                <div>
                    <h3 className="text-lg font-semibold mb-2">Tax Estimator</h3>
                    <TaxCard data={taxData} />
                </div>
            </div>
        </div>
    );
};

// --- INSURANCE VIEW ---
export const InsuranceView = () => {
    const policies = [
        { type: "Term Life", cover_amount: 10000000, reason: "20x Annual Income", est_premium_monthly: 950 },
        { type: "Health Insurance", cover_amount: 500000, reason: "Individual Base Cover", est_premium_monthly: 600 }
    ];

    return (
        <div className="p-6 space-y-6 h-full overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <Shield className="text-orange-400" /> Insurance Advisor
            </h2>
            <InsuranceCard data={policies} />
        </div>
    );
};
