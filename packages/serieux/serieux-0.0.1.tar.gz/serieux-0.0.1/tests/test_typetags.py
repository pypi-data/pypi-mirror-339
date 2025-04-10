from typing import get_args

from ovld import ovld, recurse, subclasscheck

from serieux.model import Model
from serieux.typetags import TaggedType, make_tag, pushdown
from tests.common import Point, one_test_per_assert

Apple = make_tag(name="Apple", priority=1)
Banana = make_tag(name="Banana", priority=2)
Carrot = make_tag(name="Carrot", priority=3)
Dog = make_tag(name="Dog", priority=4, inherit=False)


def test_typetag_idempotent():
    assert Apple[int] is Apple[int]


def test_typetag_commutative():
    assert Apple[Banana[int]] is Banana[Apple[int]]


@one_test_per_assert
def test_typetag_strip():
    assert Apple.strip(Apple[int]) is int
    assert Apple.strip(Apple[Banana[int]]) is Banana[int]
    assert Apple.strip(Banana[Apple[int]]) is Banana[int]
    assert Apple.strip(Banana[int]) is Banana[int]
    assert Apple.strip(int) is int


@one_test_per_assert
def test_typetags():
    assert subclasscheck(Apple[int], Apple)
    assert subclasscheck(Apple[Banana[int | str]], Apple)
    assert subclasscheck(Apple[Banana[int | str]], Banana)
    assert not subclasscheck(Apple[object], Apple[int])
    assert not subclasscheck(Apple[int], int)
    assert not subclasscheck(int, Apple[int])


@one_test_per_assert
def test_pushdown():
    assert pushdown(int) is int
    assert pushdown(Apple[int]) is int
    assert pushdown(Apple[list[int]]) == list[Apple[int]]
    assert pushdown(Apple[Banana[list[int]]]) == list[Apple[Banana[int]]]
    assert pushdown(Apple[int | str]) == Apple[int] | Apple[str]


@one_test_per_assert
def test_pushdown_no_inherit():
    # Dog is a tag that is not inherited when pushing down
    assert pushdown(Dog[list[int]]) == list[int]
    assert pushdown(Dog[Apple[list[int]]]) == list[Apple[int]]


def test_pushdown_model():
    t = Apple[Model[Point]]
    tp = t.pushdown()
    assert tp.fields[0].type is Apple[int]
    assert tp.fields[1].type is Apple[int]


def test_on_model():
    t = Model[Apple[Point]]
    assert t._cls is Model[Point]


@ovld
def pie(typ: type[TaggedType], xs):
    return recurse(typ.pushdown(), xs)


@ovld
def pie(typ: type[list[object]], xs):
    return [recurse(get_args(typ)[0], x) for x in xs]


@ovld
def pie(typ: type[Apple[int]], x):
    return x + 1


@ovld
def pie(typ: type[Banana[int]], x):
    return x * 2


@ovld
def pie(typ: type[Carrot[object]], xs):
    return "carrot"


@ovld
def pie(typ: type[int], x):
    return x


def test_with_ovld():
    assert pie(int, 3) == 3
    assert pie(Apple[int], 3) == 4
    assert pie(list[int], [1, 2, 3]) == [1, 2, 3]
    assert pie(Apple[list[int]], [1, 2, 3]) == [2, 3, 4]
    assert pie(Banana[int], 3) == 6

    assert pie(Apple[Banana[int]], 3) == 6
    assert pie(list[Apple[Banana[int]]], [1, 2, 3]) == [2, 4, 6]
    assert pie(Apple[Banana[list[int]]], [1, 2, 3]) == [2, 4, 6]

    assert pie(Carrot[list[int]], [1, 2, 3]) == "carrot"
