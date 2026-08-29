const cleanHtml = DOMPurify.sanitize(marked.parse(markdown), {
  ADD_TAGS: ["script"],
  ADD_ATTR: ["target"],
  FORBID_CONTENTS: []
});

const container = document.createElement("div");
container.innerHTML = cleanHtml;

// Convert HTML code blocks containing <script> into
// marked executable-script containers for GitHub Pages.
container.querySelectorAll("pre > code.language-html").forEach((codeBlock) => {

  const source = codeBlock.textContent;

  if (!/<script\b[\s\S]*?<\/script>/i.test(source)) {
    return;
  }

  const wrapper = document.createElement("div");
  wrapper.setAttribute("data-rtg-script", "");

  wrapper.textContent = source;

  codeBlock.parentElement.replaceWith(wrapper);
});

// Keep normal HTML scripts marked for app.js execution.
container.querySelectorAll("script").forEach((script) => {
  script.setAttribute("data-rtg-script", "");
});

return container.innerHTML;