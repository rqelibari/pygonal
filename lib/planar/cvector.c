/***************************************************************************
* Copyright (c) 2010 by Casey Duncan
* All rights reserved.
*
* This software is subject to the provisions of the BSD License
* A copy of the license should accompany this distribution.
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
****************************************************************************/
#include "Python.h"
#include <float.h>
#include "planar.h"

#define VEC2_FREE_MAX 1000
static PyObject *vec2_free_list = NULL;
static int vec2_free_size = 0;

static PlanarVec2Object *
Vec2_result(PlanarVec2Object *self, double x, double y)
{
    PlanarVec2Object *v;

    assert(PlanarVec2_Check(self));
    v = (PlanarVec2Object *)PlanarVec2Type.tp_alloc(Py_TYPE(self), 0);
    if (v == NULL) {
        return NULL;
    }
    v->x = x;
    v->y = y;
    return v;
}

static int
Vec2_init(PlanarVec2Object *self, PyObject *args)
{
    PyObject *xarg;
    PyObject *yarg;

    assert(PlanarVec2_Check(self));
    if (PyTuple_GET_SIZE(args) != 2) {
        PyErr_SetString(PyExc_TypeError, 
            "Vec2: wrong number of arguments");
        return -1;
    }
    xarg = PyObject_ToFloat(PyTuple_GET_ITEM(args, 0));
    yarg = PyObject_ToFloat(PyTuple_GET_ITEM(args, 1));
    if (xarg == NULL || yarg == NULL) {
        Py_XDECREF(xarg);
        Py_XDECREF(yarg);
        return -1;
    }

    self->x = PyFloat_AS_DOUBLE(xarg);
    self->y = PyFloat_AS_DOUBLE(yarg);
    Py_DECREF(xarg);
    Py_DECREF(yarg);
    return 0;
}

static PyObject *
Vec2_alloc(PyTypeObject *type, Py_ssize_t nitems)
{
    PlanarVec2Object *v;

    assert(PyType_IsSubtype(type, &PlanarVec2Type));
    if (vec2_free_list != NULL) {
        v = (PlanarVec2Object *)vec2_free_list;
        Py_INCREF(v);
        vec2_free_list = v->next_free;
        --vec2_free_size;
        v->x = v->y = 0.0;
        return (PyObject *)v;
    } else {
        PyObject *p = PyType_GenericAlloc(type, nitems);
        return p;
    }
}

static void
Vec2_dealloc(PlanarVec2Object *self)
{
    if (PlanarVec2_CheckExact(self) && vec2_free_size < VEC2_FREE_MAX) {
        self->next_free = vec2_free_list;
        vec2_free_list = (PyObject *)self;
        ++vec2_free_size;
    } else {
        Py_TYPE(self)->tp_free((PyObject *)self);
    }
}

static PyObject *
Vec2_compare(PyObject *a, PyObject *b, int op)
{
    double ax, bx, ay, by;
    int result = 0;

    if (PlanarVec2_Parse(a, &ax, &ay) && PlanarVec2_Parse(b, &bx, &by)) {
        switch (op) {
            case Py_EQ:
                result = ax == bx && ay == by;
                break;
            case Py_NE:
                result = ax != bx || ay != by;
                break;
            case Py_GT:
                result = (ax*ax + ay*ay) > (bx*bx + by*by);
                break;
            case Py_LT:
                result = (ax*ax + ay*ay) < (bx*bx + by*by);
                break;
            case Py_GE:
                result = (ax*ax + ay*ay) >= (bx*bx + by*by);
                break;
            case Py_LE:
                result = (ax*ax + ay*ay) <= (bx*bx + by*by);
                break;
            default:
                RETURN_NOT_IMPLEMENTED;
        }
    } else {
        /* We can't parse one or both operands */
        if (PyErr_Occurred() && PyErr_ExceptionMatches(PyExc_MemoryError)) {
            /* Don't mask memory errors */
            return NULL;
        }
        PyErr_Clear();
        switch (op) {
            case Py_EQ:
                result = 0;
                break;
            case Py_NE:
                result = 1;
                break;
            default:
                /* Other comparisons are undefined */
                RETURN_NOT_IMPLEMENTED;
        }
    }

    if (result) {
        Py_INCREF(Py_True);
        return Py_True;
    } else {
        Py_INCREF(Py_False);
        return Py_False;
    }
}

static long
Vec2_hash(PlanarVec2Object *self) 
{
    long hash;

    hash = (hash_double(self->x) + LONG_MAX/2) ^ hash_double(self->y);
    return (hash != -1) ? hash : -2;
}    

/* Property descriptors */

static PyObject *
Vec2_get_x(PlanarVec2Object *self) {
    return PyFloat_FromDouble(self->x);
}

static PyObject *
Vec2_get_y(PlanarVec2Object *self) {
    return PyFloat_FromDouble(self->y);
}

static PyObject *
Vec2_get_length(PlanarVec2Object *self) {
    return PyFloat_FromDouble(sqrt(self->y * self->y + self->x * self->x));
}

static PyObject *
Vec2_get_length2(PlanarVec2Object *self) {
    return PyFloat_FromDouble(self->y * self->y + self->x * self->x);
}

static PyObject *
Vec2_get_angle(PlanarVec2Object *self) {
    return PyFloat_FromDouble(degrees(atan2(self->y, self->x)));
}

static PyObject *
Vec2_get_is_null(PlanarVec2Object *self)
{
    PyObject *r;

    if (self->y * self->y + self->x * self->x < PLANAR_EPSILON2) {
        r = Py_True;
    } else {
        r = Py_False;
    }
    Py_INCREF(r);
    return r;
}


static PyGetSetDef Vec2_getset[] = {
    {"x", (getter)Vec2_get_x, NULL, "The horizontal coordinate.", NULL},
    {"y", (getter)Vec2_get_y, NULL, "The vertical coordinate.", NULL},
    {"length", (getter)Vec2_get_length, NULL, 
        "The length or scalar magnitude of the vector.", NULL},
    {"length2", (getter)Vec2_get_length2, NULL, 
        "The square of the length of the vector.", NULL},
    {"angle", (getter)Vec2_get_angle, NULL, 
        "The angle the vector makes to the positive x axis in the range"
        " (-180, 180]"},
    {"is_null", (getter)Vec2_get_is_null, NULL, 
        "Flag indicating if the vector is effectively zero-length."},
    {NULL}
};

/* Methods */

static PyObject *
Vec2_new_polar(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    PyObject *angle_arg;
    PyObject *length_arg;
    PlanarVec2Object *v;
    int arg_count;
    double angle;
    double length = 1.0;

    static char *kwlist[] = {"angle", "length", NULL};

    assert(PyType_IsSubtype(type, &PlanarVec2Type));
    if (kwargs == NULL) {
        /* No kwargs, do fast manual arg handling */
        arg_count = PyTuple_GET_SIZE(args);
        if (arg_count != 1 && arg_count != 2) {
            PyErr_SetString(PyExc_TypeError, 
                "Vec2.polar(): wrong number of arguments");
            return NULL;
        }
        angle_arg = PyObject_ToFloat(PyTuple_GET_ITEM(args, 0));
        if (angle_arg == NULL) {
            return NULL;
        }
        angle = PyFloat_AS_DOUBLE(angle_arg);
        Py_DECREF(angle_arg);
        if (arg_count == 2) {
            length_arg = PyObject_ToFloat(PyTuple_GET_ITEM(args, 1));
            if (length_arg == NULL) {
                return NULL;
            }
            length = PyFloat_AS_DOUBLE(length_arg);
            Py_DECREF(length_arg);
        }
    } else if (!PyArg_ParseTupleAndKeywords(
        args, kwargs, "d|d:Vec2.polar", kwlist, &angle, &length)) {
        return NULL;
    }

    v = (PlanarVec2Object *)type->tp_alloc(type, 0);
    if (v != NULL) {
        angle = radians(angle);
        v->x = cos(angle) * length;
        v->y = sin(angle) * length;
    }
    return (PyObject *)v;
}

static PyObject *
Vec2_repr(PlanarVec2Object *self)
{
    char buf[255];
    buf[0] = 0; /* paranoid */
    PyOS_snprintf(buf, 255, "Vec2(%lg, %lg)", self->x, self->y);
    return PyUnicode_FromString(buf);
}

static PyObject *
Vec2_str(PlanarVec2Object *self)
{
    char buf[255];
    buf[0] = 0; /* paranoid */
    PyOS_snprintf(buf, 255, "Vec2(%.2f, %.2f)", self->x, self->y);
    return PyUnicode_FromString(buf);
}

static PyObject *
Vec2_almost_equals(PlanarVec2Object *self, PyObject *other)
{
    double ox, oy, dx, dy;
    PyObject *r;

    assert(PlanarVec2_Check(self));
    if (PlanarVec2_Parse(other, &ox, &oy)) {
        dx = self->x - ox;
        dy = self->y - oy;
        if (dx*dx + dy*dy <= PLANAR_EPSILON2) {
            r = Py_True;
        } else {
            r = Py_False;
        }
        Py_INCREF(r);
        return r;
    } else {
        CONVERSION_ERROR();
    }
}

static PyObject *
Vec2_angle_to(PlanarVec2Object *self, PyObject *other)
{
    double ox, oy;

    assert(PlanarVec2_Check(self));
    if (PlanarVec2_Parse(other, &ox, &oy)) {
        return PyFloat_FromDouble(
            degrees(atan2(oy, ox) - atan2(self->y, self->x)));
    } else {
        CONVERSION_ERROR();
    }
}

static PyObject *
Vec2_distance_to(PlanarVec2Object *self, PyObject *other)
{
    double ox, oy, dx, dy;

    assert(PlanarVec2_Check(self));
    if (PlanarVec2_Parse(other, &ox, &oy)) {
        dx = self->x - ox;
        dy = self->y - oy;
        return PyFloat_FromDouble(sqrt(dx*dx + dy*dy));
    } else {
        CONVERSION_ERROR();
    }
}

static PyObject *
Vec2_dot(PlanarVec2Object *self, PyObject *other)
{
    double ox, oy;

    assert(PlanarVec2_Check(self));
    if (PlanarVec2_Parse(other, &ox, &oy)) {
        return PyFloat_FromDouble(self->x * ox + self->y * oy);
    } else {
        CONVERSION_ERROR();
    }
}

static PyObject *
Vec2_cross(PlanarVec2Object *self, PyObject *other)
{
    double ox, oy;

    assert(PlanarVec2_Check(self));
    if (PlanarVec2_Parse(other, &ox, &oy)) {
        return PyFloat_FromDouble(self->x * oy - self->y * ox);
    } else {
        CONVERSION_ERROR();
    }
}

static PlanarVec2Object *
Vec2_rotated(PlanarVec2Object *self, PyObject *angle_arg)
{
    double angle, sa, ca;

    assert(PlanarVec2_Check(self));
    angle_arg = PyObject_ToFloat(angle_arg);
    if (angle_arg == NULL) {
        return NULL;
    }
    angle = radians(PyFloat_AS_DOUBLE(angle_arg));
    sa = sin(angle);
    ca = cos(angle);
    return Vec2_result(self, 
        self->x * ca - self->y * sa, self->x * sa + self->y * ca);
}

static PlanarVec2Object *
Vec2_scaled_to(PlanarVec2Object *self, PyObject *length)
{
    double L, s;

    assert(PlanarVec2_Check(self));
    length = PyObject_ToFloat(length);
    if (length == NULL) {
        return NULL;
    }
    L = self->x * self->x + self->y * self->y;
    if (L >= PLANAR_EPSILON2) {
        s = PyFloat_AS_DOUBLE(length) / sqrt(L);
        Py_DECREF(length);
        return Vec2_result(self, self->x * s, self->y * s);
    } else {
        return Vec2_result(self, 0.0, 0.0);
    }
}

static PlanarVec2Object *
Vec2_project(PlanarVec2Object *self, PyObject *other)
{
    double ox, oy, L, s;

    assert(PlanarVec2_Check(self));
    if (PlanarVec2_Parse(other, &ox, &oy)) {
        L = self->x * self->x + self->y * self->y;
        if (L >= PLANAR_EPSILON2) {
            s = (self->x * ox + self->y * oy) / L;
            return Vec2_result(self, self->x * s, self->y * s);
        } else {
            return Vec2_result(self, 0.0, 0.0);
        }
    } else {
        CONVERSION_ERROR();
    }
}

static PlanarVec2Object *
Vec2_reflect(PlanarVec2Object *self, PyObject *other)
{
    double ox, oy, L, s;

    assert(PlanarVec2_Check(self));
    if (PlanarVec2_Parse(other, &ox, &oy)) {
        L = ox * ox + oy * oy;
        if (L >= PLANAR_EPSILON2) {
            s = 2 * (self->x * ox + self->y * oy) / L;
            return Vec2_result(self, ox * s - self->x, oy * s - self->y);
        } else {
            return Vec2_result(self, 0.0, 0.0);
        }
    } else {
        CONVERSION_ERROR();
    }
}

static PlanarVec2Object *
Vec2_clamped(PlanarVec2Object *self, PyObject *args, PyObject *kwargs)
{
    double min = 0.0;
    double max = DBL_MAX;
    double L, CL;

    static char *kwlist[] = {"min_length", "max_length", NULL};

    assert(PlanarVec2_Check(self));
    if (!PyArg_ParseTupleAndKeywords(
        args, kwargs, "|dd:Vec2.clamped", kwlist, &min, &max)) {
        return NULL;
    }
    if (min > max) {
        PyErr_SetString(PyExc_ValueError, 
            "Vec2.clamped: expected min_length <= max_length");
        return NULL;
    }

    L = sqrt(self->y * self->y + self->x * self->x);
    CL = (L < min) ? min : L;
    CL = (CL > max) ? max : CL;

    if (L > PLANAR_EPSILON) {
        return Vec2_result(self, 
            self->x * (CL / L), self->y * (CL / L));
    } else {
        return Vec2_result(self, 0.0, 0.0);
    }
}

static PlanarVec2Object *
Vec2_lerp(PlanarVec2Object *self, PyObject *args)
{
    PyObject *other;
    double v, ox, oy;

    assert(PlanarVec2_Check(self));
    if (!PyArg_ParseTuple(args, "Od", &other, &v)) {
        return NULL;
    }
    if (!PlanarVec2_Parse(other, &ox, &oy)) {
        return NULL;
    }
    return Vec2_result(self, 
        self->x * (1.0 - v) + ox * v, 
        self->y * (1.0 - v) + oy * v);
}

static PlanarVec2Object *
Vec2_normalized(PlanarVec2Object *self)
{
    double length;

    assert(PlanarVec2_Check(self));
    length = sqrt(self->y * self->y + self->x * self->x);
    if (length > PLANAR_EPSILON) {
        return Vec2_result(self, self->x / length, self->y / length);
    } else {
        return Vec2_result(self, 0.0, 0.0);
    }
}

static PlanarVec2Object *
Vec2_perpendicular(PlanarVec2Object *self)
{
    assert(PlanarVec2_Check(self));
    return Vec2_result(self, -self->y, self->x);
}

static PyMethodDef Vec2_methods[] = {
    {"polar", (PyCFunction)Vec2_new_polar, 
        METH_CLASS | METH_VARARGS | METH_KEYWORDS, 
        "Create a vector from polar coordinates."},
    {"almost_equals", (PyCFunction)Vec2_almost_equals, METH_O, 
        "Compare vectors for approximate equality."},
    {"angle_to", (PyCFunction)Vec2_angle_to, METH_O, 
        "Compute the smallest angle from this vector to another."},
    {"distance_to", (PyCFunction)Vec2_distance_to, METH_O, 
        "Compute the distance to another point vector."},
    {"dot", (PyCFunction)Vec2_dot, METH_O, 
        "Compute the dot product with another vector."},
    {"cross", (PyCFunction)Vec2_cross, METH_O, 
        "Compute the cross product with another vector."},
    {"rotated", (PyCFunction)Vec2_rotated, METH_O, 
        "Compute the vector rotated by an angle, in degrees."},
    {"scaled_to", (PyCFunction)Vec2_scaled_to, METH_O, 
        "Compute the vector scaled to a given length. "
        "If the vector is null, the null vector is returned."},
    {"project", (PyCFunction)Vec2_project, METH_O, 
        "Compute the projection of another vector onto this one."},
    {"reflect", (PyCFunction)Vec2_reflect, METH_O, 
        "Compute the reflection of this vector against another."},
    {"clamped", (PyCFunction)Vec2_clamped, METH_VARARGS | METH_KEYWORDS, 
        "Compute a vector in the same direction with a bounded length."},
    {"lerp", (PyCFunction)Vec2_lerp, METH_VARARGS, 
        "Compute a vector by linear interpolation between "
        "this vector and another."},
    {"normalized", (PyCFunction)Vec2_normalized, METH_NOARGS, 
        "Return the vector scaled to unit length. "
        "If the vector is null, the null vector is returned."},
    {"perpendicular", (PyCFunction)Vec2_perpendicular, METH_NOARGS, 
        "Compute the perpendicular vector."},
    {NULL, NULL}
};

/* Aritmetic operations */

static PyObject *
Vec2__add__(PyObject *a, PyObject *b)
{
    double ax, ay, bx, by;

    if (PlanarVec2_Parse(a, &ax, &ay) && PlanarVec2_Parse(b, &bx, &by)) {
        return (PyObject *)PlanarVec2_FromDoubles(ax + bx, ay + by);
    } else {
        PyErr_Clear();
        Py_INCREF(Py_NotImplemented);
        return Py_NotImplemented;
    }
}

static PyObject *
Vec2__sub__(PyObject *a, PyObject *b)
{
    double ax, ay, bx, by;

    if (PlanarVec2_Parse(a, &ax, &ay) && PlanarVec2_Parse(b, &bx, &by)) {
        return (PyObject *)PlanarVec2_FromDoubles(ax - bx, ay - by);
    } else {
        PyErr_Clear();
        Py_INCREF(Py_NotImplemented);
        return Py_NotImplemented;
    }
}

static PyObject *
Vec2__mul__(PyObject *a, PyObject *b)
{
    int a_is_vec, b_is_vec;
    double ax, ay, bx, by;

    a_is_vec = PlanarVec2_Parse(a, &ax, &ay);
    b_is_vec = PlanarVec2_Parse(b, &bx, &by);

    if (a_is_vec && b_is_vec) {
        return (PyObject *)PlanarVec2_FromDoubles(ax * bx, ay * by);
    } else if (a_is_vec) {
        b = PyObject_ToFloat(b);
        if (b != NULL) {
            bx = PyFloat_AS_DOUBLE(b);
            a = (PyObject *)PlanarVec2_FromDoubles(ax * bx, ay * bx);
            Py_DECREF(b);
            PyErr_Clear();
            return a;
        }
    } else if (b_is_vec) {
        a = PyObject_ToFloat(a);
        if (a != NULL) {
            ax = PyFloat_AS_DOUBLE(a);
            b = (PyObject *)PlanarVec2_FromDoubles(bx * ax, by * ax);
            Py_DECREF(a);
            PyErr_Clear();
            return b;
        }
    }
    PyErr_Clear();
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
}

static PyObject *
Vec2__truediv__(PyObject *a, PyObject *b)
{
    int a_is_vec, b_is_vec;
    double ax, ay, bx, by;

    a_is_vec = PlanarVec2_Parse(a, &ax, &ay);
    b_is_vec = PlanarVec2_Parse(b, &bx, &by);

    if (a_is_vec && b_is_vec) {
        if (!bx || !by) {
            goto div_by_zero;
        }
        return (PyObject *)PlanarVec2_FromDoubles(ax / bx, ay / by);
    } else if (a_is_vec) {
        b = PyObject_ToFloat(b);
        if (b != NULL) {
            bx = PyFloat_AS_DOUBLE(b);
            if (!bx) {
                goto div_by_zero;
            }
            a = (PyObject *)PlanarVec2_FromDoubles(ax / bx, ay / bx);
            Py_DECREF(b);
            PyErr_Clear();
            return a;
        }
    } else if (b_is_vec) {
        a = PyObject_ToFloat(a);
        if (a != NULL) {
            ax = PyFloat_AS_DOUBLE(a);
            if (!bx || !by) {
                goto div_by_zero;
            }
            b = (PyObject *)PlanarVec2_FromDoubles(ax / bx, ax / by);
            Py_DECREF(a);
            PyErr_Clear();
            return b;
        }
    }
    PyErr_Clear();
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;

div_by_zero:
    PyErr_SetString(PyExc_ZeroDivisionError, "Vec2 division by zero");
    return NULL;
}

static PyObject *
Vec2__floordiv__(PyObject *a, PyObject *b)
{
    PyObject *q;
    PlanarVec2Object *v;
    q = Vec2__truediv__(a, b);
    if (q != NULL && q != Py_NotImplemented) {
        /* Since q is a new vector, not referenced from outside,
           we can modify it here without breaking immutability */
        v = (PlanarVec2Object *)q;
        v->x = floor(v->x);
        v->y = floor(v->y);
    }
    return q;
}

static PlanarVec2Object *
Vec2__pos__(PlanarVec2Object *self)
{
    Py_INCREF(self);
    return self;
}

static PlanarVec2Object *
Vec2__neg__(PlanarVec2Object *self)
{
    assert(PlanarVec2_Check(self));
    return Vec2_result(self, -self->x, -self->y);
}

static int
Vec2__nonzero__(PlanarVec2Object *self)
{
    assert(PlanarVec2_Check(self));
    return self->x != 0.0 || self->y != 0.0;
}

static PyNumberMethods Vec2_as_number = {
    (binaryfunc)Vec2__add__,       /* binaryfunc nb_add */
    (binaryfunc)Vec2__sub__,       /* binaryfunc nb_subtract */
    (binaryfunc)Vec2__mul__,       /* binaryfunc nb_multiply */
#if PY_MAJOR_VERSION < 3
    0,       /* binaryfunc nb_div */
#endif
    0,       /* binaryfunc nb_remainder */
    0,       /* binaryfunc nb_divmod */
    0,       /* ternaryfunc nb_power */
    (unaryfunc)Vec2__neg__,       /* unaryfunc nb_negative */
    (unaryfunc)Vec2__pos__,       /* unaryfunc nb_positive */
    (unaryfunc)Vec2_get_length,   /* unaryfunc nb_absolute */
    (inquiry)Vec2__nonzero__,       /* inquiry nb_bool */
    0,       /* unaryfunc nb_invert */
    0,       /* binaryfunc nb_lshift */
    0,       /* binaryfunc nb_rshift */
    0,       /* binaryfunc nb_and */
    0,       /* binaryfunc nb_xor */
    0,       /* binaryfunc nb_or */
#if PY_MAJOR_VERSION < 3
    0,       /* coercion nb_coerce */
#endif
    0,       /* unaryfunc nb_int */
    0,       /* void *nb_reserved */
    0,       /* unaryfunc nb_float */
#if PY_MAJOR_VERSION < 3
    0,       /* binaryfunc nb_oct */
    0,       /* binaryfunc nb_hex */
#endif

    (binaryfunc)Vec2__add__,       /* binaryfunc nb_inplace_add */
    (binaryfunc)Vec2__sub__,       /* binaryfunc nb_inplace_subtract */
    (binaryfunc)Vec2__mul__,       /* binaryfunc nb_inplace_multiply */
#if PY_MAJOR_VERSION < 3
    0,       /* binaryfunc nb_inplace_divide */
#endif
    0,       /* binaryfunc nb_inplace_remainder */
    0,       /* ternaryfunc nb_inplace_power */
    0,       /* binaryfunc nb_inplace_lshift */
    0,       /* binaryfunc nb_inplace_rshift */
    0,       /* binaryfunc nb_inplace_and */
    0,       /* binaryfunc nb_inplace_xor */
    0,       /* binaryfunc nb_inplace_or */

    (binaryfunc)Vec2__floordiv__,    /* binaryfunc nb_floor_divide */
    (binaryfunc)Vec2__truediv__,     /* binaryfunc nb_true_divide */
    (binaryfunc)Vec2__floordiv__,    /* binaryfunc nb_inplace_floor_divide */
    (binaryfunc)Vec2__truediv__,     /* binaryfunc nb_inplace_true_divide */

    0,       /* unaryfunc nb_index */
};

/* Sequence protocol methods */

static Py_ssize_t
Vec2_len(PyObject *self)
{
    return 2;
}

static PyObject *
Vec2_getitem(PlanarVec2Object *self, Py_ssize_t i)
{
    switch (i) {
        case 0:
            return PyFloat_FromDouble(self->x);
        case 1:
            return PyFloat_FromDouble(self->y);
        default:
            return NULL;
    }
}

static PySequenceMethods Vec2_as_sequence = {
    (lenfunc)Vec2_len,      /* sq_length */
    0,                      /*sq_concat*/
    0,                      /*sq_repeat*/
    (ssizeargfunc)Vec2_getitem, /*sq_item*/
    0,                      /* sq_slice */
    0,                      /* sq_ass_item */
};

PyDoc_STRVAR(Vec2_doc, 
    "Two dimensional immutable vector.\n\n"
    "Vec2(x, y)"
);

PyTypeObject PlanarVec2Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "planar.Vec2",       /* tp_name */
    sizeof(PlanarVec2Object), /* tp_basicsize */
    0,                    /* tp_itemsize */
    (destructor)Vec2_dealloc, /* tp_dealloc */
    0,                    /* tp_print */
    0,                    /* tp_getattr */
    0,                    /* tp_setattr */
    0,                    /* reserved */
    (reprfunc)Vec2_repr,  /* tp_repr */
    &Vec2_as_number,      /* tp_as_number */
    &Vec2_as_sequence,    /* tp_as_sequence */
    0,                    /* tp_as_mapping */
    (hashfunc)Vec2_hash,  /* tp_hash */
    0,                    /* tp_call */
    (reprfunc)Vec2_str,   /* tp_str */
    0, /* PyObject_GenericGetAttr, */                   /* tp_getattro */
    0,/* PyObject_GenericSetAttr, */                    /* tp_setattro */
    0,                    /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_CHECKTYPES,   /* tp_flags */
    Vec2_doc,          /* tp_doc */
    0,                    /* tp_traverse */
    0,                    /* tp_clear */
    Vec2_compare,         /* tp_richcompare */
    0,                    /* tp_weaklistoffset */
    0,                    /* tp_iter */
    0,                    /* tp_iternext */
    Vec2_methods,                    /* tp_methods */
    0,                    /* tp_members */
    Vec2_getset,                    /* tp_getset */
    0,                    /* tp_base */
    0,                    /* tp_dict */
    0,                    /* tp_descr_get */
    0,                    /* tp_descr_set */
    0,                    /* tp_dictoffset */
    (initproc)Vec2_init,  /* tp_init */
    Vec2_alloc,           /* tp_alloc */
    0,          /* tp_new */
    0,              /* tp_free */
};

/***************************************************************************/

static PlanarVec2ArrayObject *
Vec2Array_new(Py_ssize_t size)
{
    PlanarVec2ArrayObject *varray;

    if (size < 0) {
        PyErr_BadInternalCall();
        return NULL;
    }
    varray = PyObject_NewVar(
	PlanarVec2ArrayObject, &PlanarVec2ArrayType, size);
    if (varray == NULL) {
	return NULL;
    }
    varray->vec = varray->data;
    return varray;
}

static void
Vec2Array_dealloc(PyObject *self)
{
    Py_TYPE(self)->tp_free(self);
}

static PyObject *
Vec2Array_getitem(PlanarVec2ArrayObject *self, Py_ssize_t index)
{
    if (index >= 0 && index < Py_SIZE(self)) {
        return (PyObject *)PlanarVec2_FromStruct(self->vec + index);
    }
    PyErr_Format(PyExc_IndexError, "index %d out of range", (int)index);
    return NULL;
}

static int
Vec2Array_assitem(PlanarVec2ArrayObject *self, Py_ssize_t index, PyObject *v)
{
    double x, y;
    if (index >= 0 && index < Py_SIZE(self)) {
	if (!PlanarVec2_Parse(v, &x, &y)) {
	    if (!PyErr_Occurred()) {
		PyErr_Format(PyExc_TypeError, 
		    "Cannot assign %.200s into %.200s",
		    v->ob_type->tp_name, self->ob_type->tp_name);
	    }
	    return -1;
	}
        self->vec[index].x = x;
        self->vec[index].y = y;
        return 0;
    }
    PyErr_Format(PyExc_IndexError, 
	"assignment index %d out of range", (int)index);
    return -1;
}

static Py_ssize_t
Vec2Array_length(PlanarVec2ArrayObject *self)
{
    return Py_SIZE(self);
}

static PySequenceMethods Vec2Array_as_sequence = {
	(lenfunc)Vec2Array_length,	/* sq_length */
	0,		/*sq_concat*/
	0,		/*sq_repeat*/
	(ssizeargfunc)Vec2Array_getitem,		/*sq_item*/
	0,		/* sq_slice */
	(ssizeobjargproc)Vec2Array_assitem,	/* sq_ass_item */
};

PyDoc_STRVAR(Vec2Array__doc__, "Fixed length vector array");

PyTypeObject PlanarVec2ArrayType = {
	PyObject_HEAD_INIT(NULL)
	0,			        /*ob_size*/
	"planar.Vec2Array",		/*tp_name*/
	sizeof(PlanarVec2ArrayObject),	/*tp_basicsize*/
	sizeof(planar_vec2_t),		/*tp_itemsize*/
	/* methods */
	(destructor)Vec2Array_dealloc, /*tp_dealloc*/
	0,			       /*tp_print*/
	0,                      /*tp_getattr*/
	0,                      /*tp_setattr*/
	0,		        /*tp_compare*/
	0,                      /*tp_repr*/
	0,		        /*tp_as_number*/
	&Vec2Array_as_sequence, /*tp_as_sequence*/
	0,	                /*tp_as_mapping*/
	0,	                /*tp_hash*/
	0,                      /*tp_call*/
	0,                      /*tp_str*/
	0,                      /*tp_getattro*/
	0,                      /*tp_setattro*/
	0,                      /*tp_as_buffer*/
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_CHECKTYPES,     /*tp_flags*/
	Vec2Array__doc__,       /*tp_doc*/
	0,                      /*tp_traverse*/
	0,                      /*tp_clear*/
	0,                      /*tp_richcompare*/
	0,                      /*tp_weaklistoffset*/
	0,                      /*tp_iter*/
	0,                      /*tp_iternext*/
	0,                      /*tp_methods*/
	0,                      /*tp_members*/
	0,                      /*tp_getset*/
	0,                      /*tp_base*/
	0,                      /*tp_dict*/
	0,                      /*tp_descr_get*/
	0,                      /*tp_descr_set*/
	0,                      /*tp_dictoffset*/
	0,                      /*tp_init*/
	0,                      /*tp_alloc*/
	(newfunc)Vec2Array_new, /*tp_new*/
	0,                      /*tp_free*/
	0,                      /*tp_is_gc*/
};
