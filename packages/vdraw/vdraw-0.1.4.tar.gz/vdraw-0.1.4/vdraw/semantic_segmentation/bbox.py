from dataclasses import dataclass
from pathlib import Path
import numpy as np
import cv2


@dataclass
class BBox:
    """
    Bounding box dataclass

    :param x1: x coordinate of the top left corner
    :param y1: y coordinate of the top left corner
    :param width: width of the bounding box
    :param height: height of the bounding box
    """

    x1: int
    y1: int
    width: int
    height: int

    @property
    def x2(self):
        return self.x1 + self.width

    @property
    def y2(self):
        return self.y1 + self.height

    def get_XYXY_list(self):
        return [self.x1, self.y1, self.x2, self.y2]

    def get_XYWH_list(self):
        return [self.x1, self.y1, self.width, self.height]

    def draw_bbox(
        self,
        image: np.ndarray,
        color=(120, 120, 120),
        thickness=5,
        save_image_in_path: str = None,
    ):
        img_with_bbox = image.copy()
        cv2.rectangle(
            img_with_bbox, (self.x1, self.y1), (self.x2, self.y2), color, thickness
        )

        if save_image_in_path:
            save_image_in_path = Path(save_image_in_path)
            if not save_image_in_path.parent.exists():
                raise ValueError(
                    f"Parent directory {save_image_in_path.parent} does not exist"
                )
            cv2.imwrite(save_image_in_path, img_with_bbox)

        return img_with_bbox

    def expand_horizontally(self, amount: int):
        self.x1 -= amount
        self.width += amount * 2

    def expand_vertically(self, amount: int):
        self.y1 -= amount
        self.height += amount * 2

    def expand(self, amount: int):
        self.expand_horizontally(amount)
        self.expand_vertically(amount)

    def get_dict(self):
        return {
            "x1": self.x1,
            "x2": self.x2,
            "y1": self.y1,
            "y2": self.y2,
            "width": self.width,
            "height": self.height,
        }
