"""Rewrite CST8508_Lab5.ipynb code cells with English comments matching the Demo Guide format."""
import json, pathlib

NB = pathlib.Path(__file__).parent / "CST8508_Lab5.ipynb"
nb = json.loads(NB.read_text("utf-8"))

# ── New source for each code cell (English translations of Lab5_Demo_Guide.md) ──

CELL0 = r'''# ── Cell 0: Dataset Download & Cleanup ─────────────────────────────────────────
#
# ── Imports ──
# os:              OS interface — file path operations
# zipfile:         Extract .zip archives (dataset distributed as compressed archive)
# urllib.request:  HTTP download (stdlib — no pip install needed)
# pathlib.Path:    OOP file paths (cleaner than os.path)
# PIL.Image:       Pillow imaging lib — verify() detects corrupt JPEGs
# Why all stdlib (except PIL)? → Minimal-dependency principle — fewer deps = fewer env issues
#   🪨 Irreducible: portability = code runs on any machine

import os, zipfile, urllib.request
from pathlib import Path
from PIL import Image

# ── Dataset URL & paths ──
# What: Define download URL, local ZIP path, and extracted folder path
# Dataset: Microsoft Cats vs Dogs — 12 500 cats + 12 500 dogs, ~786 MB
# Why this dataset? → Classic binary-classification benchmark with enough images (25K) to train a CNN
#   Why so many images? → CNN has ~8.5 M parameters — too few images → overfitting (memorisation)
#   Why is overfitting bad? → Model only memorises training set, fails on new images
#   🪨 Irreducible: generalisation = the ultimate goal of ML

DATASET_URL  = "https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_5340.zip"
ZIP_PATH     = Path("kagglecatsanddogs_5340.zip")
DATASET_PATH = Path("PetImages")

# ── Download dataset ──
# What: Download from Microsoft server if neither ZIP nor extracted folder exists locally
# Why check before downloading? → 786 MB is large — re-downloading wastes time
# Why check two conditions? → ZIP may have been deleted but folder already extracted → no need to re-download
if not ZIP_PATH.exists() and not DATASET_PATH.exists():
    print("Downloading dataset (~786 MB) ...")
    urllib.request.urlretrieve(DATASET_URL, ZIP_PATH)
    print("Download complete.")
else:
    print("Zip / dataset already present, skipping download.")

# ── Extract dataset ──
# What: Unzip to current directory, creating PetImages/Cat/ and PetImages/Dog/ folders
# Folder layout: PetImages/Cat/*.jpg + PetImages/Dog/*.jpg
# Why this layout? → PyTorch ImageFolder uses folder names as class labels (Cat=0, Dog=1) [ImageFolder]
#   Why not a CSV list? → ImageFolder = zero-config, folder name IS the label
#   🪨 Irreducible: convention over configuration — reduces human error
if not DATASET_PATH.exists():
    print("Extracting ...")
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(".")
    print("Extraction complete.")

# ── Remove corrupted images ──
# What: Check each JPEG with PIL verify(), delete any corrupted files
# Why verify? → This dataset has known broken JPEGs
#   Why do corrupted images cause problems? → DataLoader decode failure → entire training crashes
#   Why can't we try-except and skip? → DataLoader's collate_fn raises on any exception — no skip
#   Why do JPEGs get corrupted? → JPEG is a compressed format — even 1 wrong byte breaks the Huffman table
#   🪨 Irreducible: file integrity is a binary-level hard constraint
removed = 0
for img_path in DATASET_PATH.rglob("*.jpg"):
    try:
        with Image.open(img_path) as img:
            img.verify()
    except Exception:
        img_path.unlink()
        removed += 1
print(f"Removed {removed} corrupted images.")
print(f"Dataset ready at: {DATASET_PATH.resolve()}")
'''.strip().split('\n')

CELL1 = r'''# ── Cell 1: Data Loading & Augmentation ───────────────────────────────────────
#
# ── Imports ──
# random:                     Control randomness of data split — reproducibility
# torch:                      PyTorch core (tensor ops + autograd + GPU acceleration)
# DataLoader:                 Auto batching, shuffling, multi-process prefetch
# Subset:                     Slice train/test subsets by index list (stores indices only, not images)
# datasets.ImageFolder:       Assigns class labels by folder name [ImageFolder]
# transforms:                 Image preprocessing pipeline (Resize / Flip / Normalize etc.)

import os, random
import torch
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms

# ── Fix random seed ──
# What: Set random and torch seeds to 42
# Why fix seeds? → Ensures train/test split is identical every run → reproducible results
#   Why reproducibility? → Without it, impossible to compare "did the parameter change help or hurt?"
#   🪨 Irreducible: controlled variables = fundamental requirement of scientific experiments
random.seed(42)
torch.manual_seed(42)

# ── Select compute device ──
# What: Detect whether GPU is available; prefer GPU
# Why detect CUDA? → GPU training is 5-10× faster (parallel matrix computation)
#   Why is GPU faster? → GPU has thousands of small cores, computing matrix ops for all samples simultaneously
#   🪨 Irreducible: parallel computing is a hardware architectural advantage
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")

# What: Define data loading function — read images, augment, split train/test, wrap in DataLoader
# Why wrap in a function? → Main pipeline only needs one line: load_dataset()
#   Why parameterise split_ratio? → Easy to experiment with different splits (80/20, 70/30 etc.)
#   🪨 Irreducible: modularity = reusable + testable + maintainable
def load_dataset(path, split_ratio=0.8):

    # ══════════════════════════════════════════════════
    # Training transforms (with augmentation)
    # What: Chain multiple image transforms into a pipeline using transforms.Compose
    #       Training set adds Flip and Rotation for data augmentation (test set does not)
    # Why augmentation? → Let model see more "variants", prevent memorising raw images [DataAug]
    #   Why augment only training set? → Test set simulates real-world — must not be artificially modified
    #   🪨 Irreducible: training = studying, testing = exam — no open-book exams
    # ══════════════════════════════════════════════════
    train_transform = transforms.Compose([

        # What: Resize all images to 128×128 pixels
        # Why Resize? → Original images vary in size; must unify for batching
        #   Why must unify? → GPU matrix ops require all data in a batch to have the same shape
        #   Why 128? → Smaller than ImageNet standard (224) → 3× faster training, sufficient for lab demo
        #   Why not 64? → Too small — fine details (cat whiskers, dog ear shape) lost
        #   🪨 Irreducible: GPU parallel computation requires uniform tensor shapes
        transforms.Resize((128, 128)),

        # What: Randomly flip images horizontally with 50% probability (data augmentation)
        # Why flip? → Creates new samples for free — effectively doubles dataset size [DataAug]
        #   Why need more data? → Model has ~8.5 M parameters; too few samples → overfitting (memorisation)
        #     Why 8.5M? → Mainly from FC1 (Fully Connected Layer 1):
        #                  flattened 128×16×16=32768 dims × 256 neurons ≈ 8.39M params,
        #                  plus 3 Conv layers (~93K) + FC2 (514) ≈ 8.48M. See Cell 2 param count
        #   Why doesn't flipping break labels? → A flipped cat is still a cat → semantics preserved
        #   Why no flip for test set? → Test = simulate real usage; you don't flip user photos before inference
        #   🪨 Irreducible: increase diversity while preserving labels → forces learning essence, not surface
        transforms.RandomHorizontalFlip(),

        # What: Randomly rotate images by ±15° (data augmentation)
        # Why rotate? → Simulates camera tilt when taking photos [DataAug]
        #   Why ±15°? → Too large (90°) creates unnatural blank regions; too small (2°) has no effect
        #   Why do photos have tilt? → Handheld cameras are never perfectly level
        #   🪨 Irreducible: simulate real-world data distribution → improve generalisation
        transforms.RandomRotation(15),

        # What: Convert PIL image to PyTorch Tensor, pixel values [0,255] → [0,1]
        # Why ToTensor? → PyTorch only operates on Tensors — this step is mandatory
        #   Why [0,1]? → Smaller float range → more stable gradient magnitudes
        #   🪨 Irreducible: framework hard requirement for input format
        transforms.ToTensor(),

        # What: Normalise each RGB channel (subtract mean, divide by std) → mean≈0, std≈1
        # Why Normalise? → Gradient descent converges fastest when all dimensions are at uniform scale [ImageNet][IN-norm]
        #   Why does uniform scale help? → Unequal → loss surface is an elongated ellipsoid → gradient zig-zags
        #   Why ImageNet values? → Statistics from 1.2 M images — industry standard used by virtually all models
        #   🪨 Irreducible: gradient descent converges fastest on a spherical surface — mathematical property
        transforms.Normalize([0.485, 0.456, 0.406],   # RGB means
                             [0.229, 0.224, 0.225]),   # RGB stds
    ])

    # ══════════════════════════════════════════════════
    # Test transforms (NO augmentation — only Resize + ToTensor + Normalize)
    # What: Test set only gets size unification and normalisation, no flip/rotation
    # Why no Flip or Rotation? → Test set = simulate real-world; augmentation is a training-only technique
    #   🪨 Irreducible: evaluation must be done on unmodified original data to be meaningful
    # ══════════════════════════════════════════════════
    test_transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    # What: Read entire dataset using ImageFolder — folder names become labels automatically
    # Why ImageFolder? → Zero-config loading; folder name = label, no CSV mapping needed [ImageFolder]
    #   🪨 Irreducible: convention over configuration — reduces human error
    full = datasets.ImageFolder(root=path, transform=train_transform)
    n = len(full)

    # What: Split into training and test sets at 80/20 ratio
    # Why 80/20? → Standard split — ~20 000 train, ~5 000 test [CLT]
    #   Why not 50/50? → Too little training data to learn sufficient patterns
    #   Why not 99/1? → Test set too small (250 images) for reliable evaluation
    #   Why is 5 000 enough? → Statistics: 5 000 samples give accuracy confidence interval < ±1%
    #   🪨 Irreducible: evaluation must be on "in-distribution but unseen" data
    train_n = int(n * split_ratio)

    # What: Shuffle indices before splitting — avoids first half = all cats, second half = all dogs
    # Why shuffle? → Raw data is sorted by folder (cats first, dogs second); without shuffling train = all cats
    #   🪨 Irreducible: IID (independent & identically distributed) is a theoretical prerequisite for SGD convergence
    idx = list(range(n))
    random.shuffle(idx)
    train_data = Subset(full, idx[:train_n])
    test_data  = Subset(datasets.ImageFolder(root=path, transform=test_transform), idx[train_n:])

    # What: Create DataLoader — fetch 32 images per batch
    # Why batch_size=32? → Compromise between GPU memory and gradient estimate quality [MiniBatch]
    #   Why not all 20 000 at once? → GPU VRAM can't hold it (needs 3 GB+ for data + intermediate activations)
    #   Why not one at a time? → Single-sample gradient is extremely noisy → random direction → very slow convergence
    #   Why is 32 enough? → Central Limit Theorem: mean of 32 samples is a reasonable approximation of the true mean [CLT]
    #   🪨 Irreducible: mini-batch = Monte Carlo approximation of the true gradient under finite resources
    #
    # shuffle=True  → without shuffling, each epoch sees data in the same order → periodic bias in updates
    # num_workers=2 → child processes prefetch next batch on CPU while GPU computes → GPU never waits for I/O
    train_loader = DataLoader(train_data, batch_size=32, shuffle=True,  num_workers=2)

    # shuffle=False → test does not need shuffling, and deterministic order aids reproducibility
    test_loader  = DataLoader(test_data,  batch_size=32, shuffle=False, num_workers=2)
    print(f"Train: {train_n}  Test: {n - train_n}  Classes: {full.classes}")
    return train_loader, test_loader
'''.strip().split('\n')

CELL2 = r'''# ── Cell 2: CNN Model Definition ───────────────────────────────────────────────
#
# ── Imports ──
# torch.nn:            Layer definitions (Conv2d / Linear / Dropout / MaxPool2d / Module base class)
# torch.nn.functional: Stateless functional API (relu / softmax) — no instantiation needed

import torch.nn as nn
import torch.nn.functional as F

# What: Define SimpleCNN class, inheriting nn.Module (base class for all PyTorch models)
# Why inherit Module? → Automatic parameter registration, GPU transfer, train/eval mode switching
#   Why let the framework manage parameters? → Tracking 8.5 M weights manually is impossible → must automate
#   🪨 Irreducible: "everything is a Module" is PyTorch's core abstraction
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()

        # What: Conv layer 1 — input 3-channel RGB, output 32 feature maps, 3×3 kernel, padding=1
        #
        # Param in_channels=3
        # Why 3? → RGB colour images have red/green/blue channels
        #   Why not convert to greyscale (1 channel)? → Colour helps distinguish cats from dogs (orange cats / black dogs)
        #   🪨 Irreducible: images are physically 3-channel representations
        #
        # Param kernel_size=3
        # Why 3×3? → VGGNet proved: two 3×3 = one 5×5 receptive field, but with 44% fewer parameters [VGG]
        #   Why do fewer params matter? → 8.5 M params is already a lot — more = more overfitting
        #   Why can 3×3 extract features? → Looks at 9 local pixels; stacking layers progressively widens the view
        #   Why local rather than global? → Image features are locally composed: edges → textures → parts → whole
        #   🪨 Irreducible: images have spatial locality — nearby pixels are strongly correlated (physical world property) [VGG §2.3]
        #
        # Param padding=1
        # Why pad with zeros? → Keeps spatial size unchanged: (128+2×1−3)/1+1 = 128
        #   Why preserve size? → Downsampling is controlled entirely by MaxPool → cleaner architecture design
        #   Why zeros and not something else? → Zeros carry no information and introduce no bias
        #   🪨 Irreducible: make spatial compression controllable — one mechanism (Pool) manages it all
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)

        # What: Conv layers 2 & 3 — channel count doubles each layer: 32→64→128
        # Why increase? → Shallow layers learn simple features (edges) needing few; deep layers learn complex features (eye shapes) needing many
        #   Why do complex features need more filters? → Each channel = one feature detector. Edges have few orientations; fur textures vary enormously
        #   Why double (×2)? → Each Pool halves spatial dims (area ÷ 4); doubling channels compensates → roughly constant compute
        #   🪨 Irreducible: CNN core = layer-by-layer from "high spatial precision + simple semantics" to "low precision + rich semantics"
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)

        # What: 2×2 max-pooling layer — take max in each 2×2 window, halving width and height
        # Why take max? → Max = strongest response to a feature in that region. "There IS an edge" is more informative than "sort of an edge" [MaxPool]
        #   Why reduce pixels? → Without reduction → FC input = 128×128×128 = 2M dims → FC params > 500M → OOM + overfitting
        #   Why exactly 3 pools? → 128 ÷ 2 ÷ 2 ÷ 2 = 16; one more pool → 8, too small — almost no spatial info left
        #   🪨 Irreducible: pooling = lossy compression in information theory — keep most salient features, discard redundancy
        self.pool = nn.MaxPool2d(2, 2)

        # What: FC layer 1 — compress 128×16×16 = 32 768 dims down to 256 dims
        # Why 128×16×16? → After 3 pools: 128 channels × (128÷2÷2÷2 = 16) × 16
        # Why compress to 256? → Dimensionality reduction to extract final classification representation
        #   Why not 64? → Too small — too much information lost, can't distinguish classes
        #   Why not 1024? → Too many params (33 M) — severe overfitting
        #   🪨 Irreducible: dimensionality = trade-off between representational power and overfitting risk
        self.fc1 = nn.Linear(128 * 16 * 16, 256)

        # What: Dropout layer — randomly disable 50% of FC1 neurons during training
        # Why Dropout? → FC1 has 32768×256 ≈ 8.39 M params (99% of total) — most prone to overfitting
        #   Why does random disabling prevent overfitting? → No single neuron can be relied upon → forced to learn redundant representations → more robust
        #   Why on FC but not Conv? → Conv has few params (~93K), rarely overfits; FC has many (~8.39M) — the hot spot
        #   Why 0.5? → Recommended by Hinton's original paper. 0.5 maximises "sub-network" combinations: C(n, n/2) is the largest [Dropout §4, Table 5]
        #   🪨 Irreducible: Dropout = implicit ensemble. Each training step uses a different sub-network; inference uses the average [Dropout §7]
        self.dropout = nn.Dropout(0.5)

        # What: FC layer 2 (output layer) — produces 2 logits: [cat_score, dog_score]
        # Why 2 and not 1? → CrossEntropyLoss requires multi-class format (internal Softmax needs ≥ 2 values)
        #   Why not 1 + Sigmoid? → Also valid — just switch to BCEWithLogitsLoss; equivalent result
        #   Why output logits instead of probabilities? → Numerical stability. Computing Softmax + log separately risks log(0)
        #   🪨 Irreducible: floating-point has precision limits; framework fuses the computation to avoid numerical traps
        self.fc2 = nn.Linear(256, 2)

    def forward(self, x):                          # x: (B, 3, 128, 128)

        # What: Each layer performs Conv (preserve size) → ReLU (add non-linearity) → Pool (halve size)
        #
        # ReLU = max(0, x): negatives become 0, positives unchanged
        # Why need an activation function? → Without one → multiple linear layers = single linear layer → network can only draw straight-line boundaries
        #   Why not Sigmoid? → Sigmoid max derivative = 0.25; across 10 layers: 0.25^10 ≈ 0.000001 → vanishing gradient
        #   Why doesn't ReLU vanish? → For x > 0, derivative = 1; chained product stays 1 → gradient flows freely [ReLU]
        #   🪨 Irreducible: backprop = chain rule multiplication. derivative < 1 chained → 0 (vanish); derivative = 1 chained → 1 (stable) [Backprop]
        x = self.pool(F.relu(self.conv1(x)))       # → (B, 32, 64, 64)
        x = self.pool(F.relu(self.conv2(x)))       # → (B, 64, 32, 32)
        x = self.pool(F.relu(self.conv3(x)))       # → (B, 128, 16, 16)

        # What: Flatten + fully connected + Dropout + output
        x = x.view(x.size(0), -1)                 # Flatten: (B, 32768)
        x = F.relu(self.fc1(x))                    # → (B, 256)
        x = self.dropout(x)                        # drop 50% neurons during training
        x = self.fc2(x)                            # → (B, 2) logits
        return x
        # NOTE: no Softmax here — CrossEntropyLoss includes it internally.
        # Applying Softmax twice would produce incorrect gradients.

# ══ Parameter count ══
# Conv1: 3×32×3×3 + 32         =       896
# Conv2: 32×64×3×3 + 64        =    18 496
# Conv3: 64×128×3×3 + 128      =    73 856
# FC1:   32768×256 + 256        = 8 388 864  ← 99%!
# FC2:   256×2 + 2              =       514
# Total:                         ≈ 8 483 000

def define_model():
    model = SimpleCNN().to(DEVICE)
    return model
'''.strip().split('\n')

CELL3 = r'''# ── Cell 3: Model Training ────────────────────────────────────────────────────
#
# ── Import ──
# torch.optim: Optimiser collection (SGD / Adam / AdamW gradient update algorithms)

import torch.optim as optim

# What: Set training epochs to 10 (pass through all training data 10 times)
# Why multiple passes? → One pass is not enough to learn (like reading a textbook once)
#   Why not 100 passes? → Too many → model memorises training noise (overfitting)
#   Why not 3 passes? → Too few to learn sufficient patterns (underfitting)
#   Why 10? → Looking at output, val_acc is still rising (88%) → still learning but enough for demo
#   🪨 Irreducible: epoch count = balance point between underfitting and overfitting
def train_model(model, train_loader, test_loader, epochs=10):
    # What: Define loss function — cross-entropy loss = −log(predicted probability of the correct class)
    # Why cross-entropy? → Information-theoretically optimal loss for classification [CrossEntropy]
    #   Why not MSE? → When prediction is very wrong, MSE gradient is small (learns slowly);
    #                  CE gradient is large (learns fast) [CrossEntropy]
    #   Why −log? → Information theory: −log(p) = "surprise". p=0.9→loss=0.1; p=0.1→loss=2.3 [KL]
    #   🪨 Irreducible: CE derives from KL divergence — theoretically optimal measure of distribution difference
    criterion = nn.CrossEntropyLoss()

    # What: Define optimiser — Adam with lr=0.001
    # Why Adam? → Maintains per-parameter adaptive learning rates → no manual tuning needed [Adam]
    #   Why not SGD? → SGD shares one lr for all params; some need large steps, others small
    #   Why is Adam adaptive? → Tracks running mean (direction) and variance (step size) of each param's gradient [Adam §2]
    #   Why lr=0.001? → Suggested default from the paper. Too large (0.1) → oscillation; too small (1e-6) → no progress in 10 epochs [Adam §2 "suggested default: α=0.001"]
    #   🪨 Irreducible: gradient descent = finding the lowest point on a high-dim surface. Adam auto-tunes direction and step size using gradient history
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    for epoch in range(1, epochs + 1):

        # ════ Training phase ════
        # What: Call model.train() to enable Dropout
        # Why call train()? → Enables Dropout (random neuron masking) [PyTorch-train/eval]
        #   Why disable during validation? → Validation needs deterministic results → eval() disables it
        #   🪨 Irreducible: training and inference are two fundamentally different forward-pass behaviours
        model.train()

        train_loss, correct, total = 0.0, 0, 0
        for imgs, labels in train_loader:            # 32 images per batch
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)

            # What: ① Zero out old gradients
            # Why zero? → PyTorch accumulates gradients by default; without clearing, old gradients contaminate → wrong update direction
            #   Why designed as accumulation? → Enables gradient accumulation (simulate large batch using multiple small batches when VRAM is limited)
            #   🪨 Irreducible: gradients must precisely reflect the current batch's partial derivatives w.r.t. parameters
            optimizer.zero_grad()

            # What: ② Forward pass → ③ Compute loss
            out = model(imgs)                        # → (32, 2) logits
            loss = criterion(out, labels)

            # What: ④ Backward pass — compute gradient of every parameter using the chain rule
            # Why? → Chain rule propagates from loss backward, computing ∂loss/∂w for every layer [Backprop]
            #   🪨 Irreducible: calculus chain rule: df/dx = df/dy × dy/dx
            loss.backward()

            # What: ⑤ Update weights: w ← w − lr × grad
            optimizer.step()

            # Summary of the 5-step loop:
            # zero_grad → forward → loss → backward → step

            # What: Accumulate batch loss and correct count
            # Why multiply by batch_size? → criterion returns batch-mean loss; multiplying recovers total loss
            #   → Final division by total samples gives epoch average — more accurate than averaging batch means
            #     (last batch may not be full 32)
            train_loss += loss.item() * imgs.size(0)

            # What: argmax(1) picks the index of the larger logit → 0=Cat, 1=Dog
            correct += (out.argmax(1) == labels).sum().item()
            total += labels.size(0)

        train_loss /= total
        train_acc = correct / total

        # ════ Validation phase ════
        # What: Call model.eval() to disable Dropout, entering inference mode
        model.eval()

        val_loss, val_correct, val_total = 0.0, 0, 0

        # What: Disable gradient computation (saves VRAM + speeds up)
        # Why no_grad? → Validation doesn't need backprop; disabling saves VRAM + faster
        #   Why saves VRAM? → No need to store intermediate activations (saved during forward for backward)
        #   🪨 Irreducible: gradient computation requires storing intermediates; no gradients = no storage needed
        with torch.no_grad():
            for imgs, labels in test_loader:
                imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
                out = model(imgs)
                val_loss += criterion(out, labels).item() * imgs.size(0)
                val_correct += (out.argmax(1) == labels).sum().item()
                val_total += labels.size(0)
        val_loss /= val_total
        val_acc = val_correct / val_total

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)
        print(f"Epoch [{epoch:02d}/{epochs}]  train_loss={train_loss:.4f}  train_acc={train_acc:.4f}  val_loss={val_loss:.4f}  val_acc={val_acc:.4f}")

    return history
'''.strip().split('\n')

CELL4 = r'''# ── Cell 4: Model Evaluation ──────────────────────────────────────────────────
#
# What: Evaluate model on test set, produce accuracy and classification report (precision / recall / F1)
# Why a separate function? → Evaluation logic is independent from training — can evaluate any model+data combination anytime
#   🪨 Irreducible: decoupling training and evaluation = more flexible experiment workflow

def evaluate_and_predict(model, test_loader):
    # What: Switch to evaluation mode (disable Dropout)
    # Why eval()? → During training Dropout randomly disables neurons; evaluation needs all neurons for deterministic output [PyTorch-train/eval]
    #   🪨 Irreducible: evaluation must be deterministic — same input must produce same output
    model.eval()
    predictions, actual_labels = [], []

    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs = imgs.to(DEVICE)

            # What: Pick class with highest logit as prediction (0=Cat, 1=Dog)
            # Why argmax? → The logit with the larger value = the class the model is most confident about
            #   🪨 Irreducible: classification = pick the class with the highest probability
            preds = model(imgs).argmax(1)

            # What: Move GPU tensor back to CPU and convert to Python list
            # Why .cpu()? → sklearn is a pure CPU library — cannot use GPU tensors directly
            # Why .tolist()? → sklearn needs Python lists, not Tensors
            #   🪨 Irreducible: data format compatibility between different libraries is mandatory
            predictions.extend(preds.cpu().tolist())
            actual_labels.extend(labels.tolist())

    accuracy = sum(p == a for p, a in zip(predictions, actual_labels)) / len(actual_labels)
    print(f"Accuracy: {accuracy:.4f}")

    # What: Print sklearn classification report (per-class precision / recall / F1)
    # Why classification_report instead of just accuracy?
    #   → Accuracy only tells you "overall correctness", hides per-class performance
    #   Why need per-class metrics? → If all 1000 cats misclassified as dogs but all dogs correct → accuracy=50% yet Cat recall=0%
    #   🪨 Irreducible: a single metric hides performance differences between classes
    # Precision = TP/(TP+FP): "of those predicted Cat, how many are really Cat?"
    # Recall    = TP/(TP+FN): "of all real cats, how many were found?"
    # F1        = harmonic mean of Precision & Recall
    from sklearn.metrics import classification_report
    print(classification_report(actual_labels, predictions, target_names=['Cat', 'Dog']))

    return accuracy, predictions, actual_labels
'''.strip().split('\n')

CELL5 = r'''# ── Cell 5: Main Pipeline ─────────────────────────────────────────────────────
#
# What: 4-step pipeline — load data → create model → train → evaluate
# Modular design: swap model by changing SimpleCNN(), swap data by changing the path
train_loader, test_loader = load_dataset(str(DATASET_PATH))
model = SimpleCNN().to(DEVICE)
train_model(model, train_loader, test_loader, epochs=10)
accuracy, predictions, actual_labels = evaluate_and_predict(model, test_loader)
'''.strip().split('\n')

# ── Map cell index (code cells only) to new source ──
code_cells = [(i, c) for i, c in enumerate(nb["cells"]) if c["cell_type"] == "code"]
new_sources = [CELL0, CELL1, CELL2, CELL3, CELL4, CELL5]

for (idx, cell), new_src in zip(code_cells, new_sources):
    cell["source"] = [line + "\n" for line in new_src[:-1]] + [new_src[-1]]
    cell["outputs"] = []  # clear old outputs
    print(f"✅ Rewrote code cell {idx} ({len(new_src)} lines)")

NB.write_text(json.dumps(nb, indent=1, ensure_ascii=False), "utf-8")
print(f"\n✅ All {len(new_sources)} code cells updated in {NB.name}")
