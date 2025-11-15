# 📡 BLE Visibility Map

### _Real-time Detection, Labeling & Analysis of Nearby BLE Devices_  
**Educational Cybersecurity Project – Python Backend + React/Mantine Frontend**

---

## 📌 Overview

The **BLE Visibility Map** is an educational project designed to demonstrate how Bluetooth Low Energy devices can be discovered, profiled, tagged, monitored, and analyzed from a cybersecurity perspective.

Modern devices broadcast BLE advertisement packets even when not connected. This system captures those broadcasts using a scanning gateway, sends them to a Python backend for processing, and visualizes them in a React-based web dashboard built with **Mantine UI**.

Users can:

- 🔍 View nearby BLE devices in real-time  
- 🏷️ Tag devices with labels (e.g. “Unknown tracker”, “Suspicious”, “Peeper device”)  
- 🚨 Enable notifications for high-risk devices  
- 📊 View RSSI trends, presence history, travel patterns, and appearance frequency  
- 🌍 Visualize device movement on a map (using floor mapping or GPS where applicable)  

This project aims to demonstrate **cybersecurity, wireless scanning, IoT telemetry, backend architecture, and frontend web development**.

---

## 🎯 Project Goals

This project showcases the following cybersecurity competencies:

- **Passive wireless reconnaissance** (BLE scanning & fingerprinting)  
- **Threat modeling** for consumer BLE devices  
- **IoT device profiling** using advertising fields  
- **Data correlation & anomaly detection**  
- **Local event-based alerting**  
- **Secure API design**  
- **Secure handling of MAC addresses & PII considerations**  

And the following web engineering skills:

- Modern **React + Mantine** UI  
- **Real-time UI updates** with WebSockets or polling  
- **REST API consumption**  
- **Clean architecture + modular design**  
- **Animated SVGs, maps, and responsive components**  

---

## 🧱 Tech Stack

### **Frontend**
- React + Vite  
- Mantine UI components  
- Zustand for state  
- React Query for async data  
- Leaflet / Maplibre for mapping  
- Web Bluetooth (for direct browser scanning)

### **Backend (Python)**
- FastAPI
- SQLite   
- BLE parser (custom)  
- Device fingerprinting utility  
- Threat scoring engine  
- Event & alert system

### **Scanning Gateway**
Supports any of the following: 
- **Linux machine** using `bleak`

Gateway pushes scan events → Python backend → database → frontend dashboard.

---

## 📡 How the System Works

1. **Gateway scans BLE advertisements**  
   - Collects MAC, RSSI, device type flags, manufacturer data, UUIDs, Tx power, etc.

2. **Parsed data sent to Python API**  
   - `/scans` endpoint accepts raw scan events  
   - Device fingerprinting extracts metadata like vendor, device type, risks

3. **Device profiles stored in DB**  
   - Appear/disappear times  
   - Movement / signal trend  
   - Tags & user notes

4. **Frontend visualizes everything**  
   - Device tables & cards  
   - Risk indicators  
   - Maps  
   - History timeline  

5. **User can tag devices & enable alerts**  
   - Backend generates events when tagged devices reappear  

---

## 🗂 File Structure

```

ble-threat-tracker/
│
├── backend/
│   ├── main.py               # FastAPI/Flask entry point
│   ├── models.py             # ORM / DB models
│   ├── database.py           # Connection & migrations
│   ├── routers/
│   │   ├── scans.py          # /scans endpoint
│   │   ├── tags.py           # /tags endpoint
│   │   ├── events.py         # /events endpoint
│   ├── services/
│   │   ├── fingerprint.py    # Analyze BLE adv data
│   │   ├── threat_engine.py  # Suspicion scoring
│   │   ├── notifier.py       # Event trigger logic
│   ├── utils/
│   │   ├── rssi_tools.py     # RSSI distance estimations
│   │   ├── manufacturer_db.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Mantine components
│   │   ├── pages/            # Dashboard, Map, Device Details
│   │   ├── store/            # Zustand or context
│   │   ├── api/              # Backend API calls
│   │   ├── assets/           # Icons, animated SVGs
│   │   └── main.jsx
│   ├── vite.config.js
│   └── package.json
│
├── gateway/
│   ├── ble_scanner_simulator.py       # Python scanning code
│   └── requirements.txt          # bleak,httpx pip install
│
├── diagrams/
│   └── architecture.svg      # Animated icon-enhanced SVG
│
└── README.md

```

---

## ⚙️ Installation

### **1. Backend and Scanner (Python)**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start server
uvicorn main:app --reload
```

Backend runs by default on:
**[http://localhost:8000](http://localhost:8000)**

Once the backend is running successfully:

1.  Open a **new terminal** (keep the backend terminal running).
2.  Navigate to the **`gateway/`** directory. (`cd gateway`)
3.  Ensure you havesetup virtual env for the scanner.
    ```bash
    python3 -m venv venv_scanner
    source venv_scanner/bin/activate
    pip install -r requirements.txt
    ```
4.  Run the scanner in the same `venv_scanner` terminal:
    ```bash
    python ble_scanner_simulator.py
    ```
5.  You should see output in the scanner terminal about devices being found and posted, and in the backend terminal, you'll see successful `201 Created` responses.

**NOTE: ensure that bluetooth is turned on in the device you are scanning with**

---

### **2. Frontend (React + Mantine)**

```bash
cd frontend
npm install
npm run dev
```

Frontend runs by default on:
**[http://localhost:5173](http://localhost:5173)**

---

## 🔄 API Endpoints

### POST **/scans**

Submit a BLE scan event.

### GET **/devices**

List known devices.

### POST **/tags**

Add or update a label.

### POST **/events**

Record an alert trigger.

### GET **/history/:mac**

Device presence timeline.

---

## 🔐 Security Considerations

This project covers:

* BLE passive reconnaissance
* MAC address handling
* Device fingerprinting ethics
* Local threat detection logic
* Risks from trackers / unknown BLE beacons

It does **not** attempt to deanonymize users, decrypt traffic, or perform unauthorized tracking.

---

## ⚠️ Legal & Ethical Disclaimer

This project is strictly for:

* **Education**
* **Research**
* **Cybersecurity portfolio demonstration**

You must **only scan BLE devices in environments where you have permission**.

BLE devices broadcast public, non-encrypted advertisement frames, but:

* Do **not** attempt to track people without consent.
* Do **not** use this project for surveillance or malicious activities.
* The author(s) are **not responsible** for misuse of this software.

Use this project responsibly and ethically.

---

## 🧪 Planned Enhancements

* Machine learning identification of device categories
* Heatmaps of BLE movement
* Real-time WebSocket updates
* Offline mode for gateway
* Multi-gateway syncing
* Password-protected dashboards

---

## 📬 Contact / Hiring

If you’d like to know more or see a live demo, feel free to reach out.

---