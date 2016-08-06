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

def test_cached_property():
    from pygonal.util import cached_property

    class Thingy(object):
        not_cached_calls = 0
        cached_calls = 0

        @property
        def not_cached(self):
            """Nay"""
            self.not_cached_calls += 1
            return 'not cached'

        @cached_property
        def cached(self):
            """Yay"""
            self.cached_calls += 1
            return 'cached'

    thing = Thingy()
    assert thing.not_cached_calls == 0
    assert Thingy.not_cached.__doc__ == 'Nay'
    assert thing.cached_calls == 0
    assert Thingy.cached.__doc__ == 'Yay'

    not_cached_value = thing.not_cached
    assert thing.not_cached_calls == 1

    cached_value = thing.cached
    assert thing.cached_calls == 1

    assert not_cached_value == thing.not_cached
    assert thing.not_cached_calls == 2

    assert cached_value == thing.cached
    assert thing.cached_calls == 1

    assert not_cached_value == thing.not_cached
    assert thing.not_cached_calls == 3

    assert cached_value == thing.cached
    assert thing.cached_calls == 1

# vim: ai ts=4 sts=4 et sw=4 tw=78

