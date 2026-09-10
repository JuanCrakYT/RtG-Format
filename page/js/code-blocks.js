(function () {
  "use strict";

  function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise((resolve, reject) => {
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.style.position = "fixed";
      textarea.style.left = "-9999px";
      textarea.style.top = "0";
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();
      try {
        document.execCommand("copy");
        resolve();
      } catch (error) {
        reject(error);
      } finally {
        textarea.remove();
      }
    });
  }

  function setButtonCopied(button, originalText) {
    const span = button.querySelector("span");
    const icon = button.querySelector(".icon");
    button.classList.add("copied");
    button.setAttribute("aria-label", "Copied");
    if (span) span.textContent = "Copied!";
    if (icon) {
      icon.innerHTML = '<polyline points="20 6 9 17 4 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>';
    }
    setTimeout(() => {
      button.classList.remove("copied");
      button.setAttribute("aria-label", "Copy code");
      if (span) span.textContent = originalText || "Copy";
      if (icon) {
        icon.innerHTML = '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>';
      }
    }, 2000);
  }

  function getCodeSource(codeId) {
    const textarea = document.getElementById(codeId);
    return textarea ? textarea.value : "";
  }

  function createPreviewIframe(htmlContent) {
    const iframe = document.createElement("iframe");
    iframe.className = "rtg-preview-iframe";
    iframe.sandbox = "allow-scripts allow-same-origin";
    iframe.loading = "lazy";

    const blob = new Blob([htmlContent], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    iframe.src = url;

    iframe.onload = () => {
      URL.revokeObjectURL(url);
    };

    iframe.onerror = () => {
      URL.revokeObjectURL(url);
    };

    return iframe;
  }

  function showPreviewError(container, error) {
    const errorEl = document.createElement("div");
    errorEl.className = "rtg-preview-error";
    errorEl.textContent = "Preview error:\n" + (error.message || String(error));
    container.innerHTML = "";
    container.appendChild(errorEl);
  }

  function togglePreview(codeId, previewBtn) {
    const toolbar = previewBtn.closest(".code-toolbar");
    const isRtGPreview = toolbar?.dataset.rtgPreview === "true";
    const previewContainer = toolbar?.nextElementSibling?.nextElementSibling;

    if (!previewContainer || !previewContainer.classList.contains("rtg-preview-container")) {
      const codeBlock = toolbar?.nextElementSibling;
      if (!codeBlock || codeBlock.tagName !== "PRE") return;

      const container = document.createElement("div");
      container.className = "rtg-preview-container";
      container.dataset.rtgPreview = isRtGPreview ? "true" : "false";
      codeBlock.parentNode.insertBefore(container, codeBlock.nextSibling);

      const htmlContent = getCodeSource(codeId);
      if (!htmlContent) {
        showPreviewError(container, new Error("No source code found"));
        return;
      }

      const iframe = createPreviewIframe(htmlContent);
      container.appendChild(iframe);

      iframe.onerror = () => {
        showPreviewError(container, new Error("Failed to load preview iframe"));
      };

      const span = previewBtn.querySelector("span");
      const icon = previewBtn.querySelector(".icon");
      if (span) span.textContent = "Hide";
      if (icon) {
        icon.innerHTML = '<rect x="6" y="6" width="12" height="12" rx="2" ry="2"/>';
      }
      previewBtn.setAttribute("aria-label", "Hide preview");
      return;
    }

    if (previewContainer.style.display === "none" || previewContainer.hidden) {
      previewContainer.hidden = false;
      previewContainer.style.display = "";
      const span = previewBtn.querySelector("span");
      const icon = previewBtn.querySelector(".icon");
      if (span) span.textContent = "Hide";
      if (icon) {
        icon.innerHTML = '<rect x="6" y="6" width="12" height="12" rx="2" ry="2"/>';
      }
      previewBtn.setAttribute("aria-label", "Hide preview");
    } else {
      previewContainer.hidden = true;
      previewContainer.style.display = "none";
      const span = previewBtn.querySelector("span");
      const icon = previewBtn.querySelector(".icon");
      if (span) span.textContent = "Preview";
      if (icon) {
        icon.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"/>';
      }
      previewBtn.setAttribute("aria-label", "Run preview");
    }
  }

  function initCodeBlocks(content) {
    content.querySelectorAll(".copy-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const codeId = btn.dataset.codeId;
        const code = getCodeSource(codeId);
        if (!code) return;
        try {
          await copyToClipboard(code);
          setButtonCopied(btn, "Copy");
        } catch (error) {
          console.error("Copy failed:", error);
          const span = btn.querySelector("span");
          if (span) {
            const original = span.textContent;
            span.textContent = "Failed";
            setTimeout(() => (span.textContent = original), 1500);
          }
        }
      });
    });

    content.querySelectorAll(".preview-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const codeId = btn.dataset.codeId;
        togglePreview(codeId, btn);
      });
    });
  }

  window.RtGCodeBlocks = { initCodeBlocks };
}());