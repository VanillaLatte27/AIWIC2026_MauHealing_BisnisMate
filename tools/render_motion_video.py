#!/usr/bin/env python3
"""
BisnisMate AI — Argon 4 Broadcast Master Video Renderer v2.0
Incorporates real live application screenshots captured from http://localhost:3000/
Pre-scales assets outside the render loop for 10x faster encoding.
"""

import os
import sys
import time
import subprocess
import shutil
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FPS = 25
DURATION_SEC = 89.28
TOTAL_FRAMES = int(DURATION_SEC * FPS)

ASSET_DIR = "/Users/candrak/Downloads/AIWIC2026_MauHealing_BisnisMate/public/assets"
SCREENSHOT_DIR = os.path.join(ASSET_DIR, "screenshots")
AUDIO_PATH = "/tmp/final_narration_mixed.m4a"
OUTPUT_MP4 = "/Users/candrak/Downloads/BisnisMate_MotionGraphic_AIWIC2026.mp4"
PUBLIC_MP4 = "/Users/candrak/Downloads/AIWIC2026_MauHealing_BisnisMate/public/BisnisMate_MotionGraphic_AIWIC2026.mp4"
FFMPEG = "/Users/candrak/.local/bin/ffmpeg"

# Load Fonts
FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"
font_title = ImageFont.truetype(FONT_PATH, 44)
font_subtitle = ImageFont.truetype(FONT_PATH, 26)
font_card_val = ImageFont.truetype(FONT_PATH, 42)
font_card_lbl = ImageFont.truetype(FONT_PATH, 20)
font_body = ImageFont.truetype(FONT_PATH, 19)
font_subtitles = ImageFont.truetype(FONT_PATH, 25)
font_badge = ImageFont.truetype(FONT_PATH, 15)
font_hero = ImageFont.truetype(FONT_PATH, 54)

def load_img(p):
    return Image.open(p).convert("RGBA")

print("[INFO] Loading high-resolution assets & live app screenshots...")
img_hero_raw = load_img(os.path.join(ASSET_DIR, "cover_balinese_msme_hero.jpg"))
img_pillar_raw = load_img(os.path.join(ASSET_DIR, "pillar1_voice_emblem.jpg"))
img_ui_wa_raw = load_img(os.path.join(ASSET_DIR, "ui_whatsapp_bisnismate.png"))
img_radar_pos_raw = load_img(os.path.join(ASSET_DIR, "radar_pos_readiness.png"))
img_radar_umkm_raw = load_img(os.path.join(ASSET_DIR, "radar_umkm_pressure.png"))
img_logo_raw = load_img(os.path.join(ASSET_DIR, "bisnismate_logo.png"))
img_qr_raw = load_img(os.path.join(ASSET_DIR, "qr_bisnismate.png"))

# Live Application Screenshots
img_ss_dash_raw = load_img(os.path.join(SCREENSHOT_DIR, "app_tab_dashboard.png"))
img_ss_voice_raw = load_img(os.path.join(SCREENSHOT_DIR, "app_tab_voice_vision.png"))
img_ss_ledger_raw = load_img(os.path.join(SCREENSHOT_DIR, "app_tab_ledger.png"))
img_ss_cult_raw = load_img(os.path.join(SCREENSHOT_DIR, "app_tab_cultural.png"))
img_ss_kur_raw = load_img(os.path.join(SCREENSHOT_DIR, "app_tab_kur.png"))

print("[INFO] Pre-scaling static assets for maximum render throughput...")
# Pre-scaled Scene 1
hero_s1 = img_hero_raw.resize((660, 440), Image.Resampling.LANCZOS)
dash_s1 = img_ss_dash_raw.resize((980, 480), Image.Resampling.LANCZOS)

# Pre-scaled Scene 2
radar1_s2 = img_radar_pos_raw.resize((500, 370), Image.Resampling.LANCZOS)
radar2_s2 = img_radar_umkm_raw.resize((500, 370), Image.Resampling.LANCZOS)
cult_s2 = img_ss_cult_raw.resize((680, 370), Image.Resampling.LANCZOS)

# Pre-scaled Scene 3
voice_s3 = img_ss_voice_raw.resize((860, 460), Image.Resampling.LANCZOS)
ledger_s3 = img_ss_ledger_raw.resize((860, 460), Image.Resampling.LANCZOS)
logo_s3 = img_logo_raw.resize((260, 142), Image.Resampling.LANCZOS)

# Pre-scaled Scene 4
kur_s4 = img_ss_kur_raw.resize((900, 480), Image.Resampling.LANCZOS)

# Pre-scaled Scene 5
qr_s5 = img_qr_raw.resize((200, 200), Image.Resampling.LANCZOS)
logo_s5 = img_logo_raw.resize((320, 175), Image.Resampling.LANCZOS)

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_pill(draw, cx, cy, text, bg_color, text_color, font=font_badge):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    w = tw + 26
    h = th + 12
    draw.rounded_rectangle([cx - w//2, cy - h//2, cx + w//2, cy + h//2], radius=h//2, fill=bg_color)
    draw.text((cx - tw//2, cy - th//2 - 2), text, fill=text_color, font=font)

def draw_browser_frame(frame, draw, img, x, y, w, h, title="http://localhost:3000/"):
    bar_h = 28
    draw_rounded_rect(draw, [x, y, x + w, y + h + bar_h], 12, fill=(15, 23, 42, 245), outline=(56, 189, 248, 180), width=2)
    draw.rectangle([x, y + bar_h, x + w, y + bar_h + 1], fill=(56, 189, 248, 90))
    # macOS window dots
    draw.ellipse([x + 10, y + 9, x + 18, y + 17], fill=(239, 68, 68))
    draw.ellipse([x + 24, y + 9, x + 32, y + 17], fill=(245, 158, 11))
    draw.ellipse([x + 38, y + 9, x + 46, y + 17], fill=(16, 185, 129))
    # URL Pill
    url_w = min(380, w - 160)
    draw_rounded_rect(draw, [x + 65, y + 5, x + 65 + url_w, y + 23], 6, fill=(3, 7, 18, 200), outline=(255, 255, 255, 40), width=1)
    draw.text((x + 78, y + 7), title, fill=(148, 163, 184), font=font_badge)
    # Live Badge
    draw_pill(draw, x + w - 75, y + 14, "LIVE APP MVP", (16, 185, 129), (3, 7, 18), font=font_badge)
    # Paste image inside
    frame.paste(img, (x + 2, y + bar_h + 2))

def draw_hud(draw, t, scene_title):
    # Top HUD
    draw_rounded_rect(draw, [40, 22, 450, 66], 10, fill=(15, 23, 42, 230), outline=(56, 189, 248, 120), width=1)
    draw.ellipse([58, 40, 68, 50], fill=(239, 68, 68))
    draw.text((80, 33), "ARGON 4 MOTION GRAPHIC", fill=(226, 232, 240), font=font_badge)
    
    # Scene Title Pill
    draw_pill(draw, 720, 44, scene_title, (0, 32, 96, 230), (56, 189, 248), font=font_badge)
    
    # Timecode
    m = int(t // 60)
    s = int(t % 60)
    ms = int((t % 1) * 100)
    tc = f"{m:02d}:{s:02d}:{ms:02d} / 01:29:28 [25 FPS]"
    draw_rounded_rect(draw, [W - 380, 22, W - 40, 66], 10, fill=(15, 23, 42, 230), outline=(255, 141, 42, 120), width=1)
    draw.text((W - 355, 33), tc, fill=(255, 141, 42), font=font_badge)

def draw_subtitle_box(draw, text, t):
    sw, sh = 1760, 95
    sx = (W - sw) // 2
    sy = H - 120
    draw_rounded_rect(draw, [sx, sy, sx + sw, sy + sh], 16, fill=(3, 7, 18, 245), outline=(29, 154, 138, 200), width=2)
    draw_pill(draw, sx + 130, sy + 47, "Ibu Wayan Sudarmi (Pasar Kumbasari)", (255, 141, 42), (15, 23, 42), font=font_badge)
    draw.text((sx + 280, sy + 30), text, fill=(248, 250, 252), font=font_subtitles)

# Base background matrix
bg_base = Image.new("RGBA", (W, H), (3, 7, 18, 255))
d_bg = ImageDraw.Draw(bg_base)
for r in range(1200, 0, -30):
    alpha = int(45 * (1 - r / 1200))
    d_bg.ellipse([W//2 - r, H//2 - r, W//2 + r, H//2 + r], fill=(10, 26, 47, alpha))

grid_gap = 70
for y in range(0, H, grid_gap):
    d_bg.line([0, y, W, y], fill=(56, 189, 248, 12), width=1)
for x in range(0, W, grid_gap):
    d_bg.line([x, 0, x, H], fill=(56, 189, 248, 12), width=1)

def render_frame(t):
    frame = bg_base.copy()
    draw = ImageDraw.Draw(frame)

    # =========================================================================
    # SCENE 1 (0.0s - 16.0s): REALITAS OPERASIONAL UMKM & SCREENSHOT DASHBOARD
    # =========================================================================
    if t < 16.0:
        draw_hud(draw, t, "BABAK 1: REALITAS UMKM & LIVE DASHBOARD APP")
        
        draw.text((60, 90), "PARIWISATA MAJU, NAMUN 442K+ UMKM BALI TERJEBAK NOTA KERTAS", fill=(255, 255, 255), font=font_title)
        draw.text((60, 145), "BisnisMate AI Menggantikan Pembukuan Manual dengan Live Web Dashboard Otomatis", fill=(56, 189, 248), font=font_subtitle)

        # Left: Hero Photograph (Ibu Wayan)
        frame.paste(hero_s1, (60, 205))
        draw_rounded_rect(draw, [60, 205, 720, 645], 14, outline=(29, 154, 138), width=3)
        draw_rounded_rect(draw, [80, 590, 480, 635], 10, fill=(15, 23, 42, 230), outline=(255, 141, 42), width=1)
        draw.text((100, 603), "Ibu Wayan Sudarmi • Pasar Kumbasari Denpasar", fill=(255, 255, 255), font=font_body)

        # Right: Real Screenshot of Dashboard Web App
        draw_browser_frame(frame, draw, dash_s1, 760, 205, 980, 480, "http://localhost:3000/?tab=dashboard")
        
        # Stat Badges Bottom Row
        draw_pill(draw, 200, 690, "442.848 UMKM AKTIF", (15, 23, 42), (56, 189, 248))
        draw_pill(draw, 450, 690, "HEMAT 2.5 JAM / HARI", (15, 23, 42), (45, 212, 191))
        draw_pill(draw, 700, 690, "ZERO SELISIH KAS", (15, 23, 42), (255, 141, 42))

        # Subtitles
        if t < 7.5:
            draw_subtitle_box(draw, "\"Om Swastyastu semeton sami! Tiang Ibu Wayan Sudarmi saking Pasar Kumbasari Denpasar.\"", t)
        else:
            draw_subtitle_box(draw, "\"Saban dina, tangan tiang basah ngadep canang lan bumbu, tuyuh pisan rekap nota manual!\"", t)

    # =========================================================================
    # SCENE 2 (16.0s - 34.0s): KESENJANGAN POS & SCREENSHOT KALENDER ADAT BALI
    # =========================================================================
    elif t < 34.0:
        draw_hud(draw, t, "BABAK 2: KESENJANGAN POS & SIKLUS ADAT BALI")

        draw.text((60, 90), "TITIK BUTA DIGITALISASI & BEBAN HARI RAYA ADAT BALI", fill=(255, 255, 255), font=font_title)
        draw.text((60, 145), "Kasir POS Gagal Paham Galungan; BisnisMate AI Sinkron Kalender Caka 1948", fill=(239, 68, 68), font=font_subtitle)

        # Left: 2 Radar Charts
        frame.paste(radar1_s2, (60, 205), radar1_s2)
        draw_rounded_rect(draw, [60, 205, 560, 575], 14, outline=(239, 68, 68), width=2)
        draw_pill(draw, 310, 610, "Kesiapan POS: Rendah (90% Ditolak Pedagang)", (15, 23, 42), (248, 113, 113))

        # Center/Right: Real Screenshot of Cultural Calendar Sync Web App
        draw_browser_frame(frame, draw, cult_s2, 600, 205, 680, 370, "http://localhost:3000/?tab=cultural")
        draw_pill(draw, 940, 610, "Sinkronisasi Adat: H-7 Galungan Stock Alert", (15, 23, 42), (255, 141, 42))

        # Right: Radar UMKM Pressure
        frame.paste(radar2_s2, (1320, 205), radar2_s2)
        draw_rounded_rect(draw, [1320, 205, 1820, 575], 14, outline=(255, 141, 42), width=2)
        draw_pill(draw, 1570, 610, "Beban Modal Upacara 35% Terkendali", (15, 23, 42), (45, 212, 191))

        # Danger Banner
        draw_rounded_rect(draw, [60, 650, 1860, 715], 10, fill=(15, 23, 42, 240), outline=(239, 68, 68), width=2)
        draw.text((100, 670), "AKIBAT ASIMETRI: 35% Dead-Stock Bahan & Kas Rumah Tangga Tercampur Kas Usaha!", fill=(248, 113, 113), font=font_subtitle)

        # Subtitles
        if t < 24.5:
            draw_subtitle_box(draw, "\"Aplikasi kasir konvensional nika ribet, pedagang mekejang enggan ngetik di HP...\"", t)
        else:
            draw_subtitle_box(draw, "\"Pas Galungan lan Kuningan, harga beras lan janur mekeber, tiang rugi dead-stock 35%! Bank nolak KUR...\"", t)

    # =========================================================================
    # SCENE 3 (34.0s - 58.0s): TEROBOSAN 3 PILAR & DUAL SCREENSHOT (VOICE + SAK EMKM)
    # =========================================================================
    elif t < 58.0:
        draw_hud(draw, t, "BABAK 3: SCREENSHOT MODUL VOICE/VISION & SAK EMKM")

        # Header with Logo
        frame.paste(logo_s3, (60, 80), logo_s3)
        draw.text((340, 95), "TEROBOSAN 3 PILAR BISNISMATE AI PADA APLIKASI WEB", fill=(255, 255, 255), font=font_title)
        draw.text((340, 150), "Zero-Typing Voice/Vision Scanner Langsung Menyusun Laporan Keuangan Standar IAI", fill=(45, 212, 191), font=font_subtitle)

        # Left Browser: Real Screenshot of Voice & Vision (Live Camera + 16-Bar Mic Visualizer)
        draw_browser_frame(frame, draw, voice_s3, 60, 205, 860, 460, "http://localhost:3000/?tab=voice-vision")
        draw_pill(draw, 490, 700, "PILAR 1: MULTIMODAL VOICE & VISION (OCR NOTA KUSUT)", (15, 23, 42), (45, 212, 191))

        # Right Browser: Real Screenshot of SAK EMKM Financial Statements
        draw_browser_frame(frame, draw, ledger_s3, 980, 205, 860, 460, "http://localhost:3000/?tab=ledger")
        draw_pill(draw, 1410, 700, "PILAR 2: LAPORAN LABA RUGI & POSISI KEUANGAN SAK EMKM", (15, 23, 42), (56, 189, 248))

        # Subtitles
        if t < 46.0:
            draw_subtitle_box(draw, "\"Nah, mangkin wenten BisnisMate AI! Cukup ngomong lima detik nganggen basa Bali utawi foto nota...\"", t)
        else:
            draw_subtitle_box(draw, "\"AI langsung ngerekap dadi jurnal SAK EMKM! Wenten pengingat Kalender Adat Galungan H-pitu!\"", t)

    # =========================================================================
    # SCENE 4 (58.0s - 74.0s): KESIAPAN KUR BANK (SCREENSHOT KUR + COMPLIANCE)
    # =========================================================================
    elif t < 74.0:
        draw_hud(draw, t, "BABAK 4: SCREENSHOT MODUL SKOR KUR & INTEGRASI BANK")

        draw.text((60, 90), "SKOR KREDIT KUR 88.5 / 100 (TIER 1 PRE-APPROVED) & UU PDP NO. 27/2022", fill=(255, 255, 255), font=font_title)
        draw.text((60, 145), "Laporan Terverifikasi Otomatis Siap Diintegrasikan ke Bank Mandiri, BRI, dan BPD Bali", fill=(56, 189, 248), font=font_subtitle)

        # Left Browser: Real Screenshot of KUR Credit Scoring Module
        draw_browser_frame(frame, draw, kur_s4, 60, 205, 900, 480, "http://localhost:3000/?tab=kur")

        # Right: Speedometer Score Badge & Compliance Cards
        sx = 1000
        sw = 860
        draw_rounded_rect(draw, [sx, 205, sx + sw, 435], 16, fill=(15, 23, 42, 245), outline=(45, 212, 191), width=3)
        draw.text((sx + 35, 230), "SKOR KELAYAKAN KUR: 88.5 / 100", fill=(45, 212, 191), font=font_hero)
        draw_pill(draw, sx + 450, 320, "STATUS: TIER 1 PRE-APPROVED", (16, 124, 65), (255, 255, 255), font=font_card_lbl)
        draw.text((sx + 35, 370), "Plafon Disbursal: Rp 75 Juta • DSCR 2.85x Aman • Kepatuhan SAK EMKM 100%", fill=(203, 213, 225), font=font_subtitle)

        # Data Privacy Box
        draw_rounded_rect(draw, [sx, 455, sx + sw, 715], 16, fill=(15, 23, 42, 245), outline=(255, 141, 42), width=2)
        draw.text((sx + 35, 475), "KEPATUHAN PENUH KEDAULATAN DATA (UU PDP)", fill=(255, 141, 42), font=font_subtitle)
        draw.text((sx + 35, 525), "• Zero Raw-Voice Cloud Retention (Audio diproses in-memory & langsung purge)", fill=(226, 232, 240), font=font_body)
        draw.text((sx + 35, 565), "• Enkripsi End-to-End AES-256 untuk seluruh mutasi kas buku pedagang", fill=(226, 232, 240), font=font_body)
        draw.text((sx + 35, 605), "• Host-to-Host Sandbox API Siap Integrasi Core Banking Mandiri, BRI, & BPD Bali", fill=(56, 189, 248), font=font_body)
        draw.text((sx + 35, 645), "• Sesuai Surat Edaran OJK & Pedoman Bank Indonesia untuk UMKM Hijau", fill=(203, 213, 225), font=font_body)

        # Subtitles
        if t < 66.0:
            draw_subtitle_box(draw, "\"Skor kredit KUR tiang langsung munggah dados 88.5, Tier Satu Pre-Approved!\"", t)
        else:
            draw_subtitle_box(draw, "\"Laporan SAK EMKM niki langsung kasambung ring Bank Mandiri, BRI, BPD Bali, aman manut UU PDP...\"", t)

    # =========================================================================
    # SCENE 5 (74.0s - 89.28s): GRAND FINALE & VISI STRATEGIS B-A-L-I
    # =========================================================================
    else:
        draw_hud(draw, t, "BABAK 5: KESIMPULAN STRATEGIS B-A-L-I & PENUTUP")

        draw.text((60, 90), "MEWUJUDKAN UMKM BALI NAIK KELAS BERSAMA BISNISMATE AI", fill=(255, 255, 255), font=font_title)
        draw.text((60, 145), "Inovasi Resmi AIWIC 2026 • Tim Mau Healing • Inovator: Candra Kus Khoiri Wicaksono", fill=(255, 141, 42), font=font_subtitle)

        # 4 Pillars of B-A-L-I Formula
        col_w = 430
        col_h = 240
        spacing = 460
        start_x = 60
        start_y = 210

        # B
        draw_rounded_rect(draw, [start_x, start_y, start_x + col_w, start_y + col_h], 14, fill=(15, 23, 42, 230), outline=(45, 212, 191), width=2)
        draw_pill(draw, start_x + 60, start_y + 45, "B", (45, 212, 191), (15, 23, 42), font=font_title)
        draw.text((start_x + 105, start_y + 25), "BANKABLE", fill=(45, 212, 191), font=font_subtitle)
        draw.text((start_x + 25, start_y + 90), "Pedagang memiliki neraca resmi\n& skor kredit KUR 88.5 siap cair.", fill=(203, 213, 225), font=font_body)

        # A
        draw_rounded_rect(draw, [start_x + spacing, start_y, start_x + spacing + col_w, start_y + col_h], 14, fill=(15, 23, 42, 230), outline=(255, 141, 42), width=2)
        draw_pill(draw, start_x + spacing + 60, start_y + 45, "A", (255, 141, 42), (15, 23, 42), font=font_title)
        draw.text((start_x + spacing + 105, start_y + 25), "ADAPTIVE", fill=(255, 141, 42), font=font_subtitle)
        draw.text((start_x + spacing + 25, start_y + 90), "Bekerja hands-free tanpa ketik,\nramah pedagang tangan basah.", fill=(203, 213, 225), font=font_body)

        # L
        draw_rounded_rect(draw, [start_x + spacing*2, start_y, start_x + spacing*2 + col_w, start_y + col_h], 14, fill=(15, 23, 42, 230), outline=(56, 189, 248), width=2)
        draw_pill(draw, start_x + spacing*2 + 60, start_y + 45, "L", (56, 189, 248), (15, 23, 42), font=font_title)
        draw.text((start_x + spacing*2 + 105, start_y + 25), "LOCALIZED", fill=(56, 189, 248), font=font_subtitle)
        draw.text((start_x + spacing*2 + 25, start_y + 90), "Pahami kearifan Adat Caka 1948\n& dialek Bali pasar tradisional.", fill=(203, 213, 225), font=font_body)

        # I
        draw_rounded_rect(draw, [start_x + spacing*3, start_y, start_x + spacing*3 + col_w, start_y + col_h], 14, fill=(15, 23, 42, 230), outline=(168, 85, 247), width=2)
        draw_pill(draw, start_x + spacing*3 + 60, start_y + 45, "I", (168, 85, 247), (15, 23, 42), font=font_title)
        draw.text((start_x + spacing*3 + 105, start_y + 25), "INCLUSIVE", fill=(168, 85, 247), font=font_subtitle)
        draw.text((start_x + spacing*3 + 25, start_y + 90), "Teknologi AI gratis & ringan\nuntuk seluruh lapisan masyarakat.", fill=(203, 213, 225), font=font_body)

        # Bottom Call to Action Box
        draw_rounded_rect(draw, [60, 480, 1860, 715], 16, fill=(15, 23, 42, 245), outline=(29, 154, 138), width=3)
        frame.paste(logo_s5, (90, 505), logo_s5)
        
        draw.text((450, 520), "UJI COBA APLIKASI WEB MVP SEKARANG:", fill=(255, 255, 255), font=font_subtitle)
        draw.text((450, 565), "http://localhost:3000/ • Repositori AIWIC 2026 Commit #8f4b2e1", fill=(45, 212, 191), font=font_title)
        draw.text((450, 635), "Siap Dinilai oleh Dewan Juri AIWIC 2026 • Kategori Inovasi Finansial & Inklusi UMKM", fill=(203, 213, 225), font=font_body)
        
        # QR Code on Right
        frame.paste(qr_s5, (1620, 500), qr_s5)
        draw_rounded_rect(draw, [1620, 500, 1820, 700], 8, outline=(255, 141, 42), width=2)

        # Subtitles
        if t < 81.0:
            draw_subtitle_box(draw, "\"BisnisMate AI: Ngrajegang Ekonomi Bali, saking krama pasar ngantos nuju jagat digital!\"", t)
        else:
            draw_subtitle_box(draw, "\"Matur suksma semeton sami. Om Shanti, Shanti, Shanti, Om!\"", t)

    return frame.convert("RGB")

def main():
    print(f"[INFO] Rendering {TOTAL_FRAMES} frames ({DURATION_SEC}s) @ {FPS} FPS with Live App Screenshots...")
    t0 = time.time()

    cmd = [
        FFMPEG,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", AUDIO_PATH,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_MP4
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / FPS
        img_rgb = render_frame(t)
        proc.stdin.write(img_rgb.tobytes())

        if frame_idx % 250 == 0:
            pct = (frame_idx / TOTAL_FRAMES) * 100
            print(f"  --> Progress: {frame_idx}/{TOTAL_FRAMES} ({pct:.1f}%)")
            sys.stdout.flush()

    proc.stdin.close()
    proc.wait()

    dur = time.time() - t0
    print(f"[SUCCESS] Master MP4 Video Generated at: {OUTPUT_MP4} in {dur:.1f}s")
    sz = os.path.getsize(OUTPUT_MP4)
    print(f"File size: {sz} bytes")

    shutil.copyfile(OUTPUT_MP4, PUBLIC_MP4)
    print(f"[SUCCESS] Copied to public folder for Web Hosting: {PUBLIC_MP4}")

if __name__ == "__main__":
    main()
