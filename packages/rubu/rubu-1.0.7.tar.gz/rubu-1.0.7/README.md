# Rubu Tech – Temas Socket API

## Overview

This Python package provides an intuitive API to control and communicate with Temas hardware devices via TCP/IP socket communication. It is particularly suitable for laboratory environments, test setups, robotic systems, and other precise positioning or sensing scenarios.

---

## Features

- TCP/IP socket communication to Temas devices
- Distance measurement (laser sensor)
- Precise pan and tilt positioning
- Real-time camera frame retrieval (visual and ToF)
- Easy-to-use object-oriented API
- Built-in threading support for camera streams
- Point cloud scanning and retrieval
- Adjustable camera settings (exposure, brightness, saturation, contrast, gain, lens position)

---

## Installation

Install via pip:

```bash
pip install rubu-tech-pypi
```

---

## Usage

### Extended Example: Query distance, positioning, camera stream, and additional features

```python
import cv2
from rubu import temas

# Connect to the device (via hostname or IP address)
device = temas.Connect(hostname="temas")
# Alternatively: device = temas.Connect(ip_address="192.168.4.4")

# Initialize control class
control = temas.Control()

# Measure distance (laser, in cm)
distance = control.distance()
print(f"Measured distance: {distance} cm")

# Move to a specific position (Pan, Tilt)
control.move_pos(60, 30)

# Initialize camera (Visual Port: 8081, ToF Port: 8084)
camera = temas.Camera(port=8081)
camera.start_thread()

# Adjust camera settings
camera.set_exposure_time(5000)
camera.set_brightness(70)
camera.set_contrast(50)

# Start point cloud scan
control.start_point_cloud_scan(theta1=10, theta2=20, phi1=30, phi2=40)

while True:
    try:
        frame = camera.get_frame()
        if frame is not None:
            cv2.imshow('Visual Camera', frame)

        scan_percent = control.get_point_cloud_scan_percent()
        print(f"Scan completion: {scan_percent}%")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting camera stream...")
            break
    except Exception as e:
        print(f"Error retrieving camera frame: {e}")

# Save point cloud
control.get_pcl(path="./")

# Reset camera and control
control.move_home()
camera.stop_thread()
cv2.destroyAllWindows()
print("Program terminated.")
```

---

## Parameters

### Connection

- `hostname`: Hostname of the Temas device in the local network (default: "temas")
- `ip_address`: Direct IP address of the Temas device

### Control Class

- `Control(port=8082)`
  - `port`: TCP port for movement control commands (default: `8082`)

### Camera Class

- `Camera(port=8081)`
  - `port`: TCP port for camera stream (default visual: `8081`, ToF: `8084`)

---

## License

MIT License © 2025 rubu-tech

---

## Contact

For more information, visit [https://rubu-tech.de](https://rubu-tech.de)  
or contact us via email: **info@rubu-tech.de**
