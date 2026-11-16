/**
 * PetVision AI - Client-Side Application Logic
 * Implements image upload, drag-and-drop, camera capture,
 * API communication, and dynamic results visualization.
 */

// State Management
const state = {
  selectedFile: null,      // File object or Blob
  selectedFileName: "",
  selectedFileSize: 0,
  isAnalyzing: false,
  selectedModel: "efficientnet_b0",
  cameraStream: null
};

// DOM Elements
const elements = {
  // Model Select
  modelSelect: document.getElementById("modelSelect"),
  
  // Dropzone & Inputs
  dropzoneContainer: document.getElementById("dropzoneContainer"),
  fileInput: document.getElementById("fileInput"),
  btnBrowseFile: document.getElementById("btnBrowseFile"),
  btnCamera: document.getElementById("btnCamera"),
  
  // Preview
  previewContainer: document.getElementById("previewContainer"),
  previewImage: document.getElementById("previewImage"),
  previewFileName: document.getElementById("previewFileName"),
  previewFileSize: document.getElementById("previewFileSize"),
  btnRemoveImage: document.getElementById("btnRemoveImage"),
  btnChangeImage: document.getElementById("btnChangeImage"),
  btnAnalyze: document.getElementById("btnAnalyze"),
  scanningOverlay: document.getElementById("scanningOverlay"),
  
  // Results
  emptyResultState: document.getElementById("emptyResultState"),
  activeResultState: document.getElementById("activeResultState"),
  unsupportedWarning: document.getElementById("unsupportedWarning"),
  unsupportedWarningText: document.getElementById("unsupportedWarningText"),
  
  resultEmoji: document.getElementById("resultEmoji"),
  resultSpeciesName: document.getElementById("resultSpeciesName"),
  resultScientificName: document.getElementById("resultScientificName"),
  resultConfidenceVal: document.getElementById("resultConfidenceVal"),
  confidenceLevelTag: document.getElementById("confidenceLevelTag"),
  resultInferenceTime: document.getElementById("resultInferenceTime"),
  resultModelName: document.getElementById("resultModelName"),
  
  // Diagnostics
  diagRawLabel: document.getElementById("diagRawLabel"),
  diagRawConf: document.getElementById("diagRawConf"),
  diagResolution: document.getElementById("diagResolution"),
  diagDevice: document.getElementById("diagDevice"),
  diagDensity: document.getElementById("diagDensity"),
  
  // Camera Modal
  cameraModal: document.getElementById("cameraModal"),
  cameraVideo: document.getElementById("cameraVideo"),
  cameraCanvas: document.getElementById("cameraCanvas"),
  btnCloseCamera: document.getElementById("btnCloseCamera"),
  btnCancelCamera: document.getElementById("btnCancelCamera"),
  btnSnapPhoto: document.getElementById("btnSnapPhoto"),
  
  // Toast
  toastContainer: document.getElementById("toastContainer")
};

// Initialize App
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners();
});

// Setup All Event Listeners
function setupEventListeners() {
  // Model Switcher
  elements.modelSelect.addEventListener("change", (e) => {
    state.selectedModel = e.target.value;
    showToast(`Switched classification model to: ${e.target.options[e.target.selectedIndex].text}`, "info");
    // If an image is already in preview and was analyzed, prompt or re-analyze
    if (state.selectedFile && !elements.activeResultState.classList.contains("hidden")) {
      analyzeImage();
    }
  });

  // Browse Button
  elements.btnBrowseFile.addEventListener("click", () => {
    elements.fileInput.click();
  });

  // Dropzone Click
  elements.dropzoneContainer.addEventListener("click", (e) => {
    if (e.target !== elements.btnBrowseFile && e.target !== elements.btnCamera && !elements.btnBrowseFile.contains(e.target) && !elements.btnCamera.contains(e.target)) {
      elements.fileInput.click();
    }
  });

  // File Input Change
  elements.fileInput.addEventListener("change", handleFileInputChange);

  // Drag and Drop
  ["dragenter", "dragover"].forEach(eventName => {
    elements.dropzoneContainer.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      elements.dropzoneContainer.classList.add("drag-over");
    });
  });

  ["dragleave", "drop"].forEach(eventName => {
    elements.dropzoneContainer.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      elements.dropzoneContainer.classList.remove("drag-over");
    });
  });

  elements.dropzoneContainer.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files && files.length > 0) {
      handleFileSelected(files[0]);
    }
  });

  // Remove / Change Image
  elements.btnRemoveImage.addEventListener("click", resetUpload);
  elements.btnChangeImage.addEventListener("click", () => elements.fileInput.click());

  // Analyze Button
  elements.btnAnalyze.addEventListener("click", analyzeImage);

  // Camera Modal Events
  elements.btnCamera.addEventListener("click", openCamera);
  elements.btnCloseCamera.addEventListener("click", closeCamera);
  elements.btnCancelCamera.addEventListener("click", closeCamera);
  elements.btnSnapPhoto.addEventListener("click", snapPhoto);
}

// Handle File Input Change
function handleFileInputChange(e) {
  const file = e.target.files[0];
  if (file) {
    handleFileSelected(file);
  }
}

// Handle Selected File
function handleFileSelected(file) {
  if (!file.type.startsWith("image/")) {
    showToast("Please select a valid image file (JPEG, PNG, WEBP).", "error");
    return;
  }

  if (file.size > 15 * 1024 * 1024) {
    showToast("Image size exceeds 15MB limit. Please choose a smaller image.", "error");
    return;
  }

  state.selectedFile = file;
  state.selectedFileName = file.name;
  state.selectedFileSize = file.size;

  // Show in preview
  const reader = new FileReader();
  reader.onload = (e) => {
    showPreview(e.target.result, file.name, formatBytes(file.size));
  };
  reader.readAsDataURL(file);
}

// Show Preview View
function showPreview(imageSrc, name, sizeStr) {
  elements.previewImage.src = imageSrc;
  elements.previewFileName.textContent = name;
  elements.previewFileSize.textContent = `(${sizeStr})`;
  
  elements.dropzoneContainer.classList.add("hidden");
  elements.previewContainer.classList.remove("hidden");
}

// Reset Upload View
function resetUpload() {
  state.selectedFile = null;
  state.selectedFileName = "";
  state.selectedFileSize = 0;
  elements.fileInput.value = "";
  elements.previewImage.src = "";

  elements.previewContainer.classList.add("hidden");
  elements.dropzoneContainer.classList.remove("hidden");
  elements.scanningOverlay.classList.add("hidden");

  // Reset Results
  elements.activeResultState.classList.add("hidden");
  elements.emptyResultState.classList.remove("hidden");
}

// Analyze Image via Deep Learning API
async function analyzeImage() {
  if (!state.selectedFile || state.isAnalyzing) return;

  state.isAnalyzing = true;
  elements.btnAnalyze.disabled = true;
  elements.btnAnalyze.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...`;
  elements.scanningOverlay.classList.remove("hidden");

  const formData = new FormData();
  formData.append("file", state.selectedFile, state.selectedFileName);

  try {
    const response = await fetch(`/api/analyze?model=${state.selectedModel}`, {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({ detail: "Classification request failed." }));
      throw new Error(errData.detail || "Server error");
    }

    const result = await response.json();
    renderPredictionResults(result);
    showToast(`Identified Species: ${result.predicted_category} (${result.confidence_percentage}%)`, "success");
  } catch (err) {
    console.error("Analysis Error:", err);
    showToast(err.message || "Failed to analyze image.", "error");
  } finally {
    state.isAnalyzing = false;
    elements.btnAnalyze.disabled = false;
    elements.btnAnalyze.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> <span>Analyze Image</span>`;
    elements.scanningOverlay.classList.add("hidden");
  }
}

// Render Results to the UI
function renderPredictionResults(data) {
  // Hide empty state, show results state
  elements.emptyResultState.classList.add("hidden");
  elements.activeResultState.classList.remove("hidden");

  // Handle Unsupported Non-Pet Notice
  if (!data.is_supported_pet) {
    elements.unsupportedWarning.classList.remove("hidden");
    elements.unsupportedWarningText.innerHTML = `
      The AI model detected <strong>"${data.raw_detection.label}"</strong> (${data.raw_detection.confidence}% raw confidence) which is outside the 8 supported pet species.
      Below is the best-effort classification among the supported categories.
    `;
  } else {
    elements.unsupportedWarning.classList.add("hidden");
  }

  // 1. Prediction Identity
  elements.resultEmoji.textContent = data.emoji || "🐾";
  elements.resultSpeciesName.textContent = data.display_name || data.predicted_category;
  elements.resultScientificName.textContent = data.pet_profile.scientific_name || "";

  // 2. Confidence Score
  const conf = data.confidence_percentage;
  elements.resultConfidenceVal.textContent = conf.toFixed(1);
  
  if (conf >= 85) {
    elements.confidenceLevelTag.textContent = "High Confidence";
    elements.confidenceLevelTag.style.background = "rgba(16, 185, 129, 0.15)";
    elements.confidenceLevelTag.style.color = "#34D399";
    elements.confidenceLevelTag.style.borderColor = "rgba(16, 185, 129, 0.3)";
  } else if (conf >= 60) {
    elements.confidenceLevelTag.textContent = "Moderate Confidence";
    elements.confidenceLevelTag.style.background = "rgba(245, 158, 11, 0.15)";
    elements.confidenceLevelTag.style.color = "#FBBF24";
    elements.confidenceLevelTag.style.borderColor = "rgba(245, 158, 11, 0.3)";
  } else {
    elements.confidenceLevelTag.textContent = "Low Confidence";
    elements.confidenceLevelTag.style.background = "rgba(239, 68, 68, 0.15)";
    elements.confidenceLevelTag.style.color = "#F87171";
    elements.confidenceLevelTag.style.borderColor = "rgba(239, 68, 68, 0.3)";
  }

  // Meta
  elements.resultInferenceTime.textContent = `${data.diagnostics.inference_time_ms} ms`;
  elements.resultModelName.textContent = data.diagnostics.model_key === "mobilenet_v3" ? "MobileNet-V3" : "EfficientNet-B0";

  // Diagnostics
  elements.diagRawLabel.textContent = data.raw_detection.label;
  elements.diagRawConf.textContent = `${data.raw_detection.confidence}%`;
  elements.diagResolution.textContent = data.diagnostics.image_resolution;
  elements.diagDevice.textContent = data.diagnostics.device;
  elements.diagDensity.textContent = `${data.diagnostics.total_pet_density}%`;

  // Smooth scroll to results on mobile view
  if (window.innerWidth < 1024) {
    elements.activeResultState.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

// Camera Implementation
async function openCamera() {
  try {
    state.cameraStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment", width: { ideal: 1280 }, height: { ideal: 720 } },
      audio: false
    });
    elements.cameraVideo.srcObject = state.cameraStream;
    elements.cameraModal.classList.remove("hidden");
  } catch (err) {
    console.error("Camera access error:", err);
    showToast("Camera access was denied or is unavailable on this device.", "error");
  }
}

function closeCamera() {
  if (state.cameraStream) {
    state.cameraStream.getTracks().forEach(track => track.stop());
    state.cameraStream = null;
  }
  elements.cameraModal.classList.add("hidden");
}

function snapPhoto() {
  if (!state.cameraStream) return;

  const video = elements.cameraVideo;
  const canvas = elements.cameraCanvas;
  canvas.width = video.videoWidth || 640;
  canvas.height = video.videoHeight || 480;

  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  canvas.toBlob((blob) => {
    closeCamera();
    const file = new File([blob], `camera_pet_${Date.now()}.jpg`, { type: "image/jpeg" });
    handleFileSelected(file);
    showToast("Photo captured successfully!", "success");
  }, "image/jpeg", 0.95);
}

// Utilities
function formatBytes(bytes, decimals = 1) {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
}

function showToast(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  
  let icon = "fa-circle-info";
  if (type === "success") icon = "fa-circle-check";
  if (type === "error") icon = "fa-triangle-exclamation";

  toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
  elements.toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(10px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}
