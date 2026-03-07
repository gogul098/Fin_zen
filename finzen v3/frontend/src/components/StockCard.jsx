import React from 'react';
import { LineChart, Line, ResponsiveContainer, Tooltip } from 'recharts';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { motion } from 'framer-motion';

const StockCard = ({ data }) => {
    if (!data) return null;

    const isPositive = data.change >= 0;

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-finzen-card p-4 rounded-xl border border-slate-700/50 w-full max-w-sm mt-2"
        >
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-lg font-bold text-finzen-text">{data.symbol}</h3>
                    <p className="text-xs text-finzen-muted">{data.name}</p>
                </div>
                <div className={`flex items-center ${isPositive ? 'text-emerald-400' : 'text-red-400'}`}>
                    <span className="text-lg font-bold">₹{data.price}</span>
                    {isPositive ? <ArrowUpRight size={20} /> : <ArrowDownRight size={20} />}
                </div>
            </div>

            <div className="h-[100px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data.history}>
                        <Line
                            type="monotone"
                            dataKey="price"
                            stroke={isPositive ? '#10b981' : '#ef4444'}
                            strokeWidth={2}
                            dot={false}
                        />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }}
                            itemStyle={{ color: '#f8fafc' }}
                            labelStyle={{ display: 'none' }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            <div className="flex justify-between mt-3 text-xs text-finzen-muted">
                <span>1M Low</span>
                <span>1M High</span>
            </div>
        </motion.div>
    );
};

export default StockCard;
