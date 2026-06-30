"""Generate assets/cross-review-flow.gif — an animated, terminal-styled walkthrough of the
dual-agent cross-review cycle. Pure Pillow, no external services.

Run:  python assets/make_flow_gif.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---- palette (matches the README mermaid: teal -> violet) -------------------
BG = (13, 17, 23)            # GitHub-dark backdrop
PANEL = (22, 27, 34)
PANEL_EDGE = (48, 54, 61)
INK = (201, 209, 217)        # primary text
DIM = (110, 118, 129)        # secondary text
TEAL = (45, 212, 191)
CYAN = (34, 211, 238)
VIOLET = (167, 139, 250)
AMBER = (240, 180, 80)
GREEN = (63, 185, 80)
RED = (248, 113, 113)

W, H = 960, 540
PAD = 28

FONT_DIR = Path("C:/Windows/Fonts")


def _font(name: str, size: int) -> ImageFont.FreeTypeFont:
    for cand in (FONT_DIR / name, Path(name)):
        try:
            return ImageFont.truetype(str(cand), size)
        except OSError:
            continue
    # fallback to a Pillow-bundled TTF
    try:
        return ImageFont.truetype("DejaVuSansMono.ttf", size)
    except OSError:
        return ImageFont.load_default()


F_TITLE = _font("consolab.ttf", 26)
F_H = _font("consolab.ttf", 19)
F = _font("consola.ttf", 18)
F_SM = _font("consola.ttf", 15)


def _rrect(d: ImageDraw.ImageDraw, box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def base() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # window chrome
    _rrect(d, (PAD, PAD, W - PAD, H - PAD), 14, fill=PANEL, outline=PANEL_EDGE, width=2)
    for i, c in enumerate(((237, 106, 94), (245, 191, 79), (98, 197, 84))):
        d.ellipse((PAD + 22 + i * 26, PAD + 20, PAD + 22 + i * 26 + 13, PAD + 33), fill=c)
    d.text((PAD + 120, PAD + 18), "dual-agent-review", font=F_H, fill=DIM)
    d.line((PAD + 1, PAD + 52, W - PAD - 1, PAD + 52), fill=PANEL_EDGE, width=2)
    return img


def pill(d, x, y, text, color):
    w = d.textlength(text, font=F_SM)
    _rrect(d, (x, y, x + w + 22, y + 28), 14, outline=color, width=2)
    d.text((x + 11, y + 6), text, font=F_SM, fill=color)
    return x + w + 22


TOP_COL = PAD + 96


def actor_col(d, x, label, color, lines, active):
    top = TOP_COL
    bw = (W - 2 * PAD - 60) // 2
    box = (x, top, x + bw, H - PAD - 96)
    _rrect(d, box, 10, outline=(color if active else PANEL_EDGE), width=(3 if active else 1))
    d.text((x + 16, top + 12), label, font=F_H, fill=(color if active else DIM))
    yy = top + 48
    for txt, c in lines:
        d.text((x + 16, yy), txt, font=F, fill=c)
        yy += 26


def folder(d, status, files, status_color):
    bx = (PAD + 22, H - PAD - 82, W - PAD - 22, H - PAD - 16)
    _rrect(d, bx, 10, fill=(18, 22, 28), outline=PANEL_EDGE, width=1)
    d.text((bx[0] + 14, bx[1] + 10), ".cross-review/01-task/", font=F_H, fill=CYAN)
    x = bx[0] + 14
    for fn, c in files:
        x = pill(d, x, bx[1] + 36, fn, c) + 10
    st = f"status: {status}"
    d.text((bx[2] - d.textlength(st, font=F) - 16, bx[1] + 12), st, font=F, fill=status_color)


def frame(human, a_lines, a_active, b_lines, b_active, status, status_color, files):
    img = base()
    d = ImageDraw.Draw(img)
    d.text((PAD + 22, PAD + 60), human, font=F, fill=INK)
    lx = PAD + 22
    rx = PAD + 22 + (W - 2 * PAD - 60) // 2 + 36
    actor_col(d, lx, "Agent A  (Claude Code)", TEAL, a_lines, a_active)
    actor_col(d, rx, "Agent B  (Gemini CLI / Agy)", VIOLET, b_lines, b_active)
    folder(d, status, files, status_color)
    return img


def _ctext(d, cy, text, font, fill):
    tw = d.textlength(text, font=font)
    d.text(((W - tw) / 2, cy), text, font=font, fill=fill)


def final_frame(human, status, status_color, files):
    """Dedicated single-panel layout for the closing frame (no two columns)."""
    img = base()
    d = ImageDraw.Draw(img)
    d.text((PAD + 22, PAD + 60), human, font=F, fill=INK)

    panel = (PAD + 22, TOP_COL, W - PAD - 22, H - PAD - 96)
    _rrect(d, panel, 12, outline=GREEN, width=3)
    mid = (TOP_COL + panel[3]) / 2

    # "ACCEPTED" centered, with a hand-drawn check to its left (Consolas lacks U+2713)
    label = "ACCEPTED"
    tw = d.textlength(label, font=F_TITLE)
    tx = (W - tw) / 2
    d.text((tx, mid - 92), label, font=F_TITLE, fill=GREEN)
    cx, cy = tx - 38, mid - 78
    d.line((cx, cy, cx + 9, cy + 11), fill=GREEN, width=4)
    d.line((cx + 9, cy + 11, cx + 26, cy - 12), fill=GREEN, width=4)

    _ctext(d, mid - 50, "findings valid — fixes to apply", F_H, INK)
    _ctext(d, mid - 6, "one executes  ·  the other audits  ·  the human decides", F, DIM)

    folder(d, status, files, status_color)
    return img


def build():
    frames, durations = [], []

    # 1 - request
    frames.append(frame(
        "$ human: \"implement valida_cpf(...)\"  -> Agent A proposes roles, you confirm",
        [("• role: EXECUTOR", TEAL), ("• writing 00-request.md ...", DIM)], True,
        [("• role: REVIEWER", DIM), ("• waiting for the turn", DIM)], False,
        "proposed", AMBER, [("00-request.md", AMBER)]))
    durations.append(1700)

    # 2 - executor delivers
    frames.append(frame(
        "Agent A does the work in the code and hands off",
        [("• wrote valida_cpf.py", TEAL), ("• wrote 10-deliverable.md", TEAL),
         ("-> pass the turn to B", INK)], True,
        [("• role: REVIEWER", DIM), ("• not started yet", DIM)], False,
        "awaiting-review", AMBER,
        [("00-request.md", DIM), ("10-deliverable.md", TEAL)]))
    durations.append(1900)

    # 3 - reviewer audits
    frames.append(frame(
        "You switch terminals -> Agent B audits the deliverable + the real code",
        [("• EXECUTOR (idle)", DIM)], False,
        [("• read code + deliverable", VIOLET),
         ("• #1 blocker: all-equal digits", RED),
         ("• #2 major: loose stripping", RED),
         ("-> verdict: REQUEST-CHANGES", VIOLET)], True,
        "awaiting-user-decision", AMBER,
        [("10-deliverable.md", DIM), ("20-review.md", VIOLET)]))
    durations.append(2300)

    # 4 - human decides
    frames.append(final_frame(
        "Both views in hand, the HUMAN makes the final call",
        "closed", GREEN,
        [("20-review.md", DIM), ("99-decision.md", GREEN)]))
    durations.append(2600)

    out = Path(__file__).with_name("cross-review-flow.gif")
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=durations,
                   loop=0, optimize=True, disposal=2)
    print(f"wrote {out} ({len(frames)} frames)")


if __name__ == "__main__":
    build()
