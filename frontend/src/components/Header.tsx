/**
 * Header component for the application.
 * 
 * Displays the application title, logo, and current date/time.
 */

import React from 'react';
import { Activity } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-3">
            <Activity className="w-8 h-8" />
            <div>
              <h1 className="text-2xl font-bold">IoT Analytics Dashboard</h1>
              <p className="text-blue-100 text-sm">Real-time Device Monitoring Platform</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-sm text-blue-100">
              {new Date().toLocaleDateString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};
