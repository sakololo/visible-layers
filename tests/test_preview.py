import unittest
from pathlib import Path

from PIL import Image

from helpers import temporary_workspace
from visible_layers.metadata import make_character_metadata, make_layer_record, write_metadata
from visible_layers.preview import compose_preview, save_preview


class PreviewTests(unittest.TestCase):
    def test_preview_composites_layers_by_z_index(self):
        with temporary_workspace() as tmp:
            root = Path(tmp)
            layers_dir = root / "layers"
            layers_dir.mkdir()

            Image.new("RGBA", (2, 2), (255, 0, 0, 255)).save(layers_dir / "back.png")
            Image.new("RGBA", (2, 2), (0, 0, 255, 255)).save(layers_dir / "front.png")

            metadata = make_character_metadata(
                2,
                2,
                [
                    make_layer_record(
                        name="front",
                        file="layers/front.png",
                        z_index=20,
                        category="part",
                        width=2,
                        height=2,
                        requires_overdraw=False,
                    ),
                    make_layer_record(
                        name="back",
                        file="layers/back.png",
                        z_index=10,
                        category="part",
                        width=2,
                        height=2,
                        requires_overdraw=False,
                    ),
                ],
            )
            metadata_path = root / "character.json"
            write_metadata(metadata, metadata_path)

            preview = compose_preview(metadata_path)

            self.assertEqual(preview.getpixel((0, 0)), (0, 0, 255, 255))

    def test_save_preview_writes_file(self):
        with temporary_workspace() as tmp:
            root = Path(tmp)
            layers_dir = root / "layers"
            layers_dir.mkdir()

            Image.new("RGBA", (2, 2), (255, 0, 0, 255)).save(layers_dir / "base.png")
            metadata = make_character_metadata(
                2,
                2,
                [
                    make_layer_record(
                        name="base",
                        file="layers/base.png",
                        z_index=0,
                        category="base",
                        width=2,
                        height=2,
                        requires_overdraw=True,
                    )
                ],
            )
            metadata_path = root / "character.json"
            output_path = root / "preview.png"
            write_metadata(metadata, metadata_path)

            save_preview(metadata_path, output_path)

            self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
