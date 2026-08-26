(function () { "use strict";
  const DEFAULT_PATH = "README.md";
  function getPath() { const hash = decodeURIComponent(window.location.hash.replace(/^#\/?/, "")); const [path] = hash.split("#"); return window.RtG.normalizePath(path || DEFAULT_PATH) || DEFAULT_PATH; }
  function navigate(path, fragment) { const cleanPath = window.RtG.normalizePath(path) || DEFAULT_PATH; window.location.hash = `/${encodeURI(cleanPath)}${fragment ? `#${encodeURIComponent(fragment)}` : ""}`; }
  window.RtGRouter = { DEFAULT_PATH, getPath, navigate };
}());
