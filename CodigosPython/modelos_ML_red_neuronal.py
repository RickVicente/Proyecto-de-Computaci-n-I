import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from torch.utils.data import DataLoader, TensorDataset

# ================================
# 1. CARGA DE DATOS
# ================================
metadata_csv = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/dataset_transformado_ML.csv"
data = pd.read_csv(metadata_csv, encoding='utf-8')

target_column = "nivel_ocupacion"
X = data.drop(columns=[target_column]).values
y = data[target_column].values  

# ================================
# 2. SPLIT + ESCALADO
# ================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.long)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.long)

batch_size = 32
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# ================================
# 3. DEFINICIÓN DEL MODELO
# ================================
class NeuralNet(nn.Module):
    def __init__(self, input_dim, num_classes):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

input_dim = X_train.shape[1]
num_classes = len(torch.unique(y_train))

model = NeuralNet(input_dim, num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# ================================
# 4. ENTRENAMIENTO
# ================================
epochs = 50

for epoch in range(epochs):
    for batch_X, batch_y in train_loader:
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch+1) % 10 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

# ================================
# 5. EVALUACIÓN
# ================================
model.eval()
with torch.no_grad():
    outputs = model(X_test)
    _, predicted = torch.max(outputs.data, 1)

accuracy = accuracy_score(y_test, predicted)
print(f"\nPrecisión de la red neuronal (PyTorch): {accuracy:.4f}")

print("\n=== Reporte de Clasificación ===")
print(classification_report(y_test, predicted))

print("\n=== Matriz de Confusión ===")
print(confusion_matrix(y_test, predicted))

# ================================
# 6. GUARDADO DEL MODELO
# ================================
torch.save(model.state_dict(), "modelo_red_pytorch.pth")
print("\nModelo guardado como 'modelo_red_pytorch.pth'")