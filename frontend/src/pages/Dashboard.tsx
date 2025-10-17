/**
 * Dashboard page component.
 * 
 * Main page displaying the IoT Analytics Dashboard with statistics,
 * device list, alerts, and data visualizations.
 */

import React, { useEffect, useState } from 'react';
import { Activity, AlertTriangle, Zap, TrendingUp } from 'lucide-react';
import { Header, StatCard, DeviceList, AlertList, Chart } from '@/components';
import { useAppStore } from '@/store';
import { apiClient } from '@/services/api';
import { Device, Alert } from '@/types';

export const Dashboard: React.FC = () => {
  const {
    devices,
    setDevices,
    alerts,
    setAlerts,
    isLoading,
    setIsLoading,
    error,
    setError,
  } = useAppStore();

  const [deviceStats, setDeviceStats] = useState({ total: 0, active: 0 });
  const [alertStats, setAlertStats] = useState({ total: 0, unresolved: 0 });
  const [selectedDevice, setSelectedDevice] = useState<Device | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [devicesData, alertsData, devStats, alertStats] = await Promise.all([
        apiClient.getDevices(),
        apiClient.getAlerts(),
        apiClient.getDeviceStats(),
        apiClient.getAlertStats(),
      ]);

      setDevices(devicesData);
      setAlerts(alertsData);
      setDeviceStats(devStats);
      setAlertStats(alertStats);
      setError(null);
    } catch (err) {
      setError('Failed to load data. Please try again.');
      console.error('Error loading data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteDevice = async (deviceId: string) => {
    if (confirm('Are you sure you want to delete this device?')) {
      try {
        await apiClient.deleteDevice(deviceId);
        setDevices(devices.filter((d) => d.id !== deviceId));
        setDeviceStats((prev) => ({ ...prev, total: prev.total - 1 }));
      } catch (err) {
        setError('Failed to delete device');
      }
    }
  };

  const handleDeleteAlert = async (alertId: string) => {
    try {
      await apiClient.deleteAlert(alertId);
      setAlerts(alerts.filter((a) => a.id !== alertId));
      setAlertStats((prev) => ({
        ...prev,
        total: prev.total - 1,
        unresolved: alerts.find((a) => a.id === alertId)?.is_resolved ? prev.unresolved : prev.unresolved - 1,
      }));
    } catch (err) {
      setError('Failed to delete alert');
    }
  };

  const handleResolveAlert = async (alertId: string) => {
    try {
      await apiClient.resolveAlert(alertId);
      setAlerts(
        alerts.map((a) => (a.id === alertId ? { ...a, is_resolved: true, resolved_at: new Date().toISOString() } : a))
      );
      setAlertStats((prev) => ({ ...prev, unresolved: Math.max(0, prev.unresolved - 1) }));
    } catch (err) {
      setError('Failed to resolve alert');
    }
  };

  // Mock data for charts
  const mockChartData = [
    { timestamp: '00:00', temperature: 22, humidity: 45 },
    { timestamp: '04:00', temperature: 20, humidity: 50 },
    { timestamp: '08:00', temperature: 24, humidity: 48 },
    { timestamp: '12:00', temperature: 26, humidity: 42 },
    { timestamp: '16:00', temperature: 25, humidity: 46 },
    { timestamp: '20:00', temperature: 23, humidity: 52 },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Devices"
            value={deviceStats.total}
            icon={Activity}
            color="blue"
            subtitle={`${deviceStats.active} active`}
          />
          <StatCard
            title="Active Alerts"
            value={alertStats.unresolved}
            icon={AlertTriangle}
            color={alertStats.unresolved > 0 ? 'red' : 'green'}
            subtitle={`${alertStats.total} total`}
          />
          <StatCard
            title="System Status"
            value="Operational"
            icon={Zap}
            color="green"
            subtitle="All systems normal"
          />
          <StatCard
            title="Uptime"
            value="99.9%"
            icon={TrendingUp}
            color="green"
            subtitle="Last 30 days"
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <Chart
            data={mockChartData}
            type="line"
            dataKey="temperature"
            title="Temperature Trend"
            xAxisKey="timestamp"
          />
          <Chart
            data={mockChartData}
            type="bar"
            dataKey="humidity"
            title="Humidity Levels"
            xAxisKey="timestamp"
          />
        </div>

        {/* Device and Alert Lists */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <DeviceList
              devices={devices}
              onSelect={setSelectedDevice}
              onDelete={handleDeleteDevice}
              selectedDeviceId={selectedDevice?.id}
            />
          </div>
          <div>
            <AlertList
              alerts={alerts.slice(0, 5)}
              onResolve={handleResolveAlert}
              onDelete={handleDeleteAlert}
            />
          </div>
        </div>
      </main>
    </div>
  );
};
