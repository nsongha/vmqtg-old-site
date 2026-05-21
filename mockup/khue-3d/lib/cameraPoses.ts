// Live-tunable camera key-poses. Mutated by <CameraTuner/>, read every frame
// by <CameraRig/>. A plain object (not React state) keeps the 60fps loop
// re-render-free — same pattern as scrollProgress.
//
//   Section 1 = INSIDE  (scroll 0 — looking at the round window)
//   Section 2 = HERO    (scroll 1 — the gate sits above the CTA cards)
export const POSE_DEFAULTS = {
  insideY: 0.62,
  insideZ: -0.1,
  heroY: 0.63,
  heroZ: 1.4,
  // Scene depth — tunable too:
  videoZ: -0.19, // video plane: more negative = deeper behind the window
  modelZ: 0, // gate model: positive = nearer the camera
  clipZ: -0.155, // model clip: geometry behind this Z is cut (hides the back roof)
  // Guided Section 1 → Section 2 glide, in seconds (eased slow-fast-slow):
  glideDuration: 5,
  // Section-2 photo (fades in after the video) — aligned to the 3D silhouette:
  photoScale: 1.074,
  photoX: 0, // % of viewport, horizontal nudge
  photoY: -5.4, // % of viewport, vertical nudge
};

// Live, mutable copy. Read by the R3F components every frame.
export const cameraPoses = { ...POSE_DEFAULTS };

export type PoseKey = keyof typeof cameraPoses;

// Restore defaults — used by <CameraTuner/> on mount to undo any stale
// values the browser tries to restore into the range inputs.
export function resetPoses() {
  Object.assign(cameraPoses, POSE_DEFAULTS);
  return { ...POSE_DEFAULTS };
}
