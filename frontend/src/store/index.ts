/**
 * Global state management using Zustand.
 * 
 * Manages application-wide state for devices, alerts, sensor readings,
 * UI state, and filter preferences.
 */

import { create } from 'zustand';
import { Device, Alert, SensorReading } from '@/types';

interface AppStore {
  // Devices
  devices: Device[];
  setDevices: (devices: Device[]) => void;
  addDevice: (device: Device) => void;
  removeDevice: (deviceId: string) => void;

  // Alerts
  alerts: Alert[];
  setAlerts: (alerts: Alert[]) => void;
  addAlert: (alert: Alert) => void;
  removeAlert: (alertId: string) => void;

  // Sensor Readings
  readings: SensorReading[];
  setReadings: (readings: SensorReading[]) => void;
  addReading: (reading: SensorReading) => void;

  // UI State
  isLoading: boolean;
  setIsLoading: (isLoading: boolean) => void;
  error: string | null;
  setError: (error: string | null) => void;

  // Filters
  selectedDeviceId: string | null;
  setSelectedDeviceId: (deviceId: string | null) => void;
  selectedSensorType: string | null;
  setSelectedSensorType: (sensorType: string | null) => void;
}

export const useAppStore = create<AppStore>((set) => ({
  // Devices
  devices: [],
  setDevices: (devices) => set({ devices }),
  addDevice: (device) => set((state) => ({ devices: [...state.devices, device] })),
  removeDevice: (deviceId) =>
    set((state) => ({
      devices: state.devices.filter((d) => d.id !== deviceId),
    })),

  // Alerts
  alerts: [],
  setAlerts: (alerts) => set({ alerts }),
  addAlert: (alert) => set((state) => ({ alerts: [...state.alerts, alert] })),
  removeAlert: (alertId) =>
    set((state) => ({
      alerts: state.alerts.filter((a) => a.id !== alertId),
    })),

  // Sensor Readings
  readings: [],
  setReadings: (readings) => set({ readings }),
  addReading: (reading) => set((state) => ({ readings: [...state.readings, reading] })),

  // UI State
  isLoading: false,
  setIsLoading: (isLoading) => set({ isLoading }),
  error: null,
  setError: (error) => set({ error }),

  // Filters
  selectedDeviceId: null,
  setSelectedDeviceId: (selectedDeviceId) => set({ selectedDeviceId }),
  selectedSensorType: null,
  setSelectedSensorType: (selectedSensorType) => set({ selectedSensorType }),
}));
