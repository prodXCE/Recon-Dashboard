# Network Reconnaissance Dashboard 🚀

A web-based dashboard that automates and visualizes network reconnaissance tasks. This tool integrates Nmap, WHOIS, DNS lookups, and the Shodan API into a single, user-friendly interface, transforming command-line data into actionable, easy-to-understand insights.

---

## 🎯 The Problem

Network administrators and security analysts often need to run multiple, separate command-line tools to gather intelligence on a target. This process is manual, time-consuming, and the text-based outputs can be difficult to compare and analyze.

This dashboard solves that problem by:
* **Automating** the execution of scans from a single input field.
* **Centralizing** results from different tools into one view.
* **Visualizing** data with charts and clean tables to make it immediately understandable.

---

## ✨ Key Features

* **Nmap Port Scanning:** Performs fast (`-F`) or comprehensive (`-A`) Nmap scans and displays open ports, services, and versions.
* **Data Visualization:** Uses Chart.js to create dynamic doughnut charts of port statuses (open, closed, filtered).
* **WHOIS Lookups:** Fetches domain registration information, including registrar, creation date, and owner details.
* **DNS Resolution:** Gathers common DNS records (A, AAAA, MX, NS, TXT) for a given domain.
* **Shodan API Integration:** Pulls real-time intelligence on IP addresses, including ISP, location, known vulnerabilities, and hostnames.
* **Asynchronous Scanning:** Scans run in a background thread, providing a non-blocking user experience. The frontend polls for results and updates dynamically when the scan is complete.
* **Containerized & Production-Ready:** Fully containerized with **Docker** and includes deployment configurations for **Kubernetes**.
* **CI/CD Pipeline:** Includes a **GitHub Actions** workflow to automatically run tests and linting on every push to the `main` branch.

---

## 🛠️ Tech Stack & Architecture

This project uses a modern, scalable stack suitable for web applications and DevOps workflows.

| Category      | Technology                                                                                                  |
| :------------ | :---------------------------------------------------------------------------------------------------------- |
| **Backend** | Python 3.9+, Flask, Gunicorn                                                                                |
| **Frontend** | HTML5, CSS3, JavaScript (ES6), Chart.js                                                                     |
| **Tools** | Nmap, python-whois, dnspython, Shodan                                                                       |
| **DevOps** | Docker, Kubernetes, GitHub Actions                                                                          |
| **Monitoring**| Bugsnag (Error Monitoring)                                                                                  |

---

## 🚀 Getting Started: Local Development

Follow these instructions to get the project running on your local machine.

### Prerequisites

* Python 3.9+
* Nmap (`sudo apt install nmap` or `brew install nmap`)
* An active [Shodan](https://www.shodan.io/) account and API Key.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/prodXCE/recon-dashboard.git
    cd recon-dashboard
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # .\venv\Scripts\activate   # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your API Key:**
    * Create a `config.py` file in the root directory.
    * Add your Shodan API key to it:
        ```python
        # config.py
        SHODAN_API_KEY = "YOUR_SHODAN_API_KEY_HERE"
        ```

### Running the Application

Start the Flask development server:
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 🐳 Deployment with Docker & Kubernetes

This application is designed to be deployed as a container.

### Using Docker

1.  **Build the Docker image:**
    ```bash
    docker build -t recon-dashboard .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 5000:5000 recon-dashboard
    ```
    The application will be accessible at `http://localhost:5000`.

### Using Kubernetes

A local Kubernetes cluster (like the one in Docker Desktop) is required.

1.  **Ensure your Docker image is available** to the cluster. If using Docker Desktop, the local image is automatically available.

2.  **Apply the Kubernetes configurations:**
    ```bash
    kubectl apply -f k8s/
    ```
    This will create a `Deployment` with 2 replicas and a `Service` of type `LoadBalancer`.

3.  **Access the application:**
    Wait for the service to get an external IP (on Docker Desktop, this will be `localhost`). Check the status with `kubectl get service recon-dashboard-service`. Once ready, the application will be accessible at `http://localhost`.

---

## 🔄 CI/CD Pipeline

This project uses **GitHub Actions** for Continuous Integration. The workflow is defined in `.github/workflows/ci.yml` and performs the following on every push to `main`:
1.  Checks out the code.
2.  Sets up a Python environment.
3.  Installs all dependencies from `requirements.txt`.
4.  Runs the `flake8` linter to check for code quality and syntax errors.

---

## 🔮 Future Improvements

* **User Authentication:** Add user accounts to save and manage scan history.
* **Database Integration:** Store scan results in a database like PostgreSQL for persistent storage and analysis over time.
* **Scheduled Scans:** Implement a task queue like Celery with Celery Beat to allow users to schedule recurring scans.
* **Export Results:** Add functionality to export scan results as PDF or CSV reports.

---
