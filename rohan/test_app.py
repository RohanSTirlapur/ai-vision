"""
PetVision AI - Integration and Verification Test Suite
Tests all endpoints, deep learning inference, and 8 animal categories.
"""

import os
import sys

# Ensure torch DLL directory and torchvision stubs
torch_lib = r"C:\Users\Nagarjuna N\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\lib"
if os.path.exists(torch_lib):
    try:
        os.add_dll_directory(torch_lib)
    except Exception:
        pass

import unittest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

class TestPetVisionAI(unittest.TestCase):
    
    def test_01_index_html(self):
        """Test that the front-end page is served correctly."""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("PetVision AI", response.text)
        self.assertIn("Upload Image", response.text)
        self.assertIn("Analyze Image", response.text)
        print("✓ Index HTML served successfully")

    def test_02_categories_endpoint(self):
        """Test that the 8 supported pet animal categories are returned."""
        response = client.get("/api/categories")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["count"], 8)
        names = [c["name"] for c in data["supported_categories"]]
        expected = ["Dog", "Cat", "Rabbit", "Bird", "Hamster", "Guinea Pig", "Fish", "Turtle"]
        for exp in expected:
            self.assertIn(exp, names)
        print("✓ All 8 pet animal categories verified in /api/categories")

    def test_03_models_endpoint(self):
        """Test model descriptions and architectures."""
        response = client.get("/api/models")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        model_ids = [m["id"] for m in data["models"]]
        self.assertIn("efficientnet_b0", model_ids)
        self.assertIn("mobilenet_v3", model_ids)
        print("✓ Model backbones verified in /api/models")

    def test_04_samples_endpoint(self):
        """Test sample images endpoint."""
        response = client.get("/api/samples")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["samples"]), 8)
        print("✓ Sample images list verified in /api/samples")

    def test_05_predict_all_8_species(self):
        """Test end-to-end image classification on all 8 sample images."""
        expected_tests = [
            ("dog.jpg", "Dog"),
            ("cat.jpg", "Cat"),
            ("rabbit.jpg", "Rabbit"),
            ("bird.jpg", "Bird"),
            ("hamster.jpg", "Hamster"),
            ("guinea_pig.jpg", "Guinea Pig"),
            ("fish.jpg", "Fish"),
            ("turtle.jpg", "Turtle"),
        ]

        print("\nTesting deep learning classification across 8 animal categories:")
        for filename, expected_species in expected_tests:
            filepath = os.path.join("static", "samples", filename)
            self.assertTrue(os.path.exists(filepath), f"Missing test file {filepath}")
            
            with open(filepath, "rb") as f:
                response = client.post(
                    "/api/analyze?model=efficientnet_b0",
                    files={"file": (filename, f, "image/jpeg")}
                )
            
            self.assertEqual(response.status_code, 200)
            res = response.json()
            self.assertTrue(res["success"])
            predicted = res["predicted_category"]
            conf = res["confidence_percentage"]
            time_ms = res["diagnostics"]["inference_time_ms"]
            self.assertEqual(predicted, expected_species)
            self.assertGreaterEqual(conf, 50.0)
            print(f"  ✓ {filename:15} -> Predicted: {predicted:12} (Confidence: {conf:5.1f}%, Time: {time_ms}ms)")

    def test_06_mobilenet_v3_prediction(self):
        """Test alternative MobileNet-V3 Small model."""
        filepath = os.path.join("static", "samples", "cat.jpg")
        with open(filepath, "rb") as f:
            response = client.post(
                "/api/analyze?model=mobilenet_v3",
                files={"file": ("cat.jpg", f, "image/jpeg")}
            )
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res["predicted_category"], "Cat")
        print(f"✓ MobileNet-V3 Small successfully predicted Cat ({res['confidence_percentage']}%)")


if __name__ == "__main__":
    unittest.main()
