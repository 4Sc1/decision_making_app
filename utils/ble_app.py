# not used

# import asyncio
# import csv
# import datetime
# from datetime import timezone

# from bleak import BleakClient

# ADDRESS = 'f8:26:8c:f6:e9:6e'
# HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
# ECG_CONTROL_UUID = "fb005c81-02e7-f387-1cad-8acd2d8df0c8"
# ECG_DATA_UUID = "fb005c82-02e7-f387-1cad-8acd2d8df0c8"
# ECG_WRITE = bytearray([0x02, 0x00, 0x00, 0x01, 0x82, 0x00, 0x01, 0x01, 0x0E, 0x00])

# hr_queue = asyncio.Queue()
# ecg_queue = asyncio.Queue()

# async def handle_hr_data():
#     batch = []
#     with open('heart_rate_data.csv', 'a', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file, delimiter=';')
#         while True:
#             data = await hr_queue.get()
#             batch.append(data)
#             if len(batch) >= 73:
#                 writer.writerows(batch)
#                 file.flush()  # Flush after each batch is written
#                 batch.clear()  # Clear the batch after writing
#             hr_queue.task_done()

# async def handle_ecg_data():
#     batch = []
#     with open('ecg_data.csv', 'a', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file, delimiter=';')
#         while True:
#             data = await ecg_queue.get()
#             batch.append(data)
#             if len(batch) >= 73:
#                 writer.writerows(batch)
#                 file.flush()  # Flush after each batch is written
#                 batch.clear()  # Clear the batch after writing
#             ecg_queue.task_done()

# def decode_heart_rate(sender, data):
#     timestamp = datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
    
#     flags = data[0]
#     format_bit = flags & 0x01
#     rr_interval_present = (flags >> 4) & 0x01

#     index = 1
#     heart_rate = data[index] if format_bit == 0 else int.from_bytes(data[index:index+2], byteorder='little')
#     index += 1 if format_bit == 0 else 2

#     rr_intervals = []
    
#     if rr_interval_present:
#         while index < len(data):
#             rr_interval = int.from_bytes(data[index:index+2], byteorder='little') * (1/1024)
#             rr_intervals.append(rr_interval)
#             index += 2
    
#     for rr in rr_intervals:
#         asyncio.create_task(hr_queue.put([timestamp, heart_rate, rr]))
    
# def decode_ecg_data(sender, data):
#     timestamp = datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
    
#     if data[0] == 0x00:
#         step = 3
#         offset = 10
#         while offset < len(data):
#             ecg = int.from_bytes(data[offset:offset + step], byteorder="little", signed=True)
#             asyncio.create_task(ecg_queue.put([timestamp, ecg]))
#             offset += step
    
# async def run(client):
#     if not client.is_connected:
#         raise Exception("Failed to connect to the device.")
#     print("Device connected")

#     await client.write_gatt_char(ECG_CONTROL_UUID, ECG_WRITE)
#     await client.start_notify(HEART_RATE_UUID, decode_heart_rate)
#     await client.start_notify(ECG_DATA_UUID, decode_ecg_data)

#     hr_handler = asyncio.create_task(handle_hr_data())
#     ecg_handler = asyncio.create_task(handle_ecg_data())

#     # Correct way to handle blocking input in an async function
#     await asyncio.get_event_loop().run_in_executor(None, input, "Press Enter to exit...\n")

#     hr_handler.cancel()
#     ecg_handler.cancel()
#     await client.stop_notify(HEART_RATE_UUID)
#     await client.stop_notify(ECG_DATA_UUID)

# async def main():
#     async with BleakClient(ADDRESS) as client:
#         #await client.connect()
#         await run(client)

# if __name__ == "__main__":
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(main())