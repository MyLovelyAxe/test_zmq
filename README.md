# test_zmq: test different types of message exchange with ZMQ

This reposity tests different types of message exchange with **ZMQ**, e.g. image, compressed image, point cloud, .etc.

## Requirements

This package is tested on the following environment configuration:

- python 3.11 in conda env
- pyzmq==26.4.0

---

## About

The folder structure of this repo:

```bash
.
├── outputs
│   ├── images
│   └── pcd
├── README.md
├── receiver
│   ├── zmq_comp-img_receiver.py
│   └── zmq_str_receiver.py
├── requirements.txt
└── sender

5 directories, 4 files
```

1. The scripts in `/receiver` launch ZMQ sockets which subscribe to a port to receive message;

2. The scripts in `/sender` launch ZMQ sockets which publish to a port to send message;

3. The `/outputs` folder stores testing or temporary results;

---

## Installation

Install the `pyzmq` version specified in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

Directly run corresponding `.py` script, e.g.

```bash
cd /parent_folder/test_zmq_receiver/receiver
python zmq_comp-img_receiver.py
```