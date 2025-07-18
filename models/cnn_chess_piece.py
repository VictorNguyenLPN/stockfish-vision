# stockfish-vision/models/cnn_chess_piece.py

import torch.nn as nn
import torch.nn.functional as F

class ChessPieceCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 5, padding=2)
        self.pool = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.fc1 = nn.Linear(64 * 25 * 25, 256)
        self.fc2 = nn.Linear(256, 13)  # 12 pieces + empty

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # -> (32, 50, 50)
        x = self.pool(F.relu(self.conv2(x)))  # -> (64, 25, 25)
        x = x.view(-1, 64 * 25 * 25)
        x = F.relu(self.fc1(x))
        return self.fc2(x)
