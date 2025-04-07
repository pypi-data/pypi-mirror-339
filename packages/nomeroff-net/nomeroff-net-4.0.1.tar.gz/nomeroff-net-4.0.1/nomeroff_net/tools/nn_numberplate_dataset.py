import os
from typing import List
import numpy as np
import cv2
import json
from nomeroff_net.pipes.number_plate_keypoints_detectors.bbox_np_points_tools import (normalize_rect_new,
                                                                                      split_numberplate)
from nomeroff_net.tools.image_processing import reshape_points


def add_coordinates_offset(points: List or np.ndarray, x: float, y: float) -> List:
    """
    TODO: describe function
    """
    return [[float(point[0]) + x, float(point[1]) + y] for point in points]


class DatasetConfig:
    def __init__(self,
                 dataset_path: str,
                 ann_subdir: str = 'ann',
                 img_subdir: str = 'img',
                 src_subdir: str = 'src',
                 anb_subdir: str = 'anb',
                 box_subdir: str = 'box',
                 tmp_subdir: str = 'tmp',
                 img_ext: str = 'png',
                 json_ext: str = 'json',
                 debug: bool = False
                 ):
        self.dataset_path = dataset_path
        self.debug = debug
        self.ann_dir = os.path.join(dataset_path, ann_subdir)
        self.img_dir = os.path.join(dataset_path, img_subdir)
        self.src_dir = os.path.join(dataset_path, src_subdir)
        self.anb_dir = os.path.join(dataset_path, anb_subdir)
        self.box_dir = os.path.join(dataset_path, box_subdir)
        self.tmp_dir = os.path.join(dataset_path, tmp_subdir)
        self.img_ext = img_ext
        self.json_ext = json_ext
        self.check_dir(self.ann_dir)
        self.check_dir(self.img_dir)
        self.check_dir(self.src_dir)
        self.check_dir(self.anb_dir)
        self.check_dir(self.box_dir)
        self.check_dir(self.tmp_dir)

    @staticmethod
    def check_dir(path):
        if not os.path.exists(path):
            os.mkdir(path, mode=0o755)


class DatasetRegion:
    def __init__(self,
                 dataset_config: DatasetConfig,
                 anb_key: str,
                 img: np.ndarray,
                 region_key: str,
                 region_data: List,
                 rotate: int = 0,
                 update_lines: bool = False,
                 debug: bool = False):
        self.dataset_config = dataset_config
        self.anb_key = anb_key
        self.rotate = rotate
        self.img = img
        self.region_key = region_key
        self.region_data = region_data
        self.update_lines = update_lines
        self.debug = debug

        # normalize_keypoints
        if self.debug:
            print('self.region_data["keypoints"]')
            print(self.region_data["keypoints"])
        self.keypoints_norm = normalize_rect_new(self.region_data["keypoints"])
        if self.rotate:
            self.keypoints_norm = reshape_points(self.keypoints_norm, self.rotate)
        min_x_box = round(min([keypoint[0] for keypoint in self.keypoints_norm]))
        min_y_box = round(min([keypoint[1] for keypoint in self.keypoints_norm]))
        max_x_box = round(max([keypoint[0] for keypoint in self.keypoints_norm]))
        max_y_box = round(max([keypoint[1] for keypoint in self.keypoints_norm]))
        self.bbox = [min_x_box, min_y_box, max_x_box, max_y_box]

    def recheck(self):
        if "updated" in self.region_data and self.region_data["updated"]:
            if self.debug:
                print('Start updating...')
            new_region_key = self.get_bbox_basename()
            if self.debug:
                print(f'region_key: {self.region_key} new_region_key: {new_region_key}')
            self.rebuild_bbox()
            self.region_data["region_key_new"] = self.get_bbox_basename()
            self.region_data["keypoints"] = self.keypoints_norm.tolist()
            del self.region_data["updated"]
            self.region_data["rebuilded"] = True

    @staticmethod
    def fix_ann_line(ann_path, name):
        with open(ann_path, 'r') as f:
            data = json.load(f)
        data["name"] = name
        if "moderation" not in data:
            data["moderation"] = {"isModerated": 0, "moderatedBy": "rebuild_nn_dataset_image.py"}
        else:
            data["moderation"]["isModerated"] = 0
            data["moderation"]["moderatedBy"] = "rebuild_nn_dataset_image.py"
        with open(ann_path, "w", encoding='utf8') as jsonWF:
            json.dump(data, jsonWF, ensure_ascii=False)

    def rebuild_bbox(self):
        # remove old bbox file
        bbox_filename = self.get_bbox_filename()
        bbox_filename_new = self.get_bbox_filename(self.get_bbox_basename())
        bbox_path = os.path.join(self.dataset_config.box_dir, bbox_filename)
        bbox_path_new = os.path.join(self.dataset_config.box_dir, bbox_filename_new)
        if self.debug:
            print(f"bbox_path: {bbox_path}")
        os.remove(bbox_path)

        if self.debug:
            print("self.bbox[1]:self.bbox[3], self.bbox[0]:self.bbox[2]")
            print(f"{self.bbox[1]}:{self.bbox[3]}, {self.bbox[0]}:{self.bbox[2]}")
        # make new bbox file
        image_part = self.img[self.bbox[1]:self.bbox[3], self.bbox[0]:self.bbox[2]]
        if self.debug:
            print(f"Writing bbox to new file {bbox_path_new}")
        cv2.imwrite(bbox_path_new, image_part)

        # build new lines
        zone_norm = self.get_aligned_image(image_part)
        if self.debug:
            norm_zone_path = os.path.join(self.dataset_config.tmp_dir, self.get_bbox_filename('norm'+self.get_bbox_basename()) )
            print(f"Writing normalized zone to {norm_zone_path}")
            cv2.imwrite(norm_zone_path, zone_norm)
        parts = split_numberplate(zone_norm, len(self.region_data["lines"]))
        if self.debug:
            for i, part in enumerate(parts):
                part_zone_path = os.path.join(self.dataset_config.tmp_dir,
                                              self.get_bbox_filename(f'part-{i}-' + self.get_bbox_basename()))
                print(f"Writing part {i} to {part_zone_path}")
                cv2.imwrite(part_zone_path, part)

        # remove old img files
        idx = 0
        for i, line in self.region_data["lines"].items():
            if self.debug:
                print(f"Processing line {i} [{idx}]")
            if idx == int(i):
                ann_basename = f'{self.region_key}-line-{i}'
                ann_basename_new = f'{self.get_bbox_basename()}-line-{i}'
                ann_filename = f'{ann_basename}.{self.dataset_config.json_ext}'
                ann_filename_new = f'{ann_basename_new}.{self.dataset_config.json_ext}'
                img_filename = f'{ann_basename}.{self.dataset_config.img_ext}'
                img_filename_new = f'{ann_basename_new}.{self.dataset_config.img_ext}'
                ann_path = os.path.join(self.dataset_config.ann_dir, ann_filename)
                ann_path_new = os.path.join(self.dataset_config.ann_dir, ann_filename_new)
                img_path = os.path.join(self.dataset_config.img_dir, img_filename)
                img_path_new = os.path.join(self.dataset_config.img_dir, img_filename_new)
                if self.debug:
                    print(f"Checking existing file {ann_path}")
                if os.path.isfile(ann_path):
                    if self.debug:
                        print(f"Renaming {ann_path} to {ann_path_new}")
                    os.rename(ann_path, ann_path_new)
                    if self.debug:
                        print(f'Fix name "{ann_basename_new}" in {ann_path_new}')
                    self.fix_ann_line(ann_path_new, ann_basename_new)
                else:
                    if self.debug:
                        print(f'Create new annotation in {ann_path_new}')
                    self.write_ann_line_json(parts[idx], ann_basename_new, line, self.region_data["region_id"])
                if os.path.isfile(img_path):
                    if self.debug:
                        print(f'Remove old image for line {i} "{img_path}"')
                    os.remove(img_path)
                if self.debug:
                    print(f'Create new line {i} image  {img_path_new}')
                cv2.imwrite(img_path_new, parts[idx])
            idx += 1
        if self.update_lines:
            if self.debug:
                print(f'CleanUp old lines')
            cnt = len(self.region_data["lines"])
            if cnt < 3:
                for i in range(cnt, 3):
                    ann_basename = f'{self.region_key}-line-{i}'
                    ann_filename = f'{ann_basename}.{self.dataset_config.json_ext}'
                    img_filename = f'{ann_basename}.{self.dataset_config.img_ext}'
                    ann_path = os.path.join(self.dataset_config.ann_dir, ann_filename)
                    img_path = os.path.join(self.dataset_config.img_dir, img_filename)
                    if os.path.isfile(img_path):
                        if self.debug:
                            print(f'Remove old image for line {i} "{img_path}"')
                        os.remove(img_path)
                    if os.path.isfile(ann_path):
                        if self.debug:
                            print(f'Remove old annotation for line {i} "{ann_path}"')
                        os.remove(ann_path)

        # p17667717-519x476-566x504

    def get_bbox_basename(self):
        bbox = self.bbox
        return f'{self.anb_key}-{bbox[0]}x{bbox[1]}-{bbox[2]}x{bbox[3]}'

    def get_bbox_filename(self, region_key = ""):
        if region_key == "":
            region_key = self.region_key
        return f'{region_key}.{self.dataset_config.img_ext}'

    def get_aligned_image(self, image_part):
        h = 100
        w = 400

        count_lines = len(self.region_data["lines"])

        if count_lines > 1:
            w = 300

        # Convert keypoints to numpy array
        local_keypoints = add_coordinates_offset(self.keypoints_norm, -self.bbox[0], -self.bbox[1])
        src_points = np.array(local_keypoints, dtype="float32")

        target_points = np.float32(np.array([[0, h], [0, 0], [w, 0], [w, h]]))
        # Compute the perspective transform matrix
        M = cv2.getPerspectiveTransform(src_points, target_points)

        # Apply the perspective transformation to the image
        aligned_img = cv2.warpPerspective(image_part, M, (w, h))

        return aligned_img

    def write_ann_line_json(self, zone:List or np.ndarray, basename, desc, region_id, replace_data=None):
        if replace_data is None:
            replace_data = {}
        ann_filename = os.path.join(self.dataset_config.ann_dir, f'{basename}.{self.dataset_config.json_ext}')
        height, width = zone.shape[:2]
        data = {
            "description": desc,
            "name": basename,
            "region_id": region_id,
            "count_lines": 1,
            "size": {
                "width": width,
                "height": height
            },
            "moderation": {
                "isModerated": 0,
                "moderatedBy": "rebuild_nn_dataset_image.py"
            }
        }
        data.update(replace_data)
        with open(ann_filename, "w", encoding='utf8') as jsonWF:
            json.dump(data, jsonWF, ensure_ascii=False)


class DatasetItem:

    # default constructor
    def __init__(self,
                 dataset_config: DatasetConfig,
                 anb_key: str,
                 rotate = 0,
                 update_lines: bool = False,
                 debug: bool = False,
                 ):
        self.version = 2
        self.version = 2
        self.rotate = rotate
        self.update_lines = update_lines
        self.debug = debug
        self.dataset_config = dataset_config
        self.anb_key = anb_key
        anb_filename = f'{anb_key}.{dataset_config.json_ext}'
        self.anb_path = os.path.join(dataset_config.anb_dir,anb_filename)
        self.anb_data = self.load_image_markup_data()
        self.orig_ext = os.path.basename(self.anb_data["src"]).split(".")

        img_path = os.path.join(dataset_config.src_dir, self.anb_data["src"])
        self.img = cv2.imread(img_path)

    def recheck_regions(self):
        rename_region_arr = []
        for region_key in self.anb_data["regions"]:
            item = self.anb_data["regions"][region_key]
            dataset_region = DatasetRegion(self.dataset_config, self.anb_key, self.img, region_key, item, self.rotate, self.debug)
            dataset_region.recheck()
            if "region_key_new" in dataset_region.region_data:
                rename_region_arr.append([region_key, dataset_region.region_data["region_key_new"]])
                item["bbox"] = dataset_region.bbox
                del item["region_key_new"]

        for item in rename_region_arr:
            self.anb_data["regions"][item[1]] = self.anb_data["regions"][item[0]]
            if item[1] != item[0]:
                del self.anb_data["regions"][item[0]]
        self.write_image_markup_data()

    def load_image_markup_data(self):
        with open(self.anb_path, 'r') as f:
            return json.load(f)

    def write_image_markup_data(self):
        with open(self.anb_path, "w", encoding='utf8') as jsonWF:
            json.dump(self.anb_data, jsonWF, ensure_ascii=False)

