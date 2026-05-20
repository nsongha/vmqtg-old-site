"use client";

import { useGLTF } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useMemo, useRef } from "react";
import * as THREE from "three";
import { cameraPoses } from "@/lib/cameraPoses";

useGLTF.preload("/khue-van-cac.glb");

export default function Khue() {
  const { scene } = useGLTF("/khue-van-cac.glb");

  // A single clipping plane shared by the model material. It cuts away every
  // bit of geometry behind clipZ — so the rear roof eave can never intrude
  // into the round window when the camera looks through it.
  const clipPlane = useMemo(
    () => new THREE.Plane(new THREE.Vector3(0, 0, 1), 0.05),
    [],
  );

  const ready = useMemo(() => {
    const cloned = scene.clone(true);
    const mat = new THREE.MeshStandardMaterial({
      color: new THREE.Color("#c75832"),
      roughness: 0.62,
      metalness: 0.02,
      clippingPlanes: [clipPlane],
      clipShadows: true,
    });
    cloned.traverse((obj) => {
      if ((obj as THREE.Mesh).isMesh) {
        const m = obj as THREE.Mesh;
        m.material = mat;
        m.castShadow = true;
        m.receiveShadow = true;
      }
    });
    return cloned;
  }, [scene, clipPlane]);

  const groupRef = useRef<THREE.Group>(null);
  useFrame(() => {
    if (groupRef.current) groupRef.current.position.z = cameraPoses.modelZ;
    // keep geometry where z >= clipZ  →  plane normal (0,0,1), constant = -clipZ
    clipPlane.constant = -cameraPoses.clipZ;
  });

  return (
    <group ref={groupRef}>
      <primitive object={ready} />
    </group>
  );
}
