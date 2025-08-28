import unittest
from unittest.mock import patch
import LLM_functions as lf

# Unit tests for generate_suggestions_text()
# - Avoid real network calls by patching get_response_messages
# - Verify message construction, defaulting behavior, trimming, and error propagation

class TestGenerateSuggestionsText(unittest.TestCase):
    # Validates core branching logic and ensures requests sent to the LLM client are well-formed
    def test_messages_branch_prepends_system(self):
        # Given a messages history, the function should prepend the SYSTEM_PROMPT
        messages = [{"role": "user", "content": "Hello"}]
        captured = {}

        def fake_call(msgs, *_, **__):
            # Capture what would be sent to the LLM and return a stubbed reply
            captured["msgs"] = msgs
            return "OK"

        with patch("LLM_functions.get_response_messages", side_effect=fake_call):
            out = lf.generate_suggestions_text(messages=messages)

        self.assertEqual(out, "OK")
        self.assertEqual(captured["msgs"][0], {"role": "system", "content": lf.SYSTEM_PROMPT})
        self.assertEqual(captured["msgs"][1:], messages)

    def test_fallback_uses_default_when_input_empty(self):
        # With empty user_input and no messages, the default sample prompt is used
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
        # Leading/trailing spaces should be stripped in the single-turn branch
        captured = {}
        def fake_call(msgs, *_, **__):
            captured["msgs"] = msgs
            return "R"

        with patch("LLM_functions.get_response_messages", side_effect=fake_call):
            lf.generate_suggestions_text(user_input="  2 days in Paris  ")

        self.assertEqual(captured["msgs"][1]["content"], "2 days in Paris")

    def test_non_list_messages_uses_fallback(self):
        # Passing a non-list messages argument should route to the single-turn path
        captured = {}
        def fake_call(msgs, *_, **__):
            captured["msgs"] = msgs
            return "R"

        with patch("LLM_functions.get_response_messages", side_effect=fake_call):
            lf.generate_suggestions_text(user_input="x", messages="not-a-list")

        self.assertEqual(captured["msgs"][1]["content"], "x")

    def test_propagates_errors(self):
        # Exceptions raised by the LLM client should propagate to the caller
        with patch("LLM_functions.get_response_messages", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                lf.generate_suggestions_text(user_input="x")

if __name__ == "__main__":
    unittest.main()