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
"""Transform unit tests"""

def seq_almost_equal(t1, t2, error=0.00001):
    assert len(t1) == len(t2), "%r != %r" % (t1, t2)
    for m1, m2 in zip(t1, t2):
        assert abs(m1 - m2) <= error, "%r != %r" % (t1, t2)


class AffineBaseTestCase(object):

    def test_zero_args(self):
        with self.assertRaises(TypeError):
            self.Affine()

    def test_wrong_arg_type(self):
        with self.assertRaises(TypeError):
            self.Affine(None)

    def test_args_too_few(self):
        with self.assertRaises(TypeError):
            self.Affine(1, 2)

    def test_args_too_many(self):
        with self.assertRaises(TypeError):
            self.Affine(*range(10))

    def test_args_members_wrong_type(self):
        with self.assertRaises(TypeError):
            self.Affine(0, 2, 3, None, None, "")

    def test_len(self):
        t = self.Affine(1, 2, 3, 4, 5, 6)
        self.assertEqual(len(t), 9)

    def test_slice_last_row(self):
        t = self.Affine(1, 2, 3, 4, 5, 6)
        self.assertEqual(t[-3:], (0, 0, 1))

    def test_members_are_floats(self):
        t = self.Affine(1, 2, 3, 4, 5, 6)
        for m in t:
            assert isinstance(m, float), repr(m)

    def test_getitem(self):
        t = self.Affine(1, 2, 3, 4, 5, 6)
        self.assertEqual(t[0], 1)
        self.assertEqual(t[1], 2)
        self.assertEqual(t[2], 3)
        self.assertEqual(t[3], 4)
        self.assertEqual(t[4], 5)
        self.assertEqual(t[5], 6)
        self.assertEqual(t[6], 0)
        self.assertEqual(t[7], 0)
        self.assertEqual(t[8], 1)
        self.assertEqual(t[-1], 1)

    def test_getitem_wrong_type(self):
        t = self.Affine(1, 2, 3, 4, 5, 6)
        with self.assertRaises(TypeError):
            t['foobar']

    def test_str(self):
        self.assertEqual(
            str(self.Affine(1.111, 2.222, 3.333, -4.444, -5.555, 6.666)),
            "| 1.11, 2.22, 3.33|\n|-4.44,-5.55, 6.67|\n| 0.00, 0.00, 1.00|")

    def test_repr(self):
        self.assertEqual(
            repr(self.Affine(1.111, 2.222, 3.456, 4.444, 5.5, 6.25)),
            ("Affine(1.111, 2.222, 3.456,\n"
             "       4.444, 5.5, 6.25)"))

    def test_identity_constructor(self):
        ident = self.Affine.identity()
        assert isinstance(ident, self.Affine)
        self.assertEqual(tuple(ident), (1,0,0, 0,1,0, 0,0,1))
        assert ident.is_identity

    def test_translation_constructor(self):
        trans = self.Affine.translation((2, -5))
        assert isinstance(trans, self.Affine)
        self.assertEqual(tuple(trans), (1,0,2, 0,1,-5, 0,0,1))
        trans = self.Affine.translation(self.Vec2(9, 8))
        self.assertEqual(tuple(trans), (1,0,9, 0,1,8, 0,0,1))

    def test_scale_constructor(self):
        scale = self.Affine.scale(5)
        assert isinstance(scale, self.Affine)
        self.assertEqual(tuple(scale), (5,0,0, 0,5,0, 0,0,1))
        scale = self.Affine.scale((-1, 2))
        self.assertEqual(tuple(scale), (-1,0,0, 0,2,0, 0,0,1))
        scale = self.Affine.scale(self.Vec2(3, 4))
        self.assertEqual(tuple(scale), (3,0,0, 0,4,0, 0,0,1))
        self.assertEqual(tuple(self.Affine.scale(1)),
            tuple(self.Affine.identity()))

    def test_shear_constructor(self):
        shear = self.Affine.shear(30)
        assert isinstance(shear, self.Affine)
        sx = math.tan(math.radians(30))
        seq_almost_equal(tuple(shear), (1,0,0, sx,1,0, 0,0,1))
        shear = self.Affine.shear(-15, 60)
        sx = math.tan(math.radians(-15))
        sy = math.tan(math.radians(60))
        seq_almost_equal(tuple(shear), (1,sy,0, sx,1,0, 0,0,1))
        shear = self.Affine.shear(y_angle=45)
        seq_almost_equal(tuple(shear), (1,1,0, 0,1,0, 0,0,1))

    def test_rotation_constructor(self):
        rot = self.Affine.rotation(60)
        assert isinstance(rot, self.Affine)
        r = math.radians(60)
        s, c = math.sin(r), math.cos(r)
        self.assertEqual(tuple(rot), (c,s,0, -s,c,0, 0,0,1))
        rot = self.Affine.rotation(337)
        r = math.radians(337)
        s, c = math.sin(r), math.cos(r)
        seq_almost_equal(tuple(rot), (c,s,0, -s,c,0, 0,0,1))
        self.assertEqual(tuple(self.Affine.rotation(0)),
            tuple(self.Affine.identity()))

    def test_rotation_constructor_quadrants(self):
        self.assertEqual(tuple(self.Affine.rotation(0)), (1,0,0, 0,1,0, 0,0,1))
        self.assertEqual(tuple(self.Affine.rotation(90)), (0,1,0, -1,0,0, 0,0,1))
        self.assertEqual(tuple(self.Affine.rotation(180)), (-1,0,0, 0,-1,0, 0,0,1))
        self.assertEqual(tuple(self.Affine.rotation(-180)), (-1,0,0, 0,-1,0, 0,0,1))
        self.assertEqual(tuple(self.Affine.rotation(270)), (0,-1,0, 1,0,0, 0,0,1))
        self.assertEqual(tuple(self.Affine.rotation(-90)), (0,-1,0, 1,0,0, 0,0,1))
        self.assertEqual(tuple(self.Affine.rotation(360)), (1,0,0, 0,1,0, 0,0,1))
        self.assertEqual(tuple(self.Affine.rotation(450)), (0,1,0, -1,0,0, 0,0,1))
        self.assertEqual(tuple(self.Affine.rotation(-450)), (0,-1,0, 1,0,0, 0,0,1))

    def test_rotation_constructor_with_pivot(self):
        self.assertEqual(tuple(self.Affine.rotation(60)),
            tuple(self.Affine.rotation(60, pivot=(0,0))))
        rot = self.Affine.rotation(27, pivot=self.Vec2(2,-4))
        r = math.radians(27)
        s, c = math.sin(r), math.cos(r)
        self.assertEqual(tuple(rot),
            (c,s,2 - 2*c - 4*s, -s,c,-4 - 2*s + 4*c, 0,0,1))
        self.assertEqual(tuple(self.Affine.rotation(0, (-3, 2))),
            tuple(self.Affine.identity()))

    def test_rotation_contructor_wrong_arg_types(self):
        with self.assertRaises(TypeError):
            self.Affine.rotation(1,1)

    def test_determinant(self):
        self.assertEqual(self.Affine.identity().determinant, 1)
        self.assertEqual(self.Affine.scale(2).determinant, 4)
        self.assertEqual(self.Affine.scale(0).determinant, 0)
        self.assertEqual(self.Affine.scale((5,1)).determinant, 5)
        self.assertEqual(self.Affine.scale((-1,1)).determinant, -1)
        self.assertEqual(self.Affine.scale((-1,0)).determinant, 0)
        self.assertAlmostEqual(self.Affine.rotation(77).determinant, 1)
        self.assertAlmostEqual(self.Affine.translation((32, -47)).determinant, 1)

    def test_is_rectilinear(self):
        assert self.Affine.identity().is_rectilinear
        assert self.Affine.scale((2.5, 6.1)).is_rectilinear
        assert self.Affine.translation((4, -1)).is_rectilinear
        assert self.Affine.rotation(90).is_rectilinear
        assert not self.Affine.shear(4, -1).is_rectilinear
        assert not self.Affine.rotation(-26).is_rectilinear

    def test_is_conformal(self):
        assert self.Affine.identity().is_conformal
        assert self.Affine.scale((2.5, 6.1)).is_conformal
        assert self.Affine.translation((4, -1)).is_conformal
        assert self.Affine.rotation(90).is_conformal
        assert self.Affine.rotation(-26).is_conformal
        assert not self.Affine.shear(4, -1).is_conformal

    def test_is_orthonormal(self):
        assert self.Affine.identity().is_orthonormal
        assert self.Affine.translation((4, -1)).is_orthonormal
        assert self.Affine.rotation(90).is_orthonormal
        assert self.Affine.rotation(-26).is_orthonormal
        assert not self.Affine.scale((2.5, 6.1)).is_orthonormal
        assert not self.Affine.scale((.5, 2)).is_orthonormal
        assert not self.Affine.shear(4, -1).is_orthonormal

    def test_is_degenerate(self):
        from pygonal import EPSILON
        assert not self.Affine.identity().is_degenerate
        assert not self.Affine.translation((2, -1)).is_degenerate
        assert not self.Affine.shear(0, -22.5).is_degenerate
        assert not self.Affine.rotation(88.7).is_degenerate
        assert not self.Affine.scale(0.5).is_degenerate
        assert self.Affine.scale(0).is_degenerate
        assert self.Affine.scale((-10, 0)).is_degenerate
        assert self.Affine.scale((0, 300)).is_degenerate
        assert self.Affine.scale(0).is_degenerate
        assert self.Affine.scale(0).is_degenerate
        assert self.Affine.scale(EPSILON).is_degenerate

    def test_column_vectors(self):
        import pygonal
        a, b, c = self.Affine(2, 3, 4, 5, 6, 7).column_vectors
        assert isinstance(a, pygonal.Vec2)
        assert isinstance(b, pygonal.Vec2)
        assert isinstance(c, pygonal.Vec2)
        self.assertEqual(a, self.Vec2(2, 5))
        self.assertEqual(b, self.Vec2(3, 6))
        self.assertEqual(c, self.Vec2(4, 7))

    def test_almost_equals(self):
        from pygonal import EPSILON
        assert EPSILON != 0, EPSILON
        E = EPSILON * 0.5
        t = self.Affine(1.0, E, 0, -E, 1.0+E, E)
        assert t.almost_equals(self.Affine.identity())
        assert self.Affine.identity().almost_equals(t)
        assert t.almost_equals(t)
        t = self.Affine(1.0, 0, 0, -EPSILON, 1.0, 0)
        assert not t.almost_equals(self.Affine.identity())
        assert not self.Affine.identity().almost_equals(t)
        assert t.almost_equals(t)

    def test_equality(self):
        t1 = self.Affine(1, 2, 3, 4, 5, 6)
        t2 = self.Affine(6, 5, 4, 3, 2, 1)
        t3 = self.Affine(1, 2, 3, 4, 5, 6)
        assert t1 == t3
        assert not t1 == t2
        assert t2 == t2
        assert not t1 != t3
        assert not t2 != t2
        assert t1 != t2
        assert not t1 == 1
        assert t1 != 1

    def test_gt(self):
        with self.assertRaises(TypeError):
            self.Affine(1,2,3,4,5,6) > self.Affine(6,5,4,3,2,1)

    def test_lt(self):
        with self.assertRaises(TypeError):
            self.Affine(1,2,3,4,5,6) < self.Affine(6,5,4,3,2,1)

    def test_add(self):
        with self.assertRaises(TypeError):
            self.Affine(1,2,3,4,5,6) + self.Affine(6,5,4,3,2,1)

    def test_sub(self):
        with self.assertRaises(TypeError):
            self.Affine(1,2,3,4,5,6) - self.Affine(6,5,4,3,2,1)

    def test_mul_by_identity(self):
        t = self.Affine(1,2,3,4,5,6)
        self.assertEqual(tuple(t * self.Affine.identity()), tuple(t))

    def test_mul_transform(self):
        t = self.Affine.rotation(5) * self.Affine.rotation(29)
        assert isinstance(t, self.Affine)
        seq_almost_equal(t, self.Affine.rotation(34))
        t = self.Affine.scale((3, 5)) * self.Affine.scale(2)
        seq_almost_equal(t, self.Affine.scale((6, 10)))

    def test_mul_vector(self):
        import pygonal
        v = self.Affine.translation((4, -6)) * self.Vec2(2, 3)
        assert isinstance(v, pygonal.Vec2)
        self.assertEqual(v, self.Vec2(6, -3))
        v = self.Affine.rotation(32) * self.Vec2.polar(-26, 2)
        self.assertAlmostEqual(v.length, 2)
        self.assertAlmostEqual(v.angle, 6)
        v = self.Affine.scale(2.5) * self.Vec2.polar(123, 2)
        self.assertAlmostEqual(v.length, 5)
        self.assertAlmostEqual(v.angle, 123)

    def test_itransform(self):
        V = self.Vec2
        pts = [V(4,1), V(-1,0), V(3,2)]
        r = self.Affine.scale(-2).itransform(pts)
        assert r is None, r
        self.assertEqual(pts, [V(-8, -2), V(2,0), V(-6,-4)])

    def test_mul_wrong_type(self):
        with self.assertRaises(TypeError):
            self.Affine(1,2,3,4,5,6) * None

    def test_mul_sequence_wrong_member_types(self):
        class NotPtSeq:
            @classmethod
            def from_points(cls, points):
                list(points)
            def __iter__(self):
                yield 0
        with self.assertRaises(TypeError):
            self.Affine(1,2,3,4,5,6) * NotPtSeq()

    def test_rmul_vector(self):
        import pygonal
        t = self.Affine.rotation(-5)
        v = self.Vec2.polar(10, 2) * t
        assert isinstance(v, pygonal.Vec2)
        self.assertAlmostEqual(v.length, 2)
        self.assertAlmostEqual(v.angle, 5)

    def test_imul_transform(self):
        t = self.Affine.translation((3, 5))
        t *= self.Affine.translation((-2, 3.5))
        assert isinstance(t, self.Affine)
        seq_almost_equal(t, self.Affine.translation((1, 8.5)))

    def test_imul_vector(self):
        import pygonal
        a = self.Affine.scale(3) * self.Affine.rotation(20)
        a *= self.Vec2.polar(6, 9)
        assert isinstance(a, pygonal.Vec2)
        self.assertAlmostEqual(a.length, 27)
        self.assertAlmostEqual(a.angle, 26)

    def test_inverse(self):
        seq_almost_equal(~self.Affine.identity(), self.Affine.identity())
        seq_almost_equal(
            ~self.Affine.translation((2, -3)), self.Affine.translation((-2, 3)))
        seq_almost_equal(
            ~self.Affine.rotation(-33.3), self.Affine.rotation(33.3))
        t = self.Affine(1,2,3,4,5,6)
        seq_almost_equal(~t * t,  self.Affine.identity())

    def test_cant_invert_degenerate(self):
        from pygonal import TransformNotInvertibleError
        t = self.Affine.scale(0)
        self.assertRaises(TransformNotInvertibleError, lambda: ~t)


class PyAffineTestCase(AffineBaseTestCase, unittest.TestCase):
    from pygonal.transform import Affine
    from pygonal.vector import Vec2

    def test_mul_vector_seq(self):
        class SomePoints(tuple):
            @classmethod
            def from_points(cls, points):
                return cls(points)
        V = self.Vec2
        pts = SomePoints((V(0,0), V(1,1), V(-2,1)))
        tpts = pts * self.Affine.scale(3)
        assert isinstance(tpts, SomePoints)
        # original sequence is unchanged
        self.assertEqual(pts, SomePoints((V(0,0), V(1,1), V(-2,1))))
        self.assertEqual(tpts, SomePoints((V(0,0), V(3,3), V(-6,3))))
        rtpts = self.Affine.scale(3) * pts
        self.assertEqual(pts, SomePoints((V(0,0), V(1,1), V(-2,1))))
        self.assertEqual(rtpts, SomePoints((V(0,0), V(3,3), V(-6,3))))


if __name__ == '__main__':
    unittest.main()


# vim: ai ts=4 sts=4 et sw=4 tw=78

