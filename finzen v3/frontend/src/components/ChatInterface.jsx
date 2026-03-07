import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../services/api';
import StockCard from './StockCard';
import TradeTicket from './TradeTicket';
import { InsuranceCard, SIPCard, TaxCard } from './FinancialCards';
import { Send, User, Bot, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ChatInterface = ({ userId = 1 }) => {
    const [messages, setMessages] = useState([
        { role: 'assistant', type: 'text', content: 'Hello! I am FinZen, your AI financial guardian. How can I help you grow your wealth today?' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg = { role: 'user', type: 'text', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        const response = await sendChatMessage(userId, userMsg.content);

        if (response) {
            setMessages(prev => [...prev, response]);
        }
        setLoading(false);
    };

    return (
        <div className="flex flex-col h-full bg-slate-900 overflow-hidden relative">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                {messages.map((msg, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div className={`flex gap-3 max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                            {/* Avatar */}
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${msg.role === 'user' ? 'bg-blue-600' : 'bg-emerald-600'}`}>
                                {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                            </div>

                            {/* Content */}
                            <div className="flex flex-col">
                                {msg.content && (
                                    <div className={`p-3 rounded-2xl ${msg.role === 'user'
                                        ? 'bg-blue-600 text-white rounded-tr-none'
                                        : 'bg-finzen-card border border-slate-700/50 text-slate-200 rounded-tl-none'
                                        }`}>
                                        <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                                    </div>
                                )}

                                {/* Rich UI Components */}
                                {msg.type === 'stock-card' && <StockCard data={msg.data} />}
                                {msg.type === 'trade-ticket' && <TradeTicket data={msg.data} />}
                                {msg.type === 'insurance-card' && <InsuranceCard data={msg.data} />}
                                {msg.type === 'sip-card' && <SIPCard data={msg.data} />}
                                {msg.type === 'tax-card' && <TaxCard data={msg.data} />}
                            </div>
                        </div>
                    </motion.div>
                ))}
                {loading && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                        <div className="flex gap-3 max-w-[85%]">
                            <div className="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center flex-shrink-0">
                                <Sparkles size={16} className="animate-pulse" />
                            </div>
                            <div className="bg-finzen-card p-3 rounded-2xl rounded-tl-none border border-slate-700/50 flex items-center gap-1">
                                <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce"></span>
                                <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce delay-75"></span>
                                <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce delay-150"></span>
                            </div>
                        </div>
                    </motion.div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-slate-900 border-t border-slate-800">
                <form onSubmit={handleSend} className="relative">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask FinZen to analyze stats, buy stocks..."
                        className="w-full bg-slate-800 text-white placeholder-slate-500 pl-4 pr-12 py-3 rounded-xl border border-slate-700 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-colors"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || loading}
                        className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        <Send size={18} />
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ChatInterface;
