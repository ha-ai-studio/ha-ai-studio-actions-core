# HA AI Studio Actions Core

**A simple starting point for testing and building HA AI Studio plugins.**

This plugin provides **Echo**, an Action that returns the JSON data you send to it. Use it to check the connection between Home Assistant and [HA AI Studio](https://github.com/ha-ai-studio/ha-ai-studio), test request/result handling, or explore a minimal Action implementation before building your own.

Echo runs locally in Studio without external services or additional Python dependencies. It performs no AI inference; it helps you verify the communication path before configuring more specialized Actions.

## Before you start

- A current **[HA AI Studio](https://github.com/ha-ai-studio/ha-ai-studio)** installation.
- An **MQTT v5 broker** configured in Studio and connected to Home Assistant's MQTT integration.

## 1. Install the plugin

1. Open **Settings → Action repositories → Add repository** in Studio.
2. Select **Git** and enter this repository URL:

   ```text
   https://github.com/ha-ai-studio/ha-ai-studio-actions-core
   ```

3. Use `main` as the ref, or select a specific tag or commit.
4. Wait for the repository to become **Ready**.
5. Open **Actions → Create action**, give the Action a name and select **Echo**.
6. Open its configuration and wait for its environment to become **Ready**.

## 2. Configure Echo

Echo needs no type-specific settings. Configure its MQTT routes:

| Setting | Example |
| --- | --- |
| **Input broker** | The broker used by Home Assistant |
| **Request topic** | `ha-ai-studio/example/echo/request` |
| **Output broker** | **Same as input** |
| **Result topic** | `ha-ai-studio/example/echo/result` |

Use different request and result topics. Under **General**, select **Active** and **Save**.

## 3. Test from Home Assistant

Open **Test in Home Assistant** on the Action and copy the generated YAML into a new Home Assistant automation. Save and enable it, then choose **Run actions**. Check the resulting notification and Studio's **Live activity** view.

To send a request yourself, publish JSON to the request topic with **QoS 1** and **retain disabled**:

```json
{
  "request_id": "test-001",
  "data": {
    "message": "Hello",
    "value": 42
  }
}
```

The result arrives on the configured result topic:

```json
{
  "request_id": "test-001",
  "status": "success",
  "data": {
    "message": "Hello",
    "value": 42
  }
}
```

The matching `request_id` connects the result to your request. Use a new ID for each new test. When retrying a missing result, resend the same ID and data while Studio still has the result cached.

Echo accepts any valid JSON value in `data`, including objects, arrays, strings, numbers, booleans and `null`. It preserves the value, not the original JSON formatting.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Echo is missing from the Action types | Check the repository URL, ref and status in Settings. |
| No response arrives | Check that the Action is saved and Active, the brokers are connected, and the request/result topics match. Inspect **Live activity**. |
| Request is ignored | Ensure retain is disabled and the message uses the request envelope shown above. |
| `request_id_conflict` | The ID was already used with different data. Use a new ID for a new request. |

## Build your own Action

Echo is a minimal example of the [Studio plugin contract](https://github.com/ha-ai-studio/ha-ai-studio/blob/main/ha_ai_studio/app/action_types/README.md):

```text
actions/echo/
  action.json         # Action metadata, schemas and example request
  action.py           # execute(data, settings) implementation
  requirements.lock   # Dependency lockfile; Echo has no external dependencies
```

Studio handles MQTT, request validation, execution and result delivery. Your Action implements the processing logic and declares its input, output and settings schemas. Echo uses Python 3.12 and runs in a per-instance environment managed by Studio.

For local plugin development and source reloading, see [Studio's development guide](https://github.com/ha-ai-studio/ha-ai-studio/blob/main/docs/DEVELOPMENT.md).

Run the plugin tests from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

These tests use synthetic data and do not connect to MQTT or external services.

## License

MIT — see [LICENSE](LICENSE).
