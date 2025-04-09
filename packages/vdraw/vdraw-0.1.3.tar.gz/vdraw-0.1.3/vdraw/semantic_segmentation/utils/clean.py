from vdraw.semantic_segmentation.bbox import BBox
import numpy as np


def combine_overlapping_bboxes(bboxes: list[BBox]) -> list[BBox]:
    """
    Combine overlapping bounding boxes.

    :param bboxes: List of BBox objects.

    :return: List of combined BBox objects.
    """

    if not bboxes:
        return []

    local_bboxes = bboxes.copy()

    # Helper function to check overlap
    def is_overlapping(bbox1: BBox, bbox2: BBox):
        x1, y1, w1, h1 = bbox1.get_XYWH_list()
        x2, y2, w2, h2 = bbox2.get_XYWH_list()

        # Check if the bounding boxes overlap
        return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

    # Helper function to merge two bounding boxes
    def merge_bboxes(bbox1: BBox, bbox2: BBox):
        x1, y1, w1, h1 = bbox1.get_XYWH_list()
        x2, y2, w2, h2 = bbox2.get_XYWH_list()

        new_x = min(x1, x2)
        new_y = min(y1, y2)
        new_w = max(x1 + w1, x2 + w2) - new_x
        new_h = max(y1 + h1, y2 + h2) - new_y

        return BBox(x1=new_x, y1=new_y, width=new_w, height=new_h)

    merged = True
    while merged:
        merged = False
        new_bboxes = []
        while local_bboxes:
            current = local_bboxes.pop(0)
            for i in range(len(local_bboxes)):
                if is_overlapping(current, local_bboxes[i]):
                    # Merge and break to restart the process
                    current = merge_bboxes(current, local_bboxes.pop(i))
                    merged = True
                    break
            new_bboxes.append(current)

        local_bboxes = new_bboxes

    return new_bboxes


def small_bboxes_out_of_list(
    bboxes: list[BBox], min_width: int = 0, min_height: int = 0
) -> list[BBox]:
    """
    Removes bounding boxes that are smaller than the specified minimum width and height.

    :param bboxes: List of BBox objects.
    :param min_width: Minimum width of the bounding box (Optional)
    :param min_height: Minimum height of the bounding box (Optional)
    """
    for bbox in bboxes:
        if min_width > 0 and bbox.width < min_width:
            bboxes.remove(bbox)

        if min_height > 0 and bbox.height < min_height:
            bboxes.remove(bbox)

    return bboxes


def out_of_bounds_bbox(bbox: BBox, image: np.ndarray) -> BBox:
    """
    Clips a bounding box so it stays within the bounds of the given image.

    :param bbox: BBox object.
    :param image: RGB image as a NumPy array.
    :return: Clipped BBox object.
    """
    x1, y1, x2, y2 = bbox.get_XYXY_list()

    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(image.shape[1], x2)
    y2 = min(image.shape[0], y2)

    # safeguard
    x2 = max(x2, x1)
    y2 = max(y2, y1)

    return BBox(x1=x1, y1=y1, width=x2 - x1, height=y2 - y1)
