# Built-ins
from __future__ import absolute_import, division, print_function
import operator
import pickle

# 3rd party
import pytest

# This module
import iteration_utilities

# Test helper
import helper_funcs
from helper_cls import T, toT, failingTIterator
from helper_leak import memory_leak_decorator


duplicates = iteration_utilities.duplicates


@memory_leak_decorator()
def test_duplicates_empty1():
    assert list(duplicates([])) == []


@memory_leak_decorator()
def test_duplicates_normal1():
    assert list(duplicates([T(1), T(2), T(1)])) == [T(1)]


@memory_leak_decorator()
def test_duplicates_key1():
    assert list(duplicates([T(1), T(2), T(1)], abs)) == [T(1)]


@memory_leak_decorator()
def test_duplicates_key2():
    assert list(duplicates([T(1), T(1), T(-1)], abs)) == toT([1, -1])


@memory_leak_decorator()
def test_duplicates_unhashable1():
    assert list(duplicates([{T(1): T(1)}, {T(2): T(2)}, {T(1): T(1)}]
                           )) == [{T(1): T(1)}]


@memory_leak_decorator()
def test_duplicates_unhashable2():
    assert list(duplicates([[T(1)], [T(2)], [T(1)]])) == [[T(1)]]


@memory_leak_decorator()
def test_duplicates_unhashable3():
    assert list(duplicates([[T(1), T(1)], [T(1), T(2)],
                            [T(1), T(3)]], operator.itemgetter(0)
                           )) == [[T(1), T(2)], [T(1), T(3)]]


@memory_leak_decorator()
def test_duplicates_getter1():
    t = duplicates([T(1), T([0, 0]), T(3), T(1)])
    assert not t.seen
    assert t.key is None
    assert next(t) == T(1)
    assert T(1) in t.seen
    assert T(3) in t.seen
    assert T([0, 0]) in t.seen
    assert t.key is None


@memory_leak_decorator()
def test_duplicates_getter2():
    t = duplicates([T(1), T([0, 0]), T(3), T(1)],
                   key=iteration_utilities.return_identity)
    assert t.key is iteration_utilities.return_identity


@memory_leak_decorator(collect=True)
def test_duplicates_failure1():
    with pytest.raises(TypeError):
        list(duplicates(T(10)))


@memory_leak_decorator(collect=True)
def test_duplicates_failure2():
    with pytest.raises(TypeError):
        list(duplicates([T(1), T(2), T(3), T('a')], abs))


@memory_leak_decorator(collect=True)
def test_duplicates_failure3():
    # Test that a failing iterator doesn't raise a SystemError
    with pytest.raises(TypeError) as exc:
        next(duplicates(failingTIterator()))
    assert 'eq expected 2 arguments, got 1' in str(exc)


@memory_leak_decorator(collect=True)
def test_duplicates_failure4():
    # Too few arguments
    with pytest.raises(TypeError):
        duplicates()


@memory_leak_decorator(collect=True)
def test_duplicates_failure5():
    # Failure when comparing the object to the objects in the list
    class NoHashNoEq():
        def __hash__(self):
            raise TypeError('cannot be hashed')

        def __eq__(self, other):
            raise ValueError('bad class')

    with pytest.raises(ValueError) as exc:
        list(duplicates([[T(1)], NoHashNoEq()]))
    assert 'bad class' in str(exc)


@memory_leak_decorator(collect=True)
def test_duplicates_copy1():
    helper_funcs.iterator_copy(duplicates(toT([1, 1])))


@memory_leak_decorator(collect=True)
def test_duplicates_failure6():
    # Failure (no TypeError) when trying to hash the value
    class NoHash():
        def __hash__(self):
            raise ValueError('bad class')

    with pytest.raises(ValueError) as exc:
        list(duplicates([T(1), NoHash()]))
    assert 'bad class' in str(exc)


@memory_leak_decorator(collect=True)
def test_duplicates_failure_setstate1():
    # __setstate__ only accepts Seen instances
    dp = duplicates(toT([1, 1]))
    with pytest.raises(TypeError):
        dp.__setstate__((set(toT(range(1, 3))),))


@memory_leak_decorator(collect=True)
def test_duplicates_failure_setstate2():
    helper_funcs.iterator_setstate_list_fail(duplicates(toT([1, 1])))


@memory_leak_decorator(collect=True)
def test_duplicates_failure_setstate3():
    helper_funcs.iterator_setstate_empty_fail(duplicates(toT([1, 1])))


@pytest.mark.xfail(iteration_utilities.EQ_PY2,
                   reason='pickle does not work on Python 2')
@memory_leak_decorator(offset=1)
def test_duplicates_pickle1():
    dpl = duplicates([T(1), T(2), T(1), T(2)])
    assert next(dpl) == T(1)
    x = pickle.dumps(dpl)
    assert list(pickle.loads(x)) == [T(2)]
