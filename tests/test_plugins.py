import unittest
from cyberiq_tools.plugins import Plugin, register, run_plugin, _REGISTRY

class PluginTests(unittest.TestCase):
    def setUp(self):
        _REGISTRY.clear()

    def test_contract_rejects_empty_description(self):
        with self.assertRaises(ValueError):
            register(Plugin("demo","",lambda text: text))

    def test_duplicate_plugin_is_rejected(self):
        register(Plugin("demo","test",lambda text: text))
        with self.assertRaises(ValueError):
            register(Plugin("demo","test",lambda text: text))

    def test_plugin_failure_is_isolated(self):
        def fail(text):
            raise ValueError("boom")
        register(Plugin("demo","test",fail))
        with self.assertRaisesRegex(RuntimeError,"Plugin demo failed"):
            run_plugin("demo","sample")

if __name__=="__main__":
    unittest.main()
