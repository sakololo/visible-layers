import unittest
from pathlib import Path

from PIL import Image

from helpers import temporary_workspace
from visible_layers.layers import (
    import_layer_folder,
    infer_category,
    normalize_layer_name,
    split_layers,
    strip_order_prefix,
)


class LayerExtractionTests(unittest.TestCase):
    def test_split_layers_creates_transparent_layer_and_metadata(self):
        with temporary_workspace() as tmp:
            root = Path(tmp)
            input_path = root / "input.png"
            masks_dir = root / "masks"
            output_dir = root / "output"
            masks_dir.mkdir()

            source = Image.new("RGBA", (4, 4), (200, 10, 20, 255))
            source.save(input_path)

            mask = Image.new("L", (4, 4), 0)
            pixels = mask.load()
            for y in range(4):
                for x in range(2):
                    pixels[x, y] = 255
            mask.save(masks_dir / "body_base.png")

            metadata = split_layers(input_path, masks_dir, output_dir)
            layer_path = output_dir / metadata["layers"][0]["file"]
            layer = Image.open(layer_path).convert("RGBA")

            self.assertTrue((output_dir / "character.json").is_file())
            self.assertEqual(metadata["layers"][0]["name"], "body_base")
            self.assertEqual(layer.getpixel((0, 0))[3], 255)
            self.assertEqual(layer.getpixel((3, 0))[3], 0)

    def test_mask_size_must_match_input(self):
        with temporary_workspace() as tmp:
            root = Path(tmp)
            input_path = root / "input.png"
            masks_dir = root / "masks"
            masks_dir.mkdir()

            Image.new("RGBA", (4, 4), (0, 0, 0, 255)).save(input_path)
            Image.new("L", (2, 2), 255).save(masks_dir / "face.png")

            with self.assertRaises(ValueError):
                split_layers(input_path, masks_dir, root / "output")

    def test_layer_name_and_category_helpers(self):
        self.assertEqual(normalize_layer_name(" Front Hair! "), "front_hair")
        self.assertEqual(strip_order_prefix("00_front_hair"), "front_hair")
        self.assertEqual(infer_category("front_hair"), "hair")
        self.assertEqual(infer_category("left_arm"), "arm")
        self.assertEqual(infer_category("unknown"), "part")

    def test_import_layer_folder_creates_metadata_and_normalized_layers(self):
        with temporary_workspace() as tmp:
            root = Path(tmp)
            source_dir = root / "source_layers"
            output_dir = root / "output"
            source_dir.mkdir()

            Image.new("RGBA", (4, 4), (255, 0, 0, 255)).save(source_dir / "00_body_base.png")
            Image.new("RGBA", (4, 4), (0, 0, 255, 128)).save(source_dir / "10_front_hair.png")

            metadata = import_layer_folder(source_dir, output_dir)

            self.assertTrue((output_dir / "character.json").is_file())
            self.assertTrue((output_dir / "layers" / "00_body_base.png").is_file())
            self.assertTrue((output_dir / "layers" / "01_front_hair.png").is_file())
            self.assertEqual(metadata["layers"][0]["name"], "body_base")
            self.assertEqual(metadata["layers"][1]["category"], "hair")

    def test_import_layer_folder_requires_matching_canvas_sizes(self):
        with temporary_workspace() as tmp:
            root = Path(tmp)
            source_dir = root / "source_layers"
            source_dir.mkdir()

            Image.new("RGBA", (4, 4), (255, 0, 0, 255)).save(source_dir / "body.png")
            Image.new("RGBA", (2, 2), (0, 0, 255, 255)).save(source_dir / "hair.png")

            with self.assertRaises(ValueError):
                import_layer_folder(source_dir, root / "output")


if __name__ == "__main__":
    unittest.main()
