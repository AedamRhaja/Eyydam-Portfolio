# ADI Portfolio — Original Design Restored

This is a faithful static reconstruction of the **actual original** portfolio
design (starzz.dev/Mayank), personalized with the verified résumé data for
**Aedam Rhaja F. Morancil (ADI)**. It deliberately reuses the original
HTML/Tailwind component classes, local Hanken Grotesk fonts, light/dark theme,
same original hero composition, compact header, two-column project cards, chips
and mobile layout. The prior custom teal, rabbit/crab and diagram-heavy
redesign has been replaced.

## Open locally

Double-click index.html, or open a terminal in this folder and run:

    python -m http.server 8080

Then open http://localhost:8080. The page works under file:// without a
backend, Node, Next.js or any web fonts fetched from a CDN.

## Real content and image assets

- Name: Aedam Rhaja F. Morancil (portfolio display name ADI).
- Degree: BS Computer Engineering, currently pursuing at ICCT Colleges.
- Roles: RGT Art Glass and Aluminum Supply, Sept 2020–present; Safeway
  Diagnostic Medical Clinic Psychology Department, Nov 2018–Feb 2020;
  Safeway Diagnostic Medical Clinic Radiology Department, Jul–Nov 2018.
- Capstone Project: **Smartpoint Glasses** — A Smart Assistive Eyeglasses
  System for Individuals with Severe Mobility Impairments (ICCT Colleges COEDT,
  VISION-CON). Operates as an alternative cursor/mouse interface for individuals
  who cannot use their hands due to illness but retain functional fingers.
  Features head-tilt cursor tracking, tactile finger clicking / dwell click,
  MAX30102 heart rate & SpO2 vital signs monitoring, physical emergency panic
  alert with SMS dispatch, offline voice commands, smart health reminders,
  and CareMotion ESP32-C3 Wi-Fi synchronization.
- Project: **Power Supply** — Regulated 220V AC Mains to 12V DC Hardware
  Power Conversion System. Physical benchtop hardware implementation focused
  on AC-to-DC power conversion, step-down transformation, diode bridge
  rectification, capacitive smoothing (2200µF/35V reservoir capacitor), active
  linear voltage regulation with finned aluminum heatsink, and stepped voltage
  selection (OFF, 3V, 4.5V, 6V, 9V, 12V DC) providing stable voltage delivery
  for electronic prototyping and embedded microcontrollers.
- Project: MetroSure — Design and Development of an Automated Metal-Cutting
  System (metal-cutting purpose clarified by the site owner).
- Academic work: Sensors, ESP32, basic embedded systems and electronics,
  confirmed in the attached résumé.
- Programming tools: Python, HTML, C++, Java, Kotlin, Android Studio
  (provided by site owner).
- Contacts: email and LinkedIn were verified from the résumé. The résumé
  button opens the local assets/AEDAM_RHAJA_MORANCIL_RESUME.pdf file.
- The hero preserves the original dimensions/layout but switches between
  the user's two rabbit-theme JPGs:
  light = b67979daf081bb08eb5249c0f6e1d1c5.jpg (flower garden),
  dark = 5f365b46bbe27ebb9c77b68611bf5dc7.jpg (night balloons).
- The avatar is assets/images/05e4bc3e-208c-4542-a0bc-1b6aaf326665.jpg.
- The MetroSure card uses the generated industrial cutting-machine image,
  locally optimized as assets/images/metrosure-cnc-render.webp (1279×720).
  It is an illustrative rendering, **not** a photograph of built hardware.
- The Computer Engineering Academic Work card uses a real photograph of an
  ESP32 development board on a workbench, locally optimized as
  assets/images/computer-engineering-photo.webp (1200×675).
  Original photo: Tanha Tamanna Syed, "Arduino Circuit Board with Tools on
  Workbench," Pexels, https://www.pexels.com/photo/arduino-circuit-board-with-tools-on-workbench-35652454/
  (free Pexels License). This is an illustrative stock photograph and does
  not represent ADI's actual hardware. Both project pictures work offline.
- Six original-color technology marks are downloaded to assets/icons/ from
  [Devicon](https://github.com/devicons/devicon) (Python, HTML5, C++, Java,
  Kotlin, Android Studio). They are bundled locally as small SVG files,
  rather than generated imitations or remote image URLs. Devicon's upstream
  license is preserved in assets/icons/DEVICON-LICENSE.txt; brand names and
  logos remain the trademarks of their respective owners.
- Old reference-owner project images and superseded artwork/editing sources
  were removed; only the five images the portfolio actually uses remain.
- Work-experience dates are positioned at the right of each card on desktop
  and right-aligned below the job heading on narrow mobile screens.

The résumé is the authoritative source for current employment, dates and
contacts. No employer street addresses, unverified GitHub/X/Facebook
profiles, new awards, or completed MetroSure features were invented.

## Bunny Radio — local music player

The player follows the same rabbit photos as the website's light/dark header.
It uses the locally supplied audio file:

    assets/2Pac - Life Goes on.mp3

- Requests autoplay and loops the track automatically. Brave, Chrome, and
  other browsers may block **audible autoplay** until a user clicks Play.
  The status displays **Tap play to start** if playback was denied.
- Play/pause, seek, time display, mute/unmute and volume are provided.
- The X button hides the panel to a small **Music**/bunny restore control.
  If audio is playing, hiding the panel does **not** pause it.
- No streaming, additional player dependencies, or network requests.
- The supplied MP3 is 192 kbps, 44.1 kHz stereo, approximately 5:02 long.
  It is kept unchanged rather than lowering its quality via transcoding.

**Publishing note:** The commercial 2Pac recording may not be licensed for
public redistribution. Keep it for personal/local use unless you have the
necessary rights. Before publishing a public Git repository or deployed site,
replace the MP3 with appropriately licensed music or omit it.

## How the restored design is built

- scripts/reference-home-snapshot.html: local copy of the original
  home-page server-rendered HTML, downloaded to recover the actual layout.
- scripts/build_original_design.py: deterministic builder that extracts
  original DOM components and personalizes them. To regenerate index.html,
  run: python scripts/build_original_design.py.
- assets/static/chunks/reference.css: original local compiled Tailwind CSS.
- assets/static/media: original local WOFF2 fonts.
- styles.css: high-contrast readability across Dark and Light modes, tuned soft canvas (#f1f5f9) in light mode with subtle watermark sapphire logo (0.18 opacity), tuned dark mode background logo (0.22 opacity) removing harsh cyan glare, solid elevated cards in both modes, and smooth page entrance animations.
- app.js: theme toggle, mobile navigation menu, project modal dialogs, certificate high-resolution preview modal, and animated page transition routing (HOME, WORK, PROJECTS, SKILLS, CERTIFICATES, RESUME, CONTACT) with URL hash history synchronization.
- music.js: local audio playback/loop, progress, volume, and hide/restore (uninterrupted during page transitions).
- assets/certificates/: high-resolution WebP, PNG, and PDF certificate files with verified transcripts and citations (Secure Networking, DICT Cybersecurity, IoT Smart Environments, and Liturgical Architecture Days 1 & 2).
- assets/images/smartpoint/: optimized WebP poster, card rendering, and synchronized CareMotion companion mobile application screenshots (main panel, BPM monitor, emergency alert, and settings).

The obsolete scripts/restore_reference.py and unused reference-owner images
have been deleted to avoid accidentally reverting the personalized project.
The original HTML snapshot remains because the deterministic builder reads
its **layout/classes**, not its original images or identity.

## Tests

    python tests/smoke.py
    python tests/smoke.py --screenshots

Brave/Playwright tests 320, 390, 768 and 1440 pixel widths, profile/both themed banners,
work history, both project images, six SVG brand icons, PDF path,
local fonts, theme, menu,
dialogs, bunny music playback/loop/seek/hide and JavaScript errors.
