import json
import unittest
from pathlib import Path

from PIL import Image

from helpers import temporary_workspace
from visible_layers.reports import (
    analyze_layer_folder,
    render_import_report_markdown,
    write_import_report_json,
    write_import_report_markdown,
)


class ImportReportTests(unittest.TestCase):
    def test_analyze_layer_folder_reports_summary_and_warnings(self):
        with temporary_workspace() as tmp:
            root = Path(tmp)
            source_dir = root / "source_layers"
            source_dir.mkdir()

            Image.new("RGBA", (40, 40), (255, 0, 0, 255)).save(source_dir / "00_body_base.png")
            tiny = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
            tiny.putpixel((0, 0), (0, 0, 255, 128))
            tiny.save(source_dir / "20_part_001.png")

            report = analyze_layer_folder(source_dir)

            self.assertEqual(report["summary"]["total_layers"], 2)
            self.assertEqual(report["summary"]["canvas_width"], 40)
            self.assertTrue(report["summary"]["all_sizes_match"])
            self.assertEqual(report["summary"]["error_count"], 0)

            codes = {finding["code"] for finding in report["findings"]}
            self.assertIn("LOW_ALPHA_COVERAGE", codes)
            self.assertIn("UNKNOWN_CATEGORY", codes)
            self.assertIn("POSSIBLE_OVERDRAW_NEEDED", codes)

            part_layer = report["layers"][1]
            self.assertEqual(part_layer["name"], "part_001")
            self.assertEqual(part_layer["visible_pixel_percentage"], 0.0625)

    def test_analyze_layer_folder_reports_validation_errors(self):
        with temporary_workspace() as tmp:
            root = Path(tmp)
            source_dir = root / "source_layers"
            source_dir.mkdir()

            Image.new("RGBA", (4, 4), (255, 0, 0, 255)).save(source_dir / "body.png")
            Image.new("RGBA", (4, 4), (0, 0, 0, 0)).save(source_dir / "empty.png")
            Image.new("RGBA", (2, 2), (0, 0, 255, 255)).save(source_dir / "hair.png")

            report = analyze_layer_folder(source_dir)

            self.assertFalse(report["summary"]["all_sizes_match"])
            self.assertEqual(report["summary"]["error_count"], 2)
            codes = [finding["code"] for finding in report["findings"]]
            self.assertIn("EMPTY_LAYER", codes)
            self.assertIn("SIZE_MISMATCH", codes)

    def test_import_reports_can_be_written_as_markdown_and_json(self):
        with temporary_workspace() as tmp:
            root = Path(tmp)
            source_dir = root / "source_layers"
            output_dir = root / "output"
            source_dir.mkdir()

            Image.new("RGBA", (4, 4), (255, 0, 0, 255)).save(source_dir / "body.png")
            report = analyze_layer_folder(source_dir)

            md_path = output_dir / "import-report.md"
            json_path = output_dir / "import-report.json"
            write_import_report_markdown(report, md_path)
            write_import_report_json(report, json_path)

            self.assertIn("# Layer Import Report", render_import_report_markdown(report))
            self.assertTrue(md_path.is_file())
            self.assertTrue(json_path.is_file())
            loaded = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(loaded["summary"]["total_layers"], 1)


if __name__ == "__main__":
    unittest.main()
