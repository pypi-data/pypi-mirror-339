from vdraw.semantic_segmentation.bbox import BBox
import numpy as np
import cv2


def mask_bboxes(mask: np.ndarray) -> list[BBox]:
    """
    Finds bounding boxes of segmentation masks and optionally displays or saves the image with drawn boxes

    :param mask: Segmentation mask as a NumPy array (grayscale or binary)
    :param save_image_in_path: If provided, saves the image with bounding boxes at the given path
    :returns: List of BBox objects [BBox, ...]
    """
    # Convert mask to binary
    binary_mask = (mask > 0).astype(np.uint8) * 255

    # Find contours
    contours, _ = cv2.findContours(
        binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Get bounding boxes
    bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]

    return [BBox(*bbox) for bbox in bounding_boxes]


def largest_combined_bbox(
    mask: np.ndarray, min_widht: int = 0, min_height: int = 0
) -> list[BBox]:
    """
    Finds largest combined bounding box of all segmentation masks

    :param mask: Segmentation mask as a NumPy array (grayscale or binary)
    :param min_widht: Minimum width of the bounding box (Optional)
    :param min_height: Minimum height of the bounding box (Optional)

    :returns: BBox object
    """
    binary_mask = (mask > 0).astype(np.uint8) * 255
    contours, _ = cv2.findContours(
        binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
    min_x, min_y, max_x, max_y = mask.shape[1], mask.shape[0], 0, 0

    for x, y, w, h in bounding_boxes:

        if min_widht > 0 and w < min_widht:
            continue

        if min_height > 0 and h < min_height:
            continue

        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + w)
        max_y = max(max_y, y + h)

    width = max_x - min_x
    height = max_y - min_y

    return BBox(min_x, min_y, width, height)
