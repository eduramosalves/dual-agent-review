"""Render assets/cross-review-flow.mp4 from the same frames as the GIF, honoring each frame's
hold time. MP4 autoplays reliably on social feeds (LinkedIn/X) where GIF animation is flaky.

Run:  python assets/make_flow_mp4.py
Requires: imageio, imageio-ffmpeg (pip install imageio imageio-ffmpeg)
"""

from __future__ import annotations

import imageio.v2 as imageio
import numpy as np

import make_flow_gif as g

FPS = 30
LOOPS = 2  # repeat the whole cycle so feed viewers catch the start


def build():
    frames, durations = g.build_frames()
    out = g.Path(__file__).with_name("cross-review-flow.mp4")

    writer = imageio.get_writer(
        out, fps=FPS, codec="libx264", quality=8,
        macro_block_size=2,  # keep exact 960x540 (height not divisible by 8); even dims OK for yuv420p
        ffmpeg_params=["-pix_fmt", "yuv420p"],  # broad player compatibility
    )
    for _ in range(LOOPS):
        for img, dur_ms in zip(frames, durations):
            arr = np.asarray(img.convert("RGB"))
            for _f in range(max(1, round(dur_ms / 1000 * FPS))):
                writer.append_data(arr)
    writer.close()
    print(f"wrote {out}  ({LOOPS} loops @ {FPS}fps)")


if __name__ == "__main__":
    build()
