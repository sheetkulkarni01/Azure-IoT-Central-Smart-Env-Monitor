from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
import random
from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient
from azure.iot.device import MethodResponse

# ---------------------------------------------------
# This model ID is used by IoT Central to
# assign the device template automatically
# ---------------------------------------------------
MODEL_ID = "dtmi:candidateTest:SmartEnvironmentMonitor_1cd;1"

# ---------------------------------------------------
# Global variables
# ---------------------------------------------------
sampling_interval = 10
sending_enabled = True

# ---------------------------------------------------
# DPS Provisioning Function - Connect device to azure
# ---------------------------------------------------
async def provision_device(id_scope, device_id, device_key):
    provisioning_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host="global.azure-devices-provisioning.net",
        registration_id=device_id,
        id_scope=id_scope,
        symmetric_key=device_key,
    )
    # Send model ID to IoT Central
    provisioning_client.provisioning_payload = {
        "modelId": MODEL_ID
    }
    return await provisioning_client.register()

# ---------------------------------------------------
# Main Device Logic
# ---------------------------------------------------
async def main():
    global sampling_interval
    global sending_enabled

    print("Starting Smart Environment Monitor Device...")

    # Read environment variables
    id_scope = os.getenv("IOTHUB_DEVICE_DPS_ID_SCOPE")
    device_id = os.getenv("IOTHUB_DEVICE_DPS_DEVICE_ID")
    device_key = os.getenv("IOTHUB_DEVICE_DPS_DEVICE_KEY")

    # Provision the device
    print("Registering device using DPS...")
    registration_result = await provision_device(id_scope, device_id, device_key)

    if registration_result.status != "assigned":
        print("Device provisioning failed")
        return

    print("Device successfully registered")

    # Create IoT Hub client
    device_client = IoTHubDeviceClient.create_from_symmetric_key(
        symmetric_key=device_key,
        hostname=registration_result.registration_state.assigned_hub,
        device_id=registration_result.registration_state.device_id,
        product_info=MODEL_ID,
    )
    await device_client.connect()
    print("Connected to IoT Central")

    # ---------------------------------------------------
    # Writable Property Listener
    # ---------------------------------------------------
    async def property_listener():
        global sampling_interval
        while True:
            patch = await device_client.receive_twin_desired_properties_patch()
            print("Property update received:", patch)

            if "samplingInterval" in patch:
                sampling_interval = patch["samplingInterval"]
                print("Sampling interval updated to:", sampling_interval)

            # Report property back to IoT Central
            reported = {}
            if "samplingInterval" in patch:
                reported["samplingInterval"] = {
                    "value": patch["samplingInterval"],
                    "ac": 200,
                    "ad": "Sampling interval applied",
                    "av": patch["$version"]
                }
            await device_client.patch_twin_reported_properties(reported)

    # ---------------------------------------------------
    # Command Listener
    # ---------------------------------------------------
    async def command_listener():
        global sending_enabled
        while True:
            command = await device_client.receive_method_request()
            print("Command received:", command.name)

            if command.name == "stopSendingData":
                sending_enabled = False
                payload = {"result": "Telemetry stopped"}
                status = 200

            elif command.name == "restartDevice":
                sending_enabled = True
                payload = {"result": "Device restarted"}
                status = 200

            else:
                payload = {"error": "Unknown command"}
                status = 404

            response = MethodResponse.create_from_method_request(
                command, status, payload
            )
            await device_client.send_method_response(response)

    # ---------------------------------------------------
    # Telemetry Sender
    # ---------------------------------------------------
    async def send_telemetry():
        global sending_enabled
        while True:
            if sending_enabled:
                telemetry = {
                    "temperature": round(random.uniform(18, 30), 2),
                    "humidity": round(random.uniform(40, 70), 2),
                    "airQualityIndex": random.randint(50, 150),
                    "environmentLux": random.randint(100, 800),
                }
                print("Sending telemetry:", telemetry)
                await device_client.send_message(str(telemetry))
            await asyncio.sleep(sampling_interval)

    # Run all tasks
    await asyncio.gather(
        send_telemetry(),
        property_listener(),
        command_listener(),
    )

if __name__ == "__main__":
    asyncio.run(main())
