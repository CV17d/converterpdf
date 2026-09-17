/**
 * DocuMorph Suite - Frontend Controller
 * Soporte para 10 herramientas de conversión de documentos
 */
document.addEventListener("DOMContentLoaded", () => {
  // Tool specifications
  const TOOLS = {
    "jpg-to-pdf": {
      name: "JPG a PDF",
      accept: ".jpg,.jpeg,.png,.webp",
      multiple: true,
      inBadge: "JPG",
      outBadge: "PDF",
      dropTitle: "Arrastra tus imágenes JPG o PNG aquí",
      specText: "Imágenes .JPG, .PNG, .WEBP",
      btnText: "Convertir a PDF",
      hasPageRange: false,
      colorClass: "tool-jpg"
    },
    "word-to-pdf": {
      name: "WORD a PDF",
      accept: ".docx,.doc",
      multiple: false,
      inBadge: "DOCX",
      outBadge: "PDF",
      dropTitle: "Arrastra tu documento Word aquí",
      specText: "Documentos .DOCX, .DOC",
      btnText: "Convertir a PDF",
      hasPageRange: false,
      colorClass: "tool-word"
    },
    "ppt-to-pdf": {
      name: "POWERPOINT a PDF",
      accept: ".pptx,.ppt",
      multiple: false,
      inBadge: "PPTX",
      outBadge: "PDF",
      dropTitle: "Arrastra tu presentación PowerPoint aquí",
      specText: "Presentaciones .PPTX, .PPT",
      btnText: "Convertir a PDF",
      hasPageRange: false,
      colorClass: "tool-ppt"
    },
    "excel-to-pdf": {
      name: "EXCEL a PDF",
      accept: ".xlsx,.xls",
      multiple: false,
      inBadge: "XLSX",
      outBadge: "PDF",
      dropTitle: "Arrastra tu hoja de cálculo Excel aquí",
      specText: "Archivos .XLSX, .XLS",
      btnText: "Convertir a PDF",
      hasPageRange: false,
      colorClass: "tool-excel"
    },
    "html-to-pdf": {
      name: "HTML a PDF",
      accept: ".html,.htm",
      multiple: false,
      inBadge: "HTML",
      outBadge: "PDF",
      dropTitle: "Arrastra tu archivo HTML aquí",
      specText: "Archivos .HTML, .HTM",
      btnText: "Convertir a PDF",
      hasPageRange: false,
      colorClass: "tool-html"
    },
    "pdf-to-jpg": {
      name: "PDF a JPG",
      accept: ".pdf",
      multiple: false,
      inBadge: "PDF",
      outBadge: "JPG",
      dropTitle: "Arrastra tu archivo PDF aquí",
      specText: "Archivos .PDF",
      btnText: "Extraer a Imágenes JPG",
      hasPageRange: false,
      colorClass: "tool-jpg-rev"
    },
    "pdf-to-word": {
      name: "PDF a WORD",
      accept: ".pdf",
      multiple: false,
      inBadge: "PDF",
      outBadge: "DOCX",
      dropTitle: "Arrastra tu archivo PDF aquí",
      specText: "Archivos .PDF",
      btnText: "Convertir a Word (.docx)",
      hasPageRange: true,
      colorClass: "tool-word-rev"
    },
    "pdf-to-ppt": {
      name: "PDF a POWERPOINT",
      accept: ".pdf",
      multiple: false,
      inBadge: "PDF",
      outBadge: "PPTX",
      dropTitle: "Arrastra tu archivo PDF aquí",
      specText: "Archivos .PDF",
      btnText: "Convertir a PowerPoint (.pptx)",
      hasPageRange: false,
      colorClass: "tool-ppt-rev"
    },
    "pdf-to-excel": {
      name: "PDF a EXCEL",
      accept: ".pdf",
      multiple: false,
      inBadge: "PDF",
      outBadge: "XLSX",
      dropTitle: "Arrastra tu archivo PDF aquí",
      specText: "Archivos .PDF",
      btnText: "Extraer Tablas a Excel (.xlsx)",
      hasPageRange: false,
      colorClass: "tool-excel-rev"
    },
    "pdf-to-pdfa": {
      name: "PDF a PDF/A",
      accept: ".pdf",
      multiple: false,
      inBadge: "PDF",
      outBadge: "PDF/A",
      dropTitle: "Arrastra tu archivo PDF aquí",
      specText: "Archivos .PDF",
      btnText: "Convertir a Estándar PDF/A",
      hasPageRange: false,
      colorClass: "tool-pdfa"
    }
  };

  // State
  let activeToolId = "pdf-to-word";
  let selectedFiles = [];
  let currentTempId = null;
  let progressInterval = null;
  let historyListItems = [];

  // DOM Elements
  const themeToggleBtn = document.getElementById("themeToggleBtn");
  const sunIcon = document.getElementById("sunIcon");
  const moonIcon = document.getElementById("moonIcon");

  const filterBtns = document.querySelectorAll(".filter-btn");
  const toolCards = document.querySelectorAll(".tool-card");

  const currentToolName = document.getElementById("currentToolName");
  const currentToolExt = document.getElementById("currentToolExt");
  const scrollToGridBtn = document.getElementById("scrollToGridBtn");
  const workspaceSection = document.getElementById("workspaceSection");

  const dropzoneStage = document.getElementById("dropzoneStage");
  const previewStage = document.getElementById("previewStage");
  const processingStage = document.getElementById("processingStage");
  const resultStage = document.getElementById("resultStage");

  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const selectFileBtn = document.getElementById("selectFileBtn");
  const dropTitle = document.getElementById("dropTitle");
  const acceptExtTag = document.getElementById("acceptExtTag");
  const selectBtnText = document.getElementById("selectBtnText");

  const previewBadge = document.getElementById("previewBadge");
  const previewFilename = document.getElementById("previewFilename");
  const previewFileMeta = document.getElementById("previewFileMeta");
  const cancelFileBtn = document.getElementById("cancelFileBtn");
  const pageRangeOptionsBox = document.getElementById("pageRangeOptionsBox");
  const optionAllPages = document.getElementById("optionAllPages");
  const optionCustomPages = document.getElementById("optionCustomPages");
  const customRangeWrapper = document.getElementById("customRangeWrapper");
  const pageRangeInput = document.getElementById("pageRangeInput");
  const startConversionBtn = document.getElementById("startConversionBtn");
  const startBtnText = document.getElementById("startBtnText");

  const iconSwapInput = document.getElementById("iconSwapInput");
  const iconSwapOutput = document.getElementById("iconSwapOutput");
  const processTitle = document.getElementById("processTitle");
  const processStatus = document.getElementById("processStatus");
  const progressBar = document.getElementById("progressBar");
  const stepDots = [
    document.getElementById("step1"),
    document.getElementById("step2"),
    document.getElementById("step3"),
    document.getElementById("step4"),
  ];

  const resultFileBadge = document.getElementById("resultFileBadge");
  const resultFilename = document.getElementById("resultFilename");
  const resultMeta = document.getElementById("resultMeta");
  const downloadBtn = document.getElementById("downloadBtn");
  const downloadBtnText = document.getElementById("downloadBtnText");
  const convertAnotherBtn = document.getElementById("convertAnotherBtn");

  const historySection = document.getElementById("historySection");
  const historyList = document.getElementById("historyList");
  const clearHistoryBtn = document.getElementById("clearHistoryBtn");
  const toastContainer = document.getElementById("toastContainer");

  // ==========================================
  // Theme Toggle
  // ==========================================
  const savedTheme = localStorage.getItem("documorph_theme") || "dark";
  setTheme(savedTheme);

  themeToggleBtn.addEventListener("click", () => {
    const activeTheme = document.documentElement.getAttribute("data-theme");
    setTheme(activeTheme === "dark" ? "light" : "dark");
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
  // Category Filter Tabs
  // ==========================================
  filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      filterBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const filter = btn.dataset.filter;

      toolCards.forEach((card) => {
        if (filter === "all" || card.dataset.category === filter) {
          card.style.display = "flex";
        } else {
          card.style.display = "none";
        }
      });
    });
  });

  // ==========================================
  // Tool Selection & Activation
  // ==========================================
  toolCards.forEach((card) => {
    card.addEventListener("click", () => {
      selectTool(card.dataset.tool, true);
    });
  });

  scrollToGridBtn.addEventListener("click", () => {
    document.getElementById("toolsGrid").scrollIntoView({ behavior: "smooth" });
  });

  function selectTool(toolId, doScroll = false) {
    if (!TOOLS[toolId]) return;
    activeToolId = toolId;
    const spec = TOOLS[toolId];

    // Card highlights
    toolCards.forEach((c) => {
      c.classList.toggle("active-selection", c.dataset.tool === toolId);
    });

    // Update UI specs
    currentToolName.textContent = spec.name;
    currentToolExt.textContent = `Acepta: ${spec.accept} ➔ Genera: ${spec.outBadge}`;
    dropTitle.textContent = spec.dropTitle;
    acceptExtTag.textContent = spec.specText;
    selectBtnText.textContent = spec.multiple ? "Seleccionar Imágenes" : "Seleccionar Archivo";
    fileInput.accept = spec.accept;
    fileInput.multiple = spec.multiple;

    previewBadge.textContent = spec.inBadge;
    startBtnText.textContent = spec.btnText;
    iconSwapInput.textContent = spec.inBadge;
    iconSwapOutput.textContent = spec.outBadge;
    resultFileBadge.textContent = spec.outBadge;
    downloadBtnText.textContent = `Descargar ${spec.outBadge}`;

    if (spec.hasPageRange) {
      pageRangeOptionsBox.classList.remove("hidden");
    } else {
      pageRangeOptionsBox.classList.add("hidden");
    }

    resetWorkflow();

    if (doScroll) {
      workspaceSection.scrollIntoView({ behavior: "smooth" });
    }
  }

  // Initialize with default
  selectTool(activeToolId, false);

  // ==========================================
  // Stages Management
  // ==========================================
  function showStage(stage) {
    [dropzoneStage, previewStage, processingStage, resultStage].forEach((s) => {
      s.classList.remove("active");
      s.classList.add("hidden");
    });
    stage.classList.remove("hidden");
    stage.classList.add("active");
  }

  function resetWorkflow() {
    selectedFiles = [];
    currentTempId = null;
    fileInput.value = "";
    pageRangeInput.value = "";
    optionAllPages.checked = true;
    customRangeWrapper.classList.add("hidden");
    clearInterval(progressInterval);
    showStage(dropzoneStage);
  }

  // ==========================================
  // Drag & Drop Handling
  // ==========================================
  selectFileBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    fileInput.click();
  });

  dropzone.addEventListener("click", () => {
    fileInput.click();
  });

  ["dragenter", "dragover"].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove("dragover");
    });
  });

  dropzone.addEventListener("drop", (e) => {
    const files = Array.from(e.dataTransfer.files || []);
    if (files.length > 0) {
      handleFiles(files);
    }
  });

  fileInput.addEventListener("change", (e) => {
    const files = Array.from(e.target.files || []);
    if (files.length > 0) {
      handleFiles(files);
    }
  });

  function handleFiles(files) {
    const spec = TOOLS[activeToolId];
    const allowedExts = spec.accept.split(",").map((s) => s.trim().toLowerCase());

    const validFiles = files.filter((f) => {
      const ext = "." + f.name.split(".").pop().toLowerCase();
      return allowedExts.includes(ext);
    });

    if (validFiles.length === 0) {
      showToast(`Formato no soportado. Para ${spec.name} debes subir: ${spec.accept}`, "error");
      return;
    }

    selectedFiles = spec.multiple ? validFiles : [validFiles[0]];
    displayPreview(selectedFiles);
  }

  async function displayPreview(files) {
    showStage(previewStage);

    if (files.length === 1) {
      const f = files[0];
      previewFilename.textContent = f.name;
      const mbSize = (f.size / (1024 * 1024)).toFixed(2);
      previewFileMeta.textContent = `${mbSize} MB`;

      // Inspección rápida si es PDF
      if (f.name.toLowerCase().endsWith(".pdf")) {
        previewFileMeta.textContent = `Analizando páginas... • ${mbSize} MB`;
        const formData = new FormData();
        formData.append("file", f);
        try {
          const res = await fetch("/api/info", { method: "POST", body: formData });
          const data = await res.json();
          if (res.ok) {
            currentTempId = data.temp_id;
            previewFileMeta.textContent = `${data.page_count} ${data.page_count === 1 ? 'página' : 'páginas'} • ${data.size_mb} MB`;
          }
        } catch (e) {}
      }
    } else {
      previewFilename.textContent = `${files.length} imágenes seleccionadas`;
      const totalBytes = files.reduce((acc, f) => acc + f.size, 0);
      previewFileMeta.textContent = `${(totalBytes / (1024 * 1024)).toFixed(2)} MB en total`;
    }
  }

  // Range options
  optionAllPages.addEventListener("change", () => customRangeWrapper.classList.add("hidden"));
  optionCustomPages.addEventListener("change", () => {
    customRangeWrapper.classList.remove("hidden");
    pageRangeInput.focus();
  });

  cancelFileBtn.addEventListener("click", resetWorkflow);
  convertAnotherBtn.addEventListener("click", resetWorkflow);

  // ==========================================
  // Conversion Execution
  // ==========================================
  startConversionBtn.addEventListener("click", async () => {
    if (selectedFiles.length === 0 && !currentTempId) {
      showToast("Por favor selecciona un archivo primero.", "error");
      return;
    }

    const spec = TOOLS[activeToolId];
    let pages = "";
    if (spec.hasPageRange && optionCustomPages.checked) {
      pages = pageRangeInput.value.trim();
      if (!pages) {
        showToast("Especifica el rango de páginas (ej. 1-3, 5)", "error");
        pageRangeInput.focus();
        return;
      }
    }

    startAnimation(spec);

    const formData = new FormData();
    formData.append("tool", activeToolId);
    if (pages) formData.append("pages", pages);

    if (currentTempId && selectedFiles.length === 1) {
      formData.append("temp_id", currentTempId);
    } else {
      selectedFiles.forEach((file) => {
        formData.append("file", file);
      });
    }

    try {
      const response = await fetch("/api/convert", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Ocurrió un error en la conversión.");
      }

      finishSuccess(data);
    } catch (err) {
      clearInterval(progressInterval);
      showToast(err.message, "error");
      showStage(previewStage);
    }
  });

  function startAnimation(spec) {
    showStage(processingStage);
    progressBar.style.width = "15%";
    processTitle.textContent = `Convirtiendo con ${spec.name}...`;
    processStatus.textContent = "Preparando archivo y analizando estructura...";

    stepDots.forEach((d) => d.classList.remove("active", "done"));
    stepDots[0].classList.add("active");

    const steps = [
      { p: 35, s: 0, text: "Analizando contenido, elementos y diseño..." },
      { p: 60, s: 1, text: "Ejecutando motor de conversión especializado..." },
      { p: 85, s: 2, text: "Reconstruyendo formatos y optimizando salida..." },
      { p: 95, s: 3, text: "Finalizando empaquetado del archivo..." },
    ];

    let idx = 0;
    progressInterval = setInterval(() => {
      if (idx < steps.length) {
        const item = steps[idx];
        progressBar.style.width = `${item.p}%`;
        processStatus.textContent = item.text;

        stepDots.forEach((d, i) => {
          if (i < item.s) {
            d.classList.add("done");
            d.classList.remove("active");
          } else if (i === item.s) {
            d.classList.add("active");
          }
        });
        idx++;
      }
    }, 1500);
  }

  function finishSuccess(data) {
    clearInterval(progressInterval);
    progressBar.style.width = "100%";
    stepDots.forEach((d) => {
      d.classList.remove("active");
      d.classList.add("done");
    });
    processStatus.textContent = "¡Conversión finalizada con éxito!";

    setTimeout(() => {
      showStage(resultStage);
      resultFilename.textContent = data.original_name;
      resultMeta.textContent = `${data.size_mb} MB • Generado en ${data.elapsed_seconds}s`;
      downloadBtn.href = data.download_url;
      downloadBtn.setAttribute("download", data.original_name);

      addToHistory(data);
      showToast("¡Conversión completada exitosamente!", "success");
    }, 400);
  }

  // ==========================================
  // History Management
  // ==========================================
  function addToHistory(item) {
    historyListItems.unshift(item);
    renderHistory();
  }

  function renderHistory() {
    if (historyListItems.length === 0) {
      historySection.classList.add("hidden");
      return;
    }

    historySection.classList.remove("hidden");
    historyList.innerHTML = "";

    historyListItems.forEach((item) => {
      const div = document.createElement("div");
      div.className = "history-item";
      div.innerHTML = `
        <div class="history-item-left">
          <div class="result-file-badge" style="width:36px;height:36px;font-size:0.7rem;">
            ${escapeHtml(item.original_name.split('.').pop().toUpperCase())}
          </div>
          <div>
            <div class="history-item-name">${escapeHtml(item.original_name)}</div>
            <div class="history-item-meta">${item.size_mb} MB • ${item.elapsed_seconds}s • ${item.tool}</div>
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
    historyListItems = [];
    renderHistory();
  });

  function escapeHtml(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
  }

  // ==========================================
  // Toast
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
    }, 4500);
  }
});
