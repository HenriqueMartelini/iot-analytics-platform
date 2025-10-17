/**
 * API client service for communicating with the backend.
 * 
 * Provides methods for all API operations including device management,
 * sensor readings, and alert handling.
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import { Device, SensorReading, Alert } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  // ============ Device Endpoints ============

  async getDevices(skip = 0, limit = 100): Promise<Device[]> {
    const response = await this.client.get('/devices', { params: { skip, limit } });
    return response.data;
  }

  async getDevice(deviceId: string): Promise<Device> {
    const response = await this.client.get(`/devices/${deviceId}`);
    return response.data;
  }

  async createDevice(device: Omit<Device, 'id' | 'created_at' | 'updated_at' | 'status'>): Promise<Device> {
    const response = await this.client.post('/devices', device);
    return response.data;
  }

  async updateDevice(deviceId: string, device: Partial<Device>): Promise<Device> {
    const response = await this.client.put(`/devices/${deviceId}`, device);
    return response.data;
  }

  async deleteDevice(deviceId: string): Promise<void> {
    await this.client.delete(`/devices/${deviceId}`);
  }

  async getDeviceStats(): Promise<{ total: number; active: number }> {
    const response = await this.client.get('/devices/stats/count');
    return response.data;
  }

  // ============ Sensor Reading Endpoints ============

  async getSensorReadings(
    deviceId?: string,
    sensorType?: string,
    skip = 0,
    limit = 100
  ): Promise<SensorReading[]> {
    const response = await this.client.get('/sensor-readings', {
      params: { device_id: deviceId, sensor_type: sensorType, skip, limit },
    });
    return response.data;
  }

  async getSensorReading(readingId: number): Promise<SensorReading> {
    const response = await this.client.get(`/sensor-readings/${readingId}`);
    return response.data;
  }

  async createSensorReading(reading: Omit<SensorReading, 'id' | 'created_at'>): Promise<SensorReading> {
    const response = await this.client.post('/sensor-readings', reading);
    return response.data;
  }

  async getLatestReading(deviceId: string, sensorType: string): Promise<SensorReading> {
    const response = await this.client.get(`/sensor-readings/device/${deviceId}/latest`, {
      params: { sensor_type: sensorType },
    });
    return response.data;
  }

  async getAverageValue(
    deviceId: string,
    sensorType: string,
    hours = 24
  ): Promise<{ device_id: string; sensor_type: string; average: number; hours: number }> {
    const response = await this.client.get(`/sensor-readings/device/${deviceId}/average`, {
      params: { sensor_type: sensorType, hours },
    });
    return response.data;
  }

  // ============ Alert Endpoints ============

  async getAlerts(
    deviceId?: string,
    isResolved?: boolean,
    skip = 0,
    limit = 100
  ): Promise<Alert[]> {
    const response = await this.client.get('/alerts', {
      params: { device_id: deviceId, is_resolved: isResolved, skip, limit },
    });
    return response.data;
  }

  async getAlert(alertId: string): Promise<Alert> {
    const response = await this.client.get(`/alerts/${alertId}`);
    return response.data;
  }

  async createAlert(alert: Omit<Alert, 'id' | 'created_at' | 'resolved_at'>): Promise<Alert> {
    const response = await this.client.post('/alerts', alert);
    return response.data;
  }

  async updateAlert(alertId: string, alert: Partial<Alert>): Promise<Alert> {
    const response = await this.client.put(`/alerts/${alertId}`, alert);
    return response.data;
  }

  async resolveAlert(alertId: string): Promise<Alert> {
    const response = await this.client.post(`/alerts/${alertId}/resolve`);
    return response.data;
  }

  async deleteAlert(alertId: string): Promise<void> {
    await this.client.delete(`/alerts/${alertId}`);
  }

  async getAlertStats(): Promise<{ total: number; unresolved: number }> {
    const response = await this.client.get('/alerts/stats/count');
    return response.data;
  }

  // ============ Health Check ============

  async healthCheck(): Promise<{ status: string }> {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export const apiClient = new ApiClient();
