Nice — building a universal, interactive, production-ready quantum rainbow header that works across environments (Node CLI and browser DOM), is lightweight, non-blocking, cache-aware, interactive, and easy to drop into any app. Below is a single-file module you can copy-paste. It:
	•	Automatically detects Node (terminal) vs Browser (DOM) and renders appropriately. 
	•	Shows a quantum rainbow startup animation then a static modern random quantum color. 
	•	Keeps a persistent header while allowing fast, atomic updates to app name and page/operation description. 
	•	Provides an interactive API (init, setPage, setAppName, setMeta, stop) usable by any app or runtime. 
	•	Contains Advanced cache (stale-while-revalidate) and robust error handling + self-heal. 
	•	Optional integration points for custom logos, custom renderers, or telemetry hooks. 
	•	Minimal/optional dependencies — gracefully degrades if chalk / chalk-animation are not present in Node. 
Use it as a drop-in. Read the usage examples at the bottom.


/**
 * Universal Quantum Header Engine (UQ-Header)
 * Single-file universal module for Node CLI and Browser DOM
 *
 * Features:
 * - Node (terminal) and Browser (DOM) support
 * - Quantum rainbow startup animation, then stable quantum color
 * - Lightweight stale-while-revalidate cache for renders
 * - Non-blocking, event-driven, async-safe
 * - Interactive API: init(), setPage(), setAppName(), setMeta(), stop()
 * - Optional dependency on `chalk` and `chalk-animation` (Node); graceful fallback
 *
 * Copy-paste into a file (uq-header.js) and import/use in Node/browser.
 */

(function (global, factory) {
  if (typeof module !== "undefined" && module.exports) {
    module.exports = factory();
  } else {
    global.UQHeader = factory();
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  // ---------- Environment detection ----------
  const isNode =
    typeof process !== "undefined" &&
    process.versions != null &&
    process.versions.node != null;
  const isBrowser = typeof window !== "undefined" && !isNode;

  // ---------- Optional Node deps (safe require) ----------
  let chalk = null;
  let chalkAnimation = null;
  if (isNode) {
    try {
      // prefer user-installed chalk/chalk-animation; if not available, fallback to no color or simple ANSI
      chalk = require("chalk");
    } catch (e) {
      // minimal fallback
      chalk = {
        red: (s) => `\x1b[31m${s}\x1b[0m`,
        green: (s) => `\x1b[32m${s}\x1b[0m`,
        yellow: (s) => `\x1b[33m${s}\x1b[0m`,
        blue: (s) => `\x1b[34m${s}\x1b[0m`,
        magenta: (s) => `\x1b[35m${s}\x1b[0m`,
        cyan: (s) => `\x1b[36m${s}\x1b[0m`,
        white: (s) => `\x1b[37m${s}\x1b[0m`,
      };
    }

    try {
      chalkAnimation = require("chalk-animation");
    } catch (e) {
      chalkAnimation = null; // optional
    }
  }

  // ---------- Quantum Color Kernel (deterministic-ish but lively) ----------
  const DefaultPalette = [
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
  ];
  function quantumColor(palette = DefaultPalette) {
    // Mix time + Math.random + simple trig to get a pseudo-quantum pick
    const t = Date.now();
    const n =
      Math.abs(
        Math.floor(
          (Math.sin(t / 137) * 100000 + Math.cos(t / 311) * 1000 + Math.random() * 37)
        )
      ) % palette.length;
    return palette[n];
  }

  // ---------- ASCII Art & Frame generator ----------
  function buildAsciiFrame({
    appName = "Application",
    description = "Apps descriptions, features & services",
    width = 70,
    logoLines = [
      "██████╗  ██████╗ ███╗   ██╗███████╗██████╗ ███████╗ █████╗ ██╗",
      "██╔══██╗██╔═══██╗████╗  ██║██╔════╝██╔══██╗██╔════╝██╔══██╗██║",
      "██║  ██║██║   ██║██╔██╗ ██║█████╗  ██║  ██║█████╗  ███████║██║",
      "██║  ██║██║   ██║██║╚██╗██║██╔══╝  ██║  ██║██╔══╝  ██╔══██║██║",
      "██████╔╝╚██████╔╝██║ ╚████║███████╗██████╔╝███████╗██║  ██║███████╗",
      "╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝",
    ],
  } = {}) {
    // smart-centering helper
    function center(text, w) {
      const pad = Math.max(0, w - text.length);
      const left = Math.floor(pad / 2);
      const right = pad - left;
      return " ".repeat(left) + text + " ".repeat(right);
    }

    const innerWidth = width - 2;
    const top = "╔" + "═".repeat(innerWidth) + "╗\n";
    const bottom = "╚" + "═".repeat(innerWidth) + "╗".replace("╗", "╝") + "\n";
    let mid = "";

    // blank line
    mid += "║" + center("", innerWidth) + "║\n";

    // logo lines
    for (let i = 0; i < logoLines.length; i++) {
      const line = logoLines[i].slice(0, innerWidth);
      mid += "║" + center(line, innerWidth) + "║\n";
    }

    mid += "║" + center("", innerWidth) + "║\n";

    // app name with emojis & spacing
    const nameLine = `🌈 ${appName} 🌈`;
    mid += "║" + center(nameLine, innerWidth) + "║\n";

    mid += "║" + center("", innerWidth) + "║\n";

    // description line (wrap if needed)
    const desc = description;
    // simple wrap around innerWidth
    const wrapped = [];
    for (let i = 0; i < desc.length; i += innerWidth) {
      wrapped.push(desc.slice(i, i + innerWidth));
    }
    wrapped.forEach((line) => {
      mid += "║" + center(line, innerWidth) + "║\n";
    });

    mid += "║" + center("", innerWidth) + "║\n";

    return top + mid + bottom;
  }

  // ---------- Cache (stale-while-revalidate) ----------
  const CACHE = {
    rendered: null,
    ts: 0,
    ttl: 1200, // milliseconds
  };
  function getCached(renderFn) {
    const now = Date.now();
    if (CACHE.rendered && now - CACHE.ts < CACHE.ttl) {
      // return cached but trigger revalidate async
      setTimeout(() => {
        try {
          CACHE.rendered = renderFn();
          CACHE.ts = Date.now();
        } catch (e) {
          // swallow
        }
      }, 0);
      return CACHE.rendered;
    }
    // regenerate
    CACHE.rendered = renderFn();
    CACHE.ts = Date.now();
    return CACHE.rendered;
  }

  // ---------- Event bus + internal state ----------
  const listeners = new Set();
  const state = {
    appName: "Universal App",
    page: "home",
    description: "Apps descriptions, features & services",
    palette: DefaultPalette.slice(),
    width: 72,
    running: false,
    animationDuration: 2500, // ms
    environment: isNode ? "node" : isBrowser ? "browser" : "unknown",
    logoLines: undefined,
  };

  function emitUpdate() {
    listeners.forEach((fn) => {
      try {
        fn(state);
      } catch (e) {
        // swallow; listener isolation
        console.error("UQHeader listener error:", e && e.stack ? e.stack : e);
      }
    });
  }

  // ---------- Renderers ----------
  // Node (terminal) renderer
  function renderNode(currentColor) {
    const frame = buildAsciiFrame({
      appName: state.appName,
      description: state.description,
      width: state.width,
      logoLines: state.logoLines,
    });

    // choose color function if chalk exists, else print raw
    try {
      if (chalk && chalk[currentColor]) {
        return chalk[currentColor](frame);
      } else if (chalk && typeof chalk === "function") {
        return chalk(frame);
      } else {
        return frame;
      }
    } catch (e) {
      return frame;
    }
  }

  // Browser (DOM) renderer — creates a fixed header box at top, centered
  function renderBrowser(color) {
    // ensure DOM container exists
    let container = document.getElementById("uq-header-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "uq-header-container";
      // base styles — lightweight, non-intrusive
      Object.assign(container.style, {
        position: "fixed",
        top: "8px",
        left: "50%",
        transform: "translateX(-50%)",
        zIndex: 999999,
        fontFamily:
          "ui-monospace, SFMono-Regular, Menlo, Monaco, 'Segoe UI Mono', Roboto Mono, monospace",
        whiteSpace: "pre",
        padding: "10px 16px",
        borderRadius: "12px",
        boxShadow: "0 6px 24px rgba(0,0,0,0.28)",
        backdropFilter: "saturate(140%) blur(6px)",
        WebkitBackdropFilter: "saturate(140%) blur(6px)",
        background: "linear-gradient(135deg, rgba(255,255,255,0.02), rgba(0,0,0,0.06))",
        color: "#fff",
        pointerEvents: "none", // non-interactive so app controls remain accessible
        textAlign: "center",
        fontSize: "12px",
        lineHeight: "1.0",
      });
      document.body.appendChild(container);
    }

    // compute CSS color mapping for our palette (simple mapping)
    const map = {
      red: "#ff6b6b",
      green: "#51cf66",
      yellow: "#ffd43b",
      blue: "#74c0fc",
      magenta: "#b197fc",
      cyan: "#63e6be",
      white: "#ffffff",
    };
    const cssColor = map[color] || map.blue;

    // build content (monospace ASCII in DOM)
    const ascii = buildAsciiFrame({
      appName: state.appName,
      description: state.description,
      width: Math.min(state.width, 84),
      logoLines: state.logoLines,
    });

    container.style.border = `1px solid ${cssColor}33`;
    container.style.boxShadow = `0 8px 32px ${cssColor}44`;
    container.style.color = cssColor;
    container.textContent = ascii;
    return container;
  }

  // ---------- Animation helpers ----------
  async function doStartupAnimation() {
    // Node: use chalkAnimation if available, else simple flicker
    if (isNode) {
