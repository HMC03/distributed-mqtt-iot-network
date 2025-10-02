# Distributed MQTT IoT Network

A multi-device IoT system demonstrating **real-time sensor-to-actuator control, device presence monitoring, and fault-tolerant messaging** using the **MQTT protocol**.

## System Overview
This project coordinates **three Raspberry Pis and two laptops** through a locally hosted MQTT broker.

- **RasPi A** → Publishes sensor data (LDR + potentiometer) with retain + last-will.
- **RasPi C** → Subscribes to sensor values, compares against thresholds, publishes LED control signals.
- **RasPi B** → Subscribes to device statuses and LED signals, drives three LEDs for visualization.
- **Laptop 1** → Runs MQTT broker.
- **Laptop 2** → Subscribes to all topics, logs messages with timestamps.

## Features
- Distributed IoT architecture with multiple publishers and subscribers  
- Online/offline detection using retained messages + last-will  
- Real-time sensor threshold → actuator logic  
- Centralized logging and duplicate message suppression  

## Architecture Diagram
```mermaid
flowchart LR
    subgraph Broker [Laptop 1 - MQTT Broker]
    end
    RasPiA -->|lightSensor/threshold| Broker
    RasPiC -->|LightStatus| Broker
    RasPiA -->|Status/RaspberryPiA| Broker
    RasPiC -->|Status/RaspberryPiC| Broker
    Broker --> RasPiB
    Broker --> Laptop2
