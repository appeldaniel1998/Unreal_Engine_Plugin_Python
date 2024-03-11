def stupidLogic(length: tuple, width: tuple, height: tuple) -> list:
    """
    Stupid logic for map scanning by the drone.

    Args:
    - length (tuple): Tuple containing minimum and maximum pixel values for length.
    - width (tuple): Tuple containing minimum and maximum pixel values for width.
    - height (tuple): Tuple containing minimum and maximum pixel values for height.

    Returns:
    - list: List of tuples representing the scanning path.
    """
    min_length, max_length = length
    min_width, max_width = width

    scanning_path = []

    # Scan from left to right in each layer
    for w in range(min_width, max_width + 1, 500):  # 5M jump
        # Scan from front to back in each column
        for l in range(min_length, max_length + 1, 500):  # 5M jump
            scanning_path.append((l, w))

        # If width is odd, reverse direction in the next column
        if (max_width - min_width) % 2 != 0:
            scanning_path.extend([(l, w) for l in range(max_length, min_length - 1, -500)])

    return scanning_path


# Example usage:
# length := (0, 10)
# width := (0, 5)
# height := (0, 3)
result = stupidLogic((0, 10), (0, 5), (0, 3))
print(result)
