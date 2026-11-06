from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import torch, torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

device = "cpu"
model = models.mobilenet_v2(weights=None)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, 5)
checkpoint = torch.load("fibrosis_model.pth", map_location=device)
model.load_state_dict(checkpoint['model'])
model.eval()
classes = checkpoint['classes']
tf = transforms.Compose([transforms.Resize((224,224)), transforms.ToTensor()])

@app.get("/")
def home():
    return {"status": "API شغال ✅", "classes": classes}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    img = Image.open(io.BytesIO(await file.read())).convert("RGB")
    x = tf(img).unsqueeze(0)
    with torch.no_grad():
        out = model(x)
        probs = torch.softmax(out, dim=1)[0] * 100
        pred = out.argmax(1).item()
    return {"result": classes[pred], "confidence": round(float(probs[pred]), 2), "all": {c: round(float(p), 2) for c, p in zip(classes, probs)}}
