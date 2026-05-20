// Shared scroll progress (0..1). Mutated by the DOM scroll listener in <Stage/>,
// read by R3F's useFrame in <CameraRig/>. A plain object avoids re-renders.
export const scrollProgress = { value: 0 };

export const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const easeInOut = (t: number) =>
  t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
export const easeInOutCubic = (t: number) =>
  t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
export const mapRange = (v: number, a: number, b: number) =>
  clamp((v - a) / (b - a));
