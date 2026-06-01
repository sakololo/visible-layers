import unittest
from pathlib import Path

from helpers import temporary_workspace
from visible_layers.demo import create_demo


class DemoTests(unittest.TestCase):
    def test_create_demo_writes_complete_workflow(self):
        with temporary_workspace() as tmp:
            demo_dir = Path(tmp) / "demo"

            result = create_demo(demo_dir)

            self.assertTrue((demo_dir / "input.png").is_file())
            self.assertTrue((demo_dir / "masks" / "00_body_base.png").is_file())
            self.assertTrue((demo_dir / "output" / "character.json").is_file())
            self.assertTrue((demo_dir / "output" / "preview.png").is_file())
            self.assertTrue((demo_dir / "output" / "gaps" / "report.md").is_file())
            self.assertEqual(result["layer_count"], "5")

    def test_create_demo_refuses_to_overwrite_without_flag(self):
        with temporary_workspace() as tmp:
            demo_dir = Path(tmp) / "demo"
            demo_dir.mkdir()
            (demo_dir / "keep.txt").write_text("keep", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                create_demo(demo_dir)

    def test_create_demo_can_overwrite_with_flag(self):
        with temporary_workspace() as tmp:
            demo_dir = Path(tmp) / "demo"
            demo_dir.mkdir()
            (demo_dir / "old.txt").write_text("old", encoding="utf-8")

            create_demo(demo_dir, overwrite=True)

            self.assertFalse((demo_dir / "old.txt").exists())
            self.assertTrue((demo_dir / "input.png").is_file())


if __name__ == "__main__":
    unittest.main()
