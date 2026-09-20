import json
import os
import subprocess
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

def main():
    os.makedirs("assets/branding", exist_ok=True)
    
    with open("assets/branding/crest_normalized.json", "r") as f:
        paths = json.load(f)

    # Clean clip path for the left wings along the aerodynamic S-curve
    clip_left = (
        "M -10 -10 "
        "H 190.15 "
        "C 203.75 7.56, 223.33 35.13, 246.94 49.74 "
        "L 196.59 49.55 "
        "C 222.32 49.55, 226.54 52.68, 236.74 67.01 "
        "C 248.78 84.01, 263.30 110.20, 275.98 110.20 "
        "L 262.84 110.30 "
        "C 273.85 112.96, 280.39 124.08, 296.01 145.12 "
        "C 300.54 154.02, 309.65 159.65, 319.63 159.73 "
        "L 269.27 159.46 "
        "C 295.00 159.46, 299.23 162.58, 309.34 176.92 "
        "C 321.37 193.91, 335.98 220.10, 348.67 220.10 "
        "L 304.28 212.66 "
        "C 331.39 210.18, 342.69 224.05, 355.74 244.82 "
        "L 329.83 275.24 "
        "C 341.59 291.78, 346.73 307.03, 360.89 307.30 "
        "L 287.65 414.80 "
        "L -10 430 Z"
    )

    def get_text_path(text, family="Bahnschrift", weight="normal", size=136, baseline=545.67):
        fp = FontProperties(family=family, weight=weight)
        tp = TextPath((0, 0), text, size=size, prop=fp)
        verts = tp.vertices
        codes = tp.codes
        parts = []
        i = 0
        while i < len(codes):
            c = codes[i]
            if c == 1:
                parts.append(f"M {verts[i][0]:.2f} {baseline - verts[i][1]:.2f}")
                i += 1
            elif c == 2:
                parts.append(f"L {verts[i][0]:.2f} {baseline - verts[i][1]:.2f}")
                i += 1
            elif c == 3:
                parts.append(f"Q {verts[i][0]:.2f} {baseline - verts[i][1]:.2f}, {verts[i+1][0]:.2f} {baseline - verts[i+1][1]:.2f}")
                i += 2
            elif c == 4:
                parts.append(f"C {verts[i][0]:.2f} {baseline - verts[i][1]:.2f}, {verts[i+1][0]:.2f} {baseline - verts[i+1][1]:.2f}, {verts[i+2][0]:.2f} {baseline - verts[i+2][1]:.2f}")
                i += 3
            elif c == 79:
                parts.append("Z")
                i += 1
            else:
                i += 1
        w = max(v[0] for v in verts) - min(v[0] for v in verts)
        return " ".join(parts), w

    open_d, open_w = get_text_path("open", size=136, baseline=545.67)
    tx_voge = open_w + 16 - 49.84

    # Subtitle path
    sub_d, sub_w = get_text_path("OPEN-SOURCE TELEMETRY & CONNECTIVITY", size=26, baseline=610)

    # Reusable crest generators (transparent)
    def render_crest(color_base="#00d2ff", color_left="#ffffff", color_bottom="#ffffff", clip_id="clipLeft"):
        return f"""
        <g>
          <path d="{paths['path16']}" fill="{color_base}"/>
          <path d="{paths['path22']}" fill="{color_base}"/>
          <path d="{paths['path20']}" fill="{color_base}"/>
          <path d="{paths['path18']}" fill="{color_bottom}"/>
          <g clip-path="url(#{clip_id})">
            <path d="{paths['path16']}" fill="{color_left}"/>
            <path d="{paths['path22']}" fill="{color_left}"/>
            <path d="{paths['path20']}" fill="{color_left}"/>
          </g>
        </g>"""

    def render_voge_letters(color="#ffffff"):
        return f"""
        <g fill="{color}">
          <path d="{paths['path26']}"/>
          <path d="{paths['path28']}"/>
          <path d="{paths['path30']}"/>
          <path d="{paths['path32']}"/>
        </g>"""

    # ==========================================================
    # 1. PURE CREST (530 x 420) - 100% Transparent
    # ==========================================================
    svg_crest_light = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 530 420" width="530" height="420">
  <defs><clipPath id="clipCrest"><path d="{clip_left}"/></clipPath></defs>
  {render_crest(color_base="#00d2ff", color_left="#ffffff", color_bottom="#ffffff", clip_id="clipCrest")}
</svg>"""
    with open("assets/branding/openvoge-crest.svg", "w", encoding="utf-8") as f:
        f.write(svg_crest_light)

    svg_crest_dark = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 530 420" width="530" height="420">
  <defs><clipPath id="clipCrestD"><path d="{clip_left}"/></clipPath></defs>
  {render_crest(color_base="#0284c7", color_left="#0f172a", color_bottom="#0f172a", clip_id="clipCrestD")}
</svg>"""
    with open("assets/branding/openvoge-crest-dark.svg", "w", encoding="utf-8") as f:
        f.write(svg_crest_dark)

    # ==========================================================
    # 2. AVATAR 1:1 (512 x 512) - Centered, 100% Transparent
    # ==========================================================
    svg_avatar = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs><clipPath id="clipAv"><path d="{clip_left}"/></clipPath></defs>
  <g transform="translate(70.75, 109.18) scale(0.70)">
    {render_crest(color_base="#00d2ff", color_left="#ffffff", color_bottom="#ffffff", clip_id="clipAv")}
  </g>
</svg>"""
    with open("assets/branding/openvoge-avatar.svg", "w", encoding="utf-8") as f:
        f.write(svg_avatar)

    # ==========================================================
    # 3. HORIZONTAL LOGO (960 x 240) - 100% Transparent
    # ==========================================================
    svg_horiz = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 240" width="960" height="240">
  <defs><clipPath id="clipH"><path d="{clip_left}"/></clipPath></defs>
  <!-- Crest on left (scale = 0.45, w=238, h=188.8) -->
  <g transform="translate(10, 25.6) scale(0.45)">
    {render_crest(color_base="#00d2ff", color_left="#ffffff", color_bottom="#ffffff", clip_id="clipH")}
  </g>
  <!-- Wordmark on right -->
  <g transform="translate(280, -210) scale(0.68)">
    <path d="{open_d}" fill="#00d2ff"/>
    <g transform="translate({tx_voge:.1f}, 0)">
      {render_voge_letters(color="#ffffff")}
    </g>
  </g>
  <!-- Subtitle -->
  <g transform="translate(280, -220) scale(0.68)">
    <path d="{sub_d}" fill="#94a3b8"/>
  </g>
</svg>"""
    with open("assets/branding/openvoge-logo-horizontal.svg", "w", encoding="utf-8") as f:
        f.write(svg_horiz)

    # Dark horizontal version for light backgrounds (README light mode)
    svg_horiz_dark = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 240" width="960" height="240">
  <defs><clipPath id="clipHD"><path d="{clip_left}"/></clipPath></defs>
  <g transform="translate(10, 25.6) scale(0.45)">
    {render_crest(color_base="#0284c7", color_left="#0f172a", color_bottom="#0f172a", clip_id="clipHD")}
  </g>
  <g transform="translate(280, -210) scale(0.68)">
    <path d="{open_d}" fill="#0284c7"/>
    <g transform="translate({tx_voge:.1f}, 0)">
      {render_voge_letters(color="#0f172a")}
    </g>
  </g>
  <g transform="translate(280, -220) scale(0.68)">
    <path d="{sub_d}" fill="#64748b"/>
  </g>
</svg>"""
    with open("assets/branding/openvoge-logo-horizontal-dark.svg", "w", encoding="utf-8") as f:
        f.write(svg_horiz_dark)

    # ==========================================================
    # 4. STACKED LOGO (600 x 520) - 100% Transparent
    # ==========================================================
    # Crest width: 529.3 * 0.65 = 344px. tx = (600 - 344)/2 = 128. ty = 20. Crest bottom = 20 + 273 = 293.
    # Text width: 731.7 * 0.58 = 424px. tx = (600 - 424)/2 = 88.
    # Gap = 45. Text top = 293 + 45 = 338. Baseline = 338 + 62 = 400.
    # ty_text = 400 - 545.67 * 0.58 = 83.5.
    svg_stacked = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 520" width="600" height="520">
  <defs><clipPath id="clipS"><path d="{clip_left}"/></clipPath></defs>
  <g transform="translate(128, 20) scale(0.65)">
    {render_crest(color_base="#00d2ff", color_left="#ffffff", color_bottom="#ffffff", clip_id="clipS")}
  </g>
  <g transform="translate(88, 83.5) scale(0.58)">
    <path d="{open_d}" fill="#00d2ff"/>
    <g transform="translate({tx_voge:.1f}, 0)">
      {render_voge_letters(color="#ffffff")}
    </g>
  </g>
  <g transform="translate(88, 83.5) scale(0.58)">
    <path d="{sub_d}" fill="#94a3b8"/>
  </g>
</svg>"""
    with open("assets/branding/openvoge-logo-stacked.svg", "w", encoding="utf-8") as f:
        f.write(svg_stacked)

    svg_stacked_dark = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 520" width="600" height="520">
  <defs><clipPath id="clipSD"><path d="{clip_left}"/></clipPath></defs>
  <g transform="translate(128, 20) scale(0.65)">
    {render_crest(color_base="#0284c7", color_left="#0f172a", color_bottom="#0f172a", clip_id="clipSD")}
  </g>
  <g transform="translate(88, 83.5) scale(0.58)">
    <path d="{open_d}" fill="#0284c7"/>
    <g transform="translate({tx_voge:.1f}, 0)">
      {render_voge_letters(color="#0f172a")}
    </g>
  </g>
  <g transform="translate(88, 83.5) scale(0.58)">
    <path d="{sub_d}" fill="#64748b"/>
  </g>
</svg>"""
    with open("assets/branding/openvoge-logo-stacked-dark.svg", "w", encoding="utf-8") as f:
        f.write(svg_stacked_dark)

    # ==========================================================
    # 5. ELECTRIC APEX VARIANT (Stacked 600 x 520) - 100% Transparent
    # ==========================================================
    svg_apex = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 520" width="600" height="520">
  <g transform="translate(128, 20) scale(0.65)">
    <path d="{paths['path16']}" fill="#ffffff"/>
    <path d="{paths['path22']}" fill="#ffffff"/>
    <path d="{paths['path20']}" fill="#ffffff"/>
    <path d="{paths['path18']}" fill="#00d2ff"/>
  </g>
  <g transform="translate(88, 83.5) scale(0.58)">
    <path d="{open_d}" fill="#00d2ff"/>
    <g transform="translate({tx_voge:.1f}, 0)">
      {render_voge_letters(color="#ffffff")}
    </g>
  </g>
  <g transform="translate(88, 83.5) scale(0.58)">
    <path d="{sub_d}" fill="#94a3b8"/>
  </g>
</svg>"""
    with open("assets/branding/openvoge-electric-apex.svg", "w", encoding="utf-8") as f:
        f.write(svg_apex)

    print("All transparent SVGs generated successfully!")

    # Render PNGs with 100% transparent alpha channel
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    targets = [
        ("openvoge-crest", 530, 420),
        ("openvoge-crest-dark", 530, 420),
        ("openvoge-avatar", 512, 512),
        ("openvoge-logo-horizontal", 960, 240),
        ("openvoge-logo-horizontal-dark", 960, 240),
        ("openvoge-logo-stacked", 600, 520),
        ("openvoge-logo-stacked-dark", 600, 520),
        ("openvoge-electric-apex", 600, 520),
    ]

    for name, w, h in targets:
        in_p = os.path.abspath(f"assets/branding/{name}.svg")
        out_p = os.path.abspath(f"assets/branding/{name}.png")
        cmd = [
            edge_exe,
            "--headless=new",
            "--default-background-color=00000000",
            f"--screenshot={out_p}",
            f"--window-size={w},{h}",
            f"file:///{in_p.replace(os.sep, '/')}"
        ]
        subprocess.run(cmd, check=True)
        print(f"Rendered transparent PNG: {name}.png ({w}x{h})")

if __name__ == "__main__":
    main()
