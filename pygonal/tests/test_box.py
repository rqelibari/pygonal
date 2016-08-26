#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import math
import unittest
'''
    Pygonal

    (c) 2016 Copyright Rezart Qelibari <qelibarr@informatik.uni-freiburg.de>
    Portions copyright (c) 2010 by Casey Duncan
    Portions copyright (c) 2009 The Super Effective Team

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    See LICENSE.txt and CREDITS.txt
'''
"""BoundingBox class unit tests"""


def seq_almost_equal(t1, t2, error=0.00001):
    import pygonal
    error = pygonal.EPSILON2
    assert len(t1) == len(t2), "%r != %r" % (t1, t2)
    for m1, m2 in zip(t1, t2):
        assert abs(m1 - m2) <= error, "%r != %r" % (t1, t2)


class BoundingBoxBaseTestCase(object):

    def test_too_few_args(self):
        with self.assertRaises(TypeError):
            self.BoundingBox()

    def test_no_points(self):
        with self.assertRaises(ValueError):
            self.BoundingBox([])

    def test_one_point(self):
        box = self.BoundingBox([(2, 4)])
        self.assertEqual(box.max_point, self.Vec2(2, 4))
        self.assertEqual(box.min_point, self.Vec2(2, 4))

    def test_two_points_already_min_max(self):
        box = self.BoundingBox([(-2, -1), (3, 4)])
        self.assertEqual(box.max_point, self.Vec2(3, 4))
        self.assertEqual(box.min_point, self.Vec2(-2, -1))

    def test_two_points_not_min_max(self):
        box = self.BoundingBox([self.Vec2(2, -4), self.Vec2(-3, -1)])
        self.assertEqual(box.min_point, self.Vec2(-3, -4))
        self.assertEqual(box.max_point, self.Vec2(2, -1))

    def test_many_points(self):
        box = self.BoundingBox(((i, 10000 - i) for i in range(10000)))
        self.assertEqual(box.min_point, (0, 1))
        self.assertEqual(box.max_point, (9999, 10000))

    def test_from_points(self):
        box = self.BoundingBox.from_points([(0,2), (1,-3), (-1,0)])
        self.assertEqual(box.min_point, (-1, -3))
        self.assertEqual(box.max_point, (1, 2))

    def test_from_Seq2(self):
        box = self.BoundingBox(self.Seq2([(9,0), (-1, 0), (4, -1)]))
        self.assertEqual(box.min_point, (-1, -1))
        self.assertEqual(box.max_point, (9, 0))

    def test_bounding_box(self):
        box = self.BoundingBox([(-2, -1), (3, 4)])
        box2 = box.bounding_box
        assert isinstance(box2, self.BoundingBox)
        self.assertEqual(box.min_point, box2.min_point)
        self.assertEqual(box.max_point, box2.max_point)

    def test_min_point_max_point(self):
        import pygonal
        box = self.BoundingBox([(-2, -1), (3, 4)])
        assert isinstance(box.max_point, pygonal.Vec2)
        self.assertEqual(box.max_point, self.Vec2(3, 4))
        assert isinstance(box.min_point, pygonal.Vec2)
        self.assertEqual(box.min_point, self.Vec2(-2, -1))

    def test_immutable_min_point(self):
        import pygonal
        box = self.BoundingBox([(-2, -1), (3, 4)])
        with self.assertRaises(AttributeError):
            box.min_point = self.Vec2(4,3)

    def test_immutable_max_point(self):
        import pygonal
        box = self.BoundingBox([(-2, -1), (3, 4)])
        with self.assertRaises(AttributeError):
            box.max_point = self.Vec2(4,3)

    def test_center(self):
        import pygonal
        box = self.BoundingBox([(-3, -1), (1, 4)])
        assert isinstance(box.center, pygonal.Vec2)
        self.assertEqual(box.center, pygonal.Vec2(-1, 1.5))
        self.assertEqual(self.BoundingBox([(8, 12)]).center, pygonal.Vec2(8, 12))

    def test_width_height(self):
        box = self.BoundingBox([(-2, -3.5), (3, 4)])
        self.assertEqual(box.width, 5)
        self.assertEqual(box.height, 7.5)

    def test_is_empty(self):
        assert not self.BoundingBox([(-2, -3.5), (3, 4)]).is_empty
        assert self.BoundingBox([(-2, -3.5), (-2, 4)]).is_empty
        assert self.BoundingBox([(-2, 4), (3, 4)]).is_empty
        assert self.BoundingBox([(1, 1), (1, 1)]).is_empty

    def test_from_shapes(self):
        BoundingBox = self.BoundingBox
        class Shape(object):
            def __init__(self, x1, y1, x2, y2):
                self.bounding_box = BoundingBox([(x1, y1), (x2, y2)])
        shapes = [
            Shape(0, 0, 10, 4),
            Shape(-2, 4, -1, 5),
            Shape(20, 2, 25, 2.5),
            Shape(-5, -5, -5, -5),
            Shape(-2, -2, 2, 2),
        ]
        box = self.BoundingBox.from_shapes(shapes)
        self.assertEqual(box.min_point, (-5, -5))
        self.assertEqual(box.max_point, (25, 5))

        box = self.BoundingBox.from_shapes(iter(shapes))
        self.assertEqual(box.min_point, (-5, -5))
        self.assertEqual(box.max_point, (25, 5))

    def test_from_shapes_no_shapes(self):
        with self.assertRaises(ValueError):
            box = self.BoundingBox.from_shapes([])

    def test_from_center(self):
        box = self.BoundingBox.from_center((2, 3), 14, 3)
        self.assertEqual(box.min_point, (-5, 1.5))
        self.assertEqual(box.max_point, (9, 4.5))
        self.assertEqual(box.width, 14)
        self.assertEqual(box.height, 3)

        box = self.BoundingBox.from_center(self.Vec2(0, -4), 20, -6)
        self.assertEqual(box.min_point, (-10, -7))
        self.assertEqual(box.max_point, (10, -1))
        self.assertEqual(box.width, 20)
        self.assertEqual(box.height, 6)

    def test_from_center_bad_args(self):
        with self.assertRaises(TypeError):
            self.BoundingBox.from_center(0, 1, 1)

    def test_inflate_scalar(self):
        box1 = self.BoundingBox([(3, 1), (5, 6)])
        box2 = box1.inflate(1)
        assert box2 is not box1
        self.assertEqual(box1.width, 2)
        self.assertEqual(box1.height, 5)
        self.assertEqual(box2.width, 3)
        self.assertEqual(box2.height, 6)
        self.assertEqual(box2.center, box1.center)
        box3 = box2.inflate(-2.5)
        assert box3 is not box2
        self.assertEqual(box1.width, 2)
        self.assertEqual(box1.height, 5)
        self.assertEqual(box2.width, 3)
        self.assertEqual(box2.height, 6)
        self.assertEqual(box2.center, box1.center)
        self.assertEqual(box3.width, 0.5)
        self.assertEqual(box3.height, 3.5)
        self.assertEqual(box3.center, box2.center)

    def test_inflate_vector(self):
        box1 = self.BoundingBox([(-2, 0), (7, 1.5)])
        box2 = box1.inflate((-3, 1.5))
        assert box2 is not box1
        self.assertEqual(box1.width, 9)
        self.assertEqual(box1.height, 1.5)
        self.assertEqual(box2.width, 6)
        self.assertEqual(box2.height, 3)
        self.assertEqual(box2.center, box1.center)

    def test_inflate_bad_arg(self):
        with self.assertRaises(TypeError):
            self.BoundingBox([(3, 1), (5, 6)]).inflate('badbad')

    def test_contains_point(self):
        box = self.BoundingBox([(-1, -2), (3, 0)])
        assert box.contains_point((-0.5, -1))
        assert box.contains_point(self.Vec2(-1, 0))
        assert box.contains_point((-1, -0))
        assert box.contains_point((2.99, 0))
        assert box.contains_point((0, 0))
        assert not box.contains_point((-1, -2))
        assert not box.contains_point((3, 0))
        assert not box.contains_point((3, -2))
        assert not box.contains_point((-1.1, -2))
        assert not box.contains_point(self.Vec2(3.1, 0))
        assert not box.contains_point((-50, 0))
        assert not box.contains_point((50, 0))
        assert not box.contains_point((0, 50))
        assert not box.contains_point((50, 50))

    def test_contains_wrong_type(self):
        with self.assertRaises(AttributeError):
            self.BoundingBox([(2, 6), (5, 7)]).contains(None)

    def test_fit_box(self):
        box = self.BoundingBox([(-1, 2), (4, 5)])
        frame = self.BoundingBox([(0, 0), (50, 50)])
        fitted = frame.fit(box)
        assert fitted is not box
        assert fitted is not frame
        self.assertEqual(fitted.width, 50)
        self.assertEqual(fitted.height, 30)
        self.assertEqual(fitted.center, frame.center)
        frame = self.BoundingBox([(-100, -50), (-60, -44)])
        fitted = frame.fit(box)
        self.assertEqual(fitted.width, 10)
        self.assertEqual(fitted.height, 6)
        self.assertEqual(fitted.center, frame.center)

    def test_fit_transformable_shape(self):
        import pygonal
        BoundingBox = self.BoundingBox
        class Shape(object):
            def __init__(self, x1, y1, x2, y2):
                self.bounding_box = BoundingBox([(x1, y1), (x2, y2)])
            def __mul__(self, other):
                assert isinstance(other, pygonal.Affine)
                self.xform = other
                return self

        shape = Shape(10, -2, 14, 1)
        frame = self.BoundingBox([(-4, 1), (4, -10)])
        shape2 = frame.fit(shape)
        xv, yv, tv = shape2.xform.column_vectors
        self.assertEqual(xv, (2, 0))
        self.assertEqual(yv, (0, 2))
        self.assertEqual(tv, frame.center - shape2.bounding_box.center)

    def test_fit_wrong_arg_type(self):
        with self.assertRaises(AttributeError):
            self.BoundingBox([(0, 0), (40, 40)]).fit(None)

    def test_to_polygon(self):
        import pygonal
        poly = self.BoundingBox([(-2,0), (5,-4)]).to_polygon()
        assert isinstance(poly, pygonal.Polygon)
        assert poly.is_convex_known
        assert poly.is_convex
        self.assertEqual(tuple(poly), ((-2,-4), (-2,0), (5,0), (5,-4)))

    def test_mul_by_translating_transform(self):
        import pygonal
        a = self.BoundingBox([(-1,0), (0,1)])
        b = a * pygonal.Affine.translation((1, 0))
        assert isinstance(b, self.BoundingBox)
        assert b is not a
        self.assertEqual(b.min_point, (0, 0))
        self.assertEqual(b.max_point, (1, 1))

    def test_mul_by_rectilinear_transform(self):
        import pygonal
        a = self.BoundingBox([(-2,-1), (2,1)])
        t = pygonal.Affine.rotation(90) * pygonal.Affine.scale(2)
        assert t.is_rectilinear
        b = a * t
        assert isinstance(b, self.BoundingBox)
        assert b is not a
        self.assertEqual(b.min_point, (-2,-4))
        self.assertEqual(b.max_point, (2, 4))

    def test_mul_by_transform(self):
        import pygonal
        a = self.BoundingBox([(0,0), (2,1)])
        t = pygonal.Affine.rotation(45)
        assert not t.is_rectilinear
        b = a * t
        assert isinstance(b, pygonal.Polygon)
        s45 = math.sin(math.radians(45))
        seq_almost_equal(b, [(0,0), (-s45,s45), (s45, s45*3), (s45*2, s45*2)])

    def test_mul_incompatible(self):
        with self.assertRaises(TypeError):
            a = self.BoundingBox([(-1,0), (0,1)]) * 2

    def test_equals(self):
        a = self.BoundingBox([(-4,0), (-6,2)])
        assert a == a
        assert a == self.BoundingBox([(-6,0), (-4,2), (-5,0)])
        assert not a == self.BoundingBox([(-6,0), (-4,2), (0,0)])
        assert not a == self.BoundingBox([(1,1), (2,2)])
        assert not a == self.BoundingBox([(-4,0), (-5,2)])
        assert not a == None

    def test_not_equals(self):
        a = self.BoundingBox([(-4,0), (-6,2)])
        assert not a != a
        assert not a != self.BoundingBox([(-6,0), (-4,2), (-5,0)])
        assert a != self.BoundingBox([(-6,0), (-4,2), (0,0)])
        assert a != self.BoundingBox([(1,1), (2,2)])
        assert a != self.BoundingBox([(-4,0), (-5,2)])
        assert a != None

    def test_almost_equals(self):
        import pygonal
        a = self.BoundingBox([(-4,0), (-6,2)])
        assert a.almost_equals(a)
        assert a.almost_equals(self.BoundingBox([(-6,0), (-4,2), (-5,0)]))
        assert a.almost_equals(self.BoundingBox(
            [(-4 + pygonal.EPSILON / 2, 0), (-6,2 - pygonal.EPSILON / 2)]))
        assert not a.almost_equals(self.BoundingBox([(-4 + pygonal.EPSILON, 0), (-6,2)]))
        assert not a.almost_equals(self.BoundingBox([(-4,0), (-5,2)]))
        assert not a.almost_equals(None)

    def test_str_and_repr(self):
        bbox = self.BoundingBox([(-1.25, 0.25), (-1.5, 0.5)])
        self.assertEqual(str(bbox), 'BoundingBox([(-1.5, 0.25), (-1.25, 0.5)])')
        self.assertEqual(repr(bbox), str(bbox))


class PyBoundingBoxTestCase(BoundingBoxBaseTestCase, unittest.TestCase):
    from pygonal.vector import Vec2, Seq2
    from pygonal.box import BoundingBox


if __name__ == '__main__':
    unittest.main()


# vim: ai ts=4 sts=4 et sw=4 tw=78
