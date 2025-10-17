/**
 * TypeScript type definitions for the IoT Analytics Platform.
 */

export interface Device {
  id: string;
  name: string;
  location: string;
  device_type: string;
  status: string;
  latitude?: number;
  longitude?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface SensorReading {
  id: number;
  device_id: string;
  sensor_type: string;
  value: number;
  unit: string;
  timestamp: string;
  created_at: string;
}

export interface Alert {
  id: string;
  device_id: string;
  alert_type: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  message: string;
  threshold_value?: number;
  actual_value?: number;
  is_resolved: boolean;
  created_at: string;
  resolved_at?: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginationParams {
  skip: number;
  limit: number;
}
