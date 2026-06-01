import unittest
from pathlib import Path

from helpers import temporary_workspace
from visible_layers.metadata import (
    make_character_metadata,
    make_layer_record,
    read_metadata,
    validate_character_metadata,
    write_metadata,
)


class MetadataTests(unittest.TestCase):
    def test_valid_metadata_round_trip(self):
        layer = make_layer_record(
            name="front_hair",
            file="layers/front_hair.png",
            z_index=30,
            category="hair",
            width=4,
            height=4,
            requires_overdraw=True,
        )
        data = make_character_metadata(4, 4, [layer], source="input.png")

        with temporary_workspace() as tmp:
            path = Path(tmp) / "character.json"
            write_metadata(data, path)
            loaded = read_metadata(path)

        self.assertEqual(loaded["canvas"]["width"], 4)
        self.assertEqual(loaded["layers"][0]["name"], "front_hair")

    def test_invalid_metadata_reports_missing_fields(self):
        data = {"canvas": {"width": 4, "height": 4}, "layers": [{"name": "body"}]}

        with self.assertRaises(ValueError) as error:
            validate_character_metadata(data)

        self.assertIn("layers[0].file", str(error.exception))
        self.assertIn("layers[0].z_index", str(error.exception))


if __name__ == "__main__":
    unittest.main()
