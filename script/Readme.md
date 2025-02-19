# ⚙️ CPU Monitoring Script

This project is a Python-based CPU monitoring tool that tracks CPU usage at regular intervals, alerts when usage exceeds a specified threshold, and logs the data to a FastAPI backend. It generates a detailed report at the end of each test run.

---

## 📜 **Table of Contents**
1. [Features](#-features)
2. [Tech Stack](#-tech-stack)
3. [Installation](#️-installation)
5. [Usage](#-usage)
6. [Example Output](#-example-output)
7. [Final Report](#-final-report)
8. [Future Enhancement Work](#-future-enhancement-work)

---

## 🚀 **Features**
- User authentication (register/login).
- Monitors CPU usage every 5 seconds by default.
- Alerts when CPU usage exceeds the configured threshold.
- Logs CPU usage to the FastAPI backend.
- Generates a detailed test run report, including:
  - Total test duration.
  - Time CPU usage exceeded the threshold.
  - CPU usage logs.

---

## 🛠️ **Tech Stack**
- **Language:** Python
- **Backend API:** FastAPI
- **Database:** MongoDB
- **Libraries:** Psutil, Requests, Colorama, Tabulate

---

## ⚙️ **Installation**

1. **Install Python:**
[Follow this document](https://www.python.org/downloads/)

2. **Clone the repository:**
```bash
git clone https://github.com/yourusername/script.git
```

3. **Navigate the directory:**
```bash
cd script
```

3. **Configure the script:**
Create a `.env` file in the root directory (script). Follow .env.example as a reference.

4. **Install the script:**
```bash
pip install .
```

---

## 🚦 **Usage**

1. **Run the CPU monitoring script:**
Open the terminal and run following command:
```bash
cpu-monitor
```

2. **Interactive Menu Options:**
- **Register:** Create a new user account.
- **Login:** Authenticate to access monitoring features.
- **Scan CPU:** Start a new test run.
- **Quit:** Exit the application.

3. **Start Monitoring:**
Once logged in, select **Scan CPU**, provide:
- Test run name.
- Interval (seconds).
- Threshold (%).

Example:
```bash
Please give a name to this scan: Performance Test
Please enter interval (s) to save data: 5
Please enter a threshold value: 75
```

Press **Ctrl+C** to stop the monitoring.

---

## 📊 **Example Output**

```bash
## Welcome to CPU Monitor ##
This tool will monitor your CPU utilization and alert you if it exceeds the given threshold.

1) Register
2) Login
3) Quit
Please select an option (e.g. 1):

```

---

## 📈 **Final Report**

After stopping the scan (Ctrl+C), the following report is generated:

```bash
=== Monitoring Report ===
Test Run ID: 653a1e2bcf51a7c3f4b67b9b
Test Run Name: Performance Test
Total runtime: 300.5 seconds
Time above threshold: 45.0 seconds

+-------+---------------------+---------+
| S.No  | Timestamp           | CPU %   |
+-------+---------------------+---------+
| 1     | 2025-02-19 10:00:00 | 35.2    |
| 2     | 2025-02-19 10:00:05 | 78.6    |
| 3     | 2025-02-19 10:00:10 | 65.4    |
+-------+---------------------+---------+
```

---

## 🐍 **Uninstalling the Script**

To uninstall the script:

```bash
pip uninstall cpu-monitor
```
---

## 🚀 **Future Enhancement Work**
- **Dynamic Threshold:** Allow dynamic threshold adjustment during monitoring without restarting the script.
- **Historical Reports:** Save test run reports to a local file (CSV/JSON) for future reference.
- **Email/Slack Alerts:** Send notifications when CPU usage exceeds the threshold.
- **Resource Monitoring:** Multi-Core Monitoring: Display per-core CPU usage alongside overall usage. Extend monitoring to include memory, disk, and network usage.


 
 
 