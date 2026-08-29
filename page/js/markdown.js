(function () {
  "use strict";

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

      // Repository directories → GitHub tree URL
      if (!/\.[^/]+$/.test(path) || path.endsWith("/")) {
        const treePath = path.replace(/\/+$/, "");

        return `<a href="https://github.com/${window.RtG.REPOSITORY}/tree/${window.RtG.BRANCH}/${treePath}"${
          title ? ` title="${window.RtG.escapeHtml(title)}"` : ""
        } target="_blank" rel="noopener noreferrer">${label}</a>`;
      }

      // Repository files → raw URL
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

    marked.setOptions({
      gfm: true,
      breaks: false,
      renderer
    });

    return DOMPurify.sanitize(marked.parse(markdown), {
      ADD_ATTR: ["target"]
    });
  }

  window.RtGMarkdown = { render };
}());