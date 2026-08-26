(function () { "use strict";
  const { REPOSITORY, BRANCH, normalizePath } = window.RtG, rawBase = `https://raw.githubusercontent.com/${REPOSITORY}/${BRANCH}/`, sourceBase = `https://github.com/${REPOSITORY}/blob/${BRANCH}/`;
  function rawUrl(path) { return rawBase + normalizePath(path); } function sourceUrl(path) { return sourceBase + normalizePath(path); }
  async function fetchMarkdown(path) { const response = await fetch(rawUrl(path), { headers: { Accept: "text/plain" } }); if (!response.ok) throw new Error(response.status === 404 ? "This documentation file was not found." : `GitHub returned ${response.status}.`); return response.text(); }
  window.RtGGitHub = { rawUrl, sourceUrl, fetchMarkdown };
}());
