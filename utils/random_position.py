import random

from PyQt5.QtCore import QRectF, QPointF


def get_random_perimeter_position(scene_rect, node_radius=15):
    if not isinstance(scene_rect, QRectF):
        raise ValueError("scene_rect must be a QRectF")

    # Calculate the safe boundaries (accounting for node radius)
    left = scene_rect.left() + node_radius
    right = scene_rect.right() - node_radius
    top = scene_rect.top() + node_radius
    bottom = scene_rect.bottom() - node_radius

    # Calculate the perimeter lengths for each edge
    width = right - left
    height = bottom - top

    if width <= 0 or height <= 0:
        return scene_rect.center()

    # Total perimeter length
    total_perimeter = 2 * width + 2 * height

    # Choose a random point along the perimeter
    random_distance = random.uniform(0, total_perimeter)

    if random_distance <= width:
        # TOP EDGE
        x = left + random_distance
        y = top
        return QPointF(x, y)

    elif random_distance <= width + height:
        # RIGHT EDGE
        x = right
        y = top + (random_distance - width)
        return QPointF(x, y)

    elif random_distance <= 2 * width + height:
        # BOTTOM EDGE
        x = right - (random_distance - width - height)
        y = bottom
        return QPointF(x, y)

    else:
        # LEFT EDGE
        x = left
        y = bottom - (random_distance - 2 * width - height)
        return QPointF(x, y)