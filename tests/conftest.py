import enum
import decimal
import typing
import uuid

from pytest import fixture

from nirum.serialize import serialize_record_type, serialize_unboxed_type
from nirum.deserialize import deserialize_record_type, deserialize_unboxed_type
from nirum.validate import (validate_unboxed_type, validate_record_type,
                            validate_union_type)
from nirum.constructs import NameDict, name_dict_type


class Token:

    __nirum_inner_type__ = uuid.UUID

    def __init__(self, value: uuid.UUID) -> None:
        validate_unboxed_type(value, uuid.UUID)
        self.value = value

    def __eq__(self, other) -> bool:
        return (isinstance(other, Token) and self.value == other.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __nirum_serialize__(self) -> typing.Mapping[str, typing.Any]:
        return serialize_unboxed_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls: type, value: typing.Mapping[str, typing.Any]
    ) -> 'Token':
        return deserialize_unboxed_type(cls, value)

    def __hash__(self) -> int:  # noqa
        return hash((self.__class__, self.value))


class Offset:

    __nirum_inner_type__ = float

    def __init__(self, value: float) -> None:
        validate_unboxed_type(value, float)
        self.value = value

    def __eq__(self, other) -> bool:
        return (isinstance(other, Offset) and self.value == other.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __nirum_serialize__(self) -> typing.Mapping[str, typing.Any]:
        return serialize_unboxed_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls: type, value: typing.Mapping[str, typing.Any]
    ) -> 'Offset':
        return deserialize_unboxed_type(cls, value)

    def __hash__(self) -> int:  # noqa
        return hash((self.__class__, self.value))


class Point:

    __slots__ = (
        'left',
        'top'
    )
    __nirum_record_behind_name__ = 'point'
    __nirum_field_types__ = {
        'left': Offset,
        'top': Offset
    }
    __nirum_field_names__ = NameDict([
        ('left', 'x')
    ])

    def __init__(self, left: Offset, top: Offset) -> None:
        self.left = left
        self.top = top
        validate_record_type(self)

    def __repr__(self) -> str:
        return '{0.__module__}.{0.__qualname__}({1})'.format(
            type(self),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Point) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __nirum_serialize__(self) -> typing.Mapping[str, typing.Any]:
        return serialize_record_type(self)

    @classmethod
    def __nirum_deserialize__(cls: type, values) -> 'Point':
        return deserialize_record_type(cls, values)

    def __hash__(self) -> int:
        return hash((self.__class__, self.left, self.top))


class Shape:

    __nirum_union_behind_name__ = 'shape'
    __nirum_field_names__ = NameDict([
    ])

    class Tag(enum.Enum):
        rectangle = 'rectangle'
        circle = 'circle'

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "{0.__module__}.{0.__qualname__} cannot be instantiated "
            "since it is an abstract class.  Instantiate a concrete subtype "
            "of it instead.".format(
                type(self)
            )
        )

    def __nirum_serialize__(self) -> typing.Mapping[str, typing.Any]:
        pass

    @classmethod
    def __nirum_deserialize__(cls: type, value) -> 'Shape':
        pass


class Rectangle(Shape):

    __slots__ = (
        'upper_left',
        'lower_right'
    )
    __nirum_tag__ = Shape.Tag.rectangle
    __nirum_tag_types__ = {
        'upper_left': Point,
        'lower_right': Point
    }
    __nirum_tag_names__ = NameDict([])

    def __init__(self, upper_left: Point, lower_right: Point) -> None:
        self.upper_left = upper_left
        self.lower_right = lower_right
        validate_union_type(self)

    def __repr__(self) -> str:
        return '{0.__module__}.{0.__qualname__}({1})'.format(
            type(self),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Rectangle) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )


class Circle(Shape):

    __slots__ = (
        'origin',
        'radius'
    )
    __nirum_tag__ = Shape.Tag.circle
    __nirum_tag_types__ = {
        'origin': Point,
        'radius': Offset
    }
    __nirum_tag_names__ = NameDict([])

    def __init__(self, origin: Point, radius: Offset) -> None:
        self.origin = origin
        self.radius = radius
        validate_union_type(self)

    def __repr__(self) -> str:
        return '{0.__module__}.{0.__qualname__}({1})'.format(
            type(self),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Circle) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )


class Location:
    # TODO: docstring

    __slots__ = (
        'name',
        'lat',
        'lng',
    )
    __nirum_record_behind_name__ = 'location'
    __nirum_field_types__ = {
        'name': typing.Optional[str],
        'lat': decimal.Decimal,
        'lng': decimal.Decimal
    }
    __nirum_field_names__ = name_dict_type([
        ('name', 'name'),
        ('lat', 'lat'),
        ('lng', 'lng')
    ])

    def __init__(self, name: typing.Optional[str],
                 lat: decimal.Decimal, lng: decimal.Decimal) -> None:
        self.name = name
        self.lat = lat
        self.lng = lng
        validate_record_type(self)

    def __repr__(self) -> str:
        return '{0.__module__}.{0.__qualname__}({1})'.format(
            type(self),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Location) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __nirum_serialize__(self) -> typing.Mapping[str, typing.Any]:
        return serialize_record_type(self)

    @classmethod
    def __nirum_deserialize__(cls: type, value) -> 'Location':
        return deserialize_record_type(cls, value)


@fixture
def fx_unboxed_type():
    return Offset


@fixture
def fx_offset(fx_unboxed_type):
    return fx_unboxed_type(1.2)


@fixture
def fx_record_type():
    return Point


@fixture
def fx_point(fx_record_type, fx_unboxed_type):
    return fx_record_type(fx_unboxed_type(3.14), fx_unboxed_type(1.592))


@fixture
def fx_circle_type():
    return Circle


@fixture
def fx_rectangle_type():
    return Rectangle


@fixture
def fx_rectangle(fx_rectangle_type, fx_point):
    return fx_rectangle_type(fx_point, fx_point)


class A:

    __nirum_inner_type__ = str

    def __init__(self, value: str) -> None:
        validate_unboxed_type(value, str)
        self.value = value  # type: Text

    def __eq__(self, other) -> bool:
        return (isinstance(other, A) and
                self.value == other.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __nirum_serialize__(self) -> str:
        return serialize_unboxed_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls: type, value: typing.Mapping[str, typing.Any]
    ) -> 'A':
        return deserialize_unboxed_type(cls, value)

    def __repr__(self) -> str:
        return '{0.__module__}.{0.__qualname__}({1!r})'.format(
            type(self), self.value
        )


class B:

    __nirum_inner_type__ = A

    def __init__(self, value: A) -> None:
        validate_unboxed_type(value, A)
        self.value = value  # type: A

    def __eq__(self, other) -> bool:
        return (isinstance(other, B) and
                self.value == other.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __nirum_serialize__(self) -> str:
        return serialize_unboxed_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls: type, value: typing.Mapping[str, typing.Any]
    ) -> 'B':
        return deserialize_unboxed_type(cls, value)

    def __repr__(self) -> str:
        return '{0.__module__}.{0.__qualname__}({1!r})'.format(
            type(self), self.value
        )


class C:

    __nirum_inner_type__ = B

    def __init__(self, value: B) -> None:
        validate_unboxed_type(value, B)
        self.value = value  # type: B

    def __eq__(self, other) -> bool:
        return (isinstance(other, C) and
                self.value == other.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __nirum_serialize__(self) -> str:
        return serialize_unboxed_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls: type, value: typing.Mapping[str, typing.Any]
    ) -> 'C':
        return deserialize_unboxed_type(cls, value)

    def __repr__(self) -> str:
        return '{0.__module__}.{0.__qualname__}({1!r})'.format(
            type(self), self.value
        )


@fixture
def fx_layered_unboxed_types():
    return A, B, C


@fixture
def fx_location_record():
    return Location


@fixture
def fx_shape_type():
    return Shape


@fixture
def fx_token_type():
    return Token
