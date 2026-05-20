"use client";

import { Canvas } from "@react-three/fiber";
import { Environment, useProgress } from "@react-three/drei";
import { Suspense, useEffect } from "react";
import Khue from "./Khue";
import VideoPlane from "./VideoPlane";
import CameraRig from "./CameraRig";

export default function KhueScene({
  videoPlay,
  onVideoReady,
  onVideoProgress,
  onAssetsProgress,
}: {
  videoPlay: boolean;
  onVideoReady: () => void;
  onVideoProgress: (fraction: number) => void;
  onAssetsProgress: (fraction: number) => void;
}) {
  // The GLB gate model and the environment HDR both load through three's
  // default loading manager — useProgress reports their combined progress.
  const { progress, total } = useProgress();
  useEffect(() => {
    onAssetsProgress(total > 0 ? progress / 100 : 0);
  }, [progress, total, onAssetsProgress]);

  return (
    <Canvas
      gl={{ alpha: true, antialias: true, preserveDrawingBuffer: false }}
      camera={{ position: [0, 0.62, 0.32], fov: 42, near: 0.01, far: 50 }}
      style={{ background: "transparent" }}
      dpr={[1, 2]}
      shadows
      onCreated={({ gl }) => {
        // Needed so the gate model's clipping plane (hides the back roof) works.
        gl.localClippingEnabled = true;
      }}
    >
      <VideoPlane
        play={videoPlay}
        onReady={onVideoReady}
        onProgress={onVideoProgress}
      />

      <Suspense fallback={null}>
        <Khue />
        <Environment preset="sunset" environmentIntensity={0.55} />
      </Suspense>

      {/* warm key */}
      <directionalLight
        position={[3, 4, 2]}
        intensity={1.6}
        color={"#ffd9a8"}
        castShadow
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
      />
      {/* cool fill */}
      <directionalLight position={[-2, 2, -1]} intensity={0.35} color={"#9ab0d8"} />
      {/* warm rim from behind */}
      <directionalLight position={[0, 2, -3]} intensity={0.8} color={"#ff9a5a"} />
      <ambientLight intensity={0.18} />

      <CameraRig />
    </Canvas>
  );
}
