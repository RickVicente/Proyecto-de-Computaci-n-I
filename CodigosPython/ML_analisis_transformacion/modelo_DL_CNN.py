import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class TrafficDataset(Dataset):
    def __init__(self, csv_path, transform=None):
        self.data = pd.read_csv(csv_path)
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]

        # 1) Cargar imagen
        img_path = row["url_camara"]
        image = Image.open(img_path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        # 2) Etiqueta (target)
        label = torch.tensor(row["nivel_ocupacion"], dtype=torch.long)

        return image, label

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

csv_path = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/dataset_transformado_DL.csv"
dataset = TrafficDataset(csv_path, transform=transform)

# Train/Test split manual (para que PyTorch lo acepte)
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_data, test_data = torch.utils.data.random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
test_loader = DataLoader(test_data, batch_size=32, shuffle=False)

class CNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),  # 224x224 → 224x224
            nn.ReLU(),
            nn.MaxPool2d(2),                # 224x224 → 112x112

            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),                # 112×112 → 56×56

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)                 # 56×56 → 28×28
        )
        self.fc = nn.Linear(64 * 28 * 28, num_classes)

    def forward(self, x):
        x = self.cnn(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x
    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
num_classes = len(pd.read_csv(csv_path)["nivel_ocupacion"].unique())

model = CNN(num_classes).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 20  # puedes subirlo si quieres más precisión

for epoch in range(epochs):
    model.train()
    total_loss = 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch [{epoch+1}/{epochs}] - Loss: {total_loss:.4f}")

model.eval()
all_preds = []
all_labels = []

with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)

        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

# Resultados
accuracy = accuracy_score(all_labels, all_preds)
print(f"\nPrecisión final CNN: {accuracy:.4f}")

print("\nReporte de clasificación:")
print(classification_report(all_labels, all_preds))

print("\nMatriz de confusión:")
print(confusion_matrix(all_labels, all_preds))

torch.save(model.state_dict(), "cnn_trafico.pth")
print("\nModelo guardado como 'cnn_trafico.pth'")