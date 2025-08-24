# test/test_llm_functions.py
import unittest
from unittest.mock import patch
import LLM_functions as lf

class TestGenerateSuggestionsText(unittest.TestCase):
    def test_messages_branch_prepends_system(self):
        messages = [{"role": "user", "content": "Hello"}]
        captured = {}

        def fake_call(msgs, *_, **__):
            captured["msgs"] = msgs
            return "OK"

        with patch("LLM_functions.get_response_messages", side_effect=fake_call):
            out = lf.generate_suggestions_text(messages=messages)

        self.assertEqual(out, "OK")
        self.assertEqual(captured["msgs"][0], {"role": "system", "content": lf.SYSTEM_PROMPT})
        self.assertEqual(captured["msgs"][1:], messages)

    def test_fallback_uses_default_when_input_empty(self):
        captured = {}
        def fake_call(msgs, *_, **__):
            captured["msgs"] = msgs
            return "R"

        with patch("LLM_functions.get_response_messages", side_effect=fake_call):
            out = lf.generate_suggestions_text(user_input="")

        self.assertEqual(out, "R")
        self.assertEqual(captured["msgs"][0]["role"], "system")
        self.assertEqual(
            captured["msgs"][1]["content"],
            "3 days in Kyoto in April, mid budget, love food + temples, slow pace, hotel near Gion."
        )

    def test_fallback_strips_input(self):
        captured = {}
        def fake_call(msgs, *_, **__):
            captured["msgs"] = msgs
            return "R"

        with patch("LLM_functions.get_response_messages", side_effect=fake_call):
            lf.generate_suggestions_text(user_input="  2 days in Paris  ")

        self.assertEqual(captured["msgs"][1]["content"], "2 days in Paris")

    def test_non_list_messages_uses_fallback(self):
        captured = {}
        def fake_call(msgs, *_, **__):
            captured["msgs"] = msgs
            return "R"

        with patch("LLM_functions.get_response_messages", side_effect=fake_call):
            lf.generate_suggestions_text(user_input="x", messages="not-a-list")

        self.assertEqual(captured["msgs"][1]["content"], "x")

    def test_propagates_errors(self):
        with patch("LLM_functions.get_response_messages", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                lf.generate_suggestions_text(user_input="x")

if __name__ == "__main__":
    unittest.main()