import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class PolicyGradient:
    def __init__(self):
        self.alpha = 0.01
        self.gamma = 0.98
        self.device = torch.device('cpu')
        self.model = PolicyNet(input_size=4, hidden_size=128, output_size=2)
        self.model.to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.alpha)

    def reset(self):
        self.model = PolicyNet(input_size=4, hidden_size=128, output_size=2)
        self.model.to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.alpha)

    def action(self, state):
        s = torch.tensor(state, dtype=torch.float32).to(self.device).unsqueeze(0)
        with torch.no_grad():
            pi = self.model(s)
        action = torch.multinomial(pi, num_samples=1).item()
        return action

    def update(self, state, action, reward, next_state, done):
        #TODO:方策勾配は終端状態に到達した際に更新されるため，配列に保存しておく必要がある
        pass



class PolicyNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.softmax(x)
        return x