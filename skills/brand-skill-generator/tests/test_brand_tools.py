"""Regression checks for usable bundles, safe updates, and deterministic outputs."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
TEMPLATE_SKILL = (ROOT / "assets/brand-kit-template/SKILL.template.md").read_text()
OPERATING_BLOCKS = [
    match.group(0)
    for match in re.finditer(r"<!-- brand-skill:(apply|verify|evolve):begin -->.*?<!-- brand-skill:\1:end -->", TEMPLATE_SKILL, re.S)
]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = load("validate-brand-kit")
pantone = load("build-pantone")


class BrandToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="brand-tools-test-")
        self.addCleanup(self.temp.cleanup)
        self.kit = Path(self.temp.name) / "rook-brand"
        self.kit.mkdir()
        (self.kit / "tokens").mkdir()
        (self.kit / "assets").mkdir()
        (self.kit / "SKILL.md").write_text("---\nname: rook-brand\ndescription: Apply the Rook brand.\n---\nRead [the guide](readme.md).\n\n" + "\n\n".join(OPERATING_BLOCKS) + "\n")
        (self.kit / "readme.md").write_text("# Rook\nEstablished identity. [Portable values](brand-card.md).\n")
        (self.kit / "index.html").write_text('<!doctype html><html lang="en"><head><title>Rook brand</title><style>body { color: #315c4c; }</style></head><body><h1>Rook</h1><p>A human introduction to the identity.</p></body></html>')
        (self.kit / "brand-card.md").write_text("# Rook\n## Print decisions\nDigital-first; retain the approved green.\n<!-- colors:begin -->\nOld colors\n<!-- colors:end -->\n<!-- pantone:begin -->\nPending mapping\n<!-- pantone:end -->\n")
        (self.kit / "styles.css").write_text('@import "tokens/colors.css";\n')
        (self.kit / "tokens/colors.css").write_text(":root { --color-primary-500: #315C4C; --primary: var(--color-primary-500); }\n")

    def command(self, script, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], capture_output=True, text=True)

    def test_overview_can_be_self_contained_without_prescribed_layout(self):
        errors, warnings = validator.validate(self.kit)
        self.assertEqual(errors, [])
        self.assertTrue(any("Pantone" in message for message in warnings))
        self.assertTrue((self.kit / "index.html").exists())
        self.assertFalse((self.kit / "components").exists())

    def test_overview_is_required_for_completion_but_can_be_pending_in_draft(self):
        index = self.kit / "index.html"
        index.unlink()
        with (self.kit / "SKILL.md").open("a") as file:
            file.write("[Brand overview](index.html)\n")
        strict, _ = validator.validate(self.kit)
        draft, warnings = validator.validate(self.kit, draft=True)
        self.assertTrue(any("index.html" in message for message in strict))
        self.assertEqual(draft, [])
        self.assertTrue(any("index.html" in message for message in warnings))
        index.write_text(" \n")
        self.assertTrue(any("overview missing or empty" in message for message in validator.validate(self.kit)[0]))

    def test_overview_resource_links_must_resolve(self):
        (self.kit / "index.html").write_text('<!doctype html><html><body><img src="assets/missing-logo.svg"></body></html>')
        errors, _ = validator.validate(self.kit)
        self.assertTrue(any("missing-logo.svg" in message for message in errors))

    def test_cleanup_detects_file_urls_and_broken_asset_symlinks(self):
        work = Path(self.temp.name) / ".brand-skill-generator-work"
        work.mkdir()
        asset = work / "photo with spaces.png"
        asset.write_bytes(b"fixture")
        linked = self.kit / "assets/linked-photo.png"
        linked.symlink_to(asset)
        (self.kit / "index.html").write_text(f'<img src="{asset.as_uri()}">')
        self.assertEqual(validator.validate(self.kit)[0], [])
        shutil.rmtree(work)
        errors, _ = validator.validate(self.kit)
        self.assertTrue(any("photo%20with%20spaces.png" in message for message in errors), errors)
        self.assertTrue(any("linked-photo.png" in message for message in errors), errors)

    def test_scaffold_is_explicit_and_update_preserves_authored_files(self):
        out = Path(self.temp.name) / "north-brand"
        args = ("--brand", 'North: "Works" & Co.', "--slug", "north", "--out", out)
        result = self.command("scaffold-brand-skill.py", *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        errors, warnings = validator.validate(out, draft=True)
        self.assertEqual(errors, [])
        self.assertFalse(any("shared" in message for message in warnings), warnings)
        self.assertTrue(validator.validate(out)[0], "an unfinished scaffold must not pass strict validation")
        (out / "readme.md").write_text("Authored identity to preserve.\n")
        result = self.command("scaffold-brand-skill.py", *args)
        self.assertNotEqual(result.returncode, 0)
        (out / "brand-card.md").unlink()
        result = self.command("scaffold-brand-skill.py", *args, "--update")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((out / "readme.md").read_text(), "Authored identity to preserve.\n")
        self.assertTrue((out / "brand-card.md").exists())
        self.assertFalse((out / "index.html").exists())

    def test_all_operating_blocks_are_required_in_finished_skills(self):
        skill = self.kit / "SKILL.md"
        text = skill.read_text()
        self.assertEqual(len(OPERATING_BLOCKS), 3)
        for block in OPERATING_BLOCKS:
            text = text.replace(block, "")
        skill.write_text(text)
        errors, _ = validator.validate(self.kit)
        self.assertEqual(sum("shared" in message for message in errors), 3)
        errors, warnings = validator.validate(self.kit, draft=True)
        self.assertEqual(errors, [])
        self.assertEqual(sum("shared" in message for message in warnings), 3)

    def test_custom_templates_emit_skill_and_preserve_authored_updates(self):
        for entry_name in ("SKILL.md", "SKILL.template.md"):
            with self.subTest(entry_name=entry_name):
                template = Path(self.temp.name) / f"template-{entry_name}"
                template.mkdir()
                (template / entry_name).write_text("# {{brand}}\nname: {{slug}}-brand\n")
                out = Path(self.temp.name) / f"out-{entry_name}"
                args = ("--brand", "Rook", "--out", out, "--template", template)
                result = self.command("scaffold-brand-skill.py", *args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((out / "SKILL.md").read_text(), "# Rook\nname: rook-brand\n")
                self.assertFalse((out / "SKILL.template.md").exists())
                (out / "SKILL.md").write_text("Authored identity.\n")
                (template / "readme.md").write_text("# {{brand}}\n")
                result = self.command("scaffold-brand-skill.py", *args, "--update")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((out / "SKILL.md").read_text(), "Authored identity.\n")
                self.assertEqual((out / "readme.md").read_text(), "# Rook\n")

    def test_custom_template_rejects_two_competing_skill_entries(self):
        template = Path(self.temp.name) / "ambiguous-template"
        template.mkdir()
        (template / "SKILL.md").write_text("Old entry.\n")
        (template / "SKILL.template.md").write_text("New entry.\n")
        out = Path(self.temp.name) / "new-brand"
        result = self.command("scaffold-brand-skill.py", "--brand", "Rook", "--out", out, "--template", template)
        self.assertEqual(result.returncode, 2)
        self.assertIn("exactly one", result.stderr)
        self.assertFalse(out.exists())

    def test_operating_guidance_cannot_be_rewritten_or_duplicated(self):
        skill = self.kit / "SKILL.md"
        original = skill.read_text()
        for block in OPERATING_BLOCKS:
            with self.subTest(block=block.splitlines()[0]):
                skill.write_text(original.replace(block, block.replace("\n", "\nChanged guidance.\n", 1)))
                errors, _ = validator.validate(self.kit)
                self.assertTrue(any("block changed" in message for message in errors), errors)
                skill.write_text(original + "\n" + block)
                errors, _ = validator.validate(self.kit)
                self.assertTrue(any("exactly one shared" in message for message in errors), errors)

    def test_scaffold_rejects_unsafe_slug_and_missing_destination(self):
        out = Path(self.temp.name) / "new-brand"
        result = self.command("scaffold-brand-skill.py", "--brand", "Rook", "--slug", "../escape", "--out", out)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(out.exists())
        result = self.command("scaffold-brand-skill.py", "--brand", "Rook")
        self.assertNotEqual(result.returncode, 0)

    def test_malformed_metadata_is_a_diagnostic_not_a_crash(self):
        (self.kit / "SKILL.md").write_text("---\n- not\n- a mapping\n---\n")
        errors, _ = validator.validate(self.kit)
        self.assertTrue(any("mapping" in message for message in errors))

    def test_broken_css_import_and_font_are_detected(self):
        (self.kit / "styles.css").write_text('@import "tokens/colors.css";\n@import url("tokens/missing.css");\n')
        with (self.kit / "tokens/colors.css").open("a") as file:
            file.write('@font-face { font-family: Rook; src: url("../assets/missing.woff2"); }')
        errors, _ = validator.validate(self.kit)
        self.assertTrue(any("missing.css" in message for message in errors))
        self.assertTrue(any("missing.woff2" in message for message in errors))

    def test_unreachable_tokens_and_cycles_are_detected(self):
        (self.kit / "tokens/extra.css").write_text(":root { --space: 1rem; }")
        with (self.kit / "tokens/colors.css").open("a") as file:
            file.write('@import "../styles.css";')
        errors, _ = validator.validate(self.kit)
        self.assertTrue(any("unreachable" in message for message in errors))
        self.assertTrue(any("circular" in message for message in errors))

    def test_missing_guideline_and_specimen_assets_are_detected(self):
        (self.kit / "readme.md").write_text("Read [missing rules](missing.md).")
        (self.kit / "components").mkdir()
        (self.kit / "components/label.html").write_text('<img src="../assets/missing.svg"><a href="/example-route">Demo action</a>')
        errors, _ = validator.validate(self.kit)
        self.assertTrue(any("missing.md" in message for message in errors))
        self.assertTrue(any("missing.svg" in message for message in errors))
        self.assertFalse(any("example-route" in message for message in errors))

    def test_valid_fixed_size_svg_with_xml_declaration_passes(self):
        (self.kit / "assets/logo.svg").write_text('<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/></svg>')
        self.assertEqual(validator.validate(self.kit)[0], [])

    def test_invalid_svg_and_unresolved_definition_fail(self):
        logo = self.kit / "assets/logo.svg"
        logo.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 -1 24"><path fill="url(#missing)" d="M0 0h2v2z"/></svg>')
        errors, _ = validator.validate(self.kit)
        self.assertTrue(any("viewBox" in message for message in errors))
        self.assertTrue(any("#missing" in message for message in errors))
        logo.write_text("<svg>")
        self.assertTrue(any("invalid SVG XML" in message for message in validator.validate(self.kit)[0]))

    def test_draft_only_relaxes_unfinished_content(self):
        (self.kit / "readme.md").write_text("REPLACE: Strategy.\n[Broken](missing.md)")
        strict, _ = validator.validate(self.kit)
        draft, warnings = validator.validate(self.kit, draft=True)
        self.assertTrue(any("unfinished" in message for message in strict))
        self.assertTrue(any("unfinished" in message for message in warnings))
        self.assertTrue(any("missing.md" in message for message in draft))

    def test_palette_is_repeatable_and_card_keeps_authored_decisions(self):
        outputs = []
        for number in (1, 2):
            output = Path(self.temp.name) / str(number) / "tokens/colors.css"
            result = self.command("build-palette.py", "--seed", "#315C4C", "--out", output, "--card", self.kit / "brand-card.md")
            self.assertEqual(result.returncode, 0, result.stderr)
            outputs.append(output.read_text())
        self.assertEqual(outputs[0], outputs[1])
        card = (self.kit / "brand-card.md").read_text()
        self.assertIn("Digital-first; retain the approved green.", card)
        self.assertIn("Pending mapping", card)
        first_root = outputs[0].split("@supports", 1)[0]
        self.assertNotIn("oklch(", first_root)
        primary = re.search(r"--color-primary-500:\s*(#[a-fA-F0-9]+)", outputs[0]).group(1)
        primary_row = next(line for line in card.splitlines() if line.startswith("| primary |"))
        self.assertIn(primary, primary_row)

    def test_pantone_cli_adapter_keeps_print_decisions(self):
        response = {"results": [{"book": {"id": "testBook", "title": "Test book"}, "color": {"code": "TEST-1", "hex": "315C4C"}, "deltaE": 0.4}]}
        with patch.object(sys, "argv", ["build-pantone.py", "--kit", str(self.kit), "--books", "testBook"]), patch.object(pantone, "cli_cmd", return_value=["fixture-cli"]), patch.object(pantone, "run_match", return_value=response) as match:
            pantone.main()
        self.assertTrue(match.called)
        record = json.loads((self.kit / "pantone.json").read_text())
        self.assertEqual(record["scales"]["primary"]["levels"]["500"]["matches"]["testBook"]["code"], "TEST-1")
        card = (self.kit / "brand-card.md").read_text()
        self.assertIn("Digital-first; retain the approved green.", card)
        self.assertIn("Old colors", card)
        self.assertNotIn("REPLACE", card)
        self.assertEqual(validator.validate(self.kit), ([], []))

    def test_failed_print_mapping_does_not_replace_existing_evidence(self):
        record = self.kit / "pantone.json"
        record.write_text('{"previous": "evidence"}')
        with patch.object(sys, "argv", ["build-pantone.py", "--kit", str(self.kit)]), patch.object(pantone, "cli_cmd", return_value=["fixture-cli"]), patch.object(pantone, "run_match", return_value=None):
            with self.assertRaises(SystemExit) as caught:
                pantone.main()
        self.assertEqual(caught.exception.code, 1)
        self.assertEqual(record.read_text(), '{"previous": "evidence"}')

    def test_partial_print_mapping_preserves_both_existing_outputs(self):
        response = {"results": [{"book": {"id": "testBook", "title": "Test book"}, "color": {"code": "TEST-1", "hex": "315C4C"}, "deltaE": 0.4}]}
        record = self.kit / "pantone.json"
        record.write_text('{"previous": "evidence"}')
        card = (self.kit / "brand-card.md").read_text()
        with (self.kit / "tokens/colors.css").open("a") as file:
            file.write(":root { --color-primary-600: #244536; }")
        for books, responses in (("testBook", [response, None]), ("testBook,missingBook", [response, response])):
            with self.subTest(books=books), patch.object(sys, "argv", ["build-pantone.py", "--kit", str(self.kit), "--books", books]), patch.object(pantone, "cli_cmd", return_value=["fixture-cli"]), patch.object(pantone, "run_match", side_effect=responses):
                with self.assertRaises(SystemExit) as caught:
                    pantone.main()
                self.assertEqual(caught.exception.code, 1)
                self.assertEqual(record.read_text(), '{"previous": "evidence"}')
                self.assertEqual((self.kit / "brand-card.md").read_text(), card)


if __name__ == "__main__":
    unittest.main()
