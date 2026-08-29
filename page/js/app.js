(function () {
  "use strict";

  let requestId = 0;
  const content = document.getElementById("content"),
    sidebar = document.getElementById("sidebar"),
    menuButton = document.getElementById("menu-toggle");

  function closeMenu() {
    sidebar.classList.remove("open");
    menuButton.setAttribute("aria-expanded", "false");
  }

  menuButton.addEventListener("click", () => {
    const open = sidebar.classList.toggle("open");
    menuButton.setAttribute("aria-expanded", String(open));
  });

  async function loadRoute() {
    const id = ++requestId,
      path = window.RtGRouter.getPath();

    window.RtGNavigation.render(path);
    document.getElementById("source-link").href =
      window.RtGGitHub.sourceUrl(path);

    content.innerHTML =
      '<div class="loading" role="status">Loading documentation…</div>';

    closeMenu();

    try {
      const markdown = await window.RtGGitHub.fetchMarkdown(path);

      if (id !== requestId) return;

      content.innerHTML = window.RtGMarkdown.render(markdown, path);

      // Execute scripts from rendered Markdown.
      content.querySelectorAll("script").forEach((oldScript) => {
        const newScript = document.createElement("script");

        for (const attribute of oldScript.attributes) {
          newScript.setAttribute(attribute.name, attribute.value);
        }

        newScript.textContent = oldScript.textContent;
        oldScript.replaceWith(newScript);
      });

      await window.RtGMermaid.render(content);

      const fragment = decodeURIComponent(
        window.location.hash.split("#").slice(2).join("#")
      );

      if (fragment) {
        document.getElementById(fragment)?.scrollIntoView();
      }

      content.focus({ preventScroll: Boolean(fragment) });

      document.title = `${
        content.querySelector("h1")?.textContent || path
      } — RtG Save Format`;
    } catch (error) {
      if (id !== requestId) return;

      content.innerHTML = `<section class="error-panel"><h1>Unable to load documentation</h1><p>${window.RtG.escapeHtml(
        error.message
      )}</p><p><a href="#/README.md">Return to the home page</a></p></section>`;
    }
  }

  window.addEventListener("hashchange", loadRoute);
  loadRoute();
}());