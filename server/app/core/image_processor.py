import hashlib
import numpy as np
from PIL import Image
from io import BytesIO

class ImageProcessor:
    def process_image(self, img_data: bytes):
        """
        Returns (hash, feature_vector)
        """
        # 1) Compute hash
        img_hash = hashlib.md5(img_data).hexdigest()
        
        # 2) Convert the image to a feature vector.
        #    This is a simple example: resizing to 32x32, flattening, zero-padding to 512 dims.
        image = Image.open(BytesIO(img_data)).convert("RGB")
        image = image.resize((32, 32))
        arr = np.array(image).astype(float).flatten()

        # Zero-pad or truncate to 512
        if len(arr) > 512:
            arr = arr[:512]
        else:
            arr = np.pad(arr, (0, 512 - len(arr)), 'constant')

        return img_hash, arr.tolist()
