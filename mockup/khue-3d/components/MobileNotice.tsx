"use client";

import LogoMark from "./LogoMark";

/**
 * Shown instead of the experience on phones / small touch devices. The
 * scroll-driven 3D journey needs a pointer and a large viewport, so on
 * mobile nothing heavy is loaded — just this gentle note.
 */
export default function MobileNotice() {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center",
        padding: "40px 28px",
        boxSizing: "border-box",
        overflowY: "auto",
        background: "var(--color-ink)",
        color: "var(--color-paper)",
        fontFamily: "var(--font-montserrat), system-ui, sans-serif",
      }}
    >
      <div style={{ color: "var(--color-vermillion)" }}>
        <LogoMark height={50} />
      </div>

      <div style={{ marginTop: 16 }}>
        <div style={{ fontSize: 18, fontWeight: 700, letterSpacing: "0.02em" }}>
          Văn Miếu
        </div>
        <div
          className="uppercase"
          style={{
            fontSize: 9.5,
            letterSpacing: "0.24em",
            color: "var(--color-paper-dim)",
            marginTop: 4,
          }}
        >
          Quốc Tử Giám
        </div>
      </div>

      <span
        style={{
          width: 36,
          height: 1,
          background: "rgba(245,237,225,0.18)",
          margin: "30px 0",
        }}
      />

      <svg
        width="38"
        height="38"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth={1.4}
        style={{ color: "var(--color-paper-dim)" }}
      >
        <rect x="2.5" y="4" width="19" height="13" rx="1.5" />
        <path d="M9 21h6M12 17v4" />
      </svg>

      <h1
        style={{
          margin: "18px 0 0",
          fontSize: 17,
          fontWeight: 700,
          letterSpacing: "0.01em",
        }}
      >
        Trải nghiệm tối ưu trên máy tính
      </h1>

      <p
        style={{
          margin: "10px 0 0",
          maxWidth: 320,
          fontSize: 13,
          fontWeight: 400,
          lineHeight: 1.6,
          color: "var(--color-paper-dim)",
        }}
      >
        Đây là bản demo được thiết kế cho màn hình desktop. Vui lòng mở trên
        máy tính để xem trọn vẹn hành trình cuộn 3D.
      </p>
    </div>
  );
}
