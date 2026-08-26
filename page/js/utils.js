(function () { "use strict";
  const REPOSITORY = "JuanCrakYT/RtG-Format", BRANCH = "main";
  function normalizePath(path) { const parts = []; for (const part of String(path || "").replace(/\\/g, "/").split("/")) { if (!part || part === ".") continue; if (part === "..") parts.pop(); else parts.push(part); } return parts.join("/"); }
  function directoryOf(path) { const index = path.lastIndexOf("/"); return index === -1 ? "" : path.slice(0, index + 1); }
  function resolveRepositoryPath(target, currentPath) { if (!target || target.startsWith("#") || /^(?:[a-z][a-z0-9+.-]*:|\/\/)/i.test(target)) return target; const [pathname, suffix = ""] = target.match(/^([^?#]*)(.*)$/).slice(1); return normalizePath(pathname.startsWith("/") ? pathname.slice(1) : directoryOf(currentPath) + pathname) + suffix; }
  function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[character]); }
  window.RtG = { REPOSITORY, BRANCH, normalizePath, resolveRepositoryPath, escapeHtml };
}());
