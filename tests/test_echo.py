import asyncio
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('echo', ROOT / 'actions/echo/action.py')
echo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(echo)


class EchoTests(unittest.IsolatedAsyncioTestCase):
    async def test_all_json_values(self):
        for value in [None, False, True, 0, -1, 1.5, '', 'Hello ☀', [], {}, [1, False], {'nested': [None, {'x': 42}]}]:
            with self.subTest(value=value):
                result = await echo.execute(value, {})
                self.assertEqual(json.dumps(result), json.dumps(value))

    async def test_result_is_an_independent_copy(self):
        data = {'items': [{'value': 42}]}
        result = await echo.execute(data, {})
        result['items'][0]['value'] = 0
        self.assertEqual(data, {'items': [{'value': 42}]})

    async def test_settings_are_rejected(self):
        for settings in [None, [], False, {'unexpected': True}]:
            with self.assertRaises(ValueError):
                await echo.execute(None, settings)

    async def test_manifest_and_example(self):
        metadata = json.loads((ROOT / 'actions/echo/action.json').read_text())
        self.assertEqual(metadata['id'], 'echo')
        self.assertEqual(metadata['python'], '3.12')
        self.assertEqual(metadata['settings_schema'], {'type': 'object', 'additionalProperties': False})
        self.assertEqual(await echo.execute(metadata['example']['data'], {}), metadata['example']['data'])
        self.assertFalse([line for line in (ROOT / 'actions/echo/requirements.lock').read_text().splitlines() if line.strip() and not line.startswith('#')])


if __name__ == '__main__':
    unittest.main()
