import unittest
from pathlib import Path

from PIL import Image

from helpers import temporary_workspace
from visible_layers.cli import main


class CliTests(unittest.TestCase):
    def test_import_layers_command_generates_preview_and_gap_report(self):
        with temporary_workspace() as tmp:
            root = Path(tmp)
            source_dir = root / "source_layers"
            output_dir = root / "output"
            source_dir.mkdir()

            Image.new("RGBA", (5, 5), (20, 20, 20, 255)).save(source_dir / "00_body_base.png")
            overlay = Image.new("RGBA", (5, 5), (255, 0, 0, 255))
            overlay.save(source_dir / "10_front_hair.png")

            exit_code = main(["import-layers", "--layers", str(source_dir), "--output", str(output_dir)])

            self.assertEqual(exit_code, 0)
            self.assertTrue((output_dir / "character.json").is_file())
            self.assertTrue((output_dir / "preview.png").is_file())
            self.assertTrue((output_dir / "gaps" / "report.md").is_file())
            self.assertTrue((output_dir / "import-report.md").is_file())
            self.assertTrue((output_dir / "import-report.json").is_file())

    def test_import_layers_command_writes_report_for_invalid_layers(self):
        with temporary_workspace() as tmp:
            root = Path(tmp)
            source_dir = root / "source_layers"
            output_dir = root / "output"
            source_dir.mkdir()

            Image.new("RGBA", (5, 5), (20, 20, 20, 255)).save(source_dir / "00_body_base.png")
            Image.new("RGBA", (5, 5), (0, 0, 0, 0)).save(source_dir / "10_empty_part.png")

            exit_code = main(["import-layers", "--layers", str(source_dir), "--output", str(output_dir)])

            self.assertEqual(exit_code, 1)
            self.assertFalse((output_dir / "character.json").is_file())
            self.assertTrue((output_dir / "import-report.md").is_file())
            self.assertTrue((output_dir / "import-report.json").is_file())


if __name__ == "__main__":
    unittest.main()
