import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
from torch.utils.data import sampler
from torch.utils.tensorboard import SummaryWriter
import torch.nn.functional as F
import torchvision
import matplotlib.image as mpimg
from torchvision import datasets, models, transforms
import time
import os
import copy
from PIL import Image
model_ft = models.resnet34(pretrained=True)
class Flatten(nn.Module):
    def forward(self, input):
        return input.view(input.size(0), -1)

class ClassifierNew(nn.Module):
    def __init__(self, inp = 512, h1=256, out = 2, d=0.5):
        super().__init__()
        self.ap = nn.AdaptiveAvgPool2d((1,1))
        self.mp = nn.AdaptiveMaxPool2d((1,1))
        self.fla = Flatten()
        self.bn0 = nn.BatchNorm1d(inp*2,eps=1e-05, momentum=0.1, affine=True)
        self.dropout0 = nn.Dropout(d)
        self.fc1 = nn.Linear(inp*2, h1)
        self.bn1 = nn.BatchNorm1d(h1,eps=1e-05, momentum=0.1, affine=True)
        self.dropout1 = nn.Dropout(d)
        self.fc2 = nn.Linear(h1, out)
        nn.init.kaiming_normal_(self.fc1.weight)
        nn.init.kaiming_normal_(self.fc2.weight)

    def forward(self, x):
        ap = self.ap(x)
        mp = self.mp(x)
        x = torch.cat((ap,mp),dim=1)
        x = self.fla(x)
        x = self.bn0(x)
        x = self.dropout0(x)
        x = F.relu(self.fc1(x))
        x = self.bn1(x)
        x = self.dropout1(x)         
        x = self.fc2(x)

        return x
class Net(nn.Module):
    def __init__(self , model):
        super(Net, self).__init__()
        self.resnet_layer = nn.Sequential(*list(model.children())[:-2])
        self.newlayer = ClassifierNew()
    def forward(self, x):
        x = self.resnet_layer(x)
        x = self.newlayer(x)
 
        return x
NewRes=Net(model_ft)
NewRes.load_state_dict(torch.load('model.pt',map_location='cpu'))
NewRes.cuda()
NewRes.eval()
def get_label(path):
    image=mpimg.imread(path)
    data_transforms = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(size=(224,224)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])
    Im = data_transforms(np.uint8(image)).unsqueeze(0).cuda()
    if np.argmax(NewRes(Im).detach().cpu().numpy())==0:
        return u'无裂缝'
    else :
        return u'有裂缝'
    