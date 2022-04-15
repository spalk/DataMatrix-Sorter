import cv2
import numpy as np

from .utils import image_resize
from .utils import decode_data_matrix
from .utils import get_fancy_name

class DataMatrix:
    def __init__(self):
        self.image = None
        self.bbox = None     # preliminary bounding box (after Data Matrix area detection)
        self.rect = None     # ??? final rectangle (after successul Data Matrix decoding)
        self.parent_image_shape = None
        self.decoded_successful: bool = None
        self.decoded_info: str = None
        self.db_data = None
        self.fancy_name = None

    def decode(self,  db):
        self.db = db
        info, rect = decode_data_matrix(self.image)
        if info: 
            self.decoded_successful = True
            self.decoded_info = info.decode("utf-8") 
            self.rect = rect
            self.__get_db_data()
            self.__get_fansy_name()
        else:
            self.decoded_successful = False

    def __get_db_data(self):
        uid = self.decoded_info
        if self.db.key_exist(uid):
            self.db_data = self.db.get_item(uid)

    def __get_fansy_name(self):
        if self.decoded_successful:
            self.fancy_name = get_fancy_name(self.db_data)



class TargetImage:
    def __init__(self, path_to_original: str):
        self.path_to_original = path_to_original
        self.image = cv2.imread(self.path_to_original)
        self.data_matrices = None

    def get_image_resized(self, height):
        return image_resize(self.image, height=height)

    def detect_dm(self, data_matrix_detector):
        data_matrix_detector.detect(self.get_image_resized(500)) # TODO: size of detecting image
        data_matrices = data_matrix_detector.get_result()
        if data_matrices:
            self.data_matrices = data_matrices

    def decode_dm(self, db):
        if self.data_matrices:
            for dm in self.data_matrices:
                dm.decode(db)

    def add_plant_name(self):
        # generate name or names
        dmtxs = []
        if self.data_matrices:
            for dm in self.data_matrices:
                if dm.decoded_successful:
                    dmtxs.append(dm)
        
        # font style
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        color = (255, 255, 255)
        thickness = 1

        # number of text lines
        lines_num = len(dmtxs)

        # calculate text bounding box size
        line_h  = 0
        label_h = 0
        label_w = 0 
        for dmtx in dmtxs: 
            label_size = cv2.getTextSize(dmtx.fancy_name, font, font_scale, thickness)
            label_h += label_size[0][1]
            if label_size[0][1] > line_h:
                line_h = label_size[0][1]
            if label_size[0][0] > label_w:
                label_w = label_size[0][0]

        # interline factor
        line_h = line_h * 1.6

        # calculate text origin
        output_image = image_resize(self.image, 600)
        h, w = output_image.shape[:2]
        text_origin_x = 50
        text_origin_y = h - line_h * lines_num

        # calculate background origin and size 
        margin = 5
        bgnd_x1 = text_origin_x - 30
        bgnd_y1 = int(text_origin_y - line_h)
        bgnd_x2 = int(label_w) + bgnd_x1 + 30 + margin
        bgnd_y2 = int(line_h * lines_num) + bgnd_y1 + 2 * margin

        # crop the background rect 
        sub_img = output_image[bgnd_y1:bgnd_y2, bgnd_x1:bgnd_x2]
        black_rect = np.ones(sub_img.shape, dtype=np.uint8) * 0
        res = cv2.addWeighted(sub_img, 0.5, black_rect, 0.5, 1.0)

        # putting the image back to its position
        output_image[bgnd_y1:bgnd_y2, bgnd_x1:bgnd_x2] = res

        colors = [
            (0, 0, 255),
            (0, 255, 0),
            (255, 0, 0),
        ]
        color_index = 0

        for dmtx in dmtxs:

            cv2.putText(
                img=output_image, 
                text=dmtx.fancy_name, 
                org=(int(text_origin_x), int(text_origin_y)), 
                fontFace=font, 
                fontScale=font_scale, 
                color=color,
                thickness=thickness
            )

            if len(dmtxs) > 1:
                cv2.putText(
                    img=output_image, 
                    text='#', 
                    org=(int(text_origin_x) - 20, int(text_origin_y)), 
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, 
                    fontScale=font_scale, 
                    color=colors[color_index],
                    thickness=thickness
                )

                # calculate scale factor
                dm_parent_img_width = dm.parent_image_shape[0]
                output_image_width = output_image.shape[0]
                scale_factor = output_image_width / dm_parent_img_width

                # draw bounding boxex
                cv2.rectangle(
                    output_image,
                    (int(dmtx.bbox[0][0] * scale_factor), int(dmtx.bbox[0][1] * scale_factor)),
                    (int(dmtx.bbox[0][2] * scale_factor), int(dmtx.bbox[0][3] * scale_factor) - 5), 
                    colors[color_index], 
                    2
                )

                color_index += 1

            text_origin_y += line_h
        return output_image


                



    
