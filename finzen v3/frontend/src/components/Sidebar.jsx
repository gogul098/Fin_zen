import React from 'react';
import { LayoutDashboard, TrendingUp, Home, Shield, Calculator, MessageSquare } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
    const menuItems = [
        { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
        { id: 'stocks', label: 'Market', icon: TrendingUp },
        { id: 'properties', label: 'Real Estate', icon: Home },
        { id: 'insurance', label: 'Insurance', icon: Shield },
        { id: 'planning', label: 'Planning', icon: Calculator },
    ];

    return (
        <div className="w-64 bg-slate-900 border-r border-slate-800 h-full flex flex-col p-4">
            <div className="flex items-center gap-3 mb-8 px-2">
                <div className="w-8 h-8 bg-gradient-to-tr from-emerald-500 to-blue-500 rounded-lg"></div>
                <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
                    FinZen
                </h1>
            </div>

            <nav className="space-y-2 flex-1">
                {menuItems.map((item) => {
                    const Icon = item.icon;
                    const isActive = activeTab === item.id;

                    return (
                        <button
                            key={item.id}
                            onClick={() => setActiveTab(item.id)}
                            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${isActive
                                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-lg shadow-emerald-500/5'
                                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                                }`}
                        >
                            <Icon size={20} />
                            <span className="font-medium">{item.label}</span>
                        </button>
                    );
                })}
            </nav>

            {/* User Mini Profile */}
            <div className="mt-auto pt-4 border-t border-slate-800">
                <div className="flex items-center gap-3 p-2 rounded-lg bg-slate-800/50">
                    <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-xs font-bold">
                        SI
                    </div>
                    <div>
                        <p className="text-sm font-medium text-white">Siva</p>
                        <p className="text-xs text-slate-400">Pro Member</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
