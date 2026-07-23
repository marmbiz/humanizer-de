import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load_script(name):
    script = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


register_lint = load_script("register_lint")
run_review_eval = load_script("run_review_eval")


class ConstantsSyncTests(unittest.TestCase):
    def test_review_eval_address_regexes_use_register_forms(self):
        for form in register_lint.DU_FORMS:
            self.assertRegex(form, run_review_eval.DU_RE)
            self.assertRegex(form.capitalize(), run_review_eval.DU_RE)

        for form in register_lint.SIE_FORMS:
            self.assertRegex(form, run_review_eval.SIE_RE)

        self.assertIsNone(run_review_eval.SIE_RE.search("sie"))

    def test_review_eval_sentences_use_abbreviation_safe_splitter(self):
        text = "Das gilt z. B. für Berlin. Danach folgt mehr."
        self.assertEqual(run_review_eval.sentences(text), ["Das gilt z. B. für Berlin.", "Danach folgt mehr."])


if __name__ == "__main__":
    unittest.main()
