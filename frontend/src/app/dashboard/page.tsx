"use client";

import React, { useState } from 'react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { 
  Settings, Bell, BarChart2, TrendingUp, 
  DollarSign, AlertTriangle, ChevronUp 
} from 'lucide-react';

// Sample data matching your performance chart pattern
const performanceData = Array.from({ length: 30 }, (_, i) => ({
  date: `Day ${i + 1}`,
  portfolioValue: 600 + Math.sin(i/3) * 100 + (i * 2),
  returns: (Math.sin(i/3) * 5) + 1,
}));

export default function WealthbotDashboard() {
  const [activeTimeframe, setActiveTimeframe] = useState('1M');

  return (
    <div className="min-h-screen bg-[#0B1221] text-white">
      {/* Left Sidebar */}
      <div className="fixed left-0 top-0 w-60 h-full bg-[#0F172A] border-r border-gray-800">
        <div className="p-6">
          <h1 className="text-xl font-bold mb-8">Trader Agent</h1>
          <nav className="space-y-4">
            <button className="flex items-center space-x-3 text-[#38BDF8] w-full">
              <BarChart2 className="h-5 w-5" />
              <span>Dashboard</span>
            </button>
            <button className="flex items-center space-x-3 text-gray-400 w-full hover:text-white">
              <TrendingUp className="h-5 w-5" />
              <span>Trading</span>
            </button>
            <button className="flex items-center space-x-3 text-gray-400 w-full hover:text-white">
              <AlertTriangle className="h-5 w-5" />
              <span>Risk Management</span>
            </button>
          </nav>
        </div>

        {/* System Status */}
        <div className="absolute bottom-0 left-0 w-full p-6">
          <h3 className="text-sm font-semibold text-gray-400 mb-4">SYSTEM STATUS</h3>
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <div className="h-2 w-2 rounded-full bg-green-500" />
              <span className="text-sm text-gray-400">Trading System</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="h-2 w-2 rounded-full bg-green-500" />
              <span className="text-sm text-gray-400">Market Data Feed</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="h-2 w-2 rounded-full bg-green-500" />
              <span className="text-sm text-gray-400">Risk Management</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="ml-60 p-6">
        {/* Top Bar */}
        <div className="flex justify-between items-center mb-8">
          <div className="flex space-x-2">
            <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-500 text-sm">System Online</span>
            <span className="px-3 py-1 rounded-full bg-blue-500/20 text-blue-500 text-sm">API Connected</span>
          </div>
          <div className="flex items-center space-x-4">
            <Bell className="h-5 w-5 text-gray-400" />
            <Settings className="h-5 w-5 text-gray-400" />
          </div>
        </div>

        {/* Portfolio Overview */}
        <div className="grid grid-cols-4 gap-6 mb-8">
          <div className="bg-[#1E293B] p-6 rounded-xl">
            <h3 className="text-gray-400 mb-2">Total Equity</h3>
            <p className="text-3xl font-bold text-green-500">$750.25</p>
          </div>
          <div className="bg-[#1E293B] p-6 rounded-xl">
            <h3 className="text-gray-400 mb-2">Cash Balance</h3>
            <p className="text-3xl font-bold">$250.75</p>
          </div>
          <div className="bg-[#1E293B] p-6 rounded-xl">
            <h3 className="text-gray-400 mb-2">Today's Return</h3>
            <p className="text-3xl font-bold text-green-500">
              <span className="flex items-center">
                5.25% <ChevronUp className="h-6 w-6" />
              </span>
            </p>
          </div>
          <div className="bg-[#1E293B] p-6 rounded-xl">
            <h3 className="text-gray-400 mb-2">Total Return</h3>
            <p className="text-3xl font-bold text-green-500">50.05%</p>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="bg-[#1E293B] p-6 rounded-xl mb-8">
          <div className="flex justify-between items-center mb-2">
            <h3 className="text-gray-400">Progress to $1,000,000 Goal</h3>
            <span className="text-gray-400">0.08%</span>
          </div>
          <div className="w-full bg-gray-800 rounded-full h-2">
            <div className="bg-[#38BDF8] h-2 rounded-full" style={{ width: '0.08%' }}></div>
          </div>
        </div>

        {/* Main Chart */}
        <div className="grid grid-cols-3 gap-6">
          <div className="col-span-2 bg-[#1E293B] rounded-xl p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold">Performance</h2>
              <div className="flex space-x-2">
                {['1D', '1W', '1M', '3M', '1Y', 'ALL'].map((timeframe) => (
                  <button
                    key={timeframe}
                    className={`px-3 py-1 rounded ${
                      activeTimeframe === timeframe 
                        ? 'bg-green-500 text-white' 
                        : 'bg-[#2D3B4E] text-gray-400'
                    }`}
                    onClick={() => setActiveTimeframe(timeframe)}
                  >
                    {timeframe}
                  </button>
                ))}
              </div>
            </div>
            <div className="h-[400px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={performanceData}>
                  <defs>
                    <linearGradient id="portfolioGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#22C55E" stopOpacity={0.2}/>
                      <stop offset="95%" stopColor="#22C55E" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="date" stroke="#64748B" />
                  <YAxis stroke="#64748B" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1E293B',
                      border: '1px solid #22C55E',
                      borderRadius: '8px'
                    }}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="portfolioValue" 
                    stroke="#22C55E" 
                    fill="url(#portfolioGradient)"
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="returns" 
                    stroke="#38BDF8" 
                    strokeWidth={2}
                    dot={false}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Risk Metrics */}
          <div className="bg-[#1E293B] rounded-xl p-6">
            <h2 className="text-xl font-bold mb-6">Risk Metrics</h2>
            <div className="space-y-6">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-400">Max Drawdown</span>
                  <span className="text-yellow-500 flex items-center">
                    8.50% <AlertTriangle className="h-4 w-4 ml-1" />
                  </span>
                </div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-400">Sharpe Ratio</span>
                  <span className="text-green-500">1.80</span>
                </div>
              </div>

              <div>
                <h3 className="text-gray-400 mb-4">Exposure by Asset</h3>
                {[
                  { asset: 'BTC/USD', exposure: '30.50%' },
                  { asset: 'ETH/USD', exposure: '20.00%' },
                  { asset: 'SOL/USD', exposure: '15.00%' }
                ].map((item) => (
                  <div key={item.asset} className="flex justify-between mb-2">
                    <span className="text-gray-400">{item.asset}</span>
                    <span>{item.exposure}</span>
                  </div>
                ))}
                <div className="mt-4">
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-400">Total Exposure</span>
                    <span className="text-yellow-500">65.50%</span>
                  </div>
                  <div className="w-full bg-gray-800 rounded-full h-2">
                    <div 
                      className="bg-yellow-500 h-2 rounded-full" 
                      style={{ width: '65.50%' }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}