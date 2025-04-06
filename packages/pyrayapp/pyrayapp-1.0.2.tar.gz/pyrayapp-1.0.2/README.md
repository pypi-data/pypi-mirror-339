# pyray

Python [Ray](https://myray.ap) debugging client.

This package allows you to send structured debug payloads to Ray.app from your Python application,
including rich content like text, images, HTML, and formatted dumps — all with optional delayed sending.

## Features

- Send payloads like strings, booleans, images, dumps, and more
- Lazy evaluation — chain multiple calls and send once
- Stack trace origin support
- Compatible with Ray.app (https://myray.app)

## Installation

```bash
pip install pyrayapp
```

## Usage

```python
from pyrayapp import ray

ray("Hello from Python!").color("green").notify("Payload sent!").pause()
```

## License

MIT — see [LICENSE](./LICENSE)
