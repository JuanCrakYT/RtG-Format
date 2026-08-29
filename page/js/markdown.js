(function () {
  "use strict";

  const cleanHtml = DOMPurify.sanitize(marked.parse(markdown), {
    ADD_TAGS: ["script"],
    ADD_ATTR: ["target"],
    FORBID_CONTENTS: []
  });
  
  const container = document.createElement("div");
  container.innerHTML = cleanHtml;
  
  // Convert HTML code blocks containing <script> into executable scripts.
  container.querySelectorAll("pre > code.language-html").forEach((codeBlock) => {
    const source = codeBlock.textContent;
  
    if (!/<script\b[\s\S]*?<\/script>/i.test(source)) {
      return;
    }
  
    const fragment = document.createRange().createContextualFragment(source);
  
    fragment.querySelectorAll("script").forEach((oldScript) => {
      const newScript = document.createElement("script");
    
      for (const attribute of oldScript.attributes) {
        newScript.setAttribute(attribute.name, attribute.value);
      }
    
      newScript.textContent = oldScript.textContent;
      oldScript.replaceWith(newScript);
    });
  
    const pre = codeBlock.parentElement;
    pre.replaceWith(fragment);
  });
  
  container.querySelectorAll("script").forEach((oldScript) => {
    const newScript = document.createElement("script");
  
    for (const attribute of oldScript.attributes) {
      newScript.setAttribute(attribute.name, attribute.value);
    }
  
    newScript.textContent = oldScript.textContent;
    oldScript.replaceWith(newScript);
  });
  
  return container.innerHTML;

  window.RtGMarkdown = { render };
}());