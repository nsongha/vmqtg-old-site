"use client";

import { useEffect, useState } from "react";
import { cameraPoses, resetPoses } from "@/lib/cameraPoses";

/**
 * Dev-only panel to live-tune the Section 1 / Section 2 camera poses
 * (Y + Z only) plus the video-plane and gate-model depth. Writes straight
 * into the cameraPoses object that the R3F components read every frame.
 */
export default function CameraTuner() {
  // Hidden by default — summon with Alt+Shift+C (Option+Shift+C on Mac).
  const [open, setOpen] = useState(false);
  const [v, setV] = useState({ ...cameraPoses });
  const [copied, setCopied] = useState(false);

  // Browsers restore stale <input type=range> values across reloads, which
  // fires spurious onChange events. Re-assert the defaults after mount.
  useEffect(() => {
    setV(resetPoses());
    const t = setTimeout(() => setV(resetPoses()), 250);
    return () => clearTimeout(t);
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.altKey && e.shiftKey && e.code === "KeyC") {
        e.preventDefault();
        setOpen((o) => !o);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const set = (key: keyof typeof cameraPoses, value: number) => {
    cameraPoses[key] = value;
    setV((s) => ({ ...s, [key]: value }));
  };

  const jump = (where: "s1" | "s2") => {
    const stage = document.getElementById("khue-stage");
    if (!stage) return;
    if (where === "s1") {
      window.scrollTo(0, 0);
    } else {
      const total = (stage.offsetHeight - window.innerHeight) * 0.8;
      window.scrollTo(0, Math.round(total) + 8);
    }
  };

  const copy = () => {
    const txt =
      `insideY: ${v.insideY}, insideZ: ${v.insideZ},\n` +
      `heroY: ${v.heroY}, heroZ: ${v.heroZ},\n` +
      `videoZ: ${v.videoZ}, modelZ: ${v.modelZ}, clipZ: ${v.clipZ},\n` +
      `glideDuration: ${v.glideDuration},\n` +
      `photoScale: ${v.photoScale}, photoX: ${v.photoX}, photoY: ${v.photoY},`;
    navigator.clipboard?.writeText(txt);
    setCopied(true);
    setTimeout(() => setCopied(false), 1400);
  };

  if (!open) return null;

  return (
    <div style={panel} data-no-glide>
      <div style={head}>
        <span style={{ letterSpacing: "0.18em" }}>CAMERA TUNER</span>
        <button onClick={() => setOpen(false)} style={btnX}>
          ✕
        </button>
      </div>

      <Group label="Section 1 · ô cửa">
        <Slider
          label="Cao (Y)"
          min={0.2}
          max={1.1}
          step={0.001}
          value={v.insideY}
          onChange={(n) => set("insideY", n)}
        />
        <Slider
          label="Xa (Z)"
          min={-0.13}
          max={2.5}
          step={0.001}
          value={v.insideZ}
          onChange={(n) => set("insideZ", n)}
        />
        <button onClick={() => jump("s1")} style={btnJump}>
          → xem Section 1
        </button>
      </Group>

      <Group label="Section 2 · cổng + thẻ">
        <Slider
          label="Cao (Y)"
          min={0}
          max={1.6}
          step={0.001}
          value={v.heroY}
          onChange={(n) => set("heroY", n)}
        />
        <Slider
          label="Xa (Z)"
          min={0.5}
          max={8}
          step={0.001}
          value={v.heroZ}
          onChange={(n) => set("heroZ", n)}
        />
        <button onClick={() => jump("s2")} style={btnJump}>
          → xem Section 2
        </button>
      </Group>

      <Group label="Chiều sâu cảnh (Z)">
        <Slider
          label="Video"
          min={-0.7}
          max={0.15}
          step={0.001}
          value={v.videoZ}
          onChange={(n) => set("videoZ", n)}
        />
        <Slider
          label="Cổng 3D"
          min={-1}
          max={2.6}
          step={0.001}
          value={v.modelZ}
          onChange={(n) => set("modelZ", n)}
        />
        <Slider
          label="Cắt mái"
          min={-0.5}
          max={0.3}
          step={0.001}
          value={v.clipZ}
          onChange={(n) => set("clipZ", n)}
        />
      </Group>

      <Group label="Animation · glide Section 1 → 2">
        <Slider
          label="Giây"
          min={0.5}
          max={6}
          step={0.1}
          value={v.glideDuration}
          onChange={(n) => set("glideDuration", n)}
        />
      </Group>

      <Group label="Ảnh Section 2 · căn với cổng 3D">
        <Slider
          label="Phóng"
          min={0.5}
          max={3}
          step={0.001}
          value={v.photoScale}
          onChange={(n) => set("photoScale", n)}
        />
        <Slider
          label="Ngang X"
          min={-50}
          max={50}
          step={0.1}
          value={v.photoX}
          onChange={(n) => set("photoX", n)}
        />
        <Slider
          label="Dọc Y"
          min={-50}
          max={50}
          step={0.1}
          value={v.photoY}
          onChange={(n) => set("photoY", n)}
        />
      </Group>

      <button onClick={copy} style={btnCopy}>
        {copied ? "✓ Đã copy" : "Copy giá trị"}
      </button>
    </div>
  );
}

/* ── sub-components ─────────────────────────────────────────────── */

function Group({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div style={group}>
      <div style={groupLabel}>{label}</div>
      {children}
    </div>
  );
}

function Slider({
  label,
  min,
  max,
  step,
  value,
  unit,
  onChange,
}: {
  label: string;
  min: number;
  max: number;
  step: number;
  value: number;
  unit?: string;
  onChange: (n: number) => void;
}) {
  return (
    <label style={row}>
      <span style={rowLabel}>
        {label}
        {unit ? <span style={{ opacity: 0.55 }}> {unit}</span> : null}
      </span>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        autoComplete="off"
        onChange={(e) => onChange(parseFloat(e.target.value))}
        style={range}
      />
      {/* step="any" → the typed value is never re-rounded, so an exact
          position can be entered by hand. */}
      <input
        type="number"
        min={min}
        max={max}
        step="any"
        value={value}
        autoComplete="off"
        onChange={(e) => onChange(parseFloat(e.target.value) || 0)}
        style={num}
      />
    </label>
  );
}

/* ── inline styles (dev tool — kept self-contained) ─────────────── */

const panel: React.CSSProperties = {
  position: "fixed",
  top: 128,
  right: 16,
  zIndex: 90,
  width: 252,
  padding: "14px 14px 16px",
  background: "rgba(20,17,13,0.92)",
  backdropFilter: "blur(12px)",
  border: "1px solid rgba(199,88,50,0.4)",
  borderRadius: 4,
  color: "#f5ede1",
  fontFamily: "var(--font-sans), system-ui, sans-serif",
  fontSize: 11,
  boxShadow: "0 18px 50px rgba(0,0,0,0.55)",
};

const head: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  fontSize: 10,
  fontWeight: 600,
  color: "#e2754a",
  marginBottom: 12,
};

const group: React.CSSProperties = {
  marginBottom: 12,
  paddingBottom: 12,
  borderBottom: "1px solid rgba(245,237,225,0.1)",
};

const groupLabel: React.CSSProperties = {
  fontSize: 10,
  letterSpacing: "0.1em",
  textTransform: "uppercase",
  color: "#d8cdb9",
  marginBottom: 8,
};

const row: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  gap: 8,
  marginBottom: 7,
};

const rowLabel: React.CSSProperties = {
  width: 48,
  color: "#d8cdb9",
  flexShrink: 0,
};

const range: React.CSSProperties = {
  flex: 1,
  accentColor: "#c75832",
  height: 4,
};

const num: React.CSSProperties = {
  width: 64,
  flexShrink: 0,
  background: "rgba(245,237,225,0.08)",
  border: "1px solid rgba(245,237,225,0.16)",
  borderRadius: 3,
  color: "#f5ede1",
  fontSize: 11,
  padding: "3px 5px",
  textAlign: "right",
};

const btnJump: React.CSSProperties = {
  marginTop: 4,
  width: "100%",
  padding: "5px 0",
  background: "rgba(199,88,50,0.16)",
  border: "1px solid rgba(199,88,50,0.4)",
  borderRadius: 3,
  color: "#e2754a",
  fontSize: 10,
  letterSpacing: "0.06em",
  cursor: "pointer",
};

const btnCopy: React.CSSProperties = {
  width: "100%",
  padding: "7px 0",
  background: "#c75832",
  border: "none",
  borderRadius: 3,
  color: "#14110d",
  fontSize: 11,
  fontWeight: 600,
  letterSpacing: "0.06em",
  cursor: "pointer",
};

const btnX: React.CSSProperties = {
  background: "none",
  border: "none",
  color: "#d8cdb9",
  cursor: "pointer",
  fontSize: 12,
  lineHeight: 1,
};

