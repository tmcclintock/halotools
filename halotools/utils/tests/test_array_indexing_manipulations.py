""" Module provides testing for the array_indexing_manipulations functions.
"""
from __future__ import division, print_function, absolute_import, unicode_literals

import numpy as np
from astropy.utils.misc import NumpyRNGContext
from astropy.tests.helper import pytest

from .. import array_indexing_manipulations as aim

__all__ = ('test_calculate_first_idx_unique_array_vals1',
    'test_calculate_first_idx_unique_array_vals2', 'test_calculate_last_idx_unique_array_vals1',
    'test_calculate_last_idx_unique_array_vals2', 'test_sum_in_bins1')


def test_calculate_first_idx_unique_array_vals1():
    arr = np.array([1, 1, 2, 2, 2, 3, 3])
    result = aim.calculate_first_idx_unique_array_vals(arr)
    correct_result = np.array([0, 2, 5])
    assert np.all(result == correct_result)


def test_calculate_first_idx_unique_array_vals2():
    arr = np.array([1, 2, 3])
    result = aim.calculate_first_idx_unique_array_vals(arr)
    correct_result = np.array([0, 1, 2])
    assert np.all(result == correct_result)


def test_calculate_first_idx_unique_array_vals3():
    """ This test uses random arrays to verify that the following hold:

    1. The length of the returned result equals the number of unique elements in ``arr``

    2. The entries of the returned result are unique

    3. All elements in arr[result[i]:result[i+1]] are the same

    4. arr[result[i]] != arr[result[i]-1]

    5. arr[result[i]] != arr[result[i+1]]

    6. arr[result[-1]:] == arr.max()
    """
    low, high = -1000, 1000
    npts = int(10*(high-low))
    seed_list = [1, 100, 500, 999]
    num_random_indices_to_test = 100
    for seed in seed_list:
        with NumpyRNGContext(seed):
            arr = np.sort(np.random.randint(low, high, npts))
            result = aim.calculate_first_idx_unique_array_vals(arr)
            assert result[0] == 0
            assert len(result) == len(set(arr))
            assert len(result) == len(set(result))

            # test the outer edge
            assert np.all(arr[result[-1]:] == arr.max())

            # test random indices and random arrays
            random_idx_to_test = np.random.choice(np.arange(1, len(result)-2),
                size=num_random_indices_to_test)
            for elt in random_idx_to_test:
                first = result[elt]
                last = result[elt+1]-1
                assert len(set(arr[first:last+1])) == 1
                assert arr[first] != arr[first-1]
                assert arr[first] != arr[last+1]
                assert arr[last] != arr[last+1]


def test_calculate_last_idx_unique_array_vals1():
    arr = np.array([1, 1, 2, 2, 2, 3, 3])
    result = aim.calculate_last_idx_unique_array_vals(arr)
    correct_result = np.array([1, 4, 6])
    assert np.all(result == correct_result)


def test_calculate_last_idx_unique_array_vals2():
    arr = np.array([1, 2, 3])
    result = aim.calculate_last_idx_unique_array_vals(arr)
    correct_result = np.array([0, 1, 2])
    assert np.all(result == correct_result)


def test_calculate_last_idx_unique_array_vals3():
    """ This test uses random arrays to verify that the following hold:

    1. The length of the returned result equals the number of unique elements in ``arr``

    2. The entries of the returned result are unique

    3. All elements in arr[result[i]:result[i+1]] are the same

    4. arr[result[i]] != arr[result[i]-1]

    5. arr[result[i]] != arr[result[i+1]]

    6. arr[:result[0]+1] == arr.min()
    """
    low, high = -1000, 1000
    npts = int(10*(high-low))
    seed_list = [1, 100, 500, 999]
    num_random_indices_to_test = 100
    for seed in seed_list:
        with NumpyRNGContext(seed):
            arr = np.sort(np.random.randint(low, high, npts))
            result = aim.calculate_last_idx_unique_array_vals(arr)
            assert result[-1] == len(arr)-1
            assert len(result) == len(set(arr))
            assert len(result) == len(set(result))

            # test the outer edge
            assert np.all(arr[:result[0]+1] == arr.min())

            # test random indices and random arrays
            random_idx_to_test = np.random.choice(np.arange(1, len(result)-2),
                size=num_random_indices_to_test)
            for elt in random_idx_to_test:
                last = result[elt]
                first = result[elt-1]+1
                assert len(set(arr[first:last+1])) == 1
                assert arr[first] != arr[first-1]
                assert arr[first] != arr[last+1]
                assert arr[last] != arr[last+1]


def test_sum_in_bins1():
    sorted_bin_numbers = np.array([1, 1, 2, 2, 2, 3, 3])
    values_in_bins = np.array([0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.3])
    result = aim.sum_in_bins(values_in_bins, sorted_bin_numbers)
    correct_result = np.array([0.2, 0.6, 0.6])
    assert np.allclose(result, correct_result)


def test_sum_in_bins2():
    with pytest.raises(ValueError) as err:
        result = aim.sum_in_bins([1, 2], [1, 2, 3])
    substr = "Input ``arr`` and ``sorted_bin_numbers`` must have same length"
    assert substr in err.value.args[0]


def test_sum_in_bins3():
    with pytest.raises(ValueError) as err:
        result = aim.sum_in_bins([1, 2, 3], [1, 2, 1], testing_mode=True)
    substr = "Input ``sorted_bin_numbers`` array must be sorted in ascending order"
    assert substr in err.value.args[0]


def test_sum_in_bins4():
    """ This test uses random arrays to verify that the following hold:

    1. The length of the returned result equals the number of unique elements in ``sorted_bin_numbers``

    2. Randomly chosen entries are correct when calculated manually

    Test (2) is also a highly non-trivial integration test that the
    sum_in_bins, calculate_first_idx_unique_array_vals and
    calculate_last_idx_unique_array_vals work properly in concert with one another.
    """
    low, high = -1000, 1000
    npts = int(10*(high-low))
    seed_list = [1, 100, 500, 999]
    num_random_indices_to_test = 100
    for seed in seed_list:
        with NumpyRNGContext(seed):
            sorted_bin_numbers = np.sort(np.random.randint(low, high, npts))
            values_in_bins = np.random.rand(npts)
            result = aim.sum_in_bins(values_in_bins, sorted_bin_numbers)
            assert len(result) == len(set(sorted_bin_numbers))

            first_idx_array = aim.calculate_first_idx_unique_array_vals(sorted_bin_numbers)
            last_idx_array = aim.calculate_last_idx_unique_array_vals(sorted_bin_numbers)
            entries_to_test = np.random.choice(np.arange(len(first_idx_array)),
                num_random_indices_to_test)
            for i in entries_to_test:
                first, last = first_idx_array[i], last_idx_array[i]
                assert len(set(sorted_bin_numbers[first:last+1])) == 1
                correct_result = np.sum(values_in_bins[first:last+1])
                result_i = result[i]
                assert np.allclose(correct_result, result_i, rtol=0.0001)



