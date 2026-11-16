# PetVision AI – AI-Powered Pet Animal Recognition Website

**PetVision AI** is a complete, production-grade AI-powered web application that analyzes images of pet animals and accurately identifies which species is present using PyTorch deep learning models (EfficientNet-B0 and MobileNet-V3) with Transfer Learning.

> **Important Scope:** This project focuses strictly on **animal species recognition**, deliberately excluding breed differentiation.

---

## 🐾 Supported Animal Categories

PetVision AI classifies images into these 8 distinct pet categories:

1. 🐕 **Dogs** (`Canis lupus familiaris`)
2. 🐱 **Cats** (`Felis catus`)
3. 🐰 **Rabbits** (`Oryctolagus cuniculus`)
4. 🦜 **Birds** (`Aves` - Parrots, Finches, Canaries, Cockatoos, etc.)
5. 🐹 **Hamsters** (`Cricetinae`)
6. 🐹 **Guinea Pigs** (`Cavia porcellus`)
7. 🐠 **Fish** (`Actinopterygii` - Goldfish, Clownfish, Bettas, etc.)
8. 🐢 **Turtles** (`Testudines` - Terrapins, Box turtles, Sliders, etc.)

---

## 🚀 Key Features

- **Genuine Deep Learning Inference**: Built on PyTorch using compound-scaled **EfficientNet-B0** (5.3M parameters) and mobile-optimized **MobileNet-V3 Small** (2.5M parameters) with ImageNet transfer learning weights.
- **Species-Level Aggregation & Calibration**: Maps and aggregates probability mass across 118 dog synsets, 5 cat synsets, 63 bird synsets, aquatic fish synsets, turtle/tortoise synsets, rabbits, hamsters, and guinea pigs into normalized, calibrated species probabilities.
- **Modern Responsive Web UI**:
  - Drag-and-drop file upload zone.
  - Device file picker & live camera capture support.
  - Real-time image preview with dimensions and file size info.
  - Interactive laser-scanning animation during inference.
  - Clear, prominent prediction display with emoji, confidence percentage gauge, and status badges.
  - Deep learning diagnostics drawer showing raw ImageNet synsets, tensor dimensions, inference latency (ms), and hardware device.
  - Model architecture toggle (EfficientNet-B0 vs. MobileNet-V3).
  - Out-of-distribution non-pet warning if an unsupported object/animal is uploaded.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, FastAPI, Uvicorn, PyTorch (`torch`), Torchvision (`torchvision.models`), Pillow (`PIL`).
- **Frontend**: HTML5, Modern CSS (Glassmorphism, CSS Grid & Flexbox), Vanilla JavaScript (ES6+), FontAwesome 6, Google Fonts (*Plus Jakarta Sans*).

---

## 💻 Running the Application

### 1. Start the Server
```bash
python run.py
```

The web server will start at:
```
http://localhost:8000
```

### 2. Run the Verification Test Suite
```bash
python test_app.py
```
Runs 6 automated unit & integration tests validating all endpoints, model instantiations, and predictions across all 8 animal categories.

---

## 📂 Project Structure

```
rohan/
├── app.py                     # FastAPI application & API endpoints
├── classifier.py              # PyTorch deep learning inference engine
├── pet_data.py                # Knowledge base, care tips & facts for all 8 species
├── run.py                     # Server launcher
├── test_app.py                # Automated test suite
├── static/
│   ├── index.html             # Single-page web application UI
│   ├── css/
│   │   └── style.css          # Glassmorphism styling and responsive layout
│   ├── js/
│   │   └── app.js             # Drag-and-drop, API communication & visualization
│   └── samples/               # 8 high-quality sample pet images for 1-click testing
│       ├── dog.jpg
│       ├── cat.jpg
│       ├── rabbit.jpg
│       ├── bird.jpg
│       ├── hamster.jpg
│       ├── guinea_pig.jpg
│       ├── fish.jpg
│       └── turtle.jpg
└── README.md                  # Project documentation
```
