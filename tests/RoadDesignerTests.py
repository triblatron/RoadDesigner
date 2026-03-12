import math
import unittest
from typing import Any

from parameterized import parameterized
from pyglm import glm

from Road import Road
from RoadBuildScript import RoadBuildScript
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
    def test_configure(self, config_filename: str, mesh_index, vert_index, attr_name, ordinate_name, value: Any):
        sut = Road()
        with open(config_filename, "rb") as f:
            config = tomllib.load(f)
        sut.configure(config)
        TestUtils.assert_comparison(self, value, getattr(getattr(sut.meshes[mesh_index].verts[vert_index], attr_name), ordinate_name), 1e-3)

    @parameterized.expand([
        ("data/tests/Road/singlequad.toml", 0, 0, "position", "x", -3.65)
    ])
    def test_build(self, build_filename: str, mesh_index: int, vert_index: int, attr_name: str, ordinate_name: str, value: Any):
        build_script = RoadBuildScript()
        with open(build_filename, "rb") as f:
            config = tomllib.load(f)
            build_script.configure(config)

        sut = build_script.build()
        self.assertIsNotNone(sut)

        actual = getattr(getattr(sut.meshes[mesh_index].verts[vert_index], attr_name), ordinate_name)
        TestUtils.assert_comparison(self, value, actual, 1e-3)

    @parameterized.expand([
        ("data/tests/Road/straight.toml", "segment.length", 252.0),
        ("data/tests/Road/straight.toml", "segment.points[1].y", 252.0),
        ("data/tests/Road/straight.toml", "segment.binormals[0].x", 1.0),
        ("data/tests/Road/straight.toml", "segment.normals[0].z", 1.0),
        ("data/tests/Road/straight.toml", "segment.tangents[0].y", 1.0),
        ("data/tests/Road/straight.toml", "segment.tessellation.num_points", 2),
        ("data/tests/Road/straight.toml", "surface.num_points", 4),
        ("data/tests/Road/straight.toml", "surface.points[0].position.x", -3.65),
        ("data/tests/Road/straight.toml", "surface.points[0].position.y", 0.0),
        ("data/tests/Road/straight.toml", "surface.points[0].tex_coord.x", 0.0),
        ("data/tests/Road/straight.toml", "surface.points[0].tex_coord.y", 0.0),
        ("data/tests/Road/straight.toml", "surface.points[1].position.x", 3.65),
        ("data/tests/Road/straight.toml", "surface.points[1].position.y", 0.0),
        ("data/tests/Road/straight.toml", "surface.points[1].tex_coord.x", 1.0),
        ("data/tests/Road/straight.toml", "surface.points[1].tex_coord.y", 0.0),
        ("data/tests/Road/straight.toml", "surface.points[2].position.x", -3.65),
        ("data/tests/Road/straight.toml", "surface.points[2].position.y", 252.0),
        ("data/tests/Road/straight.toml", "surface.points[2].tex_coord.x", 0.0),
        ("data/tests/Road/straight.toml", "surface.points[2].tex_coord.y", 252.0/(0.2/0.0222222)),
        ("data/tests/Road/straight.toml", "surface.points[3].position.x", 3.65),
        ("data/tests/Road/straight.toml", "surface.points[3].position.y", 252.0),
        ("data/tests/Road/straight.toml", "surface.points[3].tex_coord.x", 1.0),
        ("data/tests/Road/straight.toml", "surface.points[3].tex_coord.y", 252.0/(0.2/0.0222222)),
        ("data/tests/Road/arc.toml", "segment.tangents[1].y", math.cos(19.25138192/180*math.pi)),
        ("data/tests/Road/arc.toml", "segment.tessellation.num_points", 11),
        ("data/tests/Road/arc.toml", "profiles.bed.width", 7.3),
        ("data/tests/Road/arc.toml", "profiles.bed.length", 0.2),
    ])
    def test_segment(self, config_filename: str, path: str, value):
        build_script = RoadBuildScript()
        with open(config_filename, "rb") as f:
            config = tomllib.load(f)
            build_script.configure(config)

        sut = build_script.build()
        self.assertIsNotNone(sut)

        actual = TestUtils.find(sut, path)
        TestUtils.assert_comparison(self, value, actual, 1e-3)