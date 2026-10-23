#!/usr/bin/env python3
"""
TP04: Big Data Analytics & Containerization
Application: Safecast Radiation Big Data Analyzer
Author: Master 2 IA & Data Science
"""

import os
import sys
import csv
import json
import socket
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# Fix Windows console encoding if needed
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Global cache for analysis results
ANALYSIS_RESULTS = {}

def find_dataset():
    candidates = [
        "/app/data/safecast_5gb.csv",
        "/app/data/sample_safecast.csv",
        "/app/sample_safecast.csv",
        "data/safecast_5gb.csv",
        "data/sample_safecast.csv",
        "sample_safecast.csv"
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

def analyze_dataset(file_path, max_rows=100000):
    start_time = time.time()
    total_records = 0
    valid_values = []
    units_count = {}
    devices = set()
    locations = set()
    elevated_count = 0  # > 50 cpm or > 0.3 uSv

    min_val = float('inf')
    max_val = float('-inf')
    val_sum = 0.0

    print("=" * 60)
    print("  [+] STARTING BIG DATA ANALYSIS: SAFECAST RADIATION DATA")
    print("=" * 60)
    print(f"[*] Reading file: {file_path}")

    # Read CSV streaming
    with open(file_path, mode='r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_records += 1
            raw_val = row.get("value")
            unit = row.get("unit", "unknown") or "unknown"
            device_id = row.get("device_id")
            loc = row.get("location_name")

            if device_id:
                devices.add(device_id)
            if loc:
                locations.add(loc)

            units_count[unit] = units_count.get(unit, 0) + 1

            if raw_val:
                try:
                    v = float(raw_val)
                    valid_values.append(v)
                    val_sum += v
                    if v < min_val:
                        min_val = v
                    if v > max_val:
                        max_val = v

                    # Check elevated threshold
                    if (unit.lower() == "cpm" and v > 50.0) or (unit.lower() in ("usv", "usv/h") and v > 0.3):
                        elevated_count += 1
                except ValueError:
                    pass

            if max_rows and total_records >= max_rows:
                print(f"[*] Reached chunk limit ({max_rows:,} records) for rapid analytics.")
                break

    duration = time.time() - start_time
    avg_val = (val_sum / len(valid_values)) if valid_values else 0.0
    if min_val == float('inf'):
        min_val = 0.0
    if max_val == float('-inf'):
        max_val = 0.0

    hostname = socket.gethostname()
    try:
        host_ip = socket.gethostbyname(hostname)
    except Exception:
        host_ip = "127.0.0.1"

    results = {
        "status": "success",
        "container_id": hostname,
        "container_ip": host_ip,
        "dataset_file": os.path.basename(file_path),
        "dataset_path": file_path,
        "total_records_processed": total_records,
        "valid_readings_count": len(valid_values),
        "radiation_metrics": {
            "min_radiation": round(min_val, 4),
            "max_radiation": round(max_val, 4),
            "avg_radiation": round(avg_val, 4),
            "elevated_readings_count": elevated_count,
            "elevated_percentage": round((elevated_count / len(valid_values) * 100), 2) if valid_values else 0.0
        },
        "units_distribution": units_count,
        "unique_devices_detected": len(devices),
        "unique_named_locations": len(locations),
        "processing_time_seconds": round(duration, 4),
        "throughput_records_per_sec": round(total_records / duration, 1) if duration > 0 else 0
    }

    print("\n[ANALYSIS] --- ANALYSIS RESULTS SUMMARY ---")
    print(f"  • Container Hostname:   {hostname} (IP: {host_ip})")
    print(f"  • Records Analyzed:     {total_records:,}")
    print(f"  • Execution Time:       {duration:.3f} seconds")
    print(f"  • Processing Speed:     {results['throughput_records_per_sec']:,} rows/sec")
    print(f"  • Min Radiation:        {results['radiation_metrics']['min_radiation']}")
    print(f"  • Max Radiation:        {results['radiation_metrics']['max_radiation']}")
    print(f"  • Average Radiation:    {results['radiation_metrics']['avg_radiation']}")
    print(f"  • Elevated Readings:    {elevated_count:,} ({results['radiation_metrics']['elevated_percentage']}%)")
    print(f"  • Units Distribution:   {units_count}")
    print("=" * 60 + "\n")

    return results


class WebDashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "container": ANALYSIS_RESULTS.get("container_id")}).encode())
            return

        if self.path in ("/api", "/api/stats", "/api/results"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(ANALYSIS_RESULTS, indent=2).encode())
            return

        # HTML Dashboard
        metrics = ANALYSIS_RESULTS.get("radiation_metrics", {})
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Big Data Analytics - Safecast Radiation Container</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: #0f172a;
      color: #f8fafc;
      margin: 0;
      padding: 30px;
    }}
    .container {{
      max-width: 900px;
      margin: 0 auto;
      background: #1e293b;
      border-radius: 12px;
      padding: 30px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      border: 1px solid #334155;
    }}
    h1 {{ color: #38bdf8; margin-top: 0; display: flex; align-items: center; gap: 10px; }}
    .badge {{
      display: inline-block;
      padding: 4px 10px;
      background: #0284c7;
      color: #fff;
      font-size: 13px;
      border-radius: 6px;
      font-weight: 600;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 15px;
      margin: 25px 0;
    }}
    .card {{
      background: #0f172a;
      padding: 16px;
      border-radius: 8px;
      border: 1px solid #334155;
    }}
    .card-title {{ color: #94a3b8; font-size: 12px; text-transform: uppercase; margin-bottom: 6px; }}
    .card-value {{ font-size: 22px; font-weight: bold; color: #f1f5f9; }}
    .highlight {{ color: #10b981; }}
    .warning {{ color: #f59e0b; }}
    pre {{
      background: #0f172a;
      padding: 15px;
      border-radius: 8px;
      overflow-x: auto;
      font-size: 13px;
      color: #a7f3d0;
      border: 1px solid #334155;
    }}
    .footer {{
      margin-top: 25px;
      font-size: 13px;
      color: #64748b;
      text-align: center;
      border-top: 1px solid #334155;
      padding-top: 15px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>
      <span>⚛️ Safecast Big Data Node</span>
      <span class="badge">TP04 Container</span>
    </h1>
    <p>Container ID: <code>{ANALYSIS_RESULTS.get('container_id', 'Unknown')}</code> &bull; IP: <code>{ANALYSIS_RESULTS.get('container_ip', '127.0.0.1')}</code></p>
    
    <div class="grid">
      <div class="card">
        <div class="card-title">Records Analyzed</div>
        <div class="card-value highlight">{ANALYSIS_RESULTS.get('total_records_processed', 0):,}</div>
      </div>
      <div class="card">
        <div class="card-title">Average Radiation</div>
        <div class="card-value">{metrics.get('avg_radiation', 0)}</div>
      </div>
      <div class="card">
        <div class="card-title">Max Radiation</div>
        <div class="card-value warning">{metrics.get('max_radiation', 0)}</div>
      </div>
      <div class="card">
        <div class="card-title">Throughput</div>
        <div class="card-value highlight">{ANALYSIS_RESULTS.get('throughput_records_per_sec', 0):,} <small style="font-size:12px;">row/s</small></div>
      </div>
    </div>

    <h3>Detailed Metrics (JSON API):</h3>
    <pre>{json.dumps(ANALYSIS_RESULTS, indent=2)}</pre>

    <div class="footer">
      Module: Big Data Analytics &bull; Master 2 IA & Data Science &bull; University of Eloued
    </div>
  </div>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def log_message(self, format, *args):
        # Quiet standard logging to keep output clean
        pass


def run():
    global ANALYSIS_RESULTS
    dataset_path = find_dataset()
    if not dataset_path:
        print("[!] Error: No dataset file found! Please provide sample_safecast.csv or mount ./data")
        sys.exit(1)

    ANALYSIS_RESULTS = analyze_dataset(dataset_path)

    # Determine mode:
    # 1. If --batch flag is present: exit
    if "--batch" in sys.argv or os.environ.get("BATCH_MODE") == "1":
        print("[*] Running in BATCH mode. Task finished successfully.")
        sys.exit(0)

    # 2. If running inside Compose volume mount without explicit server flag:
    # Notice in Task 4: volumes: - ./data:/app/data:ro and restart: "no"
    if os.path.exists("/app/data") and os.environ.get("SERVER_MODE") != "1" and "--serve" not in sys.argv:
        print("[*] Detected Task 4 Data Analysis Volume (/app/data). Analysis completed.")
        sys.exit(0)

    # 3. Server mode (default for standalone containers / Task 3)
    port = int(os.environ.get("PORT", 5000))
    server = HTTPServer(("0.0.0.0", port), WebDashboardHandler)
    print(f"[*] 🌐 HTTP Server active and listening on port {port} (Container: {ANALYSIS_RESULTS.get('container_id')})...")
    print(f"[*] Endpoints: http://localhost:{port}/ (Dashboard), /api/stats (JSON), /health (Healthcheck)")
    print("[*] Press Ctrl+C or stop container to terminate.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down server.")
        server.server_close()


if __name__ == "__main__":
    run()
