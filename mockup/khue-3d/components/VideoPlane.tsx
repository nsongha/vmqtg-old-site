"use client";

import { useEffect, useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { cameraPoses } from "@/lib/cameraPoses";
import { scrollProgress, easeInOutCubic } from "@/lib/scroll";

// Section-2 reveal timings, in seconds. Fades run purely on TIME (keyed to
// the "settled at Section 2" flag), never on scroll position — so stopping
// mid-scroll can never strand the layers half-faded over each other.
const PHOTO_FADE_IN = 2.0;
const PHOTO_FADE_OUT = 0.35;
const PANEL_FADE_IN = 0.5;
const PANEL_FADE_OUT = 0.3;

// Natural plane size in world units (square — matches the round window).
const PLANE_W = 0.34;

/**
 * The hero video as a textured plane *behind* the gate's circular window.
 * The 3D model occludes it everywhere except through the window opening —
 * so the video reads as light pouring through Khuê Văn Các, never a
 * full-bleed background.
 *
 * position / size are tuned so that:
 *  - at the INSIDE camera pose the plane fills the viewport (hero = video)
 *  - at the HERO camera pose the plane stays inside the model silhouette
 */
export default function VideoPlane({
  play,
  onReady,
  onProgress,
}: {
  play: boolean;
  onReady: () => void;
  onProgress: (fraction: number) => void;
}) {
  const video = useMemo(() => {
    const v = document.createElement("video");
    v.src = "/hero.mp4";
    v.loop = true;
    v.muted = true;
    v.defaultMuted = true;
    v.playsInline = true;
    v.preload = "auto";
    v.crossOrigin = "anonymous";
    return v;
  }, []);

  const texture = useMemo(() => {
    const t = new THREE.VideoTexture(video);
    t.colorSpace = THREE.SRGBColorSpace;
    t.minFilter = THREE.LinearFilter;
    t.magFilter = THREE.LinearFilter;
    // Crop the 16:9 source to a centred square so a round window samples
    // it without horizontal stretch.
    const ar = 9 / 16;
    t.wrapS = THREE.ClampToEdgeWrapping;
    t.wrapT = THREE.ClampToEdgeWrapping;
    t.repeat.set(ar, 1);
    t.offset.set((1 - ar) / 2, 0);
    return t;
  }, [video]);

  // Track buffering — feeds the preloader. `canplaythrough` (readyState 4) is
  // the "safe to reveal" signal; the one-off check covers a cache hit that
  // already resolved before this effect attached its listeners.
  useEffect(() => {
    const reportProgress = () => {
      if (video.duration && video.buffered.length) {
        const end = video.buffered.end(video.buffered.length - 1);
        onProgress(Math.min(1, end / video.duration));
      }
    };
    const reportReady = () => {
      onProgress(1);
      onReady();
    };
    video.addEventListener("progress", reportProgress);
    video.addEventListener("loadeddata", reportProgress);
    video.addEventListener("canplaythrough", reportReady);
    reportProgress();
    if (video.readyState >= 4) reportReady();
    return () => {
      video.removeEventListener("progress", reportProgress);
      video.removeEventListener("loadeddata", reportProgress);
      video.removeEventListener("canplaythrough", reportReady);
      video.pause();
      video.src = "";
      texture.dispose();
    };
  }, [video, texture, onReady, onProgress]);

  // The intro video only starts once the preloader clears, so the viewer
  // always catches it from frame 0.
  useEffect(() => {
    if (!play) return;
    video.currentTime = 0;
    const tryPlay = () => video.play().catch(() => {});
    tryPlay();
    window.addEventListener("pointerdown", tryPlay, { once: true });
    return () => window.removeEventListener("pointerdown", tryPlay);
  }, [play, video]);

  const meshRef = useRef<THREE.Mesh>(null);
  const matRef = useRef<THREE.MeshBasicMaterial>(null);
  const fade = useRef({ photoProg: 0, panelProg: 0 });

  useFrame((state, delta) => {
    const mesh = meshRef.current;
    if (!mesh) return;
    mesh.position.z = cameraPoses.videoZ;

    // Cap the on-screen size: the video never scales past 100% of the
    // viewport width. When the camera dives in close, the plane shrinks to
    // keep its projected width pinned at exactly the viewport width.
    const cam = state.camera as THREE.PerspectiveCamera;
    const d = Math.abs(cam.position.z - cameraPoses.videoZ);
    const visH = 2 * d * Math.tan((cam.fov * Math.PI) / 180 / 2);
    const visW = visH * (state.size.width / state.size.height);
    const r = visW / PLANE_W;

    // Soft-min(r, 1): rounds the cap corner so the video EASES — instead of
    // jerking — at the moment it stops being pinned and starts scaling with
    // the camera again. k = width of the smoothing band around the corner.
    const k = 0.6;
    const h = Math.max(k - Math.abs(r - 1), 0) / k;
    const scale = Math.min(r, 1) - h * h * k * 0.25;
    mesh.scale.setScalar(Math.max(0, scale));

    const f = fade.current;
    const p = scrollProgress.value;

    // Video: full until the camera is halfway through its journey, then
    // linearly out — completely gone by the time Section 2 is reached.
    const vOp = p <= 0.5 ? 1 : Math.max(0, 1 - (p - 0.5) * 2);
    if (matRef.current) matRef.current.opacity = vOp;

    // "Settled at Section 2" — the single flag both reveals key off. The
    // moment the viewer scrolls away (p drops at all) the photo AND the
    // panel fade out on a fixed timer, so a mid-scroll stop never strands
    // them half-transparent on top of each other.
    const atS2 = p >= 0.999;

    f.photoProg = atS2
      ? Math.min(1, f.photoProg + delta / PHOTO_FADE_IN)
      : Math.max(0, f.photoProg - delta / PHOTO_FADE_OUT);
    f.panelProg = atS2
      ? Math.min(1, f.panelProg + delta / PANEL_FADE_IN)
      : Math.max(0, f.panelProg - delta / PANEL_FADE_OUT);

    const root = document.documentElement.style;
    root.setProperty("--p-photo", easeInOutCubic(f.photoProg).toFixed(3));
    root.setProperty("--p-panel", easeInOutCubic(f.panelProg).toFixed(3));
    root.setProperty("--photo-scale", String(cameraPoses.photoScale));
    root.setProperty("--photo-x", cameraPoses.photoX + "%");
    root.setProperty("--photo-y", cameraPoses.photoY + "%");
  });

  return (
    <mesh ref={meshRef} position={[0, 0.62, cameraPoses.videoZ]}>
      <planeGeometry args={[PLANE_W, PLANE_W]} />
      <meshBasicMaterial
        ref={matRef}
        map={texture}
        toneMapped={false}
        transparent
      />
    </mesh>
  );
}
