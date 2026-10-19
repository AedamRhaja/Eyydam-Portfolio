"""Rebuild ADI's page from the saved *original* portfolio DOM.

The downloaded source is kept in scripts/reference-home-snapshot.html.
Output uses the original compiled CSS, its original classes, existing original
images, and ADI's real resume details. No frontend build/network required.
"""
from pathlib import Path
from copy import deepcopy
from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "scripts" / "reference-home-snapshot.html"
PHOTO = "assets/images/05e4bc3e-208c-4542-a0bc-1b6aaf326665.jpg"
RESUME = "assets/AEDAM_RHAJA_MORANCIL_RESUME.pdf"
EMAIL = "rhajaaedam01@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/aedam-rhaja-869ab6214/"
CARD = "group bg-background/80 hover:border-foreground/20 border-border hover:bg-background block overflow-hidden rounded-xl border px-4 py-3 transition-all duration-300"
HEADING = "jsx-67dd5df6263197bb mb-8 text-3xl font-semibold tracking-tight"
SECTION = "transition-all duration-700 ease-out"
CHIP = "bg-secondary/80 border-border/50 hover:border-border flex items-center justify-center rounded-lg border px-3 py-2 text-sm font-medium transition-all duration-200 hover:scale-105 hover:shadow-sm"
TECH_ICONS = {
    "Python": "python.svg",
    "HTML": "html5.svg",
    "C++": "cplusplus.svg",
    "Java": "java.svg",
    "Kotlin": "kotlin.svg",
    "Android Studio": "androidstudio.svg",
}

# Lightweight reusable music widget, using the same bunny imagery as the
# header. Its inline controls require no library or additional decorative art.
BUNNY_RADIO_HTML = """
<section id="bunny-radio" class="bunny-radio" aria-label="Bunny music player">
  <audio id="bunny-audio" src="assets/2Pac - Life Goes on.mp3" preload="metadata" autoplay loop></audio>
  <div class="bunny-radio-top">
    <div class="bunny-radio-cover" aria-hidden="true"><span class="bunny-radio-cover-note">♫</span></div>
    <div class="bunny-radio-copy">
      <span class="bunny-radio-heading">
        <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path d="M11 16C7 10 5 3 8 2c4-1 6 8 7 12M20 16c2-6 5-14 9-12 3 2-2 12-5 16"/>
          <path d="M8 18c1-5 6-7 11-7 8 0 12 5 11 11-1 6-6 9-13 9C10 31 5 26 8 18Z"/>
          <circle cx="23" cy="20" r="1.2" fill="currentColor" stroke="none"/>
        </svg>
        BUNNY RADIO <span aria-hidden="true">·</span> LOOP
      </span>
      <strong class="bunny-radio-song">Life Goes On</strong>
      <span class="bunny-radio-artist">2Pac <span aria-hidden="true">·</span> <span id="bunny-music-status" role="status" aria-live="polite">Loading audio…</span></span>
    </div>
    <button type="button" id="bunny-music-hide" class="bunny-radio-hide" aria-label="Hide music player" title="Hide player (music keeps playing)">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg>
    </button>
  </div>
  <div class="bunny-radio-bottom">
    <button type="button" id="bunny-music-toggle" class="bunny-radio-play" aria-label="Play music" aria-pressed="false">
      <svg class="bunny-icon-play" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.3a1.2 1.2 0 0 1 1.8-1L20 10.9a1.3 1.3 0 0 1 0 2.2L9.8 19.7a1.2 1.2 0 0 1-1.8-1V5.3Z"/></svg>
      <svg class="bunny-icon-pause" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="4" width="4" height="16" rx="1.2"/><rect x="14" y="4" width="4" height="16" rx="1.2"/></svg>
    </button>
    <div class="bunny-radio-progress">
      <label class="sr-only" for="bunny-music-seek">Seek through song</label>
      <input id="bunny-music-seek" type="range" min="0" max="1000" value="0" step="1" disabled aria-label="Seek through song"/>
      <span id="bunny-music-time" class="bunny-radio-time" aria-live="off">0:00 / --:--</span>
    </div>
    <button type="button" id="bunny-music-mute" class="bunny-radio-mute" aria-label="Mute music" aria-pressed="false" title="Mute / unmute">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M4 10v4h4l5 4V6l-5 4H4Z"/><path class="bunny-volume-wave" d="M17 9c2 1.5 2 4.5 0 6M19 6c4 3 4 9 0 12"/><path class="bunny-volume-slash" d="m17 10 5 5m0-5-5 5"/>
      </svg>
    </button>
    <label class="sr-only" for="bunny-music-volume">Music volume</label>
    <input id="bunny-music-volume" type="range" min="0" max="1" value="0.65" step="0.05" aria-label="Music volume" class="bunny-radio-volume"/>
  </div>
</section>
<button id="bunny-music-restore" type="button" class="bunny-music-restore" hidden aria-label="Show bunny music player">
  <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M11 16C7 10 5 3 8 2c4-1 6 8 7 12M20 16c2-6 5-14 9-12 3 2-2 12-5 16"/><path d="M8 18c1-5 6-7 11-7 8 0 12 5 11 11-1 6-6 9-13 9C10 31 5 26 8 18Z"/><circle cx="23" cy="20" r="1.2" fill="currentColor" stroke="none"/></svg>
  <span>Music</span><span id="bunny-music-mini-state" class="bunny-mini-state">♪</span>
</button>
"""


def node(soup, name, text="", cls=None, **attrs):
    element = soup.new_tag(name, attrs=attrs)
    if cls:
        element["class"] = cls.split()
    if text:
        element.string = text
    return element


def titlebar(soup, title):
    bar = node(soup, "div", cls=HEADING)
    word = node(soup, "span", title, "jsx-67dd5df6263197bb word inline-block transition-all duration-500 ease-out")
    word["style"] = "margin-right:0.25em"
    bar.append(word)
    return bar


def basic_section(soup, id_, heading):
    section = node(soup, "div", cls=SECTION, id=id_)
    inner = node(soup, "div", cls="px-4")
    inner.append(titlebar(soup, heading))
    section.append(inner)
    return section, inner


def experience_row(soup, title, employer, dates, details):
    article = node(soup, "article", cls=CARD + " experience-entry")
    line = node(soup, "div", cls="experience-heading flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between")
    left = node(soup, "div", cls="space-y-1")
    left.append(node(soup, "h2", title, "text-foreground text-lg font-semibold tracking-tight sm:text-xl"))
    left.append(node(soup, "p", employer, "text-muted-foreground text-sm font-medium"))
    line.append(left)
    line.append(node(soup, "span", dates, "experience-dates text-muted-foreground shrink-0 text-xs font-medium"))
    article.append(line)
    desc = node(soup, "p", details, "text-muted-foreground mt-3 max-w-3xl text-sm leading-relaxed")
    article.append(desc)
    return article


def main():
    if not SNAPSHOT.exists():
        raise FileNotFoundError(f"Saved original homepage not found: {SNAPSHOT}")
    soup = BeautifulSoup(SNAPSHOT.read_text(encoding="utf-8"), "html.parser")
    parts = [p for p in soup.body.find_all(recursive=False) if p.name == "div" and not p.has_attr("hidden")]
    if len(parts) != 5:
        raise ValueError(f"Original homepage changed: expected five visible blocks, got {len(parts)}")
    backdrop, header, main_block, footer, _bottom_overlay = parts

    main_block.name = "main"
    main_block["id"] = "home"
    main_block.attrs.pop("style", None)
    sections = main_block.select(".space-y-8 > div")
    if len(sections) != 6:
        raise ValueError(f"Expected six original content sections, found {len(sections)}")
    intro, about, projects, old_blog, skills, old_activity = sections
    for part, name in [(intro, "intro"), (about, "about"), (projects, "projects"), (old_blog, "old-blog"), (skills, "skills"), (old_activity, "old-activity")]:
        part["id"] = name
        part["class"] = [c for c in part.get("class", []) if c not in ("translate-y-8", "opacity-0")]
    for word in main_block.select(".word"):
        word["class"] = [c for c in word.get("class", []) if c not in ("translate-y-4", "opacity-0")]

    # Preserve the exact original image placement and component classes.
    # Replace its images with ADI-owned files (including both themed banners).
    images = {"banner.png": "banner.png", "profile.png": None, "rush.png": "rush.png",
              "oto.png": "oto.png", "leerio.png": "leerio.png", "kestro.png": "kestro.png",
              "typescript.png": "typescript.png", "mongo.png": "mongo.png"}
    for image in main_block.select("img"):
        src = image.get("src", "")
        chosen = next((name for name in images if name in src), None)
        if chosen is None:
            raise ValueError(f"Unexpected original image: {src}")
        image["src"] = PHOTO if chosen == "profile.png" else "assets/images/" + images[chosen]
        image["loading"] = "eager"
        for attr in ("srcset", "sizes", "data-nimg"):
            image.attrs.pop(attr, None)
        if chosen == "profile.png":
            image["alt"] = "Aedam Rhaja F. Morancil — ADI"
    hero_img = intro.find("img", attrs={"alt": "hero banner"})
    if hero_img is None:
        raise ValueError("Original header banner markup not found")
    hero_img["src"] = "assets/images/b67979daf081bb08eb5249c0f6e1d1c5.jpg"
    hero_img["alt"] = "Rabbit cycling in a bright meadow of flowers"
    hero_img["class"] = hero_img.get("class", []) + ["adi-hero-light"]
    dark_img = deepcopy(hero_img)
    dark_img["src"] = "assets/images/5f365b46bbe27ebb9c77b68611bf5dc7.jpg"
    dark_img["alt"] = "Floating rabbit with balloons beneath a blue night sky"
    dark_img["class"] = [c for c in dark_img.get("class", []) if c != "adi-hero-light"] + ["adi-hero-dark"]
    hero_img.insert_after(dark_img)

    banner_quote = intro.select_one(".h-52 p")
    if banner_quote:
        banner_quote.string = "Curious enough to learn. Committed enough to finish."
    greeting = intro.find(string=lambda s: s and "Mayank" in s)
    if greeting:
        greeting.replace_with("Aedam Rhaja")
    descriptor = intro.select_one(".jsx-67dd5df6263197bb.text-2xl")
    if descriptor:
        descriptor.clear()
        for word in ("Computer", "Engineering", "Student"):
            span = node(soup, "span", word, "jsx-67dd5df6263197bb word inline-block transition-all duration-500 ease-out")
            span["style"] = "margin-right:0.25em"
            descriptor.append(span)

    # Use the identical old layout for the about/status row and buttons.
    for old_loading in list(about.select(".animate-pulse")):
        if "Loading" in old_loading.get_text(" ", strip=True):
            old_loading.decompose()
    status = about.find(string=lambda s: s and "Open to work" in s)
    if status:
        status.replace_with("Engineering & operations")
    bio = about.select_one("p.font-hanken")
    if bio:
        bio.clear()
        bio.append(
            "I'm Aedam Rhaja F. Morancil (ADI), a Computer Engineering student at ICCT Colleges and an experienced procurement and operations professional. "
            "I bring hands-on experience in supplier sourcing, project coordination, quality assurance, and problem-solving into my growing interest in electronics, embedded systems, and practical technology."
        )

    for anchor in about.select("a[href]"):
        href = anchor.get("href", "")
        if href == "/resume":
            anchor["href"] = RESUME
            anchor["target"] = "_blank"
            anchor["rel"] = "noopener noreferrer"
        elif href == "/contact":
            anchor["href"] = "#contact"
        elif "linkedin.com" in href:
            anchor["href"] = LINKEDIN
            anchor["aria-label"] = "ADI on LinkedIn"
        elif href.startswith("mailto:"):
            anchor["href"] = "mailto:" + EMAIL
            anchor["aria-label"] = "Email ADI"
        else:
            # Never attribute someone else's Twitter, GitHub, Discord or Codeforces.
            # Remove only the unavailable link, leaving social rows intact.
            wrapper = anchor.parent
            anchor.decompose()
            if wrapper and not wrapper.get_text(" ", strip=True) and not wrapper.select("a"):
                wrapper.decompose()

    # Keep the original two-column project cards, now with original,
    # project-specific concept illustrations rather than reference screenshots.
    project_heading = projects.select_one(".word")
    if project_heading:
        project_heading.string = "Projects"
    project_grid = projects.select_one(".grid")
    if project_grid is None:
        raise ValueError("Original project grid not found")
    project_grid.clear()
    for title, subtitle, desc, tags, thumb in [
        ("MetroSure",
         "Design and Development of an Automated Metal-Cutting System",
         "MetroSure focuses on automating the metal-cutting workflow. It explores controlled cutting operations that aim to improve precision, make repeated cuts more consistent, and reduce unnecessary manual effort in fabrication. The image is a concept illustration; the cutting method, hardware, and testing results are not yet documented here.",
         ["Metal Cutting", "Automation", "Precision", "Fabrication"], "metrosure-cnc-render.webp"),
        ("Computer Engineering Academic Work",
         "Electronics, sensors, and embedded-system coursework",
         "Hands-on academic work at ICCT Colleges involving ESP32 microcontrollers, sensors, digital measurement, electronics prototyping, basic embedded programming, hardware troubleshooting, and technical documentation.",
         ["ESP32", "Sensors", "Electronics", "Embedded Systems"], "computer-engineering-photo.webp")
    ]:
        card = node(soup, "div", cls="group border-border/50 bg-card hover:border-border relative flex flex-col overflow-hidden rounded-xl border shadow-sm transition-all duration-300 ease-out hover:-translate-y-1 hover:scale-[1.01] hover:shadow-lg")
        imagebox = node(soup, "div", cls="px-4 pt-4")
        imageframe = node(soup, "div", cls="relative w-full overflow-hidden")
        imageframe["style"] = "aspect-ratio:16 / 9"
        image = node(soup, "img", cls="object-cover", src="assets/images/" + thumb, alt=("Automated metal cutting concept visual for MetroSure" if title == "MetroSure" else "ESP32 microcontroller board and electronics tools on a workbench"))
        image["loading"] = "eager"
        image["style"] = "position:absolute;height:100%;width:100%;left:0;top:0;right:0;bottom:0;color:transparent"
        imageframe.append(image)
        imagebox.append(imageframe)
        card.append(imagebox)
        body = node(soup, "div", cls="grow space-y-4 p-4")
        body.append(node(soup, "h2", title, "text-foreground text-xl font-semibold tracking-tight"))
        body.append(node(soup, "p", subtitle, "text-foreground text-sm font-medium"))
        body.append(node(soup, "p", desc, "text-muted-foreground text-sm leading-relaxed"))
        chipheader = node(soup, "h3", "Focus areas", "text-muted-foreground mb-2 text-xs font-semibold tracking-wider uppercase")
        body.append(chipheader)
        pills = node(soup, "div", cls="flex flex-wrap gap-2")
        for tag in tags:
            pills.append(node(soup, "span", tag, "bg-secondary/80 text-secondary-foreground border-border/30 rounded-md border px-2.5 py-1 text-xs font-medium"))
        body.append(pills)
        card.append(body)
        action = node(soup, "div", cls="relative z-20 mt-auto flex flex-wrap gap-3 p-4 pt-0")
        button = node(soup, "button", "Details", "details-trigger")
        button["type"] = "button"
        button["aria-haspopup"] = "dialog"
        action.append(button)
        card.append(action)
        project_grid.append(card)
    for link in list(projects.select('a[href="/projects"]')):
        parent_of_link = link.parent
        link.decompose()
        if parent_of_link and not parent_of_link.get_text(" ", strip=True):
            parent_of_link.decompose()
    projects.select_one(".px-4").append(node(
        soup, "p",
        "Project artwork is illustrative and does not depict completed hardware or testing.",
        "text-muted-foreground mt-4 text-xs leading-relaxed"
    ))

    # Original blog-card appearance, repurposed for real, dated work history.
    old_blog.decompose()
    exp, exp_inner = basic_section(soup, "experience", "Work Experience")
    worklist = node(soup, "div", cls="flex flex-col gap-6")
    for role in [
        ("Office Administrator / Purchasing Officer / PIC", "RGT Art Glass and Aluminum Supply",
         "Sep 2020 – Present",
         "Prepare quotations and project documents; coordinate with clients and job sites; source, compare and negotiate with local and international suppliers; manage purchasing, importation, delivery schedules and quality checks."),
        ("Psychological Test Administrator", "Safeway Diagnostic Medical Clinic · Psychology Department",
         "Nov 2018 – Feb 2020",
         "Administer standardized assessments; explain testing procedures; organize materials and results; maintain confidential records; coordinate schedules and provide department administration support."),
        ("X-Ray Clerk", "Safeway Diagnostic Medical Clinic · Radiology Department",
         "Jul 2018 – Nov 2018",
         "Assist with patient registration, appointments, records and scheduling; coordinate with clinical staff; keep documentation and sensitive patient information organized.")
    ]:
        worklist.append(experience_row(soup, *role))
    exp_inner.append(worklist)

    # Preserve the original skill chips, adding downloaded original-color
    # Devicon SVG technology marks without changing their layout or palette.
    skill_parent = skills.select_one(".flex.flex-wrap.gap-3")
    if skill_parent is None:
        raise ValueError("Original skill chips not found")
    skill_parent.clear()
    for tech, icon_name in TECH_ICONS.items():
        chip = node(soup, "div", cls=CHIP + " skill-tech-chip")
        img = node(soup, "img", cls="skill-icon", src="assets/icons/" + icon_name, alt="")
        img["width"] = "22"
        img["height"] = "22"
        img["loading"] = "lazy"
        img["decoding"] = "async"
        img["aria-hidden"] = "true"
        chip.append(img)
        chip.append(node(soup, "span", tech))
        skill_parent.append(chip)
    skills.select_one(".word").string = "Skills & Tools"

    # Replace the remote GitHub graph with a résumé-supported education card.
    old_activity.decompose()
    education, ed_inner = basic_section(soup, "education", "Education")
    education_card = node(soup, "article", cls=CARD)
    education_card.append(node(soup, "h2", "BS in Computer Engineering", "text-foreground text-lg font-semibold tracking-tight sm:text-xl"))
    education_card.append(node(soup, "p", "ICCT Colleges · Currently pursuing", "text-muted-foreground text-sm"))
    education_card.append(node(soup, "p", "Academic interests include ESP32, sensors, embedded systems, digital measurements, electronics prototyping, and hardware troubleshooting.", "text-muted-foreground mt-3 text-sm leading-relaxed"))
    ed_inner.append(education_card)

    # Arrange the new sections in the exact original width and vertical rhythm.
    parent = intro.parent
    parent.clear()
    for block in (intro, about, projects, exp, skills, education):
        parent.append(block)

    header.name = "header"
    header["id"] = "site-header"
    desktop_nav = header.select_one(".hidden.translate-y-1")
    if not desktop_nav:
        desktop_nav = header.find("a", href="/").parent
    desktop_nav.clear()
    for title, url in [
        ("Home", "#home"), ("Work", "#experience"), ("Projects", "#projects"),
        ("Skills", "#skills"), ("Resume", RESUME), ("Contact", "#contact")
    ]:
        link = node(soup, "a", cls="hover:text-foreground relative px-1 py-1 text-sm font-medium transition-all duration-200 sm:px-2 sm:text-base")
        link["href"] = url
        if url == RESUME:
            link["target"] = "_blank"
            link["rel"] = "noopener noreferrer"
        link.append(node(soup, "span", title, "relative z-10"))
        desktop_nav.append(link)
    theme = header.find("button", attrs={"aria-label": "Toggle theme"})
    menu = header.find("button", attrs={"aria-haspopup": "menu"})
    theme["id"] = "theme-toggle"
    theme["aria-pressed"] = "false"
    menu["id"] = "menu-toggle"
    menu["aria-label"] = "Open navigation menu"
    menu["aria-expanded"] = "false"
    menu["aria-controls"] = "mobile-nav"
    menu.attrs.pop("aria-haspopup", None)
    menu.attrs.pop("data-state", None)
    mobile = node(soup, "nav", id="mobile-nav")
    mobile["aria-label"] = "Mobile navigation"
    mobile["hidden"] = ""
    for title, url in [("Home", "#home"), ("Work", "#experience"), ("Projects", "#projects"),
                       ("Skills", "#skills"), ("Resume", RESUME), ("Contact", "#contact")]:
        link = node(soup, "a", title, href=url)
        if url == RESUME:
            link["target"] = "_blank"
            link["rel"] = "noopener noreferrer"
        mobile.append(link)
    header.append(mobile)

    # Contact typography reuses the original card and border utility palette.
    contact = node(soup, "section", cls="local-contact container mx-auto max-w-3xl px-8", id="contact")
    contact.append(node(soup, "h2", "Let's connect", "text-foreground text-3xl font-semibold tracking-tight"))
    contact.append(node(soup, "p", "I welcome opportunities to collaborate, exchange ideas, and apply my background in procurement, operations and computer engineering.", "text-muted-foreground text-sm leading-relaxed"))
    links = node(soup, "div", cls="flex flex-wrap items-center gap-3")
    for label, url in [("Email", "mailto:" + EMAIL), ("Gmail", "mailto:" + EMAIL), ("LinkedIn", LINKEDIN),
                       ("Résumé (PDF)", RESUME)]:
        anchor = node(soup, "a", label, "contact-link group border-border hover:border-foreground/20 bg-card hover:bg-accent relative inline-flex h-9 items-center gap-2 rounded-lg border px-4 text-sm font-medium shadow-sm transition-all duration-200", href=url)
        if not url.startswith("mailto:"):
            anchor["target"] = "_blank"
            anchor["rel"] = "noopener noreferrer"
        links.append(anchor)
    contact.append(links)
    contact.append(node(soup, "p", "GitHub, Twitter/X and Facebook: profiles can be added when verified.", "text-muted-foreground mt-4 text-xs"))
    contact.append(node(soup, "p", f"Email: {EMAIL} · LinkedIn: linkedin.com/in/aedam-rhaja-869ab6214", "text-muted-foreground mt-2 text-xs contact-inline"))

    footer.name = "footer"
    footer["id"] = "site-footer"
    quote = footer.find("blockquote")
    if quote:
        quote.string = "Grounded in experience. Growing through engineering."
    attribution = footer.select_one("p.text-right")
    if attribution:
        attribution.string = "— ADI"
    for span in footer.select("span"):
        if "visitor" in span.get_text(" ", strip=True).lower():
            span.string = "Learning, building, improving"
    for text in footer.find_all(string=True):
        if "Starz099" in text:
            text.replace_with(str(text).replace("Starz099", "ADI"))
    for bad in list(footer.find_all(string=True)):
        if "2026" in str(bad) and "©" not in str(bad):
            bad.replace_with(str(bad).replace("2026", "© 2026"))

    dialog = node(soup, "dialog", id="project-dialog")
    dialog["aria-labelledby"] = "dialog-title"
    dbody = node(soup, "div", cls="project-dialog-content")
    close = node(soup, "button", "Close ×", id="dialog-close", type="button")
    close["aria-label"] = "Close project details"
    dbody.extend([close, node(soup, "h2", id="dialog-title"),
                  node(soup, "p", id="dialog-description"), node(soup, "div", id="dialog-tags")])
    dialog.append(dbody)

    # The new document has no Next.js scripts or unavailable API endpoints.
    output = BeautifulSoup("<!doctype html><html lang='en' class='dark'><head></head><body></body></html>", "html.parser")
    for tag, attrs in [
        ("meta", {"charset": "utf-8"}),
        ("meta", {"name": "viewport", "content": "width=device-width, initial-scale=1"}),
        ("meta", {"name": "description", "content": "Aedam Rhaja F. Morancil (ADI) — Computer Engineering, procurement, operations and MetroSure project."}),
        ("link", {"rel": "icon", "href": PHOTO, "type": "image/jpeg"}),
        ("link", {"rel": "stylesheet", "href": "assets/static/chunks/reference.css"}),
        ("link", {"rel": "stylesheet", "href": "styles.css"}),
        ("script", {"src": "app.js", "defer": ""}),
        ("script", {"src": "music.js", "defer": ""})
    ]:
        output.head.append(output.new_tag(tag, attrs=attrs))
    output.head.insert(3, node(output, "title", "ADI | Aedam Rhaja F. Morancil"))
    output.body["class"] = "hanken_grotesk_868c7ba5-module__0hqQZq__variable antialiased"
    for item in (backdrop, header, main_block, contact, footer, dialog):
        output.body.append(item.extract())
    for widget in BeautifulSoup(BUNNY_RADIO_HTML, "html.parser").find_all(recursive=False):
        output.body.append(widget)
    for comment in output.find_all(string=lambda x: isinstance(x, Comment)):
        comment.extract()
    (ROOT / "index.html").write_text(str(output), encoding="utf-8")
    print(f"Built {ROOT / 'index.html'} using original reference DOM and local styles/assets")


if __name__ == "__main__":
    main()
