"use client";

import { useFrame } from "@react-three/fiber";
import { useRef } from "react";
import * as THREE from "three";
import { scrollProgress } from "@/lib/scroll";
import { cameraPoses } from "@/lib/cameraPoses";

// Two keyframes ONLY — both fully owned by <CameraTuner/>:
//   p = 0  → INSIDE  (Section 1, looking straight into the window)
//   p = 1  → HERO    (Section 2, the gate above the CTA cards)
// The camera interpolates directly between them, so the UI values are
// the single source of truth — no fixed intermediate poses left to bleed in.

const POSE_INSIDE = new THREE.Vector3();
const POSE_HERO = new THREE.Vector3();
const TARGET_NEAR = new THREE.Vector3();
const TARGET_HERO = new THREE.Vector3();

export default function CameraRig() {
  const pos = useRef(new THREE.Vector3(0, 0.62, 1.05));
  const tgt = useRef(new THREE.Vector3(0, 0.62, 0));
  const wantPos = useRef(new THREE.Vector3());
  const wantTgt = useRef(new THREE.Vector3());

  useFrame((state, delta) => {
    const p = scrollProgress.value;

    POSE_INSIDE.set(0, cameraPoses.insideY, cameraPoses.insideZ);
    POSE_HERO.set(0, cameraPoses.heroY, cameraPoses.heroZ);
    // INSIDE looks straight down -Z (level) so the camera Z can dive past the
    // window — even negative — without the look direction ever flipping.
    TARGET_NEAR.set(0, cameraPoses.insideY, cameraPoses.insideZ - 1);
    // HERO looks at the gate's centre.
    TARGET_HERO.set(0, 0.5, 0);

    // Linear in p — the slow-fast-slow easing is applied once, by the glide
    // animation that drives scrollProgress (avoids double-easing).
    wantPos.current.lerpVectors(POSE_INSIDE, POSE_HERO, p);
    wantTgt.current.lerpVectors(TARGET_NEAR, TARGET_HERO, p);

    // Critically-damped smoothing so flicks of the wheel feel fluid.
    const k = 1 - Math.pow(0.0015, delta);
    pos.current.lerp(wantPos.current, k);
    tgt.current.lerp(wantTgt.current, k);

    state.camera.position.copy(pos.current);
    state.camera.lookAt(tgt.current);
  });

  return null;
}
