import torch.nn.functional as F
from PIL import Image
from torch.autograd import Variable
from torchvision import transforms
import numpy as np
import os
import sys
import py_gflops_model

model_name = sys.argv[1]
device_name = sys.argv[2]
input_size = sys.argv[3]

batchsize_throughput = sys.argv[4]
input_size = int(input_size)
batchsize_throughput = int(batchsize_throughput)

result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize_throughput)
os.environ['CUDA_VISIBLE_DEVICES'] = "0"

device = device_name
print("device:", device)

transform = transforms.Compose(
    [transforms.Resize(input_size),
     transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

net = py_gflops_model.mobilenetv2()

if model_name == "shufflenet05":
    net = py_gflops_model.shufflenet05()
elif model_name == "mobilenetv2":
    net = py_gflops_model.mobilenetv2()
elif model_name == "resnet50":
    net = py_gflops_model.resnet50()
elif model_name == "resnet34":
    net = py_gflops_model.resnet34()
elif model_name == "vgg19":
    net = py_gflops_model.vgg19()

net.to(device)
net.to(device).eval()

im = Image.open("8_190.jpg")
a = np.asarray(im)
img = Image.fromarray(a)
img = transform(img)
img = img.to(device)
img = img.unsqueeze(0)
output = None
for i in range(100):
    output = net(img)
prob = F.softmax(output, dim=1)
prob = Variable(prob)
prob = prob.cpu().numpy()
pred = np.argmax(prob)
classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
pred_class = classes[pred]
print(pred_class)
