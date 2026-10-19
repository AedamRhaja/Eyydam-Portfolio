"""Brave smoke test for the ORIGINAL reference design personalized for ADI.

Run: python tests/smoke.py [--screenshots]
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "index.html").as_uri()
BRAVE = Path(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe")


def main():
    failures = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=str(BRAVE) if BRAVE.exists() else None)
        for width, height in ((320, 760), (390, 844), (768, 1024), (1440, 900)):
            page = browser.new_page(viewport={"width": width, "height": height})
            errors = []
            failed = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("requestfailed", lambda request: failed.append((request.url, request.failure)))
            page.goto(URL, wait_until="load")
            page.evaluate("document.querySelectorAll('img').forEach(img => img.loading='eager')")
            page.wait_for_timeout(300)
            metrics = page.evaluate("""() => ({
                doc: document.documentElement.scrollWidth,
                window: innerWidth,
                heroLight: document.querySelector('img.adi-hero-light')?.naturalWidth,
                heroDark: document.querySelector('img.adi-hero-dark')?.naturalWidth,
                projectImages: [...document.querySelectorAll('#projects .grid img')].map(img => img.getAttribute('src')),
                heroDarkVisible: getComputedStyle(document.querySelector('img.adi-hero-dark')).display !== 'none',
                portrait: document.querySelector('img[alt*="Morancil"]')?.naturalWidth,
                icons: [...document.querySelectorAll('#skills .skill-icon')].map(img => ({
                  src: img.getAttribute('src'), visible: !!img.getBoundingClientRect().width,
                  loaded: img.complete && img.naturalWidth > 0
                })),
                images: [...document.images].filter(img => !img.complete || !img.naturalWidth).map(img => img.src),
                cards: [...document.querySelectorAll('#projects .grid > .group')].length,
                jobs: document.querySelectorAll('#experience article').length,
                skills: [...document.querySelectorAll('#skills .flex.flex-wrap.gap-3 > div')].map(el => el.textContent.trim()),
                text: document.body.innerText,
                font: document.fonts.check('16px "Hanken Grotesk"'),
                resume: document.querySelector('a[href$=".pdf"]')?.getAttribute('href'),
                dateMargins: [...document.querySelectorAll('.experience-entry')].map(card => {
                  const date = card.querySelector('.experience-dates')?.getBoundingClientRect();
                  const container = card.getBoundingClientRect();
                  return Math.round(container.right - date.right);
                }),
                radio: (() => {
                  const audio = document.querySelector('#bunny-audio');
                  return { source: audio?.currentSrc, count: document.querySelectorAll('audio').length,
                    readyState: audio?.readyState, error: audio?.error?.code,
                    duration: audio?.duration, loop: audio?.loop,
                    playerVisible: !!document.querySelector('#bunny-radio')?.getClientRects().length,
                    overflow: document.querySelector('#bunny-radio')?.getBoundingClientRect().right > innerWidth + 1 };
                })()
            })""")
            if metrics["doc"] > metrics["window"] + 1:
                failures.append(f"{width}: horizontal overflow {metrics['doc']-metrics['window']}")
            if metrics["images"] or not metrics["heroLight"] or not metrics["heroDark"] or not metrics["portrait"]:
                failures.append(f"{width}: image failure {metrics['images']}")
            if metrics["cards"] != 3:
                failures.append(f"{width}: expected 3 project cards, found {metrics['cards']}")
            if len(metrics["icons"]) != 6 or not all(icon["loaded"] and icon["visible"] for icon in metrics["icons"]):
                failures.append(f"{width}: missing or invisible technology icons: {metrics['icons']}")
            if "Smartpoint Glasses" not in metrics["text"]:
                failures.append(f"{width}: Smartpoint Glasses copy missing")
            if "Automated Metal-Cutting System" not in metrics["text"]:
                failures.append(f"{width}: MetroSure copy does not describe metal cutting")
            if max(metrics["dateMargins"], default=999) > 45:
                failures.append(f"{width}: experience dates are not right-aligned: {metrics['dateMargins']}")
            if not metrics["font"]:
                failures.append(f"{width}: local font missing")
            if metrics["jobs"] != 3:
                failures.append(f"{width}: missing work history cards")
            if set(metrics["skills"]) != {"Python", "HTML", "C++", "Java", "Kotlin", "Android Studio"}:
                failures.append(f"{width}: skill labels incorrect {metrics['skills']}")
            if metrics["resume"] != "assets/AEDAM_RHAJA_MORANCIL_RESUME.pdf":
                failures.append(f"{width}: résumé path incorrect")
            if "Starz099" in metrics["text"] or "Mayank" in metrics["text"]:
                failures.append(f"{width}: original person's identity still present")
            if "Aedam" not in metrics["text"] or "MetroSure" not in metrics["text"]:
                failures.append(f"{width}: personalized content missing")
            radio = metrics["radio"]
            if (radio["count"] != 1 or not radio["source"].endswith("2Pac%20-%20Life%20Goes%20on.mp3") or
                    not radio["loop"] or radio["error"] is not None or
                    radio["readyState"] < 1 or abs(radio["duration"] - 301.836) > 1):
                failures.append(f"{width}: MP3 not loaded or looping: {radio}")
            if not radio["playerVisible"] or radio["overflow"]:
                failures.append(f"{width}: bunny player hidden or offscreen: {radio}")
            if "--screenshots" in sys.argv and width in (390, 1440):
                page.screenshot(path=str(ROOT / "tests" / f".reference-{width}.png"), full_page=True)
            player = page.locator("#bunny-radio")
            audio = page.locator("#bunny-audio")
            page.locator("#bunny-music-toggle").click()
            page.wait_for_timeout(230)
            if audio.evaluate("(a) => a.paused || a.error !== null"):
                failures.append(f"{width}: click-to-play failed")
            if player.get_attribute("data-playing") != "true":
                failures.append(f"{width}: player does not show playing state")
            if width == 390:
                # A real wraparound checks the browser's loop behavior,
                # rather than trusting the presence of the loop attribute.
                audio.evaluate("(a) => {a.currentTime = a.duration - 0.55;}")
                page.wait_for_timeout(1450)
                playback = audio.evaluate("(a) => ({paused:a.paused,time:a.currentTime})")
                if playback["paused"] or playback["time"] > 3:
                    failures.append(f"{width}: MP3 did not loop at the end: {playback}")
            page.locator("#bunny-music-mute").click()
            if not audio.evaluate("(a) => a.muted"):
                failures.append(f"{width}: mute control failed")
            page.locator("#bunny-music-mute").click()
            if audio.evaluate("(a) => a.muted"):
                failures.append(f"{width}: unmute control failed")
            page.locator("#bunny-music-volume").evaluate("(el) => {el.value='0.3';el.dispatchEvent(new Event('input',{bubbles:true}));}")
            if abs(audio.evaluate("(a) => a.volume") - 0.3) > .01:
                failures.append(f"{width}: volume slider failed")
            page.locator("#bunny-music-seek").evaluate("(el) => {el.value='500';el.dispatchEvent(new Event('input',{bubbles:true}));}")
            if abs(audio.evaluate("(a) => a.currentTime") - radio["duration"] / 2) > 3:
                failures.append(f"{width}: seek failed")
            page.locator("#bunny-music-hide").click()
            if player.is_visible() or not page.locator("#bunny-music-restore").is_visible():
                failures.append(f"{width}: hide/restore affordance failed")
            if audio.evaluate("(a) => a.paused"):
                failures.append(f"{width}: hiding unexpectedly paused audio")
            page.locator("#bunny-music-restore").click()
            if not player.is_visible() or page.locator("#bunny-music-restore").is_visible():
                failures.append(f"{width}: restore player failed")
            page.locator("#bunny-music-toggle").click()
            if not audio.evaluate("(a) => a.paused"):
                failures.append(f"{width}: pause control failed")
            theme = page.locator("#theme-toggle")
            before = page.locator("html").get_attribute("class")
            theme.click()
            if before == page.locator("html").get_attribute("class"):
                failures.append(f"{width}: theme switch failed")
            afterDarkVisible = page.locator("img.adi-hero-dark").evaluate("(el) => getComputedStyle(el).display !== 'none'")
            if afterDarkVisible == metrics["heroDarkVisible"]:
                failures.append(f"{width}: light/dark header images failed to swap")
            if width < 640:
                page.locator("#menu-toggle").click()
                if not page.locator("#mobile-nav").is_visible():
                    failures.append(f"{width}: mobile menu did not open")
                page.locator('#mobile-nav a[href="#experience"]').click()
                if page.locator("#mobile-nav").is_visible():
                    failures.append(f"{width}: mobile menu stayed open")
            page.locator(".details-trigger").first.click()
            if not page.locator("#project-dialog").is_visible():
                failures.append(f"{width}: details dialog failed")
            page.locator("#dialog-close").click()
            if page.locator("#project-dialog").is_visible():
                failures.append(f"{width}: dialog did not close")
            # Chromium may abort an early file:// audio-range request after it
            # has already buffered valid data. Verify the media state above;
            # don't mistake that expected cancellation for a missing asset.
            failed = [entry for entry in failed if not (
                "2Pac%20-%20Life%20Goes%20on.mp3" in entry[0] and
                "ERR_ABORTED" in str(entry[1]) and
                radio["readyState"] >= 1 and radio["error"] is None
            )]
            if errors or failed:
                failures.append(f"{width}: JavaScript errors {errors}, failed requests {failed}")
            print(f"{width}px: overflow={max(0,metrics['doc']-width)}, portrait={bool(metrics['portrait'])}, "
                  f"jobs={metrics['jobs']}, projects={metrics['cards']}, errors={len(errors)}, failed={len(failed)}")
            page.close()
        browser.close()
    if failures:
        for failure in failures:
            print("FAIL:", failure)
        return 1
    print("PASS: faithful reference layout, verified content, interactions and local assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
