import json
import sys
import os
import torch
from torchvision import transforms
from PIL import Image
from fitz import Rect
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Patch

sys.path.append("../detr")
from models import build_model

class MaxResize(object):
    def __init__(self, max_size=800):
        self.max_size = max_size

    def __call__(self, image):
        width, height = image.size
        current_max_size = max(width, height)
        scale = self.max_size / current_max_size
        resized_image = image.resize((int(round(scale*width)), int(round(scale*height))))
        
        return resized_image

detection_transform = transforms.Compose([
    MaxResize(800),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

structure_transform = transforms.Compose([
    MaxResize(1000),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def get_class_map(data_type):
    if data_type == 'structure':
        class_map = {
            'table': 0,
            'table column': 1,
            'table row': 2,
            'table column header': 3,
            'table projected row header': 4,
            'table spanning cell': 5,
            'no object': 6
        }
    elif data_type == 'detection':
        class_map = {'table': 0, 'table rotated': 1, 'no object': 2}
    return class_map

detection_class_thresholds = {
    "table": 0.5,
    "table rotated": 0.5,
    "no object": 10
}


# for output bounding box post-processing
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(-1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h), (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)


def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b


def iob(bbox1, bbox2):
    """
    Compute the intersection area over box area, for bbox1.
    """
    intersection = Rect(bbox1).intersect(bbox2)
    
    bbox1_area = Rect(bbox1).get_area()
    if bbox1_area > 0:
        return intersection.get_area() / bbox1_area
    
    return 0


def outputs_to_objects(outputs, img_size, class_idx2name):
    m = outputs['pred_logits'].softmax(-1).max(-1)
    pred_labels = list(m.indices.detach().cpu().numpy())[0]
    pred_scores = list(m.values.detach().cpu().numpy())[0]
    pred_bboxes = outputs['pred_boxes'].detach().cpu()[0]
    pred_bboxes = [elem.tolist() for elem in rescale_bboxes(pred_bboxes, img_size)]

    objects = []
    for label, score, bbox in zip(pred_labels, pred_scores, pred_bboxes):
        class_label = class_idx2name[int(label)]
        if not class_label == 'no object':
            objects.append({'label': class_label, 'score': float(score),
                            'bbox': [float(elem) for elem in bbox]})

    return objects

def objects_to_crops(img, tokens, objects, class_thresholds, padding=10):
    """
    Process the bounding boxes produced by the table detection model into
    cropped table images and cropped tokens.
    """

    table_crops = []
    for obj in objects:
        if obj['score'] < class_thresholds[obj['label']]:
            continue

        cropped_table = {}

        bbox = obj['bbox']
        bbox = [bbox[0]-padding - 10, bbox[1]-padding, bbox[2]+padding + 10, bbox[3]+padding]

        cropped_img = img.crop(bbox)

        table_tokens = [token for token in tokens if iob(token['bbox'], bbox) >= 0.5]
        for token in table_tokens:
            token['bbox'] = [token['bbox'][0]-bbox[0],
                             token['bbox'][1]-bbox[1],
                             token['bbox'][2]-bbox[0],
                             token['bbox'][3]-bbox[1]]

        # If table is predicted to be rotated, rotate cropped image and tokens/words:
        if obj['label'] == 'table rotated':
            cropped_img = cropped_img.rotate(270, expand=True)
            for token in table_tokens:
                bbox = token['bbox']
                bbox = [cropped_img.size[0]-bbox[3]-1,
                        bbox[0],
                        cropped_img.size[0]-bbox[1]-1,
                        bbox[2]]
                token['bbox'] = bbox

        cropped_table['image'] = cropped_img
        cropped_table['tokens'] = table_tokens

        table_crops.append(cropped_table)

    return table_crops


def visualize_detected_tables(img, det_tables, out_path):
    plt.imshow(img, interpolation="lanczos")
    plt.gcf().set_size_inches(20, 20)
    ax = plt.gca()
    
    for det_table in det_tables:
        bbox = det_table['bbox']

        if det_table['label'] == 'table':
            facecolor = (1, 0, 0.45)
            edgecolor = (1, 0, 0.45)
            alpha = 0.3
            linewidth = 2
            hatch='//////'
        elif det_table['label'] == 'table rotated':
            facecolor = (0.95, 0.6, 0.1)
            edgecolor = (0.95, 0.6, 0.1)
            alpha = 0.3
            linewidth = 2
            hatch='//////'
        else:
            continue
 
        rect = patches.Rectangle(bbox[:2], bbox[2]-bbox[0], bbox[3]-bbox[1], linewidth=linewidth, 
                                    edgecolor='none',facecolor=facecolor, alpha=0.1)
        ax.add_patch(rect)
        rect = patches.Rectangle(bbox[:2], bbox[2]-bbox[0], bbox[3]-bbox[1], linewidth=linewidth, 
                                    edgecolor=edgecolor,facecolor='none',linestyle='-', alpha=alpha)
        ax.add_patch(rect)
        rect = patches.Rectangle(bbox[:2], bbox[2]-bbox[0], bbox[3]-bbox[1], linewidth=0, 
                                    edgecolor=edgecolor,facecolor='none',linestyle='-', hatch=hatch, alpha=0.2)
        ax.add_patch(rect)

    plt.xticks([], [])
    plt.yticks([], [])

    legend_elements = [Patch(facecolor=(1, 0, 0.45), edgecolor=(1, 0, 0.45),
                                label='Table', hatch='//////', alpha=0.3),
                        Patch(facecolor=(0.95, 0.6, 0.1), edgecolor=(0.95, 0.6, 0.1),
                                label='Table (rotated)', hatch='//////', alpha=0.3)]
    plt.legend(handles=legend_elements, bbox_to_anchor=(0.5, -0.02), loc='upper center', borderaxespad=0,
                    fontsize=10, ncol=2)  
    plt.gcf().set_size_inches(10, 10)
    plt.axis('off')
    plt.savefig(out_path, bbox_inches='tight', dpi=150)
    plt.close()

    return


class TableExtractionPipeline(object):
    def __init__(self, det_device=None,
                 det_model_path=None,
                 det_config_path=None):

        self.det_device = det_device

        self.det_class_name2idx = get_class_map('detection')
        self.det_class_idx2name = {v:k for k, v in self.det_class_name2idx.items()}
        self.det_class_thresholds = detection_class_thresholds

        if not det_config_path is None:
            with open(det_config_path, 'r') as f:
                det_config = json.load(f)
            det_args = type('Args', (object,), det_config)
            det_args.device = det_device
            self.det_model, _, _ = build_model(det_args)
            print("Detection model initialized.")

            if not det_model_path is None:
                self.det_model.load_state_dict(torch.load(det_model_path,
                                                     map_location=torch.device(det_device)))
                self.det_model.to(det_device)
                self.det_model.eval()
                print("Detection model weights loaded.")
            else:
                self.det_model = None

       
    def __call__(self, page_image, page_tokens=None):
        return self.extract(self, page_image, page_tokens)

    def detect(self, img, tokens=None, out_objects=True, out_crops=False, crop_padding=10):
        out_formats = {}
        if self.det_model is None:
            print("No detection model loaded.")
            return out_formats

        # Transform the image how the model expects it
        img_tensor = detection_transform(img)

        # Run input image through the model
        outputs = self.det_model([img_tensor.to(self.det_device)])

        # Post-process detected objects, assign class labels
        objects = outputs_to_objects(outputs, img.size, self.det_class_idx2name)
        if out_objects:
            out_formats['objects'] = objects
        if not out_crops:
            return out_formats

        # Crop image and tokens for detected table
        if out_crops:
            tables_crops = objects_to_crops(img, tokens, objects, self.det_class_thresholds,
                                            padding=crop_padding)
            out_formats['crops'] = tables_crops

        return out_formats


def output_result(key, val, out_dir, visualize, img, img_file):
    if key == 'objects':
        out_file = img_file.replace(".jpg", "_objects.json")
        with open(os.path.join(out_dir, out_file), 'w') as f:
            json.dump(val, f)
        if visualize:
            out_file = img_file.replace(".jpg", "_fig_tables.jpg")
            out_path = os.path.join(out_dir, out_file)
            visualize_detected_tables(img, val, out_path)
    elif not key == 'image' and not key == 'tokens':
        for idx, elem in enumerate(val):
            if key == 'crops':
                for idx, cropped_table in enumerate(val):
                    out_img_file = img_file.replace(".jpg", "_table_{}.jpg".format(idx))
                    cropped_table['image'].save(os.path.join(out_dir,
                                                                out_img_file))
                    out_words_file = out_img_file.replace(".jpg", "_words.json")
                    with open(os.path.join(out_dir, out_words_file), 'w') as f:
                        json.dump(cropped_table['tokens'], f)
            else:
                out_file = img_file.replace(".jpg", "_{}.{}".format(idx, key))
                with open(os.path.join(out_dir, out_file), 'w') as f:
                    f.write(elem)
                        

def main():
    img_path = "inputs/fbc_1.jpg"
    out_dir = './results'
    detection_config_path = 'detection_config.json'
    detection_model_path = 'checkpoints\pubtables1m_detection_detr_r18.pth'
    detection_device = 'cuda'
    crops = True  # or False
    objects = False  # or False
    visualize = False  # or False

    print('-' * 100)

    if not out_dir is None and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Create inference pipeline
    print("Creating inference pipeline")
    pipe = TableExtractionPipeline(det_device=detection_device,
                                   det_config_path=detection_config_path, 
                                   det_model_path=detection_model_path)

    img = Image.open(img_path)
    print("Image loaded.")

    tokens = []

    detected_tables = pipe.detect(img, tokens, out_objects=objects, out_crops=crops)
    print("Table(s) detected.")

    for key, val in detected_tables.items():
        output_result(key, val, out_dir, visualize, img, os.path.basename(img_path))

main()