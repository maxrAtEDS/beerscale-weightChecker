import asyncio
from bleak import BleakScanner

def parse_mi_weight(manufacturer_data: dict):
    """
    Versucht, aus dem manufacturer_data-Feld das Gewicht zu extrahieren.
    Viele Xiaomi-Waagen senden das in bytes[10:12], skaliert durch 200.
    """
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
    print(f"🔍 Scanne nach BLE-Geräten für {timeout} Sekunden...\n")
    devices = await BleakScanner.discover(timeout=timeout)
    found = False

    for d in devices:
        name = d.name or "Unbekanntes Gerät"
        addr = d.address
        md = d.metadata.get("manufacturer_data", {})

        # Versuche, Gewicht zu dekodieren
        weight, raw = parse_mi_weight(md)
        if weight is not None:
            print(f"📟 Gerät: {name}")
            print(f"   Adresse: {addr}")
            print(f"   Gewicht: {weight:.2f} kg")
            print(f"   Rohdaten: {raw.hex()}\n")
            found = True
        else:
            # Optionale Ausgabe, falls du alle Geräte sehen willst:
            # print(f"Gefunden: {name} ({addr})")
            pass

    if not found:
        print("❌ Keine Xiaomi-Waage erkannt – bitte auf die Waage stellen und erneut probieren.")


if __name__ == "__main__":
    asyncio.run(scan_once())
