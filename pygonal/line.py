#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import pygonal
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


class _LinearGeometry(object):
    """Abstract base class for linear shapes"""

    @property
    def direction(self):
        """Direction of the line as a unit vector. You may set this
        attribute to any non-null vector, however it will be normalized
        to unit-length.
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        direction = pygonal.Vec2(*value).normalized()
        if direction.is_null:
            raise ValueError("Line direction vector must not be null")
        self._direction = direction
        self._normal = -direction.perpendicular()

    @property
    def normal(self):
        """Normal unit vector perpendicular to the line. You may set this
        attribute to any non-null vector, however it will be normalized
        to unit-length. Modifying this will also affect the direction
        vector accordingly.
        """
        return self._normal

    @normal.setter
    def normal(self, value):
        normal = pygonal.Vec2(*value).normalized()
        if normal.is_null:
            raise ValueError("Line normal vector must not be null")
        self._normal = normal
        self._direction = normal.perpendicular()


class Line(_LinearGeometry):
    """Infinite directed line.

    :param point: A point on the line.
    :type point: Vec2
    :param direction: Direction of the line as a vector, must not
        be null. Does not need to be unit-length.
    :type direction: Vec2
    """
    def __init__(self, point, direction):
        self.direction = direction
        self.offset = pygonal.Vec2(*point).dot(self.normal)

    @classmethod
    def from_points(cls, points):
        """Create a line from two or more collinear points.  The direction of
        the line is derived from the first two distinct points, the order of
        the remaining points is unimportant.

        :param points: Iterable of at least 2 distinct points.
        """
        points = iter(points)
        try:
            try:
                start = end = pygonal.Vec2(*points.__next__())
                while end == start:
                    end = pygonal.Vec2(*points.__next__())
            except AttributeError:
                start = end = pygonal.Vec2(*points.next())
                while end == start:
                    end = pygonal.Vec2(*points.next())
        except StopIteration:
            raise ValueError("Expected iterable of 2 or more distinct points")
        line = _LinearGeometry.__new__(cls)
        line.direction = end - start
        line.offset = start.dot(line.normal)
        for p in points:
            if not line.contains_point(p):
                raise ValueError("All points provided must be collinear")
        return line

    @classmethod
    def from_normal(cls, normal, offset):
        """Create a line given a normal vector perpendicular to it, at the
        specified distance from the origin.

        :param normal: A non-null vector perpendicular to the line.
            Does not need to be unit-length.
        :type normal: Vec2
        :param offset: The signed distance from the line to the origin.
        :type offset: float
        """
        line = _LinearGeometry.__new__(cls)
        line.normal = normal
        line.offset = offset * 1.0
        return line

    offset = 0.0
    """The signed distance from the origin to the line."""

    @property
    def points(self):
        """Return two distinct points along the line, such that
        ``line.from_points(line.points)`` will construct an equivalent line.
        """
        point = self._normal * self.offset
        return (point, point + self._direction)

    def distance_to(self, point):
        """Return the signed distance from the line to the specified point.
        The sign indicates which half-plane contains the point. If the
        distance is negative, the point is in the "left" half plane with
        respect to the line, if it is positive, the point is in the "right"
        half plane.

        :param point: The point to measure the distance to.
        :type point: Vec2
        """
        point = pygonal.Vec2(*point)
        return point.dot(self._normal) - self.offset

    def point_left(self, point):
        """Return True if the specified point is in the half plane
        to the left of the line.
        """
        return self.distance_to(point) <= -pygonal.EPSILON

    def point_right(self, point):
        """Return True if the specified point is in the half plane
        to the right of the line.
        """
        return self.distance_to(point) >= pygonal.EPSILON

    def contains_point(self, point):
        """Return True if the specified point is on the line."""
        return abs(self.distance_to(point)) < pygonal.EPSILON

    def parallel(self, point):
        """Return a line parallel to this one that passes through the
        given point.

        :param point: A point on the parallel line.
        :type point: Vec2
        """
        return Line(point, self.direction)

    def perpendicular(self, point):
        """Return a line perpendicular to this one that passes through the
        given point. The orientation of this line is consistent with
        :meth:`pygonal.Vec2.perpendicular`.

        :param point: A point on the perpendicular line.
        :type point: Vec2
        """
        return Line(point, self.direction.perpendicular())

    def project(self, point):
        """Compute the projection of a point onto the line. This
        is the closest point on the line to the specified point.

        :param point: The point to project.
        :type point: Vec2
        """
        parallel = self.direction.project(point)
        return parallel + self._normal * self.offset

    def reflect(self, point):
        """Reflect a point across the line.

        :param point: The point to reflect.
        :type point: Vec2
        """
        point = pygonal.Vec2(*point)
        offset_distance = point.dot(self._normal) - self.offset
        return point - 2.0 * self._normal * offset_distance

    def __imul__(self, other):
        p1, p2 = self.points
        p1 = other.__mul__(p1)
        p2 = other.__mul__(p2)
        if p1 is NotImplemented or p2 is NotImplemented:
            return NotImplemented
        self.direction = p2 - p1
        self.offset = p1.dot(self.normal)
        return self

    def __eq__(self, other):
        return (self.__class__ is other.__class__
            and self.offset == other.offset
            and self.direction == other.direction)

    def __ne__(self, other):
        return not self.__eq__(other)

    def almost_equals(self, other):
        """Return True if this line is approximately equal to
        another line, within precision limits.
        """
        return (self.__class__ is other.__class__
            and abs(self.offset - other.offset) < pygonal.EPSILON
            and self.direction.almost_equals(other.direction))

    def __str__(self):
        """Concise string representation."""
        return "Line(%s, %s)" % (
            tuple(self.project((0,0))), tuple(self.direction))

    def __repr__(self):
        """Precise string representation."""
        return "Line(%r, %r)" % (
            tuple(self.project((0,0))), tuple(self.direction))


class Ray(_LinearGeometry):
    """Directed ray anchored by a single point.

    :param anchor: The anchor, or starting point of the ray.
    :type anchor: Vec2
    :param direction: The direction of the ray as a vector, must not
        be null. Does not need to be unit-length.
    :type direction: Vec2
    """
    def __init__(self, anchor, direction):
        self.anchor = pygonal.Vec2(*anchor)
        self.direction = direction

    @classmethod
    def from_points(cls, points):
        """Create a ray from two or more collinear points.  The direction of
        the ray is derived from the first two distinct points, with the first
        point assumed to be the anchor. The order of the remaining points is
        unimportant, however they must all be on the ray.

        :param points: Iterable of at least 2 distinct points.
        """
        points = iter(points)
        try:
            try:
                start = end = pygonal.Vec2(*points.__next__())
                while end == start:
                    end = pygonal.Vec2(*points.__next__())
            except AttributeError:
                start = end = pygonal.Vec2(*points.next())
                while end == start:
                    end = pygonal.Vec2(*points.next())
        except StopIteration:
            raise ValueError("Expected iterable of 2 or more distinct points")
        ray = _LinearGeometry.__new__(cls)
        ray.direction = end - start
        ray.anchor = start
        for p in points:
            if not ray.contains_point(p):
                raise ValueError("All points provided must be collinear")
        return ray

    @property
    def points(self):
        """Return two distinct points along the ray, such that
        ``ray.from_points(ray.points)`` will construct an equivalent ray.
        The first point returned is always the anchor point.
        """
        return (self._anchor, self._anchor + self._direction)

    @property
    def anchor(self):
        """The anchor, or starting point of the ray."""
        return self._anchor

    @anchor.setter
    def anchor(self, value):
        self._anchor = pygonal.Vec2(*value)

    start = anchor
    """The starting point of the ray. Alias for ``anchor``"""

    @property
    def line(self):
        """Return a line collinear with this ray."""
        return Line(self._anchor, self._direction)

    def distance_to(self, point):
        """Return the distance between the given point and the ray."""
        to_point = pygonal.Vec2(*point) - self._anchor
        if self.direction.dot(to_point) >= 0.0:
            # Point "beside" ray
            return abs(to_point.dot(self._normal))
        else:
            # Point "behind" ray
            return to_point.length

    def contains_point(self, point):
        """Return True if the specified point is on the ray."""
        return self.distance_to(point) < pygonal.EPSILON

    def point_behind(self, point):
        """Return True if the specified point is behind the anchor point with
        respect to the direction of the ray.  In other words, the angle
        between the ray direction and the vector pointing from the ray's
        anchor to the given point is greater than 90 degrees.
        """
        to_point = pygonal.Vec2(*point) - self._anchor
        return self.direction.dot(to_point) <= -pygonal.EPSILON

    def point_left(self, point):
        """Return True if the specified point is in the space
        to the left of, but not behind the ray.
        """
        to_point = pygonal.Vec2(*point) - self._anchor
        return (self._direction.dot(to_point) > -pygonal.EPSILON
            and self._normal.dot(to_point) <= -pygonal.EPSILON)

    def point_right(self, point):
        """Return True if the specified point is in the space
        to the right of, but not behind the ray.
        """
        to_point = pygonal.Vec2(*point) - self._anchor
        return (self._direction.dot(to_point) > -pygonal.EPSILON
            and self._normal.dot(to_point) >= pygonal.EPSILON)

    def project(self, point):
        """Compute the projection of a point onto the ray. This
        is the closest point on the ray to the specified point.

        :param point: The point to project.
        :type point: Vec2
        """
        to_point = pygonal.Vec2(*point) - self._anchor
        parallel = self.direction.project(to_point)
        if parallel.dot(self.direction) > -pygonal.EPSILON:
            # Point "beside" ray
            return parallel + self._anchor
        else:
            # Point "behind" ray
            return self._anchor

    def __imul__(self, other):
        p1, p2 = self.points
        p1 = other.__mul__(p1)
        p2 = other.__mul__(p2)
        if p1 is NotImplemented or p2 is NotImplemented:
            return NotImplemented
        self.direction = p2 - p1
        self.anchor = p1
        return self

    def __eq__(self, other):
        return (self.__class__ is other.__class__
            and self.anchor == other.anchor
            and self.direction == other.direction)

    def __ne__(self, other):
        return not self.__eq__(other)

    def almost_equals(self, other):
        """Return True if this ray is approximately equal to
        another ray, within precision limits.
        """
        return (self.__class__ is other.__class__
            and self.anchor.almost_equals(other.anchor)
            and self.direction.almost_equals(other.direction))

    def __str__(self):
        """Concise string representation."""
        return "Ray(%s, %s)" % (
            tuple(self.anchor), tuple(self.direction))

    def __repr__(self):
        """Precise string representation."""
        return "Ray(%r, %r)" % (
            tuple(self.anchor), tuple(self.direction))


class LineSegment(_LinearGeometry):
    """Directed line segment between two points.

    :param anchor: The anchor, or starting point of the line segment.
    :type anchor: Vec2
    :param vector: The direction and magnitude vector of the line segment,
        must not be null.
    :type vector: Vec2
    """
    def __init__(self, anchor, vector):
        self.vector = vector
        self._anchor = pygonal.Vec2(*anchor)

    @classmethod
    def from_points(cls, points):
        """Create a line segment from one or more collinear points.  The first
        point is assumed to be the anchor.  The order of the remaining points
        is unimportant, however they must all be collinear.  The furthest
        point from the anchor determines the line segment's vector.

        :param points: Iterable of at least 2 distinct points.
        """
        points = iter(points)
        try:
            try:
                start = end = pygonal.Vec2(*points.__next__())
            except AttributeError:
                start = end = pygonal.Vec2(*points.next())
        except StopIteration:
            raise ValueError("Expected iterable of 1 or more points")
        furthest = 0.0
        pt_vectors = []
        for p in points:
            p = pygonal.Vec2(*p)
            dist = (p - start).length2
            if dist > furthest:
                furthest = dist
                end = p
            pt_vectors.append(p)
        segment = _LinearGeometry.__new__(cls)
        if end != start:
            segment.vector = end - start
        else:
            # degenerate case
            segment.direction = (1, 0)
            segment.length = 0.0
        segment._anchor = start
        for p in pt_vectors:
            if not segment.contains_point(p):
                raise ValueError("All points provided must be collinear")
        return segment

    @classmethod
    def from_normal(cls, normal, offset, start_distance, end_distance):
        """Create a line segment from a normal vector perpendicular to the
        line containing the segment, the offset distance from that line to
        origin, and the signed distances along that line from the projection
        of the origin to the start and end points of the segment respectively.

        :param normal: A non-null vector perpendicular to the line segment.
            Does not need to be unit-length.
        :type normal: Vec2
        :param offset: The signed distance from the line containing the
            segment to the origin.
        :type offset: float
        :param start_distance: The signed distance along the segment's
            containing line from the projection of the origin to the
            segment's start (anchor) point.
        :type start_distance: float
        :param end_distance: The signed distance along the containing line
            from the projection of the origin to the segment's end point.
        :type end_distance: float
        """
        segment = _LinearGeometry.__new__(cls)
        segment.normal = normal
        start_distance *= 1.0
        segment._anchor = (segment.normal * offset
            + start_distance * segment.direction)
        segment.length = end_distance - start_distance
        return segment

    length = 0.0
    """The distance between the line segments endpoints."""

    @property
    def points(self):
        """Return the two endpoints of the line segment as a sequence."""
        return (self._anchor, self._anchor + self.direction * self.length)

    @property
    def anchor(self):
        """The anchor, or starting point of the line segment."""
        return self._anchor

    @anchor.setter
    def anchor(self, value):
        self._anchor = pygonal.Vec2(*value)

    start = anchor
    """The starting point of the line segment. Alias for ``anchor``"""

    @property
    def vector(self):
        """The vector that comprises the length and direction of the
        line segment from its anchor point.
        """
        return self.direction * self.length

    @vector.setter
    def vector(self, value):
        vector = pygonal.Vec2(*value)
        length = vector.length
        if length:
            self.direction = vector
        else:
            self.direction = (1, 0)
        self.length = vector.length

    @property
    def end(self):
        """The end point of the line sequence."""
        return self._anchor + self.direction * self.length

    @end.setter
    def end(self, value):
        end = pygonal.Vec2(*value)
        self.vector = end - self._anchor

    @property
    def mid(self):
        """The midpoint of the line segment (read-only)."""
        return self._anchor + self.direction * (self.length * 0.5)

    @property
    def line(self):
        """Return a containing line collinear with this line segment."""
        return Line(self._anchor, self.direction)

    def distance_to(self, point):
        """Return the distance between the given point and the line segment."""
        point = pygonal.Vec2(*point)
        to_point = point - self._anchor
        along = self.direction.dot(to_point)
        if along < 0.0:
            # Point "behind"
            return to_point.length
        if along > self.length:
            # Point "ahead"
            return (point - self.end).length
        else:
            # Point "beside"
            return abs(to_point.dot(self._normal))

    def contains_point(self, point):
        """Return True if the specified point is on the line segment."""
        return self.distance_to(point) < pygonal.EPSILON

    def point_ahead(self, point):
        """Return True if the specified point is ahead of the endpoint
        of the line segment with respect to its direction.
        """
        to_point = pygonal.Vec2(*point) - self._anchor
        return self.direction.dot(to_point) >= self.length + pygonal.EPSILON

    def point_behind(self, point):
        """Return True if the specified point is behind the anchor point with
        respect to the direction of the line segment.
        """
        to_point = pygonal.Vec2(*point) - self._anchor
        return self.direction.dot(to_point) <= -pygonal.EPSILON

    def point_left(self, point):
        """Return True if the specified point is in the space
        to the left of, but not behind the line segment.
        """
        to_point = pygonal.Vec2(*point) - self._anchor
        along = self._direction.dot(to_point)
        return (self.length + pygonal.EPSILON > along > -pygonal.EPSILON
            and self._normal.dot(to_point) <= -pygonal.EPSILON)

    def point_right(self, point):
        """Return True if the specified point is in the space
        to the right of, but not behind the line segment.
        """
        to_point = pygonal.Vec2(*point) - self._anchor
        along = self._direction.dot(to_point)
        return (self.length + pygonal.EPSILON > along > -pygonal.EPSILON
            and self._normal.dot(to_point) >= pygonal.EPSILON)

    def project(self, point):
        """Compute the projection of a point onto the line segment. This
        is the closest point on the segment to the specified point.

        :param point: The point to project.
        :type point: Vec2
        """
        to_point = pygonal.Vec2(*point) - self._anchor
        parallel = self.direction.project(to_point)
        along = parallel.dot(self.direction)
        if along <= -pygonal.EPSILON:
            # Point "behind"
            return self._anchor
        elif along >= self.length + pygonal.EPSILON:
            # Point "ahead"
            return self.end
        else:
            # Point "beside"
            return parallel + self._anchor

    def __imul__(self, other):
        p1, p2 = self.points
        p1 = other.__mul__(p1)
        p2 = other.__mul__(p2)
        if p1 is NotImplemented or p2 is NotImplemented:
            return NotImplemented
        self.vector = p2 - p1
        self._anchor = p1
        return self

    def __eq__(self, other):
        return (self.__class__ is other.__class__
            and self.anchor == other.anchor
            and self.vector == other.vector)

    def __ne__(self, other):
        return not self.__eq__(other)

    def almost_equals(self, other):
        """Return True if this line segment is approximately equal to
        another, within precision limits.
        """
        return (self.__class__ is other.__class__
            and self.anchor.almost_equals(other.anchor)
            and self.vector.almost_equals(other.vector))

    def __str__(self):
        """Concise string representation."""
        return "LineSegment(%s, %s)" % (
            tuple(self.anchor), tuple(self.vector))

    def __repr__(self):
        """Precise string representation."""
        return "LineSegment(%r, %r)" % (
            tuple(self.anchor), tuple(self.vector))


# vim: ai ts=4 sts=4 et sw=4 tw=78

