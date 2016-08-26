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

__all__ = ('TransformNotInvertibleError', 'set_epsilon',
    'Vec2', 'Point', 'Vec2Array', 'Seq2',
    'Line', 'Ray', 'LineSegment',
    'Affine', 'BoundingBox', 'Polygon')

__versioninfo__ = (0, 1, 0)
__version__ = '.'.join(str(n) for n in __versioninfo__)

from pygonal.vector import Vec2, Vec2Array, Seq2
from pygonal.transform import Affine
from pygonal.line import Line, Ray, LineSegment
from pygonal.box import BoundingBox
from pygonal.polygon import Polygon

class TransformNotInvertibleError(Exception):
    """The transform could not be inverted"""

def _set_epsilon(e): pass

__implementation__ = 'Python'

Point = Vec2
"""``Point`` is an alias for ``Vec2``.
Use ``Point`` where desired for clarity in your code.
"""

def set_epsilon(epsilon):
    """Set the global absolute error value and rounding limit for approximate
    floating point comparison operations. This value is accessible via the
    :attr:`pygonal.EPSILON` global variable.

    The default value of ``0.00001`` is suitable for values
    that are in the "countable range". You may need a larger
    epsilon when using large absolute values, and a smaller value
    for very small values close to zero. Otherwise approximate
    comparison operations will not behave as expected.
    """
    global EPSILON, EPSILON2
    EPSILON = float(epsilon)
    EPSILON2 = EPSILON**2
    _set_epsilon(EPSILON)

set_epsilon(1e-2)


# vim: ai ts=4 sts=4 et sw=4 tw=78
