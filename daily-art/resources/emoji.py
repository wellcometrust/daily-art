import json
from io import BytesIO

import numpy as np
import requests
import torch
from PIL import Image
from torchvision.models import resnet101
from torchvision import transforms

class_json_path = (
    "/Users/pimh/personal/daily-art/daily-art/resources/imagenet_classes.json"
)

with open(class_json_path, "r") as f:
    classes = json.load(f)

model = resnet101(pretrained=True).eval()

transform = transforms.Compose(
    [
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def get_image(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    return image.convert("RGB")


def assign_emoji_to_image(image_url):
    image = get_image(image_url)
    image_tensor = transform(image).unsqueeze(0)
    out = model(image_tensor)
    _, classification_index = torch.max(out, 1)
    # torch.nn.functional.softmax(out, dim=1)[0]
    return classes[str(classification_index.item())]
