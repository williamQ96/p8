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


def treemap(values: list[Real], width: int, height: int):
    """Create treemap of values in width x height pixel display
    in Tk interface and in SVG file written to treemap.svg.
    """
    display.init(width, height)
    area = geometry.Rect(geometry.Point(0, 0),
                         geometry.Point(width, height))
    layout(values, area)
    display.wait_close()



def layout(items: list[Real], rect: geometry.Rect):
    """Lay elements of nest out in rectangle.
    Version 0 (skeleton code) just takes a slice off the canvas for
    each rectangle.  You will replace it with much better recursive
    layouts.
    """
    while len(items) > 0:
        log.debug(f"Laying out {items} in {rect}")
        proportion = items[0] / sum(items)
        left_rect, rect = rect.split(proportion)
        label = str(items[0])
        display.draw_tile(left_rect, label)
        items = items[1:]

        
def bisect(li: list[Real]) -> tuple[list[Real], list[Real]]:
    """Returns (prefix, suffix) such that prefix+suffix == nest
    and abs(sum(prefix) - sum(suffix)) is minimal.
    Breaks tie in favor of earlier split, e.g., bisect([1,5,1]) == ([1], [5, 1]).
    Requires len(nest) >= 2, and all elements of nest positive.

    >>> bisect([1, 1, 2])  # Perfect balance
    ([1, 1], [2])
    >>> bisect([1.5, 1.5, 3.0])  # Similar, works with floats
    ([1.5, 1.5], [3.0])
    >>> bisect([2.0, 1, 1.0])  # Perfect balance, mixed
    ([2.0], [1, 1.0])
    >>> bisect([1, 2, 1])  # Equally bad either way; split before pivot
    ([1], [2, 1])
    >>> bisect([6, 5, 4, 3, 2, 1])  # Must include element at split
    ([6, 5], [4, 3, 2, 1])
    >>> bisect([1, 2, 3, 4, 5])
    ([1, 2, 3], [4, 5])
    """
    # for i in range(len(li)):
    #     if sum(li[:i+1]) > sum(li) / 2:
    #         break
    # return li[:i], li[i:]
    total_sum = sum(li)
    target = total_sum / 2

    # Compute partial sums
    partial_sums = []
    running_sum = 0
    for num in li:
        running_sum += num
        partial_sums.append(running_sum)

    # Find the optimal split point
    for i, partial_sum in enumerate(partial_sums):
        if partial_sum >= target:
            # Decide whether to include or exclude the current element
            if i == 0 or abs(partial_sum - target) < abs(partial_sums[i - 1] - target):
                return li[:i + 1], li[i + 1:]
            else:
                return li[:i], li[i:]

if __name__ == "__main__":
    doctest.testmod()



