import React, { useEffect, useState } from 'react';
import { getDashboardData } from '../services/api';
import UploadStatement from './UploadStatement';
import { PieChart, Pie, Cell, ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';
import { TrendingUp, Wallet, AlertCircle, CheckCircle } from 'lucide-react';

const COLORS = ['#10b981', '#fbbf24', '#ef4444', '#3b82f6'];

const Dashboard = ({ userId = 1 }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            const result = await getDashboardData(userId);
            setData(result);
            setLoading(false);
        };
        fetchData();
    }, [userId]);

    if (loading) return <div className="p-8 text-finzen-muted animate-pulse">Loading Financial Data...</div>;
    if (!data) return <div className="p-8 text-red-400">Failed to load data.</div>;

    return (
        <div className="p-6 space-y-6 h-full overflow-y-auto bg-finzen-dark text-finzen-text">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-bold">Welcome back, {data.user_name}</h1>
                    <p className="text-finzen-muted">Here is your financial overview.</p>
                </div>
                <div className="bg-finzen-card p-3 rounded-xl border border-slate-700/50">
                    <p className="text-sm text-finzen-muted">Risk Score</p>
                    <p className="text-xl font-bold text-amber-400">{data.risk_score}/100</p>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-finzen-card p-4 rounded-xl border border-slate-700/50 flex items-center gap-4">
                    <div className="p-3 bg-emerald-500/20 rounded-full text-emerald-400">
                        <Wallet size={24} />
                    </div>
                    <div>
                        <p className="text-sm text-finzen-muted">Net Worth</p>
                        <p className="text-2xl font-bold">{data.net_worth}</p>
                    </div>
                </div>

                <div className="bg-finzen-card p-4 rounded-xl border border-slate-700/50 flex items-center gap-4">
                    <div className={`p-3 rounded-full ${data.daily_goal.includes('STOP') ? 'bg-red-500/20 text-red-400' : 'bg-blue-500/20 text-blue-400'}`}>
                        {data.daily_goal.includes('STOP') ? <AlertCircle size={24} /> : <CheckCircle size={24} />}
                    </div>
                    <div>
                        <p className="text-sm text-finzen-muted">Daily Goal</p>
                        <p className="font-medium">{data.daily_goal}</p>
                    </div>
                </div>
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Budget Pie */}
                <div className="bg-finzen-card p-4 rounded-xl border border-slate-700/50 min-h-[300px]">
                    <h3 className="font-semibold mb-4 text-lg">Monthly Budget</h3>
                    <div className="h-[250px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={data.budget_pie}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={80}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {data.budget_pie.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px' }}
                                    itemStyle={{ color: '#f8fafc' }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="flex flex-wrap justify-center gap-4 mt-2">
                        {data.budget_pie.map((entry, index) => (
                            <div key={index} className="flex items-center gap-2 text-sm">
                                <span className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[index % COLORS.length] }}></span>
                                <span className="text-finzen-muted">{entry.name}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Stock Graphs */}
                <div className="bg-finzen-card p-4 rounded-xl border border-slate-700/50 min-h-[300px]">
                    <h3 className="font-semibold mb-4 text-lg">Top Assets</h3>
                    {data.stock_graphs.map((stock, idx) => (
                        <div key={idx} className="mb-6 last:mb-0">
                            <div className="flex justify-between mb-2">
                                <span className="font-medium text-emerald-400">{stock.symbol}</span>
                                <span className="font-bold">₹{stock.current_value}</span>
                            </div>
                            <div className="h-[100px] w-full">
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart data={stock.data}>
                                        <Line type="monotone" dataKey="value" stroke="#10b981" strokeWidth={2} dot={false} />
                                        <Tooltip
                                            contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px' }}
                                            itemStyle={{ color: '#10b981' }}
                                            labelStyle={{ display: 'none' }}
                                        />
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    ))}
                    {data.stock_graphs.length === 0 && (
                        <div className="flex items-center justify-center h-[200px] text-finzen-muted">
                            No active stock assets found.
                        </div>
                    )}
                </div>

                {/* Upload Statement */}
                <div className="lg:col-span-2">
                    <UploadStatement userId={userId} onUploadComplete={() => window.location.reload()} />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
