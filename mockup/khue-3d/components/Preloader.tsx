"use client";

import LogoMark from "./LogoMark";

/**
 * Full-screen branded loading gate. Held over the scene until the hero video,
 * the 3D gate model and its lighting are all decoded — so the experience is
 * never scrolled while it is still empty.
 */
export default function Preloader({
  progress,
  done,
}: {
  progress: number; // 0 → 1
  done: boolean;
}) {
  const pct = Math.round(Math.min(1, Math.max(0, progress)) * 100);

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 200,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "var(--color-ink)",
        color: "var(--color-paper)",
        fontFamily: "var(--font-montserrat), system-ui, sans-serif",
        opacity: done ? 0 : 1,
        transition: "opacity 600ms ease",
        pointerEvents: done ? "none" : "auto",
      }}
    >
      <div className="preloader-pulse" style={{ color: "var(--color-vermillion)" }}>
        <LogoMark height={58} />
      </div>

      <div style={{ marginTop: 20, textAlign: "center" }}>
        <div style={{ fontSize: 20, fontWeight: 700, letterSpacing: "0.02em" }}>
          Văn Miếu
        </div>
        <div
          className="uppercase"
          style={{
            fontSize: 10,
            letterSpacing: "0.24em",
            color: "var(--color-paper-dim)",
            marginTop: 5,
          }}
        >
          Quốc Tử Giám
        </div>
      </div>

      <div
        style={{
          marginTop: 36,
          width: 208,
          height: 2,
          background: "rgba(245,237,225,0.14)",
          borderRadius: 2,
          overflow: "hidden",
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${pct}%`,
            background: "var(--color-vermillion)",
            transition: "width 260ms ease",
          }}
        />
      </div>

      <div
        className="uppercase"
        style={{
          marginTop: 13,
          fontSize: 10,
          letterSpacing: "0.18em",
          color: "var(--color-paper-dim)",
        }}
      >
        Đang tải trải nghiệm · {pct}%
      </div>
    </div>
  );
}
