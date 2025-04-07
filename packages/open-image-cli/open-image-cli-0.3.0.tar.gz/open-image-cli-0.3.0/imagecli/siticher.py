'''
ALERT: 
Please ensure that after taking the first screenshot, scroll 1/3 before taking the second screenshot.
You can manually take screenshots (slide up from 2/3 of the screen height to 1/3)
Alternatively, screenshots can be taken through UI automation, with a screen height ranging from 2/3 to 1/3

code by https://github.com/Meituan-Dianping/vision-ui/blob/master/resources/vision_merge.md

'''
import cv2
import numpy as np


class ImageStitcher:
    def __init__(self, image_paths, padding_width=80):
        self.image_paths = image_paths
        self.padding_width = padding_width

    @staticmethod
    def add_padding(image, padding_width):
        """Add padding to the right side of the image."""
        height = image.shape[0]
        padding = np.full((height, padding_width, 3), 210, dtype=np.uint8)
        return np.hstack((image, padding))

    @staticmethod
    def merge_with_scaling(img1, img2, padding_width, roi_scale, tail_scale, index):
        """Merge two images with specific scaling parameters."""
        img1_crop = img1[:-int(tail_scale * img2.shape[0])].copy()
        img2 = img2.copy()

        if img1.shape[1] == img2.shape[1]:
            img1_crop = ImageStitcher.add_padding(img1_crop, padding_width)

        if img1_crop.shape[1] != img2.shape[1]:
            raise ValueError("Image merge: Different image widths.")

        roi_height = int(img2.shape[0] * roi_scale)
        roi = img1_crop[-roi_height:, :, :]
        match_result = cv2.matchTemplate(img2, roi, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(match_result)

        stddev = np.std(roi)
        if stddev < 10:
            max_val = 0.95
        
        cut_y = max_loc[1] + roi_height
        img2_padded = ImageStitcher.add_padding(img2, padding_width)
        merged_img = np.vstack((img1_crop, img2_padded[cut_y:, :, :]))

        cv2.putText(merged_img, f"-{index}", (img2.shape[1], img1_crop.shape[0]), 
                    cv2.FONT_ITALIC, 1.5, (123, 189, 60), 5)

        return merged_img, max_val

    @staticmethod
    def stack_images(img1, img2, padding_width, index):
        """Stack two images vertically."""
        img1_padded = ImageStitcher.add_padding(img1, padding_width)
        img2_padded = ImageStitcher.add_padding(img2, padding_width)
        stacked_img = np.vstack((img1_padded, img2_padded))
        
        cv2.putText(stacked_img, f"-{index}", (img2.shape[1], img1_padded.shape[0]), 
                    cv2.FONT_ITALIC, 1.5, (123, 189, 60), 5)

        return stacked_img

    def __merge_images(self, img1, img2, index, padding_width, attempt_merge=True):
        """Merge two images with configurable scales."""
        match_threshold = 0.98
        minimum_threshold = 0.92

        scale_parameters = [
            {"roi_scale": 0.12, "tail_scale": 0.18},
            {"roi_scale": 0.08, "tail_scale": 0.32},
            {"roi_scale": 0.08, "tail_scale": 0.08},
            {"roi_scale": 0.05, "tail_scale": 0.2},
            {"roi_scale": 0.1,  "tail_scale": 0.4},
            {"roi_scale": 0.08, "tail_scale": 0.15},
        ]

        image_combinations = []
        scores = []

        if attempt_merge:
            for params in scale_parameters:
                merged_img, score = ImageStitcher.merge_with_scaling(
                    img1, img2, padding_width, params["roi_scale"], params["tail_scale"], index)
                image_combinations.append(merged_img)
                scores.append(score)

                if score > match_threshold:
                    return merged_img

            if max(scores) < minimum_threshold:
                return ImageStitcher.stack_images(img1, img2, padding_width, index)
            
            return image_combinations[scores.index(max(scores))]
        else:
            return ImageStitcher.stack_images(img1, img2, padding_width, index)

    def stitch_images(self, output_path, remove_padding=False, attempt_merge=True):
        """Stitch images from the configured list and save the result."""
        if len(self.image_paths) < 2:
            cv2.imwrite(str(output_path), cv2.imread(self.image_paths[0]))
            return str(output_path)

        padding_width = 0 if remove_padding else self.padding_width

        img1 = cv2.imread(self.image_paths[0])
        for index, path in enumerate(self.image_paths[1:], start=1):
            img2 = cv2.imread(path)
            if img1 is None or img2 is None:
                raise IOError(f"Failed to read one of the images; check paths and integrity.")

            img1 = self.__merge_images(img1, img2, index, padding_width, attempt_merge)

        cv2.imwrite(str(output_path), img1)
        return str(output_path)


if __name__ == '__main__':
    import os
    from pathlib import Path

    base_path = Path(os.path.dirname(__file__)).parent / 'static' / 'image_merge'
    image_paths = [
        os.path.join(base_path, 'taobaoPage1.JPG'),
        os.path.join(base_path, 'taobaoPage2.JPG'),
        os.path.join(base_path, 'taobaoPage3.JPG'),
    ]

    stitcher = ImageStitcher(image_paths)
    output_image_path = Path(base_path) / 'merged.png'
    merged_image_path = stitcher.stitch_images(output_image_path, True)
    print(f'Merged image saved to: {merged_image_path}')