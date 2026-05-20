"use client";

import dynamic from "next/dynamic";
import { useEffect, useRef, useState } from "react";
import { scrollProgress, clamp, easeInOut, mapRange } from "@/lib/scroll";
import { cameraPoses } from "@/lib/cameraPoses";
import CameraTuner from "./CameraTuner";

// R3F Canvas is browser-only — never SSR it.
const KhueScene = dynamic(() => import("./KhueScene"), { ssr: false });

export default function Stage() {
  const stageRef = useRef<HTMLDivElement>(null);
  // Lets the "Cuộn xuống" cue trigger the same guided glide as a wheel-down.
  const glideRef = useRef<() => void>(() => {});

  useEffect(() => {
    // A scrollytelling page should always open at the top.
    if ("scrollRestoration" in history) history.scrollRestoration = "manual";
    window.scrollTo(0, 0);
  }, []);

  useEffect(() => {
    const html = document.documentElement;

    // p = 1 lands at 80% of the scrollable range — the scroll Y where
    // Section 2 fully settles.
    const landingY = () => {
      const el = stageRef.current;
      if (!el) return 0;
      return (el.offsetHeight - window.innerHeight) * 0.8;
    };

    // ── Forward navigation is a guided glide; backward is free scrubbing ──
    // Scroll down (or click) in Section 1 → the camera auto-animates all the
    // way to Section 2. Scroll up at any time → full manual control.
    let gliding = false;
    let glideRAF = 0;

    const glideTo = (targetY: number) => {
      cancelAnimationFrame(glideRAF);
      const startY = window.scrollY;
      const dist = targetY - startY;
      if (Math.abs(dist) < 2) {
        gliding = false;
        return;
      }
      gliding = true;
      // glideDuration (s) covers the full Section 1 → 2 journey; a partial
      // glide takes proportionally less time.
      const full = Math.max(1, landingY());
      const seconds = cameraPoses.glideDuration || 3;
      const dur = Math.max(
        300,
        seconds * 1000 * Math.min(1, Math.abs(dist) / full),
      );
      const t0 = performance.now();
      const tick = (now: number) => {
        if (!gliding) return;
        const t = Math.min(1, (now - t0) / dur);
        // easeInOutCubic — slow start, fast middle, slow end.
        const e = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
        window.scrollTo(0, startY + dist * e);
        if (t < 1) glideRAF = requestAnimationFrame(tick);
        else gliding = false;
      };
      glideRAF = requestAnimationFrame(tick);
    };
    const cancelGlide = () => {
      gliding = false;
      cancelAnimationFrame(glideRAF);
    };

    const onScroll = () => {
      const el = stageRef.current;
      if (!el) return;
      const rect = el.getBoundingClientRect();
      const total = (rect.height - window.innerHeight) * 0.8;
      const p = clamp(-rect.top / total);
      scrollProgress.value = p;

      // --p-hide (hero text) stays scroll-driven. --p-panel (Section-2 photo
      // + cards) is driven on a timer inside <VideoPlane/> instead, so it
      // can't be left half-faded by a mid-scroll stop.
      const pHide = easeInOut(mapRange(p, 0.06, 0.26));
      html.style.setProperty("--p",      p.toFixed(4));
      html.style.setProperty("--p-hide", pHide.toFixed(4));
    };

    const onWheel = (e: WheelEvent) => {
      const p = scrollProgress.value;
      if (e.deltaY > 0) {
        // Downward intent → guided glide to Section 2.
        if (p < 0.97) {
          e.preventDefault();
          if (!gliding) glideTo(landingY());
        }
        // p ≥ 0.97 → let the native scroll carry on past Section 2.
      } else if (e.deltaY < 0) {
        // Upward intent → hand back full manual control.
        if (gliding) cancelGlide();
      }
    };

    // Exposed to the "Cuộn xuống" cue button.
    glideRef.current = () => {
      if (!gliding && scrollProgress.value < 0.97) glideTo(landingY());
    };

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("wheel", onWheel, { passive: false });
    onScroll();
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("wheel", onWheel);
      cancelAnimationFrame(glideRAF);
    };
  }, []);

  return (
    <>
      <Frame />
      {process.env.NODE_ENV === "development" && <CameraTuner />}

      <section
        ref={stageRef}
        id="khue-stage"
        className="relative"
        style={{ height: "500vh" }}
      >
        <div className="sticky top-0 h-screen w-full overflow-hidden bg-ink">
          {/* ─── LAYER 1 · atmospheric backdrop ───
              The video is no longer a full-bleed background — it lives inside
              the 3D scene as a plane behind the gate's window. This dark warm
              field is what sits *around* the gate. */}
          <div
            className="absolute inset-0"
            style={{
              background:
                "radial-gradient(ellipse 70% 55% at 50% 42%, #3a221a 0%, #211711 45%, #14110d 80%)",
            }}
          />

          {/* fine grain / vignette for depth */}
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              background:
                "radial-gradient(ellipse at 50% 40%, transparent 46%, rgba(20,17,13,0.7) 100%)," +
                "linear-gradient(180deg, rgba(20,17,13,0.35) 0%, transparent 22%, transparent 74%, rgba(20,17,13,0.9) 100%)",
            }}
          />

          {/* section-2 scrim — deepens the lower third so the cards read */}
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              opacity: "var(--p-panel, 0)",
              background:
                "linear-gradient(180deg, transparent 0%, transparent 44%, rgba(20,17,13,0.55) 74%, rgba(20,17,13,0.82) 100%)",
            }}
          />

          {/* ─── LAYER 2 · 3D model (transparent canvas over video) ─── */}
          <div className="absolute inset-0">
            <KhueScene />
          </div>

          {/* ─── LAYER 2.5 · Section-2 real photo ───
              Fades in once the video has faded out — aligned (scale + nudge,
              tunable in the panel) to the 3D gate's silhouette so the model
              dissolves seamlessly into the real Khuê Văn Các. */}
          <div
            data-photo
            className="absolute inset-0 pointer-events-none"
            style={{
              opacity: "var(--p-photo, 0)",
              backgroundImage: "url(/khue-real.jpg)",
              backgroundRepeat: "no-repeat",
              backgroundPosition: "center",
              backgroundSize: "cover",
              transformOrigin: "center",
              transform:
                "scale(var(--photo-scale, 1)) translate(var(--photo-x, 0%), var(--photo-y, 0%))",
            }}
          />
          {/* photo bottom-vignette so the CTA cards keep their contrast */}
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              opacity: "var(--p-photo, 0)",
              background:
                "linear-gradient(180deg, rgba(20,17,13,0.32) 0%, transparent 26%, transparent 56%, rgba(20,17,13,0.62) 82%, rgba(20,17,13,0.86) 100%)",
            }}
          />

          {/* ─── LAYER 3 · hero text (fades during phase 0) ─── */}
          <div
            className="absolute inset-0 grid place-items-center text-center pointer-events-none"
            style={{
              opacity: "calc(1 - var(--p-hide, 0))",
              transform: "translateY(calc(var(--p-hide, 0) * -2vh))",
            }}
          >
            {/* soft dark halo so the text holds up over a bright video */}
            <div
              className="absolute pointer-events-none"
              style={{
                width: "min(900px, 96vw)",
                height: "min(620px, 70vh)",
                background:
                  "radial-gradient(ellipse at center, rgba(20,17,13,0.78) 0%, rgba(20,17,13,0.42) 45%, transparent 72%)",
                opacity: "calc(1 - var(--p-hide, 0))",
              }}
            />
            <div
              className="hero-intro relative px-6"
              style={{
                maxWidth: "min(860px, 92vw)",
                fontFamily: "var(--font-montserrat), system-ui, sans-serif",
              }}
            >
              <p
                className="inline-flex items-center gap-3 mb-7 text-paper-dim uppercase"
                style={{ fontSize: 11, letterSpacing: "0.34em" }}
              >
                <span className="block w-10 h-px bg-current opacity-60" />
                Di tích quốc gia đặc biệt
                <span className="block w-10 h-px bg-current opacity-60" />
              </p>

              <h1
                className="m-0 text-paper uppercase"
                style={{
                  fontFamily: "var(--font-montserrat), sans-serif",
                  fontWeight: 800,
                  lineHeight: 1.02,
                  letterSpacing: "0.005em",
                  fontSize: "clamp(40px, 8vw, 104px)",
                  textShadow: "0 6px 36px rgba(0,0,0,0.6)",
                }}
              >
                Văn Miếu
                <span
                  className="block text-vermillion"
                  style={{
                    fontWeight: 600,
                    fontSize: "0.6em",
                    letterSpacing: "0.045em",
                    marginTop: "0.08em",
                  }}
                >
                  Quốc Tử Giám
                </span>
              </h1>

              <p
                className="mx-auto mt-6 text-paper-dim"
                style={{
                  fontFamily: "var(--font-montserrat), sans-serif",
                  fontSize: "clamp(13px, 1.35vw, 16px)",
                  fontWeight: 400,
                  lineHeight: 1.5,
                  maxWidth: 560,
                  letterSpacing: "0.01em",
                }}
              >
                Trường đại học đầu tiên của Việt Nam — nơi đạo học nghìn năm
                vẫn còn vẹn nguyên giữa lòng Hà Nội.
              </p>

              <div
                className="mx-auto mt-9 grid grid-cols-3"
                style={{ maxWidth: 540 }}
              >
                <Stat value="1070" label="Năm khởi dựng" />
                <Stat value="1304" label="Vị tiến sĩ đề danh" divider />
                <Stat value="Hàng triệu" label="Lượt khách mỗi năm" divider />
              </div>
            </div>
          </div>

          {/* ─── LAYER 4 · scroll cue (click to glide into Section 2) ─── */}
          <button
            type="button"
            onClick={() => glideRef.current()}
            data-no-glide
            className="scroll-cue-btn absolute left-1/2 -translate-x-1/2 bottom-9 flex flex-col items-center gap-3.5 text-paper-dim uppercase cursor-pointer bg-transparent border-0"
            style={{
              fontSize: 10,
              letterSpacing: "0.42em",
              opacity: "calc(1 - var(--p-hide, 0) * 1.5)",
            }}
          >
            <span>Cuộn xuống</span>
            <span className="scroll-line" />
          </button>

          {/* ─── LAYER 5 · approach panel (section 2 lands here) ─── */}
          <Approach />
        </div>
      </section>
    </>
  );
}

/* ──────────────────────────────────────────────────────────────────────── */

function Stat({
  value,
  label,
  divider,
}: {
  value: string;
  label: string;
  divider?: boolean;
}) {
  return (
    <div
      className="flex flex-col items-center text-center px-2"
      style={
        divider
          ? { borderLeft: "1px solid rgba(245,237,225,0.16)" }
          : undefined
      }
    >
      <span
        className="text-paper"
        style={{
          fontFamily: "var(--font-montserrat), sans-serif",
          fontWeight: 700,
          fontSize: "clamp(18px, 2vw, 26px)",
          lineHeight: 1,
        }}
      >
        {value}
      </span>
      <span
        className="uppercase text-paper-dim"
        style={{
          marginTop: 8,
          fontFamily: "var(--font-montserrat), sans-serif",
          fontSize: 9.5,
          letterSpacing: "0.14em",
          fontWeight: 500,
        }}
      >
        {label}
      </span>
    </div>
  );
}

/* ──────────────────────────────────────────────────────────────────────── */

const NAV_LINKS = ["Tham quan", "Di tích", "Trưng bày", "Các hoạt động", "Dịch vụ"];

function LogoMark({ height = 30 }: { height?: number }) {
  // The source artwork only fills a portrait slice of its 140×140 canvas —
  // this viewBox is cropped tight to the glyph so it fills the badge.
  return (
    <svg
      width={height * 0.506}
      height={height}
      viewBox="42.7 16 54.7 108"
      fill="currentColor"
      aria-hidden
    >
      <g transform="matrix(1,0,0,1,0,-942)">
        <g transform="matrix(1.044776,0,0,0.751982,269.552239,266.099147)">
          <g transform="matrix(0.957143,0,0,1.329818,-190.302243,994.851051)">
            <path d="M2.826,-4.771L-4.283,-4.771C-5.557,-4.771 -6.589,-3.738 -6.589,-2.464C-6.589,-1.19 -5.557,-0.158 -4.283,-0.158L2.826,-0.158C4.1,-0.158 5.133,-1.19 5.133,-2.465C5.133,-3.738 4.1,-4.771 2.826,-4.771ZM-21.712,47.79C-20.438,47.79 -19.406,46.758 -19.406,45.484L-19.406,12.988L-3.036,12.988L-3.036,45.481C-3.036,46.755 -2.004,47.788 -0.73,47.788C0.544,47.788 1.577,46.755 1.577,45.481L1.577,12.988L17.948,12.988L17.948,45.484C17.948,46.758 18.981,47.79 20.255,47.79C21.53,47.79 22.562,46.758 22.562,45.484L22.562,10.682C22.562,9.408 21.53,8.375 20.255,8.375L-21.712,8.375C-22.987,8.375 -24.02,9.408 -24.02,10.682L-24.02,45.484C-24.02,46.758 -22.987,47.79 -21.712,47.79M-23.524,-48.572C-24.228,-49.779 -23.907,-51.278 -22.806,-51.919C-21.705,-52.561 -20.243,-52.102 -19.539,-50.894L-16.854,-46.29L-0.728,-18.62L15.398,-46.29L18.081,-50.894C18.784,-52.102 20.248,-52.561 21.349,-51.919C22.45,-51.278 22.771,-49.779 22.068,-48.572L20.658,-46.154L4.114,-17.767L1.431,-13.163C1.175,-12.723 0.816,-12.386 0.413,-12.162C0.401,-12.155 0.393,-12.145 0.381,-12.138C0.035,-11.937 -0.346,-11.855 -0.728,-11.859C-1.11,-11.855 -1.491,-11.937 -1.837,-12.138C-1.85,-12.145 -1.858,-12.155 -1.87,-12.162C-2.273,-12.386 -2.631,-12.723 -2.887,-13.163L-5.571,-17.767L-22.115,-46.154L-23.524,-48.572Z" />
          </g>
        </g>
      </g>
    </svg>
  );
}

function Frame() {
  // Tier 1 (utility bar) collapses while scrolling down; Tier 2 (main nav)
  // stays sticky. Always revealed when parked at the very top.
  const [utilHidden, setUtilHidden] = useState(false);

  useEffect(() => {
    let last = window.scrollY;
    const onScroll = () => {
      const y = window.scrollY;
      if (y < 40) setUtilHidden(false);
      else if (y > last + 4) setUtilHidden(true);
      else if (y < last - 4) setUtilHidden(false);
      last = y;
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className="fixed top-0 inset-x-0 z-30"
      style={{
        background: "rgba(20,17,13,0.58)",
        backdropFilter: "blur(20px) saturate(1.35)",
        WebkitBackdropFilter: "blur(20px) saturate(1.35)",
        borderBottom: "1px solid rgba(245,237,225,0.1)",
        fontFamily: "var(--font-montserrat), system-ui, sans-serif",
      }}
    >
      {/* ── Tier 1 · utility bar (solid bar, collapses on scroll-down) ── */}
      <div
        style={{
          height: utilHidden ? 0 : 40,
          opacity: utilHidden ? 0 : 1,
          overflow: "hidden",
          background: "var(--color-ink)",
          transition:
            "height 320ms cubic-bezier(0.4,0,0.2,1), opacity 200ms ease",
        }}
      >
        <div
          className="flex items-center justify-between"
          style={{
            height: 40,
            padding: "0 clamp(20px, 4vw, 48px)",
            borderBottom: "1px solid rgba(245,237,225,0.07)",
          }}
        >
          <div
            className="flex items-center gap-2 text-paper-dim"
            style={{ fontSize: 12 }}
          >
            <svg
              width="13"
              height="13"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth={1.7}
            >
              <circle cx="12" cy="12" r="9" />
              <path d="M12 7.5V12l3 1.8" />
            </svg>
            <span>Giờ mở cửa hôm nay</span>
            <span style={{ color: "var(--color-gold)" }}>
              (Mở cửa: 08:00 – 17:00)
            </span>
          </div>

          <div className="flex items-center gap-4">
            <div
              className="hidden lg:flex items-center gap-2"
              style={{
                height: 28,
                padding: "0 12px",
                borderRadius: 999,
                border: "1px solid rgba(245,237,225,0.18)",
                background: "rgba(245,237,225,0.05)",
              }}
            >
              <svg
                width="13"
                height="13"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth={1.8}
                className="text-paper-dim shrink-0"
              >
                <circle cx="11" cy="11" r="7" />
                <path d="M21 21l-4.3-4.3" />
              </svg>
              <input
                placeholder="Tìm kiếm di tích, hiện vật, sự kiện…"
                className="bg-transparent border-0 outline-none text-paper"
                style={{ fontSize: 12, width: 230 }}
              />
            </div>

            <span
              className="hidden lg:block"
              style={{
                width: 1,
                height: 16,
                background: "rgba(245,237,225,0.18)",
              }}
            />

            <div className="flex items-center gap-3" style={{ fontSize: 12 }}>
              <button
                type="button"
                className="hdr-link flex items-center gap-1.5 text-paper bg-transparent border-0 cursor-pointer"
                style={{ fontWeight: 600 }}
              >
                <span style={{ fontSize: 13 }}>🇻🇳</span> VI
              </button>
              <button
                type="button"
                className="hdr-link flex items-center gap-1.5 text-paper-dim bg-transparent border-0 cursor-pointer"
              >
                <span style={{ fontSize: 13 }}>🇬🇧</span> EN
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* ── Tier 2 · main navigation (sticky) ── */}
      <div
        className="flex items-center justify-between"
        style={{ height: 72, padding: "0 clamp(20px, 4vw, 48px)" }}
      >
        <a href="#" className="flex items-center gap-3 no-underline shrink-0">
          <span
            className="grid place-items-center shrink-0"
            style={{
              width: 46,
              height: 46,
              borderRadius: "50%",
              background: "var(--color-vermillion)",
              color: "var(--color-paper)",
              boxShadow: "0 4px 16px rgba(199,88,50,0.4)",
            }}
          >
            <LogoMark height={30} />
          </span>
          <span className="leading-tight">
            <span
              className="block text-paper"
              style={{
                fontSize: 18,
                fontWeight: 700,
                letterSpacing: "0.005em",
              }}
            >
              Văn Miếu
            </span>
            <span
              className="block text-paper-dim uppercase"
              style={{ fontSize: 9.5, letterSpacing: "0.14em", marginTop: 2 }}
            >
              Quốc Tử Giám · 1070
            </span>
          </span>
        </a>

        <nav
          className="hidden md:flex items-center gap-7"
          style={{ fontSize: 13.5 }}
        >
          {NAV_LINKS.map((label, i) => (
            <a
              key={label}
              href="#"
              className="hdr-link no-underline relative"
              style={{
                color: i === 0 ? "var(--color-paper)" : "var(--color-paper-dim)",
                fontWeight: i === 0 ? 600 : 400,
              }}
            >
              {label}
              {i === 0 && (
                <span
                  style={{
                    position: "absolute",
                    left: 0,
                    right: 0,
                    bottom: -8,
                    height: 2,
                    background: "var(--color-vermillion)",
                    borderRadius: 2,
                  }}
                />
              )}
            </a>
          ))}
        </nav>

        <a
          href="#"
          className="hdr-cta flex items-center gap-2 no-underline text-paper shrink-0"
          style={{
            background: "var(--color-vermillion)",
            padding: "10px 22px",
            borderRadius: 999,
            fontSize: 13.5,
            fontWeight: 600,
          }}
        >
          Mua Vé
          <svg
            width="15"
            height="9"
            viewBox="0 0 18 8"
            fill="none"
            stroke="currentColor"
            strokeWidth={1.7}
          >
            <path d="M0 4h16M12 1l4 3-4 3" />
          </svg>
        </a>
      </div>
    </header>
  );
}

/* ──────────────────────────────────────────────────────────────────────── */

function Approach() {
  return (
    <div
      className="absolute inset-0 z-10 flex items-center justify-between gap-8 pointer-events-none"
      style={{
        padding: "clamp(40px, 6vw, 80px) clamp(24px, 5vw, 72px)",
        opacity: "var(--p-panel, 0)",
      }}
    >
      <h2
        className="m-0 text-paper"
        style={{
          fontFamily: "var(--font-montserrat), sans-serif",
          fontWeight: 700,
          fontSize: "clamp(30px, 4.7vw, 62px)",
          lineHeight: 1.1,
          letterSpacing: "-0.01em",
          maxWidth: "13ch",
          textShadow: "0 8px 30px rgba(0,0,0,0.5)",
          transform: "translateY(calc((1 - var(--p-panel, 0)) * 40px))",
        }}
      >
        <span className="text-vermillion" style={{ fontWeight: 800 }}>
          Cái nôi đạo học
        </span>{" "}
        của kinh kỳ ngàn năm tuổi
      </h2>

      <div
        className="flex flex-col gap-3 pointer-events-auto shrink-0"
        style={{ width: "clamp(300px, 26vw, 358px)" }}
      >
          <QCard
            i={0}
            num="I."
            han="Tickets"
            title="Mua vé nhanh"
            desc="Vé phổ thông, vé đoàn và vé trải nghiệm số — đặt trước 15 phút."
            cta="Đặt vé"
            icon={
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.4}>
                <path d="M3 9h18M3 9v9a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9M3 9V7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v2M8 5V3M16 5V3" />
              </svg>
            }
          />
          <QCard
            i={1}
            num="II."
            han="Heritage"
            title="Di tích"
            desc="Năm khu sân thiêng, 82 bia tiến sĩ và bản đồ tương tác đa lớp."
            cta="Khám phá"
            icon={
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.4}>
                <path d="M4 21V8l8-5 8 5v13M9 21v-7h6v7M9 11h.01M15 11h.01" />
              </svg>
            }
          />
          <QCard
            i={2}
            num="III."
            han="Events"
            title="Sự kiện"
            desc="Lễ vinh danh thủ khoa, đêm thư pháp, trình diễn nhạc cung đình."
            cta="Lịch tháng này"
            icon={
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.4}>
                <path d="M3 6h18M6 6v14a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V6M9 6V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M10 11l2 2 4-4" />
              </svg>
            }
          />
      </div>
    </div>
  );
}

function QCard({
  i,
  num,
  han,
  title,
  desc,
  cta,
  icon,
}: {
  i: number;
  num: string;
  han: string;
  title: string;
  desc: string;
  cta: string;
  icon: React.ReactNode;
}) {
  return (
    <a
      href="#"
      className="qcard group relative block p-[22px] pb-6 text-paper no-underline overflow-hidden"
      style={
        {
          background: "rgba(20,17,13,0.55)",
          backdropFilter: "blur(10px) saturate(1.1)",
          border: "1px solid rgba(245,237,225,0.12)",
          transition: "transform 320ms cubic-bezier(0.22,0.61,0.36,1), border-color 320ms, background 320ms",
          transform: `translateY(calc((1 - var(--p-panel, 0)) * (40px + ${i} * 18px)))`,
        } as React.CSSProperties
      }
    >
      <div className="absolute top-[22px] right-[22px] w-7 h-7 text-paper-dim transition-colors group-hover:text-vermillion">
        {icon}
      </div>
      <span
        className="font-display italic text-vermillion"
        style={{ fontSize: 13, letterSpacing: "0.2em" }}
      >
        {num}
      </span>
      <div className="mt-6 font-display italic text-paper" style={{ fontSize: "clamp(22px, 2vw, 28px)", lineHeight: 1.05 }}>
        <span
          className="block not-italic text-paper-dim uppercase mb-2"
          style={{ fontSize: 12, letterSpacing: "0.42em", fontFamily: "var(--font-sans)" }}
        >
          {han}
        </span>
        {title}
      </div>
      <p className="mt-3 text-paper-dim" style={{ fontSize: 13, lineHeight: 1.55 }}>
        {desc}
      </p>
      <span
        className="mt-5 inline-flex items-center gap-2.5 uppercase text-paper"
        style={{ fontSize: 11, letterSpacing: "0.4em" }}
      >
        {cta}
        <svg
          viewBox="0 0 18 8"
          fill="none"
          stroke="currentColor"
          strokeWidth={1.4}
          className="w-[18px] h-2 transition-transform group-hover:translate-x-1.5"
        >
          <path d="M0 4h17M13 1l4 3-4 3" />
        </svg>
      </span>
    </a>
  );
}
