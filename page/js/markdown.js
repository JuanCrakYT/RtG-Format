(function () {
  "use strict";

  function isRtGPreviewBlock(text) {
    return (
      /RtGPreview\.render\s*\(/i.test(text) ||
      /cdn\.jsdelivr\.net.*RtG-Preview\/preview\.js/i.test(text) ||
      /RtG-Preview\/preview\.js/i.test(text)
    );
  }

  function createCodeBlock(text, lang, isRtGPreview) {
    const escapedCode = window.RtG.escapeHtml(text);
    const languageClass = lang ? ` language-${lang}` : "";
    const previewAttr = isRtGPreview ? ' data-rtg-preview="true"' : "";
    const codeId = "code-" + Math.random().toString(36).slice(2, 10);

    const toolbar = `
      <div class="code-toolbar"${previewAttr} data-code-id="${codeId}">
        <span class="code-lang">${lang || "code"}</span>
        <div class="code-actions">
          <button class="code-btn copy-btn" type="button" data-code-id="${codeId}" aria-label="Copy code">
            <svg class="icon" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            <span>Copy</span>
          </button>
          ${isRtGPreview ? `
          <button class="code-btn preview-btn" type="button" data-code-id="${codeId}" aria-label="Run preview">
            <svg class="icon" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            <span>Preview</span>
          </button>
          ` : ""}
        </div>
      </div>
    `;

    const codeContent = `<pre><code class="${languageClass.slice(1)}">${escapedCode}</code></pre>`;

    const hiddenTextarea = `<textarea id="${codeId}" class="code-source" hidden>${window.RtG.escapeHtml(text)}</textarea>`;

    return `${toolbar}${codeContent}${hiddenTextarea}`;
  }

  function render(markdown, currentPath) {
    const renderer = new marked.Renderer();

    renderer.link = function ({ href, title, text }) {
      const resolved = window.RtG.resolveRepositoryPath(href, currentPath);
      const label = text || href;

      if (/\.md(?:[?#].*)?$/i.test(resolved)) {
        const [path, fragment = ""] = resolved.split("#");

        return `<a href="#/${encodeURI(path)}${
          fragment ? `#${encodeURIComponent(fragment)}` : ""
        }">${label}</a>`;
      }

      if (/^(?:https?:|mailto:)/i.test(resolved)) {
        return `<a href="${resolved}"${
          title ? ` title="${window.RtG.escapeHtml(title)}"` : ""
        } target="_blank" rel="noopener noreferrer">${label}</a>`;
      }

      const [path, suffix = ""] = resolved.match(/^([^?#]*)(.*)$/).slice(1);

      if (!/\.[^/]+$/.test(path) || path.endsWith("/")) {
        const treePath = path.replace(/\/+$/, "");

        return `<a href="https://github.com/${window.RtG.REPOSITORY}/tree/${window.RtG.BRANCH}/${treePath}"${
          title ? ` title="${window.RtG.escapeHtml(title)}"` : ""
        } target="_blank" rel="noopener noreferrer">${label}</a>`;
      }

      const safeHref = window.RtGGitHub.rawUrl(path) + suffix;

      return `<a href="${safeHref}"${
        title ? ` title="${window.RtG.escapeHtml(title)}"` : ""
      } target="_blank" rel="noopener noreferrer">${label}</a>`;
    };

    renderer.image = function ({ href, title, text }) {
      const resolved = window.RtG.resolveRepositoryPath(href, currentPath);

      const src =
        /^(?:https?:|data:)/i.test(resolved)
          ? resolved
          : window.RtGGitHub.rawUrl(resolved);

      return `<img src="${src}" alt="${window.RtG.escapeHtml(
        text || ""
      )}"${title ? ` title="${window.RtG.escapeHtml(title)}"` : ""} loading="lazy">`;
    };

    renderer.code = function ({ text, lang }) {
      const isRtGPreview = lang && lang.toLowerCase() === "html" && isRtGPreviewBlock(text);
      return createCodeBlock(text, lang, isRtGPreview);
    };

    marked.setOptions({
      gfm: true,
      breaks: false,
      renderer
    });

    const cleanHtml = DOMPurify.sanitize(marked.parse(markdown), {
      ADD_TAGS: ["script", "textarea", "button", "svg", "rect", "path", "polygon"],
      ADD_ATTR: ["target", "data-code-id", "data-rtg-preview", "hidden", "type", "aria-label", "viewBox", "width", "height", "class", "id"]
    });

    return cleanHtml;
  }

  window.RtGMarkdown = { render };
}());
