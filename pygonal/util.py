#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import math

# Define assert_unorderable() depending on the language
# implicit ordering rules. This keeps things consistent
# across major Python versions
try:
    3 > ""
except TypeError: # pragma: no cover
    # No implicit ordering (newer Python)
    def assert_unorderable(a, b):
        """Assert that a and b are unorderable"""
        return NotImplemented
else: # pragma: no cover
    # Implicit ordering by default (older Python)
    # We must raise an exception ourselves
    # To prevent nonsensical ordering
    def assert_unorderable(a, b):
        """Assert that a and b are unorderable"""
        raise TypeError("unorderable types: %s and %s"
            % (type(a).__name__, type(b).__name__))

def cached_property(func):
    """Special property decorator that caches the computed
    property value in the object's instance dict the first
    time it is accessed.
    """

    def getter(self, name=func.__name__):
        try:
            return self.__dict__[name]
        except KeyError:
            self.__dict__[name] = value = func(self)
            return value

    getter.func_name = func.__name__
    return property(getter, doc=func.__doc__)

def cos_sin_deg(deg):
    """Return the cosine and sin for the given angle
    in degrees, with special-case handling of multiples
    of 90 for perfect right angles
    """
    deg = deg % 360.0
    if deg == 90.0:
        return 0.0, 1.0
    elif deg == 180.0:
        return -1.0, 0
    elif deg == 270.0:
        return 0, -1.0
    rad = math.radians(deg)
    return math.cos(rad), math.sin(rad)


# vim: ai ts=4 sts=4 et sw=4 tw=78

