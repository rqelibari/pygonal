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
from nose.tools import assert_equal, assert_almost_equal, raises

def test_version_info():
    import pygonal
    assert_equal('%s.%s.%s' % pygonal.__versioninfo__, pygonal.__version__)

def test_default_epsilon():
    import pygonal
    assert_equal(pygonal.EPSILON, 1e-5)
    assert_equal(pygonal.EPSILON2, 1e-5**2)

def test_set_epsilon():
    import pygonal
    old_e = pygonal.EPSILON
    assert not pygonal.Vec2(0,0).almost_equals((0.01, 0))
    try:
        pygonal.set_epsilon(0.02)
        assert_equal(pygonal.EPSILON, 0.02)
        assert_equal(pygonal.EPSILON2, 0.0004)
        assert pygonal.Vec2(0,0).almost_equals((0.01, 0))
    finally:
        pygonal.set_epsilon(old_e)
    assert_equal(pygonal.EPSILON, old_e)
    assert_equal(pygonal.EPSILON2, old_e**2)
    assert not pygonal.Vec2(0,0).almost_equals((0.01, 0))

def test_direct_imports():
	from pygonal import (Vec2, Point, Vec2Array, Seq2,
		Affine, BoundingBox, Polygon)

