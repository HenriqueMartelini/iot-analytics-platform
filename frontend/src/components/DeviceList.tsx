/**
 * DeviceList component for displaying devices in a table.
 * 
 * Shows all devices with their status and provides actions for selection,
 * editing, and deletion.
 */

import React from 'react';
import { Device } from '@/types';
import { Trash2, Edit2, CheckCircle, AlertCircle } from 'lucide-react';

interface DeviceListProps {
  devices: Device[];
  onSelect: (device: Device) => void;
  onDelete: (deviceId: string) => void;
  selectedDeviceId?: string;
}

export const DeviceList: React.FC<DeviceListProps> = ({
  devices,
  onSelect,
  onDelete,
  selectedDeviceId,
}) => {
  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Devices ({devices.length})</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {devices.map((device) => (
              <tr
                key={device.id}
                className={`hover:bg-gray-50 cursor-pointer transition ${
                  selectedDeviceId === device.id ? 'bg-blue-50' : ''
                }`}
                onClick={() => onSelect(device)}
              >
                <td className="px-6 py-4 text-sm font-medium text-gray-900">{device.name}</td>
                <td className="px-6 py-4 text-sm text-gray-600">{device.location}</td>
                <td className="px-6 py-4 text-sm text-gray-600">{device.device_type}</td>
                <td className="px-6 py-4 text-sm">
                  <div className="flex items-center gap-2">
                    {device.is_active ? (
                      <>
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span className="text-green-600 font-medium">Active</span>
                      </>
                    ) : (
                      <>
                        <AlertCircle className="w-4 h-4 text-red-600" />
                        <span className="text-red-600 font-medium">Inactive</span>
                      </>
                    )}
                  </div>
                </td>
                <td className="px-6 py-4 text-sm">
                  <div className="flex gap-2">
                    <button className="text-blue-600 hover:text-blue-800 p-1">
                      <Edit2 className="w-4 h-4" />
                    </button>
                    <button
                      className="text-red-600 hover:text-red-800 p-1"
                      onClick={(e) => {
                        e.stopPropagation();
                        onDelete(device.id);
                      }}
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {devices.length === 0 && (
          <div className="px-6 py-8 text-center text-gray-500">
            <p>No devices found. Create one to get started.</p>
          </div>
        )}
      </div>
    </div>
  );
};
