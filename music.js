/* Bunny Radio — one local track, no framework or network dependency.
 * Autoplay is requested on load. Browsers may block unmuted autoplay;
 * in that case the Play button is the accessible fallback.
 */
(() => {
  "use strict";

  const audio = document.getElementById("bunny-audio");
  const player = document.getElementById("bunny-radio");
  const restore = document.getElementById("bunny-music-restore");
  const hide = document.getElementById("bunny-music-hide");
  const toggle = document.getElementById("bunny-music-toggle");
  const mute = document.getElementById("bunny-music-mute");
  const volume = document.getElementById("bunny-music-volume");
  const seek = document.getElementById("bunny-music-seek");
  const time = document.getElementById("bunny-music-time");
  const status = document.getElementById("bunny-music-status");
  const miniState = document.getElementById("bunny-music-mini-state");
  if (!audio || !player || !restore || !hide || !toggle || !mute || !volume || !seek || !time || !status) return;

  // Keep the actual audio element mounted even when the display is hidden.
  // This intentionally means hiding the player doesn't pause a playing song.
  audio.loop = true;
  audio.autoplay = true;
  audio.preload = "metadata";
  audio.volume = 0.65;

  const timeLabel = (seconds) => {
    if (!Number.isFinite(seconds)) return "--:--";
    const s = Math.max(0, Math.floor(seconds));
    return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
  };

  function refreshTime() {
    const duration = audio.duration;
    const total = Number.isFinite(duration) && duration > 0;
    time.textContent = `${timeLabel(audio.currentTime)} / ${total ? timeLabel(duration) : "--:--"}`;
    seek.disabled = !total;
    if (total && !seek.matches(":active")) {
      seek.value = String(Math.max(0, Math.min(1000, Math.round((audio.currentTime / duration) * 1000))));
    }
  }

  function refreshPlayback() {
    const playing = !audio.paused && !audio.ended;
    player.dataset.playing = String(playing);
    toggle.setAttribute("aria-label", playing ? "Pause music" : "Play music");
    toggle.setAttribute("title", playing ? "Pause" : "Play");
    toggle.setAttribute("aria-pressed", String(playing));
    if (miniState) miniState.textContent = playing ? "♫" : "♪";
    restore.setAttribute("aria-label", playing ? "Show bunny player (music is playing)" : "Show bunny music player");
    if (playing) status.textContent = "Playing";
    else if (audio.ended) status.textContent = "Replay";
    else if (status.textContent !== "Tap play to start" && status.textContent !== "Audio unavailable") {
      status.textContent = "Paused";
    }
  }

  function refreshVolume() {
    const muted = audio.muted || audio.volume === 0;
    player.dataset.muted = String(muted);
    mute.setAttribute("aria-label", muted ? "Unmute music" : "Mute music");
    mute.setAttribute("title", muted ? "Unmute" : "Mute");
    mute.setAttribute("aria-pressed", String(muted));
    volume.value = String(audio.volume);
  }

  async function startPlayback({ initial = false } = {}) {
    try {
      await audio.play();
      refreshPlayback();
    } catch (error) {
      refreshPlayback();
      if (error?.name === "NotAllowedError" || error?.name === "AbortError") {
        status.textContent = "Tap play to start";
        player.dataset.autoplay = "blocked";
      } else {
        status.textContent = "Audio unavailable";
        player.dataset.autoplay = "failed";
        if (!initial) console.warn("Unable to play the supplied audio file:", error);
      }
    }
  }

  toggle.addEventListener("click", () => {
    if (audio.paused) {
      startPlayback();
    } else {
      audio.pause();
      refreshPlayback();
    }
  });

  hide.addEventListener("click", () => {
    player.hidden = true;
    restore.hidden = false;
    restore.focus();
  });
  restore.addEventListener("click", () => {
    restore.hidden = true;
    player.hidden = false;
    hide.focus();
  });

  mute.addEventListener("click", () => {
    if (audio.volume === 0) audio.volume = 0.65;
    else audio.muted = !audio.muted;
    refreshVolume();
  });

  volume.addEventListener("input", () => {
    audio.volume = Math.max(0, Math.min(1, Number(volume.value)));
    if (audio.volume > 0) audio.muted = false;
    refreshVolume();
  });

  seek.addEventListener("input", () => {
    if (Number.isFinite(audio.duration) && audio.duration > 0) {
      audio.currentTime = (Number(seek.value) / 1000) * audio.duration;
      refreshTime();
    }
  });

  audio.addEventListener("loadedmetadata", refreshTime);
  audio.addEventListener("durationchange", refreshTime);
  audio.addEventListener("timeupdate", refreshTime);
  audio.addEventListener("volumechange", refreshVolume);
  audio.addEventListener("play", refreshPlayback);
  audio.addEventListener("pause", refreshPlayback);
  audio.addEventListener("ended", refreshPlayback);
  audio.addEventListener("error", () => {
    status.textContent = "Audio unavailable";
    seek.disabled = true;
  });

  refreshTime();
  refreshVolume();
  refreshPlayback();

  // Browser autoplay policy decides whether audible sound can start here.
  // Never pretend audio started if it was blocked.
  startPlayback({ initial: true });
})();
