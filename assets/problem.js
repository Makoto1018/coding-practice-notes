(function () {
  "use strict";

  const AI_PREFIX = "🤖 AI 補充";
  const content = document.getElementById("content");
  const pager = document.getElementById("pager");

  function showError(message) {
    const p = document.createElement("p");
    p.className = "error";
    p.textContent = message;
    const back = document.createElement("a");
    back.href = "index.html";
    back.textContent = "← 回首頁";
    content.replaceChildren(p, back);
    pager.replaceChildren();
    document.title = "找不到題目 | 刷題手札";
  }

  function markAiNotes(root) {
    root.querySelectorAll("blockquote").forEach((bq) => {
      if (bq.textContent.trim().startsWith(AI_PREFIX)) bq.classList.add("ai-note");
    });
  }

  function pagerLink(problem, text, cls) {
    const a = document.createElement("a");
    a.className = `pager-link ${cls}`;
    a.href = `problem.html?id=${encodeURIComponent(problem.id)}`;
    a.textContent = text;
    return a;
  }

  function renderPager(problems, current) {
    const sorted = problems.slice().sort((a, b) => a.order - b.order);
    const i = sorted.findIndex((p) => p.id === current.id);
    const prev = sorted[i - 1];
    const next = sorted[i + 1];
    pager.replaceChildren();
    if (prev) pager.appendChild(pagerLink(prev, `← 上一題：${Number(prev.id)}. ${prev.title}`, "prev"));
    if (next) pager.appendChild(pagerLink(next, `下一題：${Number(next.id)}. ${next.title} →`, "next"));
  }

  async function main() {
    const raw = new URLSearchParams(window.location.search).get("id");
    if (!raw) {
      showError("網址缺少題號，例如 problem.html?id=0704。");
      return;
    }
    const id = /^\d+$/.test(raw) ? raw.padStart(4, "0") : raw;
    try {
      const res = await fetch("problems.json");
      if (!res.ok) throw new Error(`problems.json 回應 ${res.status}`);
      const data = await res.json();
      const problem = data.problems.find((p) => p.id === id);
      if (!problem) {
        showError(`找不到題號 ${raw} 的筆記。`);
        return;
      }
      const mdRes = await fetch(problem.file);
      if (!mdRes.ok) throw new Error(`${problem.file} 回應 ${mdRes.status}`);
      const markdown = await mdRes.text();
      content.innerHTML = marked.parse(markdown);
      content.querySelectorAll("pre code").forEach((block) => hljs.highlightElement(block));
      markAiNotes(content);
      content.querySelectorAll('a[href^="http"]').forEach((a) => {
        a.target = "_blank";
        a.rel = "noopener";
      });
      document.title = `${Number(problem.id)}. ${problem.title} | 刷題手札`;
      renderPager(data.problems, problem);
    } catch (err) {
      showError(`讀取失敗：${err.message}`);
    }
  }

  main();
})();
