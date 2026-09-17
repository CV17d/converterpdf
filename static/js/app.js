/**
 * DocuMorph PDF to Word Pro - Frontend Controller
 */
document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const themeToggleBtn = document.getElementById("themeToggleBtn");
  const sunIcon = document.getElementById("sunIcon");
  const moonIcon = document.getElementById("moonIcon");

  const dropzoneStage = document.getElementById("dropzoneStage");
  const previewStage = document.getElementById("previewStage");
  const processingStage = document.getElementById("processingStage");
  const resultStage = document.getElementById("resultStage");

  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const selectFileBtn = document.getElementById("selectFileBtn");

  const previewFilename = document.getElementById("previewFilename");
  const previewFileMeta = document.getElementById("previewFileMeta");
  const cancelFileBtn = document.getElementById("cancelFileBtn");

  const optionAllPages = document.getElementById("optionAllPages");
  const optionCustomPages = document.getElementById("optionCustomPages");
  const customRangeWrapper = document.getElementById("customRangeWrapper");
  const pageRangeInput = document.getElementById("pageRangeInput");
  const startConversionBtn = document.getElementById("startConversionBtn");

  const processTitle = document.getElementById("processTitle");
  const processStatus = document.getElementById("processStatus");
  const progressBar = document.getElementById("progressBar");
  const stepDots = [
    document.getElementById("step1"),
    document.getElementById("step2"),
    document.getElementById("step3"),
    document.getElementById("step4"),
  ];

  const resultFilename = document.getElementById("resultFilename");
  const resultMeta = document.getElementById("resultMeta");
  const downloadBtn = document.getElementById("downloadBtn");
  const convertAnotherBtn = document.getElementById("convertAnotherBtn");

  const historySection = document.getElementById("historySection");
  const historyList = document.getElementById("historyList");
  const clearHistoryBtn = document.getElementById("clearHistoryBtn");
  const toastContainer = document.getElementById("toastContainer");

  // State
  let currentFile = null;
  let currentTempId = null;
  let currentMetadata = null;
  let progressInterval = null;
  let conversionHistory = [];

  // ==========================================
  // Theme Management
  // ==========================================
  const savedTheme = localStorage.getItem("documorph_theme") || "dark";
  setTheme(savedTheme);

  themeToggleBtn.addEventListener("click", () => {
    const activeTheme = document.documentElement.getAttribute("data-theme");
    const nextTheme = activeTheme === "dark" ? "light" : "dark";
    setTheme(nextTheme);
  });

  function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("documorph_theme", theme);
    if (theme === "light") {
      sunIcon.classList.remove("hidden");
      moonIcon.classList.add("hidden");
    } else {
      sunIcon.classList.add("hidden");
      moonIcon.classList.remove("hidden");
    }
  }

  // ==========================================
  // Stage Switching
  // ==========================================
  function showStage(stage) {
    [dropzoneStage, previewStage, processingStage, resultStage].forEach((s) => {
      s.classList.remove("active");
      s.classList.add("hidden");
    });
    stage.classList.remove("hidden");
    stage.classList.add("active");
  }

  // ==========================================
  // Drag and Drop & File Selection
  // ==========================================
  selectFileBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    fileInput.click();
  });

  dropzone.addEventListener("click", () => {
    fileInput.click();
  });

  ["dragenter", "dragover"].forEach((eventName) => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove("dragover");
    });
  });

  dropzone.addEventListener("drop", (e) => {
    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleSelectedFile(files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleSelectedFile(e.target.files[0]);
    }
  });

  function handleSelectedFile(file) {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      showToast("Por favor selecciona un archivo con extensión .PDF", "error");
      return;
    }

    if (file.size > 150 * 1024 * 1024) {
      showToast("El archivo supera el límite máximo de 150 MB", "error");
      return;
    }

    currentFile = file;
    inspectAndPreview(file);
  }

  async function inspectAndPreview(file) {
    previewFilename.textContent = file.name;
    const mbSize = (file.size / (1024 * 1024)).toFixed(2);
    previewFileMeta.textContent = `Analizando páginas... • ${mbSize} MB`;
    showStage(previewStage);

    // Enviar a inspección rápida
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/info", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "No se pudo inspeccionar el PDF.");
      }

      if (data.is_encrypted) {
        showToast("El archivo está protegido con contraseña. Desbloquéalo primero.", "error");
        resetConverter();
        return;
      }

      currentTempId = data.temp_id;
      currentMetadata = data;
      previewFileMeta.textContent = `${data.page_count} ${data.page_count === 1 ? 'página' : 'páginas'} • ${data.size_mb} MB`;
    } catch (err) {
      showToast(err.message, "error");
      previewFileMeta.textContent = `${mbSize} MB`;
    }
  }

  // ==========================================
  // Page Range Radio Buttons
  // ==========================================
  optionAllPages.addEventListener("change", () => {
    customRangeWrapper.classList.add("hidden");
  });

  optionCustomPages.addEventListener("change", () => {
    customRangeWrapper.classList.remove("hidden");
    pageRangeInput.focus();
  });

  cancelFileBtn.addEventListener("click", () => {
    resetConverter();
  });

  function resetConverter() {
    currentFile = null;
    currentTempId = null;
    currentMetadata = null;
    fileInput.value = "";
    pageRangeInput.value = "";
    optionAllPages.checked = true;
    customRangeWrapper.classList.add("hidden");
    clearInterval(progressInterval);
    showStage(dropzoneStage);
  }

  // ==========================================
  // Conversion Flow
  // ==========================================
  startConversionBtn.addEventListener("click", async () => {
    if (!currentFile && !currentTempId) {
      showToast("No hay ningún archivo seleccionado.", "error");
      return;
    }

    let pagesValue = "";
    if (optionCustomPages.checked) {
      pagesValue = pageRangeInput.value.trim();
      if (!pagesValue) {
        showToast("Por favor especifica el rango de páginas (ej. 1-3, 5)", "error");
        pageRangeInput.focus();
        return;
      }
    }

    startProcessingAnimation();

    const formData = new FormData();
    if (currentTempId) {
      formData.append("temp_id", currentTempId);
    } else {
      formData.append("file", currentFile);
    }
    if (pagesValue) {
      formData.append("pages", pagesValue);
    }

    try {
      const response = await fetch("/api/convert", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Error al procesar el documento.");
      }

      finishProcessingSuccess(data);
    } catch (err) {
      clearInterval(progressInterval);
      showToast(err.message, "error");
      showStage(previewStage);
    }
  });

  function startProcessingAnimation() {
    showStage(processingStage);
    progressBar.style.width = "15%";
    processTitle.textContent = "Convirtiendo documento...";
    processStatus.textContent = "Iniciando análisis estructural del PDF...";

    stepDots.forEach((d) => d.classList.remove("active", "done"));
    stepDots[0].classList.add("active");

    let progress = 15;
    let step = 0;

    const messages = [
      { p: 35, s: 0, text: "Analizando bloques de texto y tipografía..." },
      { p: 55, s: 1, text: "Extrayendo imágenes y detectando tablas de datos..." },
      { p: 75, s: 2, text: "Reconstruyendo estilos y párrafos en formato Word..." },
      { p: 90, s: 2, text: "Optimizando la disposición y finalizando documento..." },
    ];

    let msgIdx = 0;
    progressInterval = setInterval(() => {
      if (msgIdx < messages.length) {
        const item = messages[msgIdx];
        progress = item.p;
        progressBar.style.width = `${progress}%`;
        processStatus.textContent = item.text;

        stepDots.forEach((d, idx) => {
          if (idx < item.s) {
            d.classList.add("done");
            d.classList.remove("active");
          } else if (idx === item.s) {
            d.classList.add("active");
          }
        });
        msgIdx++;
      }
    }, 1800);
  }

  function finishProcessingSuccess(data) {
    clearInterval(progressInterval);
    progressBar.style.width = "100%";
    stepDots.forEach((d) => {
      d.classList.remove("active");
      d.classList.add("done");
    });
    processStatus.textContent = "¡Completado con éxito!";

    setTimeout(() => {
      showStage(resultStage);
      resultFilename.textContent = data.original_name;
      resultMeta.textContent = `${data.size_mb} MB • Convertido en ${data.elapsed_seconds}s`;
      downloadBtn.href = data.download_url;
      downloadBtn.setAttribute("download", data.original_name);

      // Agregar al historial
      addToHistory(data);

      showToast("¡Documento Word generado exitosamente!", "success");
    }, 450);
  }

  // ==========================================
  // Reset & History
  // ==========================================
  convertAnotherBtn.addEventListener("click", () => {
    resetConverter();
  });

  function addToHistory(item) {
    conversionHistory.unshift(item);
    renderHistory();
  }

  function renderHistory() {
    if (conversionHistory.length === 0) {
      historySection.classList.add("hidden");
      return;
    }

    historySection.classList.remove("hidden");
    historyList.innerHTML = "";

    conversionHistory.forEach((item) => {
      const div = document.createElement("div");
      div.className = "history-item";
      div.innerHTML = `
        <div class="history-item-left">
          <div class="result-file-badge" style="width:36px;height:36px;font-size:0.7rem;">DOCX</div>
          <div>
            <div class="history-item-name">${escapeHtml(item.original_name)}</div>
            <div class="history-item-meta">${item.size_mb} MB • ${item.elapsed_seconds}s</div>
          </div>
        </div>
        <a href="${item.download_url}" download="${escapeHtml(item.original_name)}" class="btn-ghost history-download-btn">
          Descargar
        </a>
      `;
      historyList.appendChild(div);
    });
  }

  clearHistoryBtn.addEventListener("click", () => {
    conversionHistory = [];
    renderHistory();
  });

  function escapeHtml(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
  }

  // ==========================================
  // Toast Notifications
  // ==========================================
  function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;

    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateX(100%)";
      toast.style.transition = "all 0.3s ease";
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }
});
