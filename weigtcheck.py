import asyncio
from bleak import BleakScanner

def parse_mi_weight(manufacturer_data: dict):
    for cid, payload in manufacturer_data.items():
        b = bytes(payload)
        if len(b) >= 12:
            try:
                raw = int.from_bytes(b[10:12], byteorder="little")
                weight = raw / 200.0
                if 10.0 <= weight <= 300.0:
                    return weight, b
            except Exception:
                pass
    return None, None

async def scan_once(timeout=5.0):
    devices = await BleakScanner.discover(timeout=timeout)
    found = False
    for d in devices:
        md = d.metadata.get("manufacturer_data", {})
        if md:
            weight, raw = parse_mi_weight(md)
            if weight is not None:
                print(f"Waage gefunden: {d.address} | Gewicht: {weight:.2f} kg | raw={raw.hex()}")
                found = True
    if not found:
        print("Keine Waage erkannt – bitte auf die Waage stellen und erneut probieren.")

if __name__ == "__main__":
    asyncio.run(scan_once())
