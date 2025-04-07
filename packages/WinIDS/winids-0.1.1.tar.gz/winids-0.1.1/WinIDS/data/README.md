# WinIDS Data Files

This directory contains data files used by the WinIDS system.

## Expected Files

- `traffic_log.json`: Log of recent traffic data
- `alert_history.json`: History of detected alerts
- `system_stats.json`: System statistics and performance metrics
- `config.json`: Configuration settings for the WinIDS system

## File Formats

### traffic_log.json

This file contains the most recent network traffic processed by the system:

```json
[
  {
    "timestamp": "2023-04-06T20:15:30.123Z",
    "features": [0.1, 0.2, 0.3, ...],
    "prediction": 0.12,
    "classification": "normal"
  },
  ...
]
```

### alert_history.json

This file contains a history of detected intrusions:

```json
[
  {
    "timestamp": "2023-04-06T20:15:30.123Z",
    "attack_type": "dos",
    "confidence": 0.95,
    "source_ip": "192.168.1.100",
    "details": { ... }
  },
  ...
]
```

### system_stats.json

This file contains system performance statistics:

```json
{
  "uptime": 3600,
  "total_packets": 50000,
  "alerts": 12,
  "last_update": "2023-04-06T20:15:30.123Z",
  "cpu_usage": 5.2,
  "memory_usage": 128.5
}
```

### config.json

This file contains configuration settings:

```json
{
  "threshold": 0.7,
  "buffer_size": 10,
  "check_interval": 1,
  "bridge_host": "localhost",
  "bridge_port": 5000,
  "disable_attacks": false
}
```

## Data Retention

By default, the WinIDS system retains the last 1000 traffic entries and 100 alerts. 
These limits can be configured in the system settings. 