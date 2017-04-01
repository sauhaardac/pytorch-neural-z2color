import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as initialization
from torch.autograd import Variable


class Z2Color(nn.Module):
    def __init__(self):
        super(Z2Color, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=12, out_channels=96, kernel_size=11, stride=3, groups=1)
        self.conv1_pool = nn.MaxPool2d(kernel_size=3, stride=2)
        self.conv1_pool_drop = nn.Dropout2d(p=0.0)

        self.conv2 = nn.Conv2d(in_channels=102, out_channels=256, kernel_size=3, stride=2, groups=2)
        self.conv2_pool = nn.MaxPool2d(kernel_size=3, stride=2)
        self.conv2_pool_drop = nn.Dropout2d(p=0.0)
        self.ip1 = nn.Linear(in_features=2560, out_features=512)
        self.ip1_drop = nn.Dropout(p=0.0)
        self.ip2 = nn.Linear(in_features=512, out_features=20)

        # Initialize weights
        nn.init.normal(self.conv1.weight, std=0.00001)
        nn.init.normal(self.conv2.weight, std=0.1)

        nn.init.xavier_normal(self.ip1.weight)
        nn.init.xavier_normal(self.ip2.weight)

    def forward(self, x, metadata):
        # conv1
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv1_pool(x)
        x = self.conv1_pool_drop(x)

        # metadata_concat
        x = torch.cat((metadata, x), 1)

        # conv2
        x = self.conv2_pool_drop(self.conv2_pool(F.relu(self.conv2(x))))
        
        x = x.view(-1, 2560)

        # ip1
        x = self.ip1_drop(F.relu(self.ip1(x)))

        # ip2
        x = self.ip2(x)
        
        return x

