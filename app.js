/* ADI Portfolio — Interactive Logic & Page View Router
   Features:
   - Theme management (Dark / Light with persistence)
   - Animated page transition routing for HOME, WORK, PROJECTS, SKILLS, RESUME, CONTACT
   - View Transition API with CSS keyframe fallback
   - Mobile navigation menu
   - Project details modal dialog
   - Browser history (Back/Forward) integration
*/
(() => {
  "use strict";

  const root = document.documentElement;
  const theme = document.getElementById("theme-toggle");
  const menuButton = document.getElementById("menu-toggle");
  const mobileNav = document.getElementById("mobile-nav");
  const dialog = document.getElementById("project-dialog");
  const dialogTitle = document.getElementById("dialog-title");
  const dialogDescription = document.getElementById("dialog-description");
  const dialogTags = document.getElementById("dialog-tags");
  const dialogMedia = document.getElementById("dialog-media");
  const dialogActions = document.getElementById("dialog-actions");
  const storageKey = "adi-portfolio-theme";

  // =========================================================================
  // Theme Toggle (Dark / Light)
  // =========================================================================

  function readTheme() {
    try {
      const value = localStorage.getItem(storageKey);
      if (value === "light" || value === "dark") return value;
    } catch (_) { /* Storage can be disabled for local files. */ }
    return "dark";
  }

  function setTheme(value, persist = false) {
    const dark = value === "dark";
    root.classList.toggle("dark", dark);
    root.classList.toggle("light", !dark);
    root.style.colorScheme = value;
    theme?.setAttribute("aria-pressed", String(dark));
    theme?.setAttribute("title", dark ? "Switch to light theme" : "Switch to dark theme");
    if (persist) {
      try { localStorage.setItem(storageKey, value); } catch (_) { /* ignore */ }
    }
  }

  setTheme(readTheme());
  theme?.addEventListener("click", () => {
    setTheme(root.classList.contains("dark") ? "light" : "dark", true);
  });

  // =========================================================================
  // Mobile Navigation
  // =========================================================================

  function toggleMenu(open) {
    if (!menuButton || !mobileNav) return;
    mobileNav.hidden = !open;
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.setAttribute("aria-label", open ? "Close navigation menu" : "Open navigation menu");
  }

  menuButton?.addEventListener("click", () => toggleMenu(mobileNav.hidden));
  mobileNav?.addEventListener("click", event => {
    if (event.target.closest("a")) toggleMenu(false);
  });
  document.addEventListener("pointerdown", event => {
    if (!mobileNav?.hidden && !event.target.closest("#site-header")) toggleMenu(false);
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") toggleMenu(false);
  });
  window.matchMedia("(min-width: 640px)").addEventListener?.("change", event => {
    if (event.matches) toggleMenu(false);
  });

  // =========================================================================
  // Project & Certificate Details Dialog Modal
  // =========================================================================

  // Regular Project Details modal
  for (const button of document.querySelectorAll(".details-trigger")) {
    button.addEventListener("click", () => {
      if (!dialog?.showModal) return;
      const card = button.closest(".group");
      if (!card) return;
      if (dialogMedia) dialogMedia.replaceChildren();
      if (dialogActions) dialogActions.replaceChildren();
      
      const title = card.querySelector("h2")?.textContent.trim() || "Project";
      dialogTitle.textContent = title;

      // Check if project has custom modal image or poster
      const modalImgSrc = card.getAttribute("data-modal-image") || card.querySelector("img")?.getAttribute("src");
      if (dialogMedia && modalImgSrc) {
        const img = document.createElement("img");
        img.src = modalImgSrc;
        img.alt = title;
        dialogMedia.appendChild(img);
      }

      // Check if project has rich custom modal content
      const richContent = card.querySelector(".project-modal-content");
      if (richContent && dialogDescription) {
        dialogDescription.replaceChildren();
        const clone = richContent.cloneNode(true);
        clone.classList.remove("hidden");
        dialogDescription.appendChild(clone);
      } else if (dialogDescription) {
        dialogDescription.textContent = [...card.querySelectorAll("p")]
          .map(p => p.textContent.trim()).filter(Boolean).join("\n\n");
        dialogDescription.style.whiteSpace = "pre-line";
      }

      // Populate tags
      dialogTags.replaceChildren();
      const pills = card.querySelector(".flex.flex-wrap.gap-2") || card.querySelector(".flex.flex-wrap.gap-1\\.5");
      for (const tag of pills?.querySelectorAll("span") || []) {
        const chip = document.createElement("span");
        chip.textContent = tag.textContent.trim();
        dialogTags.append(chip);
      }

      // Actions
      if (dialogActions) {
        dialogActions.replaceChildren();
        if (title.toLowerCase().includes("smartpoint")) {
          const posterBtn = document.createElement("a");
          posterBtn.href = "assets/images/smartpoint/smartpoint-glasses-poster.webp";
          posterBtn.target = "_blank";
          posterBtn.rel = "noopener noreferrer";
          posterBtn.className = "bg-primary text-primary-foreground hover:bg-primary/90 group relative inline-flex h-9 items-center gap-2 overflow-hidden rounded-lg px-4 text-xs font-semibold shadow-xs transition-all duration-200 hover:scale-[1.02]";
          posterBtn.innerHTML = `<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg><span>Open Full Academic Poster</span>`;

          const hardwareImgBtn = document.createElement("a");
          hardwareImgBtn.href = "assets/images/smartpoint-glasses-card.webp";
          hardwareImgBtn.target = "_blank";
          hardwareImgBtn.rel = "noopener noreferrer";
          hardwareImgBtn.className = "border-border hover:border-foreground/20 bg-card hover:bg-accent relative inline-flex h-9 items-center gap-2 overflow-hidden rounded-lg border px-4 text-xs font-semibold shadow-xs transition-all duration-200 hover:scale-[1.02]";
          hardwareImgBtn.innerHTML = `<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg><span>View Hardware Image</span>`;

          dialogActions.append(posterBtn, hardwareImgBtn);
        } else if (title.toLowerCase().includes("power supply")) {
          const internalBtn = document.createElement("a");
          internalBtn.href = "assets/images/power-supply/power-supply-internal.webp";
          internalBtn.target = "_blank";
          internalBtn.rel = "noopener noreferrer";
          internalBtn.className = "bg-primary text-primary-foreground hover:bg-primary/90 group relative inline-flex h-9 items-center gap-2 overflow-hidden rounded-lg px-4 text-xs font-semibold shadow-xs transition-all duration-200 hover:scale-[1.02]";
          internalBtn.innerHTML = `<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg><span>View Internal Circuitry</span>`;

          const enclosureBtn = document.createElement("a");
          enclosureBtn.href = "assets/images/power-supply/power-supply-enclosure.webp";
          enclosureBtn.target = "_blank";
          enclosureBtn.rel = "noopener noreferrer";
          enclosureBtn.className = "border-border hover:border-foreground/20 bg-card hover:bg-accent relative inline-flex h-9 items-center gap-2 overflow-hidden rounded-lg border px-4 text-xs font-semibold shadow-xs transition-all duration-200 hover:scale-[1.02]";
          enclosureBtn.innerHTML = `<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg><span>View Front Panel &amp; Dial</span>`;

          dialogActions.append(internalBtn, enclosureBtn);
        } else {
          const posterLink = card.getAttribute("data-modal-image") || card.querySelector("img")?.getAttribute("src");
          if (posterLink) {
            const actionA = document.createElement("a");
            actionA.href = posterLink;
            actionA.target = "_blank";
            actionA.rel = "noopener noreferrer";
            actionA.className = "bg-primary text-primary-foreground hover:bg-primary/90 group relative inline-flex h-9 items-center gap-2 overflow-hidden rounded-lg px-4 text-xs font-semibold shadow-xs transition-all duration-200 hover:scale-[1.02]";
            actionA.innerHTML = `<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg><span>View Project Image</span>`;
            dialogActions.appendChild(actionA);
          }
        }
      }

      dialog.showModal();
    });
  }

  // App & Hardware thumbnail preview handler (CareMotion screens, Power Supply hardware)
  document.addEventListener("click", event => {
    const thumb = event.target.closest(".smartpoint-app-thumb, .powersupply-thumb");
    if (!thumb) return;
    if (!dialog?.showModal) return;
    const img = thumb.querySelector("img");
    if (!img) return;

    if (dialogMedia) {
      dialogMedia.replaceChildren();
      const largeImg = document.createElement("img");
      largeImg.src = img.src;
      largeImg.alt = img.alt || "Hardware Preview";
      dialogMedia.appendChild(largeImg);
    }

    dialogTitle.textContent = thumb.getAttribute("title") || img.alt || "Hardware View";
    if (dialogDescription) {
      dialogDescription.replaceChildren();
      const desc = document.createElement("p");
      desc.className = "text-muted-foreground text-sm leading-relaxed";
      desc.textContent = thumb.getAttribute("data-caption") || "High-resolution hardware and electrical view.";
      dialogDescription.appendChild(desc);
    }

    dialogTags.replaceChildren();
    const isPowerSupply = thumb.classList.contains("powersupply-thumb");
    const tagList = isPowerSupply
      ? ["Power Supply", "220V AC to 12V DC", "Voltage Regulation", "Hardware Design", "Transformer & Rectifier"]
      : ["CareMotion", "ESP32-C3", "Wi-Fi Telemetry", "Assistive IoT", "MAX30102"];

    tagList.forEach(text => {
      const chip = document.createElement("span");
      chip.textContent = text;
      dialogTags.appendChild(chip);
    });

    if (dialogActions) {
      dialogActions.replaceChildren();
      const openFullBtn = document.createElement("a");
      openFullBtn.href = img.src;
      openFullBtn.target = "_blank";
      openFullBtn.rel = "noopener noreferrer";
      openFullBtn.className = "bg-primary text-primary-foreground hover:bg-primary/90 group relative inline-flex h-9 items-center gap-2 overflow-hidden rounded-lg px-4 text-xs font-semibold shadow-xs transition-all duration-200 hover:scale-[1.02]";
      openFullBtn.innerHTML = `<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg><span>Open Full-Resolution Image</span>`;
      dialogActions.appendChild(openFullBtn);
    }
    dialog.showModal();
  });

  // Certificate High-Resolution Preview Modal
  document.addEventListener("click", event => {
    const trigger = event.target.closest(".cert-preview-trigger");
    if (!trigger) return;
    if (!dialog?.showModal) return;

    const card = trigger.closest(".cert-item") || trigger.closest("article");
    if (!card) return;

    const certTitle = card.getAttribute("data-cert-title") || card.querySelector("h3")?.textContent.trim() || "Certificate";
    const certImage = card.getAttribute("data-cert-image") || card.querySelector("img")?.getAttribute("src") || "";
    const certPdf = card.getAttribute("data-cert-pdf") || card.querySelector("a[download]")?.getAttribute("href") || "";
    const certIssuer = card.getAttribute("data-cert-issuer") || "";
    const certDate = card.getAttribute("data-cert-date") || "";

    // Set Media
    if (dialogMedia) {
      dialogMedia.replaceChildren();
      if (certImage) {
        const img = document.createElement("img");
        img.src = certImage;
        img.alt = certTitle;
        dialogMedia.appendChild(img);
      }
    }

    // Set Title
    dialogTitle.textContent = certTitle;

    // Set Description & Transcript
    if (dialogDescription) {
      const transcriptBox = card.querySelector(".cert-transcript-box");
      if (transcriptBox) {
        dialogDescription.replaceChildren();
        const clone = transcriptBox.cloneNode(true);
        dialogDescription.appendChild(clone);
      } else {
        dialogDescription.textContent = [...card.querySelectorAll("p")]
          .map(p => p.textContent.trim()).filter(Boolean).join("\n\n");
      }
    }

    // Set Tags
    if (dialogTags) {
      dialogTags.replaceChildren();
      const tagsContainer = card.querySelector(".flex.flex-wrap.gap-1\\.5") || card.querySelector(".flex.flex-wrap.gap-2");
      for (const tag of tagsContainer?.querySelectorAll("span") || []) {
        const chip = document.createElement("span");
        chip.textContent = tag.textContent.trim();
        dialogTags.append(chip);
      }
    }

    // Set Actions
    if (dialogActions) {
      dialogActions.replaceChildren();
      if (certPdf) {
        const viewLink = document.createElement("a");
        viewLink.href = certPdf;
        viewLink.target = "_blank";
        viewLink.rel = "noopener noreferrer";
        viewLink.className = "border-border hover:border-foreground/20 bg-card hover:bg-accent relative inline-flex h-9 items-center gap-2 overflow-hidden rounded-lg border px-4 text-xs font-semibold shadow-xs transition-all duration-200 hover:scale-[1.02]";
        viewLink.innerHTML = `<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg><span>Open Full PDF</span>`;

        const downloadLink = document.createElement("a");
        downloadLink.href = certPdf;
        downloadLink.download = certPdf.split("/").pop() || "certificate.pdf";
        downloadLink.className = "bg-primary text-primary-foreground hover:bg-primary/90 group relative inline-flex h-9 items-center gap-2 overflow-hidden rounded-lg px-4 text-xs font-semibold shadow-xs transition-all duration-200 hover:scale-[1.02]";
        downloadLink.innerHTML = `<svg class="h-3.5 w-3.5 transition-transform group-hover:translate-y-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg><span>Download PDF</span>`;

        dialogActions.append(viewLink, downloadLink);
      }
    }

    dialog.showModal();
  });

  document.getElementById("dialog-close")?.addEventListener("click", () => dialog?.close());
  dialog?.addEventListener("click", event => { if (event.target === dialog) dialog.close(); });

  // =========================================================================
  // Animated Page Transitions & Router
  // Navigation for HOME, WORK, PROJECTS, SKILLS, CERTIFICATES, RESUME, CONTACT
  // =========================================================================

  const VALID_VIEWS = ["home", "work", "projects", "skills", "certificates", "resume", "contact"];
  const VIEW_ALIASES = {
    "experience": "work",
    "about": "home",
    "intro": "home",
    "education": "home",
    "certs": "certificates",
    "cert": "certificates",
    "credentials": "certificates",
    "seminars": "certificates"
  };

  function normalizeView(hash) {
    const clean = (hash || "").replace(/^#\/?/, "").trim().toLowerCase();
    if (VIEW_ALIASES[clean]) return VIEW_ALIASES[clean];
    if (VALID_VIEWS.includes(clean)) return clean;
    return "home";
  }

  function setActiveView(targetView, updateHistory = true) {
    const viewName = VALID_VIEWS.includes(targetView) ? targetView : "home";
    const targetElement = document.getElementById(`view-${viewName}`);
    if (!targetElement) return;

    const performUpdate = () => {
      // Toggle page view visibility
      const allViews = document.querySelectorAll(".page-view");
      allViews.forEach(view => {
        if (view === targetElement) {
          view.classList.add("active-view");
        } else {
          view.classList.remove("active-view");
        }
      });

      // Update active nav indicators (both desktop and mobile)
      document.querySelectorAll("[data-view]").forEach(link => {
        const linkView = link.getAttribute("data-view");
        if (linkView === viewName) {
          link.classList.add("active-nav-link");
          link.setAttribute("aria-current", "page");
        } else {
          link.classList.remove("active-nav-link");
          link.removeAttribute("aria-current");
        }
      });

      // Smooth scroll back to top of the view
      window.scrollTo({ top: 0, behavior: "smooth" });
    };

    // Use modern View Transition API if supported for extra smooth transitions
    if (typeof document.startViewTransition === "function") {
      document.startViewTransition(() => performUpdate());
    } else {
      performUpdate();
    }

    if (updateHistory) {
      if (window.location.hash !== `#${viewName}`) {
        history.pushState(null, "", `#${viewName}`);
      }
    }

    toggleMenu(false);
  }

  // Intercept navigation link clicks for smooth page transitions
  document.addEventListener("click", event => {
    const anchor = event.target.closest("a");
    if (!anchor) return;

    // Check if it's an explicit data-view link
    const dataView = anchor.getAttribute("data-view");
    if (dataView && VALID_VIEWS.includes(dataView)) {
      event.preventDefault();
      setActiveView(dataView, true);
      return;
    }

    // Check if it's an internal hash anchor
    const href = anchor.getAttribute("href");
    if (href && href.startsWith("#")) {
      const resolvedView = normalizeView(href);
      if (VALID_VIEWS.includes(resolvedView)) {
        event.preventDefault();
        setActiveView(resolvedView, true);
      }
    }
  });

  // Handle browser back and forward navigation
  window.addEventListener("popstate", () => {
    setActiveView(normalizeView(window.location.hash), false);
  });
  window.addEventListener("hashchange", () => {
    setActiveView(normalizeView(window.location.hash), false);
  });

  // Initialize initial page view from URL hash on load
  const initialHash = normalizeView(window.location.hash);
  setActiveView(initialHash, false);

})();
