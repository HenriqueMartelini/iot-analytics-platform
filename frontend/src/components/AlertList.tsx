/**
 * AlertList component for displaying system alerts.
 * 
 * Shows alerts with severity levels, messages, and actions for resolution
 * and deletion.
 */

import React from 'react';
import { Alert } from '@/types';
import { AlertTriangle, AlertCircle, Info, CheckCircle, Trash2 } from 'lucide-react';

interface AlertListProps {
  alerts: Alert[];
  onResolve: (alertId: string) => void;
  onDelete: (alertId: string) => void;
}

const severityConfig = {
  LOW: { icon: Info, color: 'text-blue-600', bg: 'bg-blue-50', border: 'border-blue-200' },
  MEDIUM: { icon: AlertCircle, color: 'text-yellow-600', bg: 'bg-yellow-50', border: 'border-yellow-200' },
  HIGH: { icon: AlertTriangle, color: 'text-orange-600', bg: 'bg-orange-50', border: 'border-orange-200' },
  CRITICAL: { icon: AlertTriangle, color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200' },
};

export const AlertList: React.FC<AlertListProps> = ({ alerts, onResolve, onDelete }) => {
  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Alerts ({alerts.length})</h2>
      </div>
      <div className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
        {alerts.map((alert) => {
          const config = severityConfig[alert.severity];
          const IconComponent = config.icon;

          return (
            <div key={alert.id} className={`p-4 ${config.bg} border-l-4 ${config.border}`}>
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3 flex-1">
                  <IconComponent className={`w-5 h-5 ${config.color} mt-0.5 flex-shrink-0`} />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-gray-900">{alert.alert_type}</h3>
                      <span className={`text-xs font-bold ${config.color}`}>{alert.severity}</span>
                      {alert.is_resolved && (
                        <span className="text-xs font-bold text-green-600 flex items-center gap-1">
                          <CheckCircle className="w-3 h-3" /> Resolved
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-700 mt-1">{alert.message}</p>
                    {alert.threshold_value && alert.actual_value && (
                      <p className="text-xs text-gray-600 mt-1">
                        Threshold: {alert.threshold_value} | Actual: {alert.actual_value}
                      </p>
                    )}
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(alert.created_at).toLocaleString()}
                    </p>
                  </div>
                </div>
                <div className="flex gap-2 ml-4">
                  {!alert.is_resolved && (
                    <button
                      className="text-green-600 hover:text-green-800 p-1"
                      onClick={() => onResolve(alert.id)}
                      title="Mark as resolved"
                    >
                      <CheckCircle className="w-4 h-4" />
                    </button>
                  )}
                  <button
                    className="text-red-600 hover:text-red-800 p-1"
                    onClick={() => onDelete(alert.id)}
                    title="Delete alert"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
        {alerts.length === 0 && (
          <div className="px-6 py-8 text-center text-gray-500">
            <p>No alerts at the moment. Everything looks good!</p>
          </div>
        )}
      </div>
    </div>
  );
};
