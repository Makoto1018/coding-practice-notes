(function () {
  "use strict";

  const DIFFICULTIES = ["Easy", "Medium", "Hard"];
  const state = { difficulty: "All", tag: "All" };
  let data = null;

  function el(tag, attrs, children) {
    const node = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([key, value]) => {
      if (key === "class") node.className = value;
      else if (key === "text") node.textContent = value;
      else node.setAttribute(key, value);
    });
    (children || []).forEach((child) => node.appendChild(child));
    return node;
  }

  function renderStats() {
    const box = document.getElementById("stats");
    box.replaceChildren(el("span", { class: "stat", text: `共 ${data.problems.length} 題` }));
    DIFFICULTIES.forEach((d) => {
      const n = data.problems.filter((p) => p.difficulty === d).length;
      box.appendChild(el("span", { class: `stat badge ${d.toLowerCase()}`, text: `${d} ${n}` }));
    });
  }

  function renderChips(containerId, values, key) {
    const box = document.getElementById(containerId);
    box.replaceChildren();
    ["All", ...values].forEach((value) => {
      const active = state[key] === value;
      const button = el("button", {
        type: "button",
        class: active ? "chip active" : "chip",
        "aria-pressed": String(active),
        text: value === "All" ? "全部" : value,
      });
      button.addEventListener("click", () => {
        state[key] = value;
        render();
      });
      box.appendChild(button);
    });
  }

  function matches(p) {
    return (state.difficulty === "All" || p.difficulty === state.difficulty) &&
      (state.tag === "All" || p.tags.includes(state.tag));
  }

  function problemItem(p) {
    const link = el("a", { class: "problem-link", href: `problem.html?id=${encodeURIComponent(p.id)}` }, [
      el("span", { class: "problem-no", text: `${Number(p.id)}.` }),
      el("span", { class: "problem-title", text: p.title }),
    ]);
    const meta = el("span", { class: "problem-meta" }, [
      el("span", { class: `badge ${p.difficulty.toLowerCase()}`, text: p.difficulty }),
      ...p.tags.map((t) => el("span", { class: "tag", text: t })),
    ]);
    return el("li", { class: "problem-item" }, [link, meta]);
  }

  function renderChapters() {
    const box = document.getElementById("chapters");
    box.replaceChildren();
    data.chapters.forEach((chapter) => {
      const list = data.problems
        .filter((p) => p.chapter === chapter.id && matches(p))
        .sort((a, b) => a.order - b.order);
      if (list.length === 0) return;
      box.appendChild(el("section", { class: "card chapter" }, [
        el("h2", { text: `${chapter.name}（${list.length}）` }),
        el("ul", { class: "problem-list" }, list.map(problemItem)),
      ]));
    });
    if (!box.hasChildNodes()) {
      box.appendChild(el("p", { class: "empty", text: "沒有符合條件的題目。" }));
    }
  }

  function render() {
    renderStats();
    renderChips("difficulty-filter", DIFFICULTIES, "difficulty");
    const usedTags = data.tags.filter((t) => data.problems.some((p) => p.tags.includes(t)));
    renderChips("tag-filter", usedTags, "tag");
    renderChapters();
  }

  fetch("problems.json")
    .then((res) => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then((json) => {
      data = json;
      render();
    })
    .catch((err) => {
      document.getElementById("chapters").replaceChildren(
        el("p", { class: "error", text: `題目清單讀取失敗：${err.message}` })
      );
    });
})();
