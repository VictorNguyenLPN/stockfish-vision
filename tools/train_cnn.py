# stockfish-vision/tools/train_cnn.py

import torch, os
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.nn as nn
from models.cnn_chess_piece import ChessPieceCNN

transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((100, 100)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

dataset = datasets.ImageFolder('dataset', transform=transform)
loader = DataLoader(dataset, batch_size=64, shuffle=True)

model = ChessPieceCNN()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()

for epoch in range(50):
    total_loss = 0
    for imgs, labels in loader:
        preds = model(imgs)
        loss = loss_fn(preds, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss:.10f}")

torch.save(model, "models/cnn_chess_piece.pt")
print("Model saved at models/cnn_chess_piece.pt")
