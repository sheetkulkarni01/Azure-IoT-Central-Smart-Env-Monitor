# Architecture Overview

## 1. System Overview

This project implements a simulated IoT device using Azure IoT Central and Azure Device Provisioning Service (DPS). The architecture demonstrates end-to-end device modeling, provisioning, telemetry ingestion, command handling, and dashboard visualization using Azure IoT Plug and Play.

---

## 2. High-Level Architecture

Device (Python App)
        │
        │  (MQTT via DPS)
        ▼
Azure Device Provisioning Service (DPS)
        │
        ▼
Azure IoT Hub (Managed by IoT Central)
        │
        ▼
Azure IoT Central
        │
        ▼
Dashboards & Monitoring

---

## 3. Components

### 3.1 Simulated Device (Python)

The device application is implemented in Python using the Azure IoT Device SDK.

Responsibilities:
- Authenticate via DPS using symmetric key
- Send telemetry at configurable intervals
- Handle writable properties
- Handle direct method commands
- Maintain asynchronous event loop

Key features:
- Configurable sampling interval
- Enable/disable telemetry via command
- Realistic simulated environmental data

---

### 3.2 Azure Device Provisioning Service (DPS)

DPS is used to:
- Register the device securely
- Assign it automatically to the correct IoT Hub
- Attach the correct device template via model ID (DTMI)

The device sends its `modelId` during provisioning so IoT Central can automatically bind it to the correct device template.

---

### 3.3 Azure IoT Central

IoT Central provides:
- Device template definition
- Telemetry visualization
- Command invocation
- Writable property management
- Device twin management

The device template defines:
- Telemetry (temperature, humidity, airQualityIndex, environmentLux)
- Writable property (samplingInterval)
- Commands (stopSendingData, restartDevice)

---

## 4. Communication Model

### Telemetry (Device → Cloud)
- Sent via MQTT
- JSON payload format
- Periodic transmission based on samplingInterval


Example:
```json
{
  "temperature": 25.4,
  "humidity": 60.2,
  "airQualityIndex": 90,
  "environmentLux": 450
}
```

### Writable Properties (Cloud → Device)
IoT Central updates desired properties.

The device:
1. Receives the desired property patch
2. Applies the change locally
3. Sends acknowledgment 

Acknowledgment structure:
- value
- ac (acknowledgment code)
- ad (description)
- av (version)

### Commands (Cloud → Device)
Commands are received asynchronously:
- stopSendingData
- restartDevice

The device:
1. Executes the action
2. Sends a method response with status code

---

## 5. Asynchronous Design
The device uses asyncio to concurrently run:
- Telemetry sender loop
- Property listener loop
- Command listener loop

This mimics real IoT devices that must:
- Send data continuously
- React to configuration changes
- Respond to remote control requests

---

## 6. Scalability Considerations
In production environments:
- Telemetry would be routed to Event Hub or Data Lake
- Data retention and aggregation strategies would be applied
- Real-time alerts could be configured
- Device authentication would likely use X.509 certificates

---

## 7. Security Considerations
- Device credentials are stored in environment variables
- Secrets are excluded from version control
- DPS enables secure provisioning at scale

---

## 8. Key Architectural Principles Demonstrated
- Separation of concerns (device logic vs cloud management)
- Event-driven communication
- Scalable provisioning model
- Cloud-native IoT design
- Secure credential handling
