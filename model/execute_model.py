import timm
import urllib
from PIL import Image
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
import torch
import os
import tempfile

def execute_model(image_url: str):
    # create model
    model = timm.create_model('mobilenetv3_large_100', pretrained=True)
    #load and process image
    config = resolve_data_config({}, model=model)
    transform = create_transform(**config)

    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_img:
        urllib.request.urlretrieve(image_url, tmp_img.name)
        img = Image.open(tmp_img.name).convert('RGB')
        tensor = transform(img).unsqueeze(0)

    # model predict
    with torch.no_grad():
        out = model(tensor)
    probabilities = torch.nn.functional.softmax(out[0], dim=0)

    with tempfile.NamedTemporaryFile(suffix=".txt") as tmp_classes:
        url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
        urllib.request.urlretrieve(url, tmp_classes.name)
        with open(tmp_classes.name, "r") as f:
            categories = [s.strip() for s in f.readlines()]

    # Print top categories per image
    top5_prob, top5_catid = torch.topk(probabilities, 5)
    res = []
    for i in range(top5_prob.size(0)):
        res.append({categories[top5_catid[i]]: round(top5_prob[i].item(), 4)})
    return res