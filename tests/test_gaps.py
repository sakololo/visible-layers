import unittest
from pathlib import Path

from PIL import Image

from helpers import temporary_workspace
from visible_layers.gaps import detect_gaps
from visible_layers.metadata import make_character_metadata, make_layer_record, write_metadata


class GapDetectionTests(unittest.TestCase):
    def test_detect_gaps_marks_transparent_pixels_inside_character_bbox(self):
        with temporary_workspace() as tmp:
            root = Path(tmp)
            layers_dir = root / "layers"
            layers_dir.mkdir()

            layer = Image.new("RGBA", (5, 5), (0, 0, 0, 0))
            pixels = layer.load()
            for i in range(5):
                pixels[i, 0] = (255, 0, 0, 255)
                pixels[i, 4] = (255, 0, 0, 255)
                pixels[0, i] = (255, 0, 0, 255)
                pixels[4, i] = (255, 0, 0, 255)
            layer.save(layers_dir / "outline.png")

            metadata = make_character_metadata(
                5,
                5,
                [
                    make_layer_record(
                        name="outline",
                        file="layers/outline.png",
                        z_index=0,
                        category="part",
                        width=5,
                        height=5,
                        requires_overdraw=False,
                    )
                ],
            )
            metadata_path = root / "character.json"
            write_metadata(metadata, metadata_path)

            report = detect_gaps(metadata_path, root / "gaps")
            gap_mask = Image.open(root / "gaps" / "transparent_gaps.png").convert("L")

            self.assertEqual(report["gap_pixels"], 9)
            self.assertEqual(gap_mask.getpixel((2, 2)), 255)
            self.assertTrue((root / "gaps" / "report.md").is_file())


if __name__ == "__main__":
    unittest.main()
