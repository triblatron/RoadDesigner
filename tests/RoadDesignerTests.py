import math
import unittest
from typing import Any

from parameterized import parameterized
from pyglm import glm

from Road import Road
from Straight import Straight
import tomllib

from tests import TestUtils


class RoadDesignerTests(unittest.TestCase):
    @parameterized.expand([
        (glm.vec3(0.0,0.0,0.0), glm.vec3(0.0, 252.0, 0.0), 252.0)
    ])
    def test_length(self, start_point: glm.vec3, end_point: glm.vec3, length: float):
        sut = Straight()
        sut.points = [start_point, end_point]
        self.assertEqual(length, sut.length())

    @parameterized.expand([
        ("data/tests/Road/Bed.toml", 0, 0, "position", "x", -3.65),
        ("data/tests/Road/Bed.toml", 0, 0, "position", "y", 0.0),
        ("data/tests/Road/Bed.toml", 0, 0, "position", "z", 0.0),
        ("data/tests/Road/Bed.toml", 0, 0, "tex_coord", "x", 0.0),
        ("data/tests/Road/Bed.toml", 0, 0, "tex_coord", "y", 0.0),
        ("data/tests/Road/Bed.toml", 0, 2, "position", "x", -3.65),
        ("data/tests/Road/Bed.toml", 0, 2, "position", "y", 0.2),
        ("data/tests/Road/Bed.toml", 0, 2, "position", "z", 0.0),
        ("data/tests/Road/Bed.toml", 0, 2, "tex_coord", "x", 0.0),
        ("data/tests/Road/Bed.toml", 0, 2, "tex_coord", "y", 0.0222),
        ("data/tests/Road/Bed.toml", 1, 0, "position", "x", -5.0),
        ("data/tests/Road/Bed.toml", 1, 0, "position", "y", 0.0),
        ("data/tests/Road/Bed.toml", 1, 0, "position", "z", 0.0),
        ("data/tests/Road/Bed.toml", 1, 0, "tex_coord", "x", 0.0),
        ("data/tests/Road/Bed.toml", 1, 0, "tex_coord", "y", 0.0),
        ("data/tests/Road/Bed.toml", 1, 2, "position", "x", -5.0),
        ("data/tests/Road/Bed.toml", 1, 2, "position", "y", 0.2),
        ("data/tests/Road/Bed.toml", 1, 2, "position", "z", 0.0),
        ("data/tests/Road/Bed.toml", 1, 2, "tex_coord", "x", 0.0),
        ("data/tests/Road/Bed.toml", 1, 2, "tex_coord", "y", 1.0),
        ("data/tests/Road/Bed.toml", 2, 0, "position", "x", -5.0-5.0*math.cos(math.pi/4.0)),
        ("data/tests/Road/Bed.toml", 2, 0, "position", "y", 0.0),
        ("data/tests/Road/Bed.toml", 2, 0, "position", "z", 5.0*math.sin(math.pi/4.0)),
        ("data/tests/Road/Bed.toml", 2, 0, "tex_coord", "x", 0.0),
        ("data/tests/Road/Bed.toml", 2, 0, "tex_coord", "y", 0.0),
        ("data/tests/Road/Bed.toml", 2, 2, "position", "x", -5.0-5.0*math.cos(math.pi/4.0)),
        ("data/tests/Road/Bed.toml", 2, 2, "position", "y", 0.2),
        ("data/tests/Road/Bed.toml", 2, 2, "position", "z", 5.0*math.sin(math.pi/4.0)),
        ("data/tests/Road/Bed.toml", 2, 2, "tex_coord", "x", 0.0),
        ("data/tests/Road/Bed.toml", 2, 2, "tex_coord", "y", 1.0)
    ])
    def test_set_polygons(self, config_filename: str, mesh_index, vert_index, attr_name, ordinate_name, value: Any):
        sut = Road()
        with open(config_filename, "rb") as f:
            config = tomllib.load(f)
        sut.configure(config)
        TestUtils.assert_comparison(self, value, getattr(getattr(sut.meshes[mesh_index].verts[vert_index], attr_name), ordinate_name), 1e-3)
