# Smart Environment Monitor – Azure IoT Central

This project demonstrates an end-to-end IoT device implementation using **Azure IoT Central**.
It was developed to showcase device modeling, telemetry ingestion,
command handling, and writable properties using Azure IoT Plug and Play.

---

## 🏗 Architecture Overview

- Azure IoT Central for device management and visualization
- Device provisioning using DPS (Device Provisioning Service)
- Python-based simulated IoT device
- Telemetry, writable properties, and commands implemented using IoT Plug and Play

---

## 📡 Device Capabilities

### Telemetry
- Temperature (°C)
- Humidity (%)
- Air Quality Index
- Environment Lux

### Writable Properties
- `samplingInterval` – controls telemetry frequency

### Commands
- `stopSendingData`
- `restartDevice`

---

## 🚀 Running the Device Locally

1. **Clone the Repository**

   ```bash
   git clone https://github.com/<your-username>/Azure-IoT-Central-Smart-Env-Monitor.git
   cd Azure-IoT-Central-Smart-Env-Monitor
   ```

2. **(Optional) Create and activate a virtual environment**

    ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate  
   ```

3. **Install the dependencies**

    ```bash
   pip install -r requirements.txt 
   ```

4. **Configure environment variables**
Create a `.env` file based on `.env.example` and fill in your Azure IoT Central credentials.

5. **Run the device**

    ```bash
   python src/smart_environment_device.py
   ```

## IoT Central Dashboard
The IoT Central dashboard visualizes telemetry data using time-series charts for all sensor values.

## Documentation
Additional explanation and design decisions can be found in the `docs/` folder. 

## Security Notes
Secrets are managed via environment variables and excluded from version control using `.gitignore`.

## Project Organization

```plaintext

Azure-IoT-Central-Smart-Env-Monitor/
│
├── src/
│   └── smart_environment_device.py     # Main IoT device simulation script
│
├── docs/
│   ├── architecture.md                 # System architecture and design explanation
│   └── iot-central-setup.md            # Step-by-step IoT Central configuration guide
│
├── .env.example                        # Example environment variable template
├── .gitignore                          # Excludes secrets and local files
├── requirements.txt                    # Python dependencies
├── README.md                           # Project overview and usage instructions
```