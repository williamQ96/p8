""" Construct a treemap.
Author: Jolin Wang

Instructions:  Copy this file to treemap.py and then edit it. REMOVE this part of the
docstring and complete the identifying information above.  Credits should start out
empty, but add classmates or outside sources (including web sources or AI helpers)
as appropriate.  Be certain you understand it well enough to recreate it without help.

Example use:  python3 mapper.py data/small_flat.json 500 500
"""

# Standard Python library modules
import logging
import doctest

# Project modules, provided
import geometry
import display

# Enable logging with log.debug(msg), log.info(msg), etc.
logging.basicConfig()
log = logging.getLogger(__name__)  # Log messages will look like "DEBUG:mapper:msg"
log.setLevel(logging.DEBUG)   # Change to logging.INFO to suppress debugging messages


# Layout works with integers, floating point numbers, or a mix of the two.
Real = int | float    # Named type for use in type annotations
Nest = Real | list['Nest'] | dict[ str, 'Nest'] | tuple[str, 'Nest']

def treemap(values: list[Real], width: int, height: int):
    """Create treemap of values in width x height pixel display
    in Tk interface and in SVG file written to treemap.svg.
    """
    display.init(width, height)
    area = geometry.Rect(geometry.Point(0, 0),
                         geometry.Point(width, height))
    layout(values, area)
    display.wait_close()



def layout(nest: Nest, rect: geometry.Rect):
    """Lay elements of nest out in rectangle.
    Recursively lays out a nested list of integers
    """
    if isinstance(nest, Real):  # Base case: single number
        display.draw_tile(rect, label=str(nest))

    elif isinstance(nest, list):  # Recursive cases: list of Nests
        if len(nest) == 1:  # Single element list
            layout(nest[0], rect)
        elif len(nest) > 1:  # Multiple elements
            left, right = bisect(nest)
            left_rect, right_rect = rect.split(deep_sum(left) / deep_sum(nest))
            layout(left, left_rect)
            layout(right, right_rect)

    elif isinstance(nest, dict):  # Convert dict to list of tuples
        layout(list(nest.items()), rect)

    elif isinstance(nest, tuple):  # (label, value) pair
        key, value = nest
        if isinstance(value, Real):  # Single number
            display.draw_tile(rect, label=f"{key}\n{value}")
        else:  # Nested group
            display.begin_group(rect, label=key)
            layout(value, rect)
            display.end_group()

    else:
        assert False, f"Unexpected type in layout: {type(nest)}"

        
def bisect(li: list[Real]) -> tuple[list[Real], list[Real]]:
    """Returns (prefix, suffix) such that prefix+suffix == nest
    and abs(sum(prefix) - sum(suffix)) is minimal.
    Breaks tie in favor of earlier split, e.g., bisect([1,5,1]) == ([1], [5, 1]).
    Requires len(nest) >= 2, and all elements of nest positive.

    >>> bisect([1, 1, 2])  # Perfect balance
    ([1, 1], [2])
    >>> bisect([2, 1, 1])  # Perfect balance
    ([2], [1, 1])
    >>> bisect([1, 2, 1])  # Equally bad either way; split before pivot
    ([1], [2, 1])
    >>> bisect([6, 5, 4, 3, 2, 1])  # Must include element at split
    ([6, 5], [4, 3, 2, 1])
    >>> bisect([1, 2, 3, 4, 5])
    ([1, 2, 3], [4, 5])
    >>> bisect([1, 1, [1, 1]])
    ([1, 1], [[1, 1]])
    >>> bisect([[3, 3], 5, [2, 2], [1, 1, 1]])
    ([[3, 3], 5], [[2, 2], [1, 1, 1]])
    """
    # for i in range(len(li)):
    #     if sum(li[:i+1]) > sum(li) / 2:
    #         break
    # return li[:i], li[i:]
    assert isinstance(li, list), f"bisect is only for lists, can't split {li}"
    assert len(li) >= 2, f"Cannot bisect {li}; length must be at least 2"

    total_sum = deep_sum(li)
    target = total_sum / 2

    # Compute partial sums
    partial_sums = []
    running_sum = 0
    for item in li:
        running_sum += deep_sum(item)
        partial_sums.append(running_sum)

    # Find the optimal split point
    for i, partial_sum in enumerate(partial_sums):
        if partial_sum >= target:
            # Decide whether to include or exclude the current element
            if i == 0 or abs(partial_sum - target) < abs(partial_sums[i - 1] - target):
                return li[:i + 1], li[i + 1:]
            else:
                return li[:i], li[i:]
            
def deep_sum(nest: Nest) -> Real:
    """Returns the total of all numbers in the Nest.

    >>> deep_sum(12)
    12
    >>> deep_sum([12, 13, 10])
    35
    >>> deep_sum([[7, 3], [1, [2, 7]], 10])
    30
    >>> deep_sum([[1.0, 2.0], [3, 4]])
    10.0
    >>> deep_sum({ "Cake": { "Chocolate": 10, "Carrot": 4 }, "Ice Cream": 15 })
    29
    """
    if isinstance(nest, dict):  # Convert dict to list of tuples
        nest = list(nest.items())
    
    if isinstance(nest, Real):  # Base case: single number
        return nest
    elif isinstance(nest, tuple):  # Handle (label, value) pairs
        key, value = nest
        return deep_sum(value)
    elif isinstance(nest, list):  # Recursive case: list of nested items
        return sum(deep_sum(item) for item in nest)
    else:
        raise ValueError(f"Unsupported type in deep_sum: {type(nest)}")
    
if __name__ == "__main__":
    doctest.testmod()



