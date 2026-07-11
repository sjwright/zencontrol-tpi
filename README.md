# Zencontrol TPI

Home Assistant custom integration for [zencontrol](https://zencontrol.com) application controllers over TPI Advanced.

## Currently supports

- **Profiles**
- **Lights**
- **Groups**, including scene recall for groups
- **Button events**
- **System variables**, where the SV name is suffixed with `switch` or `sensor`

## Requirements

- A zencontrol application controller with a **TPI Advanced** license
- Network reachability to the controller (host/port); MAC address is used for identification
- [`zencontrol-python`](https://github.com/sjwright/zencontrol-python)

## Install

Copy `custom_components/zencontrol_tpi` into your Home Assistant `custom_components` directory (or install via HACS once published), then add **Zencontrol TPI** from Settings → Devices & services.

Install the Python dependency from the sibling library, for example:

```bash
pip install "zencontrol-python@git+https://github.com/sjwright/zencontrol-python.git@main"
```

For local development against an editable checkout:

```bash
pip install -e /path/to/zencontrol-python
```

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install homeassistant
pip install -e ../zencontrol-python   # or the git URL above
./run-ha
```

`./run-ha` starts Home Assistant with `dev-config/`. Use `./reset-ha` to wipe the local HA config state.

## License

[LGPL-2.1](LICENSE)
