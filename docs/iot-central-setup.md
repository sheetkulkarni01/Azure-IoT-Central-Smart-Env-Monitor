# Azure IoT Central Setup Guide

This document describes how the Smart Environment Monitor device was configured in Azure IoT Central.

---

## 1. Create Device Template

1. Navigate to IoT Central application
2. Go to "Device Templates"
3. Click "New"
4. Select "IoT Device"
5. Name it: `Smart Environment Monitor` 

---

## 2. Define Telemetry

Add the following telemetry fields:

| Name | Type | Unit |
|------|------|------|
| temperature | Double | °C |
| humidity | Double | % |
| airQualityIndex | Integer | AQI |
| environmentLux | Integer | lux |

All telemetry values are time-series data.

---

## 3. Add Writable Property

Property:
- Name: samplingInterval
- Type: Integer
- Writable: Yes
- Default: 10 seconds

This property allows dynamic adjustment of telemetry frequency.

---

## 4. Add Commands

Create two commands:

### stopSendingData
- No payload
- Stops telemetry transmission

### restartDevice
- No payload
- Resumes telemetry transmission

---

## 5. Publish Template

After configuration:
- Click "Publish"
- Ensure template is active

---

## 6. Create Device Instance

1. Navigate to "Devices"
2. Select Smart Environment Monitor template
3. Click "New"
4. Assign a device name
5. Save

---

## 7. Retrieve DPS Credentials

From the device:
- ID Scope
- Device ID
- Primary Key

These are used for DPS provisioning in the Python device application.

---

## 8. Dashboard Creation

1. Navigate to "Dashboards"
2. Create a new dashboard
3. Add time-series charts for:
   - Temperature
   - Humidity
   - Air Quality Index
   - Environment Lux

Charts allow real-time monitoring of sensor values.

---

## 9. Testing

Test the system by:

1. Running the Python device
2. Verifying telemetry appears in IoT Central
3. Updating samplingInterval
4. Triggering commands
5. Confirming device responses

---

## 10. Validation Checklist

- Device provisions successfully via DPS
- Telemetry appears in dashboard
- Writable property updates are acknowledged
- Commands return successful method response
- No twin update errors