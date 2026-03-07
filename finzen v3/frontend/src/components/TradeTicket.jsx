import React from 'react';
import { CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';

const TradeTicket = ({ data }) => {
    if (!data) return null;

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-finzen-card p-4 rounded-xl border border-emerald-500/30 w-full max-w-sm mt-2 relative overflow-hidden"
        >
            <div className="absolute top-0 right-0 p-4 opacity-10">
                <CheckCircle size={80} className="text-emerald-500" />
            </div>

            <div className="flex items-center gap-2 text-emerald-400 mb-2">
                <CheckCircle size={20} />
                <span className="font-bold uppercase tracking-wider text-xs">Order Executed</span>
            </div>

            <h3 className="text-xl font-bold text-white mb-1">Bought {data.qty} {data.symbol}</h3>
            <p className="text-finzen-muted text-sm mb-4">@ ₹{data.price} per share</p>

            <div className="border-t border-slate-700/50 pt-3 flex justify-between text-sm">
                <span className="text-finzen-muted">Total Value</span>
                <span className="font-bold text-emerald-400">₹{(data.qty * data.price).toFixed(2)}</span>
            </div>
        </motion.div>
    );
};

export default TradeTicket;
