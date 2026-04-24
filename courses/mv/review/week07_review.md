# Week 7 Review — Introduction to PyTorch

> 📋 Based on instructor's revision topics:
> **What is PyTorch? Key features, PyTorch vs TensorFlow, Core components, Tensor, Neural network module, Building a simple neural network, Best practices in PyTorch**

---

## Q1: What is PyTorch?

PyTorch is an **open-source machine learning library** for Python, known for:
- **Flexibility** and **ease of use**
- **Dynamic computation graph** (Define-by-Run)
- One of the **most popular** deep learning frameworks

Developed by **Facebook AI Research Lab (FAIR)** in 2016, evolved from Torch (Lua, 2002).

---

## Q2: What are the key features of PyTorch?

| Feature | Description |
|---|---|
| **Dynamic computation graph** | Allows on-the-fly network modification (Define-by-Run) |
| **GPU acceleration** | Leverages CUDA for faster computation |
| **Python integration** | Seamless compatibility with NumPy, SciPy |
| **Auto differentiation** | Autograd system |
| **Cloud support** | AWS, GCP, Azure |
| **Hardware support** | CPU, GPU, TPU, parallel processing |

---

## Q3: PyTorch vs TensorFlow Comparison

| Aspect | PyTorch | TensorFlow |
|---|---|---|
| **Computation graphs** | **Dynamic** (Define-by-Run) | **Static** (Define-and-Run) |
| **Ease of use** | More user-friendly | Steeper learning curve |
| **Debugging** | Easier (Pythonic) | More complex |
| **Community** | Strong in **research** | Strong in **production** |
| **Deployment** | Growing (mobile, web) | Extensive (TFLite, TF Serving) |
| **Pre-trained models** | TorchVision | TensorFlow Hub |

**Use PyTorch if:** beginner, research, need flexibility (NLP, CV)
**Use TensorFlow if:** enterprise, mobile deployment, production-ready

---

## Q4: What are the core components of PyTorch?

| Component | Role |
|---|---|
| **Tensors** | Fundamental data structure, similar to NumPy ndarray but with GPU support |
| **Autograd** | Automatic gradient computation (gradient-based optimization) |
| **Optimizers** | Abstract optimization algorithms for training neural networks (SGD, Adam, RMSprop) |

---

## Q5: What is a Tensor?

**Tensor** = a **multi-dimensional array** containing elements of a single data type, a generalization of scalars → vectors → matrices.

| Advantage | Description |
|---|---|
| **GPU acceleration** | Significantly faster computation using GPU |
| **Distributed processing** | Large-scale processing across multiple CPUs/GPUs |
| **Computation graph tracking** | Tracks the computation graph that created them (for autograd) |

**Math definition:** Tensors = generalization of scalars (0D), vectors (1D), matrices (2D) to any dimension (nD)

---

## Q6: How to build a simple neural network?

1. Define a model class inheriting from `nn.Module`
2. Define layers in `__init__()` function
3. Define data flow in `forward()` function

```python
class SimpleNN(nn.Module):
    def __init__(self):
        # Define layers: Conv, ReLU, FC
    def forward(self, x):
        # Define data flow through layers
```

---

## Q7: What are the best practices in PyTorch?

| Practice | Description |
|---|---|
| **GPU acceleration** | Use GPU whenever possible |
| **Data splitting** | Properly split train / validation / test |
| **DataLoader** | Use PyTorch's built-in DataLoader for data management |
| **Model saving/loading** | Regularly save and load models to prevent data loss |
| **Modular code** | Keep code modular and well-documented |
| **Transfer learning** | Use pre-trained models from torchvision (e.g., ResNet) |

---

## Q8: Three Phases of Deep Learning Training

| Phase | Description |
|---|---|
| **1. Data Preparation** | Convert data to tensors → transforms preprocessing → batching |
| **2. Model Development** | Design model, train and test (train/val/test split) |
| **3. Model Deployment** | Save model → deploy to cloud server or edge devices |
