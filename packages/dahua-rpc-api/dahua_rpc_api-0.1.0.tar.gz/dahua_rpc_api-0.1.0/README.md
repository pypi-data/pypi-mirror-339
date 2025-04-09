# Dahua RPC API

A Python package that provides a convenient API for interacting with Dahua RPC services.

## Installation

You can install this package using pip directly from PyPI. Simply run:

```bash
pip install dahua-rpc-api
```

If you prefer to install from source, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/dahua-rpc-api.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd dahua-rpc-api
   ```

3. **Install the package:**

   ```bash
   pip install .
   ```

## Usage

After installation, you can import the package in your Python scripts as follows:

```python
from dahua.client import DahuaRpc

client = DahuaRpc(host="172.20.10.254", port=80)
client.login(username="admin", password="password")

print("Serial Number: " + client.magic_box.get_serial_number())
```

Find a few examples [here](./examples/)

## Contributing

Contributions and feedback are welcome. Please submit bug reports or pull requests via the project repository.

## License

This project is licensed under the MIT License.
