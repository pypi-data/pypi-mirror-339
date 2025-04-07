import os
import cv2
import numpy as np
import inspect
from typing import Union, Literal
from PIL import Image as PillowImage
from PIL.ImageFile import ImageFile as PillowImageFile
from PIL import ImageDraw, ImageFont
class ImageSize:    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

class ImageCli:
    
    def __init__(self, local_file: str):
        self.local_file = local_file
        self.pillow_image_instance: PillowImageFile = self.__load_image_instance()

    def __load_image_instance(self):
        return PillowImage.open(self.local_file)

    @property
    def size(self) -> ImageSize:
        return ImageSize(self.pillow_image_instance.width, self.pillow_image_instance.height)

    @property
    def file_size(self) -> int:
        return os.path.getsize(self.local_file)

    def turn(self, direction: Union[Literal["LEFT"], Literal["RIGHT"]], angle: int) -> str:        
        """
        Rotate the image by a specified angle.
        :param direction: 'LEFT' or 'RIGHT' for the rotation direction.
        :param angle: Angle in degrees for the rotation.
        :return: Path to the rotated image.
        """
        if direction not in ["LEFT", "RIGHT"]:
            raise ValueError("Invalid direction. Use 'LEFT' or 'RIGHT'.")
        
        if direction == "LEFT":
            rotated_image = self.pillow_image_instance.rotate(angle)
        else:
            rotated_image = self.pillow_image_instance.rotate(-angle)
        
        # Extract directory and original filename
        directory, filename = os.path.split(self.local_file)
        base, extension = os.path.splitext(filename)
        
        # Save the rotated image with a new name
        rotated_image_path = os.path.join(directory, f"rotated_{base}{extension}")
        rotated_image.save(rotated_image_path)
        
        return rotated_image_path

    def compress_image(self, target_size: float, unit: Union[Literal["MB", "KB", "bytes"]] = "MB") -> str:
        """
        Compress image to target file size.

        :param target_size: Desired target size for the compressed image.
        :param unit: Unit of the target size ('MB', 'KB', 'bytes'). Default is 'MB'.
        :return: Path to the compressed image.
        """
        conversion_factors = {
            "bytes": 1,
            "KB": 1024,
            "MB": 1024 ** 2
        }
        
        if unit not in conversion_factors:
            raise ValueError(f"Unsupported unit: {unit}. Choose from: {', '.join(conversion_factors.keys())}")
        
        current_size_bytes = self.file_size
        target_size_bytes = target_size * conversion_factors[unit]

        if current_size_bytes <= target_size_bytes:
            return self.local_file

        # Extract directory and original filename
        directory, filename = os.path.split(self.local_file)
        base, extension = os.path.splitext(filename)
        
        # Construct compressed file path by prepending "compressed_" to base name
        output_file = os.path.join(directory, f"compressed_{base}{extension}")

        # Start compression by adjusting quality
        quality = 95
        while True:
            self.pillow_image_instance.save(output_file, format='JPEG', quality=quality)
            if os.path.getsize(output_file) <= target_size_bytes or quality <= 10:
                break
            quality -= 5  # Reduce quality and try again

        return output_file
    

    def change_photo_backgroundcolor(self, color_enum: Union[Literal["BLUE", "WHITE", "RED"]] = "RED") -> str:
        """
        Change the background color of a passport photo based on a color enumeration.

        :param color_enum: 'BLUE', 'WHITE', 'RED' for the desired background color
        :return: Path to the modified image
        """
        # Load the image
        img = cv2.imread(self.local_file)
        rows, cols, channels = img.shape
        print(f"Image resolution: {rows}x{cols}, Channels: {channels}")
        
        # Convert image to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Detect blueish background (you may need to adjust these values based on the actual image background)
        lower_blue = np.array([85, 70, 70])
        upper_blue = np.array([110, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Apply dilation and erosion
        dilate = cv2.dilate(mask, None, iterations=1)
        erode = cv2.erode(dilate, None, iterations=1)

        # Define the new background color based on enum
        if color_enum == "BLUE":
            new_background = (255, 0, 0)  # BGR for blue
        elif color_enum == "RED":
            new_background = (0, 0, 255)  # BGR for red
        elif color_enum == "WHITE":
            new_background = (255, 255, 255)  # BGR for white
        else:
            raise ValueError("Invalid color_enum value. Use 'BLUE', 'RED', or 'WHITE'.")

        # Replace the color
        for i in range(rows):
            for j in range(cols):
                if erode[i, j] == 255:
                    img[i, j] = new_background
        
        # Extract directory and original filename
        directory, filename = os.path.split(self.local_file)
        base, extension = os.path.splitext(filename)

        # Save the image with a new name
        modified_image_path = os.path.join(directory, f"background_{color_enum}_{base}{extension}")
        cv2.imwrite(modified_image_path, img)
        
        return modified_image_path


    def get_formatted_size(self, unit: Union[Literal["bytes", "KB", "MB", "GB"]] = "bytes") -> str:
        """
        Get the formatted file size in the specified unit.

        :param unit: The unit for file size ('bytes', 'KB', 'MB', 'GB').
        :return: Formatted file size with unit.
        :raises ValueError: If the unit is unsupported.
        """
        bytes_size = self.file_size
        units = {
            "bytes": bytes_size,
            "KB": bytes_size / 1024,
            "MB": bytes_size / (1024 ** 2),
            "GB": bytes_size / (1024 ** 3)
        }

        if unit not in units:
            raise ValueError(f"Unsupported unit: {unit}. Choose from: {', '.join(units.keys())}")
        
        return f"{units[unit]:.2f} {unit}"
    
    def pillow_image_call(self, attribute_name: str, *args, **kwargs):
        try:
            # Check if the attribute exists
            if not hasattr(self.pillow_image_instance, attribute_name):
                raise AttributeError(f"{attribute_name} is not a valid attribute or method name.")

            # Get the attribute
            attribute = getattr(self.pillow_image_instance, attribute_name)

            # Check if it is a callable or a property
            if callable(attribute):
                # Get the expected argument names if it's callable
                sig = inspect.signature(attribute)
                expected_args = sig.parameters

                # Validate provided arguments against expected arguments
                for key in kwargs:
                    if key not in expected_args:
                        raise ValueError(f"Unexpected keyword argument: {key}")

                # Call the method with the arguments
                return attribute(*args, **kwargs)
            else:
                # If it's a property, return it directly
                return attribute

        except Exception as e:
            raise Exception(f"Error accessing {attribute_name}: {e}")
