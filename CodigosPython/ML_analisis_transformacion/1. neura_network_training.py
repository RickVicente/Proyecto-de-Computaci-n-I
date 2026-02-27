import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from torch.utils.data import DataLoader, TensorDataset
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

output_csv   = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/3. datasetNormalizadoSinImagen.csv"
df = pd.read_csv(output_csv, encoding='utf-8')

target_column = "nivel_ocupacion"
X = df.drop(columns=["id_entrada", "nivel_ocupacion"]) .values 
y = df[target_column].values  

X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.long)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

batch_size = 32
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

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

classes = np.array([0, 1, 2, 3])
weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=y_train.numpy()
)

class_weights = torch.tensor(weights, dtype=torch.float32)

criterion = nn.CrossEntropyLoss(weight=class_weights)
optimizer = optim.Adam(model.parameters(), lr=0.001)

acc_history = []
epoch_history = []

epochs = 50

for epoch in range(epochs):
    model.train()
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 5 == 0:
        model.eval()
        with torch.no_grad():
            outputs = model(X_test)
            _, preds = torch.max(outputs, 1)
            acc = accuracy_score(y_test, preds)

        acc_history.append(acc)
        epoch_history.append(epoch + 1)

        print(f"Epoch {epoch+1}/{epochs} - Accuracy: {acc:.4f}")

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

torch.save(model.state_dict(), "modelo_red_ML.pth")
print("\nModelo guardado como 'modelo_red_pytorch.pth'")