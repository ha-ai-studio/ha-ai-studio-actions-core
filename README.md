# HA AI Studio Actions Core

Core Git action types for HA AI Studio. This repository contains Echo, a technical
transport test that returns the supplied JSON data unchanged. It contains no
MQTT client, application credentials or workflow orchestration.

## Install in HA AI Studio

1. Publish this repository to a public HTTPS Git remote.
2. Open **Settings → Action repositories → Add repository** in HA AI Studio.
3. Enter the actual HTTPS clone URL and a branch, tag or commit, then wait for Ready.
4. Choose **Create action → Echo**. Each instance installs into its own Python venv.
5. Wait for the environment to become Ready, configure Input and Output, then activate.

No local repository source is required or supported by the app. The app's Git
runner requires Python 3.12. Echo uses only the standard library and installs no
third-party packages. Repository refresh never executes action code. Installation
imports the entrypoint to verify the contract; execution happens in a separate
process. Install only code you trust: a venv is not a security sandbox.

Existing app-bundled Echo instances keep their original IDs, configuration, jobs
and runtime as compatibility instances. They are not automatically migrated to
this repository. New instances use the Git catalog and a fixed commit. Git action
draft preview is currently unavailable; use isolated brokers and synthetic data
for integration tests.

## Repository layout

```text
actions/echo/
  action.json         # Metadata, schemas, version and example request
  action.py           # async execute(data, settings)
  requirements.lock   # No external dependencies
```

The input and output schemas describe the envelope's `data` value. Echo accepts
any finite JSON value, including null, booleans, strings, numbers, arrays and
objects. Settings must be an empty object. The HA AI Studio runtime owns envelope
validation, MQTT, durable request IDs, deduplication and result delivery.

Example request:

```json
{"request_id": "test-001", "data": {"message": "Hello", "value": 42}}
```

Successful result:

```json
{"request_id": "test-001", "status": "success", "data": {"message": "Hello", "value": 42}}
```

## Tests

Run `python3 -m unittest discover -s tests -v`. Tests use synthetic data and do not
connect to MQTT or any external service. This repository has no dependency on the
HA AI Studio source tree.

Licensed under MIT; see LICENSE.
