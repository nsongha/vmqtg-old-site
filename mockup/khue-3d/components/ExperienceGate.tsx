"use client";

import { useEffect, useState } from "react";
import Stage from "./Stage";
import MobileNotice from "./MobileNotice";
import Preloader from "./Preloader";

// Phones and small touch devices can't drive the wheel-guided scroll journey,
// so they get a notice instead — and none of the 3D / video payload loads.
function isMobileDevice(): boolean {
  const ua = /Android|iPhone|iPod|webOS|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent,
  );
  const coarse = window.matchMedia("(pointer: coarse)").matches;
  return ua || (coarse && window.innerWidth < 1024);
}

export default function ExperienceGate() {
  const [device, setDevice] = useState<"unknown" | "mobile" | "desktop">(
    "unknown",
  );

  useEffect(() => {
    setDevice(isMobileDevice() ? "mobile" : "desktop");
  }, []);

  if (device === "mobile") return <MobileNotice />;
  // <Stage/> only mounts once desktop is confirmed — so the GLB, the HDR and
  // the hero video are never fetched on a phone.
  if (device === "desktop") return <Stage />;
  // First paint, before detection resolves — the neutral loading veil hands
  // off seamlessly into <Stage/>'s own preloader on desktop.
  return <Preloader progress={0} done={false} />;
}
