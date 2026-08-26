(function () { "use strict";
  let initialized = false;
  async function render(container) { const blocks = container.querySelectorAll("pre code.language-mermaid"); if (!blocks.length || !window.mermaid) return; if (!initialized) { mermaid.initialize({ startOnLoad: false, theme: "dark", securityLevel: "strict" }); initialized = true; } for (const block of blocks) { const pre = block.parentElement, holder = document.createElement("div"); holder.className = "mermaid-diagram"; try { const result = await mermaid.render(`rtg-mermaid-${crypto.randomUUID()}`, block.textContent); holder.innerHTML = result.svg; pre.replaceWith(holder); } catch (error) { holder.classList.add("mermaid-error"); holder.textContent = `Unable to render Mermaid diagram: ${error.message}`; pre.replaceWith(holder); } } }
  window.RtGMermaid = { render };
}());
