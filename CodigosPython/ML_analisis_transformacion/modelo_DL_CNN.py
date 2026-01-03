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

        # Imagen
        image = Image.open(row["url_camara"]).convert("RGB")
        if self.transform:
            image = self.transform(image)

        # Datos tabulares (19 features, los mismos que usas en Streamlit)
        tabular = torch.tensor([
            row["id_camara"],
            row["cars"],
            row["trucks"],
            row["buses"],
            row["bikes"],
            row["total"],
            row["anio"],
            row["mes"],
            row["dia"],
            row["hora"],
            row["minuto"],
            row["carretera_numero"],
            row["carretera_letra_A"],
            row["carretera_letra_M"],
            row["carretera_letra_N"],
            row["franja_horaria_mañana"],
            row["franja_horaria_noche"],
            row["franja_horaria_tarde"]
        ], dtype=torch.float32)

        label = torch.tensor(row["nivel_ocupacion"], dtype=torch.long)

        return image, tabular, label


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

csv_path = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/8. dataset_DL.csv"
dataset = TrafficDataset(csv_path, transform=transform)

# Train/Test split manual (para que PyTorch lo acepte)
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_data, test_data = torch.utils.data.random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
test_loader = DataLoader(test_data, batch_size=32, shuffle=False)

class CNN(nn.Module):
    def __init__(self, num_tab_features, num_classes):
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
        self.fc_img = nn.Linear(64*28*28, 128)
        self.fc_tab = nn.Linear(num_tab_features, 32)
        self.fc_final = nn.Linear(128 + 32, num_classes)


    def forward(self, x_img, x_tab):
        x = self.cnn(x_img)
        x = x.view(x.size(0), -1)
        x_img_feat = torch.relu(self.fc_img(x))

        x_tab_feat = torch.relu(self.fc_tab(x_tab))

        x = torch.cat([x_img_feat, x_tab_feat], dim=1)
        return self.fc_final(x)
    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
num_classes = len(pd.read_csv(csv_path)["nivel_ocupacion"].unique())

num_tab_features = 18
model = CNN(num_tab_features, num_classes).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 20  # puedes subirlo si quieres más precisión

for epoch in range(epochs):
    model.train()
    total_loss = 0

    for images, tabular, labels in train_loader:
        images = images.to(device)
        tabular = tabular.to(device)
        labels = labels.to(device)

        outputs = model(images, tabular)
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
    for images, tabular, labels in test_loader:
        images = images.to(device)
        tabular = tabular.to(device)
        labels = labels.to(device)

        outputs = model(images, tabular)
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

torch.save(model.state_dict(), "modelo_cnn.pth")
print("\nModelo guardado como 'modelo_cnn.pth'")