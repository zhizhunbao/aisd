---
topic: auto_encoders
dimension: code
created: 2026-04-15
last_verified: 2026-04-15
source_versions:
  - "📖 Docs: PyTorch — https://pytorch.org/docs/stable/"
  - "📚 Book: Stevens et al., 《Deep Learning with PyTorch》 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/stevens_deep_learning_with_pytorch.pdf"
expiry: 6m
status: current
---

# Auto-Encoders 代码参考

> 📖 Docs: [PyTorch](https://pytorch.org/docs/stable/)
> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf)

---

## 快速开始

```python
# ============================================================
# Simplest Autoencoder — MNIST, 10 seconds to understand
# 最简自编码器 — MNIST 手写数字，10 秒上手
# ============================================================
import torch
import torch.nn as nn

# Define autoencoder / 定义自编码器
class SimpleAE(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(784, 128),  # 784d → 128d (compress / 压缩)
            nn.ReLU(),
            nn.Linear(128, 32),   # 128d → 32d (bottleneck / 瓶颈)
        )
        self.decoder = nn.Sequential(
            nn.Linear(32, 128),   # 32d → 128d (expand / 扩展)
            nn.ReLU(),
            nn.Linear(128, 784),  # 128d → 784d (reconstruct / 重构)
            nn.Sigmoid(),         # output in [0,1] / 输出归一化到 [0,1]
        )

    def forward(self, x):
        z = self.encoder(x)       # encode / 编码
        x_hat = self.decoder(z)   # decode / 解码
        return x_hat

# Train / 训练
model = SimpleAE()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()

# Assume `dataloader` yields batches of flattened MNIST images
# 假设 dataloader 提供扁平化的 MNIST 图像批次
for epoch in range(10):
    for x_batch, _ in dataloader:
        x_flat = x_batch.view(-1, 784)  # flatten / 扁平化
        x_hat = model(x_flat)
        loss = loss_fn(x_hat, x_flat)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
```

> 📖 Docs: [PyTorch nn.Module](https://pytorch.org/docs/stable/generated/torch.nn.Module.html)

---

## 完整实现示例

### 示例 1: Convolutional AE for MNIST

```python
# ============================================================
# Conv Autoencoder — Better for images than MLP
# 卷积自编码器 — 比 MLP 更适合图像
# ============================================================
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

class ConvAE(nn.Module):
    """Convolutional autoencoder for 28x28 grayscale images.
    卷积自编码器，适用于 28x28 灰度图像。"""
    def __init__(self, latent_dim=16):
        super().__init__()
        # Encoder: 1x28x28 → 32x14x14 → 64x7x7 → latent_dim
        # 编码器：逐层降采样 + 展平到隐空间
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 32, 3, stride=2, padding=1),   # → 32x14x14
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1),  # → 64x7x7
            nn.ReLU(),
            nn.Flatten(),                                 # → 64*7*7 = 3136
            nn.Linear(64 * 7 * 7, latent_dim),           # → latent_dim
        )
        # Decoder: latent_dim → 64x7x7 → 32x14x14 → 1x28x28
        # 解码器：隐空间 → 逐层上采样恢复图像
        self.decoder_fc = nn.Linear(latent_dim, 64 * 7 * 7)
        self.decoder_conv = nn.Sequential(
            nn.ConvTranspose2d(64, 32, 3, stride=2, padding=1, output_padding=1),  # → 32x14x14
            nn.ReLU(),
            nn.ConvTranspose2d(32, 1, 3, stride=2, padding=1, output_padding=1),   # → 1x28x28
            nn.Sigmoid(),
        )

    def encode(self, x):
        return self.encoder(x)

    def decode(self, z):
        x = self.decoder_fc(z)
        x = x.view(-1, 64, 7, 7)          # reshape to feature map / 重塑为特征图
        return self.decoder_conv(x)

    def forward(self, x):
        z = self.encode(x)
        return self.decode(z)

# ---- Training loop / 训练循环 ----
transform = transforms.Compose([transforms.ToTensor()])
train_data = datasets.MNIST('./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=128, shuffle=True)

model = ConvAE(latent_dim=16)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(20):
    total_loss = 0
    for x, _ in train_loader:
        x_hat = model(x)
        loss = nn.functional.mse_loss(x_hat, x)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1:2d} | Loss: {total_loss/len(train_loader):.4f}")
```

### 示例 2: VAE with Reparameterization Trick

```python
# ============================================================
# VAE — Variational Autoencoder with reparameterization
# 变分自编码器 — 可从隐空间采样生成新数据
# ============================================================
class VAE(nn.Module):
    def __init__(self, input_dim=784, hidden_dim=256, latent_dim=20):
        super().__init__()
        # Encoder outputs μ and log(σ²) / 编码器输出均值和对数方差
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc_mu = nn.Linear(hidden_dim, latent_dim)      # mean / 均值
        self.fc_logvar = nn.Linear(hidden_dim, latent_dim)   # log variance / 对数方差

        # Decoder / 解码器
        self.fc3 = nn.Linear(latent_dim, hidden_dim)
        self.fc4 = nn.Linear(hidden_dim, input_dim)

    def encode(self, x):
        h = torch.relu(self.fc1(x))
        return self.fc_mu(h), self.fc_logvar(h)

    def reparameterize(self, mu, logvar):
        """Reparameterization trick: z = μ + σ·ε
        重参数化技巧：将采样变为可微操作"""
        std = torch.exp(0.5 * logvar)   # σ = exp(0.5 * log(σ²))
        eps = torch.randn_like(std)      # ε ~ N(0, I)
        return mu + std * eps            # z = μ + σ·ε

    def decode(self, z):
        h = torch.relu(self.fc3(z))
        return torch.sigmoid(self.fc4(h))

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        x_hat = self.decode(z)
        return x_hat, mu, logvar

def vae_loss(x, x_hat, mu, logvar):
    """ELBO loss = Reconstruction + KL divergence
    ELBO 损失 = 重构损失 + KL 散度"""
    # Reconstruction loss (BCE) / 重构损失
    recon = nn.functional.binary_cross_entropy(x_hat, x, reduction='sum')
    # KL divergence: -0.5 * Σ(1 + log(σ²) - μ² - σ²)
    kl = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return recon + kl

# Training / 训练
model = VAE()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(20):
    for x, _ in train_loader:
        x_flat = x.view(-1, 784)
        x_hat, mu, logvar = model(x_flat)
        loss = vae_loss(x_flat, x_hat, mu, logvar)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

# Generate new samples / 生成新样本
with torch.no_grad():
    z = torch.randn(16, 20)        # sample from N(0,I) / 从标准正态采样
    generated = model.decode(z)     # decode to images / 解码为图像
    generated = generated.view(-1, 1, 28, 28)
```

> 📖 Paper: Kingma & Welling, [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)

---

## API 速查

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `nn.Linear(in, out)` | in_features, out_features | — | 全连接层，AE 的基本组件 |
| `nn.Conv2d(in_ch, out_ch, k)` | in_channels, out_channels, kernel_size | — | 卷积层，用于 Conv AE 编码器 |
| ↳ `stride` | int | 1 | 步幅，用 stride=2 实现下采样 |
| ↳ `padding` | int | 0 | 填充，padding=1 保持尺寸 |
| `nn.ConvTranspose2d(...)` | 同 Conv2d | — | 转置卷积，用于解码器上采样 |
| ↳ `output_padding` | int | 0 | 输出填充，配合 stride=2 |
| `nn.functional.mse_loss` | input, target | reduction='mean' | MSE 重构损失（连续数据） |
| `nn.functional.binary_cross_entropy` | input, target | reduction='mean' | BCE 重构损失（二值数据） |
| `torch.randn_like(tensor)` | 任意 tensor | — | 重参数化用：采样 ε ~ N(0,I) |

> 📖 Docs: [PyTorch nn](https://pytorch.org/docs/stable/nn.html)

---

## 目录结构模板

### 简单版（学习用）

```
autoencoder_project/
├── train.py          # 训练脚本（含模型定义）
├── data/             # MNIST 自动下载到这里
└── requirements.txt  # torch, torchvision
```

### 标准版（实验用）

```
autoencoder_project/
├── models/
│   ├── ae.py         # 基本 AE
│   ├── conv_ae.py    # 卷积 AE
│   └── vae.py        # VAE
├── train.py          # 训练入口
├── evaluate.py       # 可视化重构 + 隐空间
├── configs/
│   └── default.yaml  # 超参数配置
├── data/
└── outputs/
    ├── checkpoints/  # 模型权重
    └── figures/      # 重构对比图
```

### 高级版（生产用）

```
autoencoder_project/
├── src/
│   ├── models/       # AE, VAE, Conv-AE, β-VAE
│   ├── losses/       # 重构损失 + KL + 感知损失
│   ├── data/         # Dataset + DataModule
│   └── utils/        # 可视化、隐空间分析
├── configs/          # Hydra/YAML 配置
├── scripts/
│   ├── train.py
│   ├── generate.py   # 从隐空间采样生成
│   └── anomaly.py    # 异常检测
├── tests/
├── notebooks/        # 探索性分析
└── docker/           # 部署
```

> 📖 Docs: [PyTorch Project Template](https://pytorch.org/tutorials/)
