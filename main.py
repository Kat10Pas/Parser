import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import sys
from torch.utils.data import DataLoader, TensorDataset
import numpy as np


class NNetTorch(nn.Module):
    def __init__(self):
        super(NNetTorch, self).__init__()
        self.l0_input = nn.Linear(5, 16)

        # print(self.l0_input.weight)

        self.l1_hidden = nn.Linear(16, 16)
        self.l2_hidden = nn.Linear(16, 16)
        self.l3_output = nn.Linear(16, 1)

    # Прямое распространение
    def forward(self, x):
        x = torch.relu(self.l0_input(x))
        x = torch.relu(self.l1_hidden(x))
        x = torch.relu(self.l2_hidden(x))
        x = self.l3_output(x)
        return x

    # Функция тренировки
    def trainNN(self, train_data, learning_rate, epochs):
        # функция оптимизирующая функцию стоимости (уменьшать ошибку)
        optimazer = optim.Adam(self.parameters(), lr=learning_rate)
        loss_func = nn.BCEWithLogitsLoss()

        for e in range(epochs):
            for (inputs, target) in train_data:
                inputs = Variable(inputs)
                # print(inputs)
                target = Variable(target)
                # print(target)
                # input()

                optimazer.zero_grad()
                netOutData = self.forward(inputs)

                target = target.view(-1, 1)  # tensor.view() == numpy.reshape()
                # print(f"target after reshape: {target}")
                # input()

                loss = loss_func(netOutData, target)
                loss.backward()  # обратное распространение ошибки
                optimazer.step()  # шаг градиента к минимуму (изменению весов)

                sys.stdout.write(f"\rТекущая эпоха: {e}, значение ошибки: {loss.item():.10f}")


p1 = torch.FloatTensor([0.4, 1, 1, 1, 0.7])

train_data = torch.FloatTensor([
    [0, 0, 38, 1, 1],
    [1, 0, 39, 1, 1],
    [1, 1, 38, 1, 0],
    [0, 0, 37, 1, 1],
    [1, 0, 38, 1, 1],
    [1, 1, 38, 1, 1],
    [1, 0, 36, 0, 0],
    [0, 1, 38, 1, 1],
    [0, 0, 36, 0, 0],
    [1, 1, 36, 0, 0]
])

train_data = train_data * p1

target_data = torch.FloatTensor([
    1, 1, 1, 1, 1, 1, 0, 1, 0, 0
])

t_dataset = TensorDataset(train_data, target_data)
trainData = DataLoader(t_dataset, batch_size=1, shuffle=True)  # скормлен набор из одной строки

nnCovid = NNetTorch()
nnCovid.trainNN(trainData, 0.01, 500)

print()

while True:
    print("Enter data:")

    input_d = Variable(torch.FloatTensor(np.array(input().split(' '), dtype=float)))
    input_d = input_d * p1
    print(f"{torch.sigmoid(nnCovid(input_d)).data[0]: .5f}")
