import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import ChatInterface from './components/ChatInterface';
import { StocksView, PropertiesView, InsuranceView, PlanningView } from './components/views/Modules';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderView = () => {
    switch (activeTab) {
      case 'dashboard': return <Dashboard userId={1} />;
      case 'stocks': return <StocksView />;
      case 'properties': return <PropertiesView />;
      case 'insurance': return <InsuranceView />;
      case 'planning': return <PlanningView />;
      default: return <Dashboard userId={1} />;
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-200 font-sans selection:bg-emerald-500/30">
      {/* LEFT: Sidebar Navigation */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* CENTER: Active Module View */}
      <div className="flex-1 h-full overflow-hidden relative">
        {renderView()}
      </div>

      {/* RIGHT: Global Chat Assistant (Always Visible) */}
      <div className="w-[400px] border-l border-slate-800 bg-slate-900 h-full flex flex-col shadow-2xl z-20">
        <div className="h-14 border-b border-slate-800 flex items-center px-4 font-semibold bg-slate-900/50 backdrop-blur-md">
          FinZen Assistant
        </div>
        <div className="flex-1 overflow-hidden">
          <ChatInterface userId={1} />
        </div>
      </div>
    </div>
  );
}

export default App;
