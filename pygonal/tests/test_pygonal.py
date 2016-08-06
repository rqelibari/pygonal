#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Cityparcelator

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

def test_version_info():
    import planar
    self.assertEqual('%s.%s.%s' % planar.__versioninfo__, planar.__version__)

def test_default_implementation():
    import planar
    import planar.c
    self.assertEqual(planar.__implementation__, 'C')
    assert planar.Vec2 is planar.c.Vec2, planar.Vec2

def test_default_epsilon():
    import planar
    self.assertEqual(planar.EPSILON, 1e-5)
    self.assertEqual(planar.EPSILON2, 1e-5**2)

def test_set_epsilon():
    import planar
    old_e = planar.EPSILON
    assert not planar.Vec2(0,0).almost_equals((0.01, 0))
    try:
        planar.set_epsilon(0.02)
        self.assertEqual(planar.EPSILON, 0.02)
        self.assertEqual(planar.EPSILON2, 0.0004)
        assert planar.Vec2(0,0).almost_equals((0.01, 0))
    finally:
        planar.set_epsilon(old_e)
    self.assertEqual(planar.EPSILON, old_e)
    self.assertEqual(planar.EPSILON2, old_e**2)
    assert not planar.Vec2(0,0).almost_equals((0.01, 0))

def test_py_imports():
	import planar
	import planar.py
	from planar.py import (Vec2, Point, Vec2Array, Seq2,
		Line, Ray, LineSegment, Affine, BoundingBox, Polygon)
	assert set(planar.py.__all__).issubset(set(planar.__all__)), (
		planar.py.__all__, planar.__all__)

def test_c_imports():
	import planar.c
	from planar.c import (Vec2, Vec2Array, Seq2,
		Affine, BoundingBox, Polygon)

def test_direct_imports():
	from planar import (Vec2, Point, Vec2Array, Seq2,
		Affine, BoundingBox, Polygon)

