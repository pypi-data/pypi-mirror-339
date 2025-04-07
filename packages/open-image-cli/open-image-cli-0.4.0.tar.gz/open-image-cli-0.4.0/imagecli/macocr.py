import os
import json
from pathlib import Path
from typing import List
from imagecli.utils.subprocessing import CustomProcess, shell
from imagecli.element import OCRElement

class MacOCR:

    def __init__(self):
        self.bin = Path(os.path.abspath(os.path.dirname(__file__))) / 'bin' / 'macocr'
    
    def ocr(self, image_path: str) -> List[OCRElement]:
        """
        OCR image.
        """
        return [OCRElement.from_dict(data) for data in json.loads(shell(f'{self.bin} -p {image_path} -v=true').stdout)]


if __name__ == '__main__':
    macocr = MacOCR()
    ocr_elements: List[OCRElement] = macocr.ocr('/Users/youngfreefjs/Desktop/code/github/imagecli/static/image_merge/taobaoPage720P.JPG')
    print(json.dumps([OCRElement.to_dict(element) for element in ocr_elements], indent=4, ensure_ascii=False))