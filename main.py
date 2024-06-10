from bleak import BleakClient
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Union

app = FastAPI()

# UUIDs for the BLE service and characteristics
SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
CHARACTERISTIC_UUID_RX = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

# Replace this with your ESP32's MAC address
DEVICE_ADDRESS = "AE3E8C07-584F-76DE-5522-F8ABCAFC0030"

async def send_command(command: int) -> dict:
    try:
        async with BleakClient(DEVICE_ADDRESS) as client:
            if client.is_connected:
                print(f"Connected to {DEVICE_ADDRESS}")
                command_str = str(command).encode()
                await client.write_gatt_char(CHARACTERISTIC_UUID_RX, command_str, response=True)
                print(f"Sent command: {command}")
                return {"status": "success", "command": command}
            else:
                print("Failed to connect to the device")
                return {"status": "failed", "reason": "Failed to connect"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "failed", "reason": str(e)}

@app.post("/left")
async def left(request: Request):
    data = await request.json()
    check = data.get("value")
    if check is not None:
        result = await send_command(3)  # Directly await the async function
        return result
    else:
        return {"status": "failed", "reason": "value not provided"}

@app.get("/check")
async def check():
      # Directly await the async function
      result = await send_command(2) 
      return result
@app.get("/right")
async def right():
      # Directly await the async function
      result = await send_command(2) 
      return result
@app.get("/front")
async def front():
      # Directly await the async function
      result = await send_command(1) 
      return result
@app.get("/down")
async def down():
      # Directly await the async function
      result = await send_command(4) 
      return result
@app.get("/stop")
async def stop():
      # Directly await the async function
    result = await send_command(-1)  # Directly await the async function
    return result
