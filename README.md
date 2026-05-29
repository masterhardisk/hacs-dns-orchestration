# DNS Orchestration - Home Assistant Integration

This is a custom Home Assistant integration for exposing DNS Orchestration backend data as native Home Assistant sensors.

It currently focuses on providing the **public IP address** of the system, with support for additional DNS-related metrics in future versions.

---

## 📦 Current Features (v1)

- Public IP sensor

- Backend-driven data via REST API

- Periodic polling using Home Assistant DataUpdateCoordinator

- Docker-friendly networking support

---

## 🧠 Architecture

The integration acts as a lightweight client for your DNS Orchestration backend.

Flow:

DNS Orchestration Backend
↓
GET /system/ip
↓
Home Assistant Coordinator
↓
Sensor Entity (DNS Public IP)
↓
Dashboard / Automations

---

## 🔌 Backend Requirement

This integration depends on the DNS Orchestration backend:

👉 https://github.com/masterhardisk/Dns-Orchestration

The backend must be running and reachable from Home Assistant in order for the integration to function correctly.

The integration consumes REST endpoints exposed by the backend (see API documentation in the repository).

### GET `/system/ip`

Example response:

```json

{

  "current_ip": "79.159.56.23",

  "last_change": "29/05/2026 14:10",

  "last_change_relative": 1618

}
```

---

## 🚀 Installation (HACS)

1. Add repository to HACS

	* Go to HACS → Integrations
	* Click ⋮ → Custom repositories
	* Add this GitHub repository
	* Category: Integration

2. Install integration

	Search:
	`DNS Orchestration`
	
	Click install.
	
3. Restart Home Assistant

	Required after installation.
	
4. Add integration

	Go to:
	`Settings → Devices & Services → Add Integration`
	
	Select:
	`DNS Orchestration`
	
5. Configure

	You will be prompted for:
	
	* Backend URL
	
	Examples:
	
	Docker (recommended)
	`http://host.docker.internal:8010`
	
	LAN
	`http://192.168.1.X:8010`
	
---

## 🧪 Sensor created

After setup, the following entity will be available:

DNS Public IP

Entity ID: `sensor.dns_public_ip`

State: `79.159.56.23`

Attributes:

* `last_change`
* `last_change_relative`

---

## ⚙️ Update behavior

The integration uses:

* Home Assistant DataUpdateCoordinator
* Periodic polling of /system/ip
* Cached state updates

Default update interval is defined in the integration options.

---

## 🧱 Requirements

* Home Assistant 2024.1+
* HACS installed
* DNS Orchestration backend running and reachable
		
---

## 📄 License

This project is licensed under the MIT License.
You are free to use, modify and distribute this software under the terms of the MIT license.

---

## 👤 Maintainer

This project was created and is maintained by [MasterHardisk](https://gerardcontador.com).

---

<p align="center">
  Built for automation, extensibility, and clean system design.
</p>
