#!/usr/bin/env python3
"""Generate the bankruptcy-essays site: a show homepage + one page per episode.

Add a new episode by appending to EPISODES (media already sitting in ep/<slug>/)
and re-running:  python build_site.py
"""
from pathlib import Path
import html

SITE = Path(__file__).parent

EPISODES = [
    {
        "num": "02", "slug": "procedure_fees", "kicker": "נוהל · שכר טרחה",
        "title": "היכן נגמר התפקיד, היכן מתחיל השכר",
        "dek": "נוהל השכר של הממונה מותח קו חד בין פעולות שהן חלק מהתפקיד לבין פעולות שמזכות בתשלום — שלושת המסלולים, מדרגות האישור, והמוקשים שכל נאמן חייב להכיר לפני בקשת השכר הבאה.",
        "chips": ["נוהל שכר טרחה", "2019", "≈ 10 דקות"],
        "lede": "רק תקבולים שנכנסו בפועל לקופה מזכים בשכר — לא הכנסות רעיוניות, ולא ביטול תביעות חוב.",
        "body": "הפרק מוקדש לנוהל הממונה משנת 2019 בעניין שכר טרחת בעלי תפקיד — המסמך שמאחד את כללי המשחק לפסיקת שכר ניהול, מימוש וחלוקה, ומעגן את הפסיקה המרכזית בתחום, מ״שילר״ ועד ״מגה״. נדבר על מה באמת מזכה בשכר, על תקרות ההוצאות והשכר השעתי, ועל התנאים הצרים לתוספת מאמץ מיוחד. למי שמגיש בקשות שכר טרחה — זה הבסיס להבין מראש איך מייצגי הממונה יגיבו לבקשה, ואיך לבנות אותה נכון כדי לא להשאיר כסף על השולחן.",
        "glyph": "₪", "essay_title": "שלושת המסלולים, מדרגות האישור, והמוקשים",
    },
    {
        "num": "01", "slug": "standards-procedure-7th", "kicker": "נוהל · אמות מידה",
        "title": "מחצית, לא יותר",
        "dek": "מהדורה 7 של נוהל אמות המידה לקביעת תשלום חודשי קובעת נוסחה אחת, טבלה אחת וכללי זקיפת הכנסה — היכן נותר שיקול הדעת של הנאמן, והיכן מסתתר המוקש.",
        "chips": ["📄 גרסת יוני 2026", "אמות מידה · תשלום חודשי", "≈ 10 דקות"],
        "lede": "הנוהל מחליף סופית את מחשבון האומדנים של ועדת חריס — במודל פשוט ושקוף של הכנסה פנויה.",
        "body": "בפרק הזה צוללים למהדורה המעודכנת של נוהל אמות המידה לקביעת התשלום החודשי לחייב: הכנסה פנויה של התא המשפחתי, בניכוי סכום בסיסי המבוסס על קצבת הנכות הכללית, כשהחייב מותיר בידיו מחצית מחלקו היחסי. עבור הנאמן, המשמעות המעשית היא עבודה עם טבלת סכומים מעודכנת ל־2025, הכרת ההוצאות המיוחדות שניתן להפחית — בריאות, מעונות, צהרונים, מזונות — וכללי ייחוס הכנסה לחייב או לבן זוג שאינם עובדים ללא הצדק. כלים שתצטרכו בכל בדיקת דוחות חודשיים והמלצה לתכנית פירעון.",
        "glyph": "½", "essay_title": "הנוסחה, הטבלה, והמוקש — בגלילה אחת",
    },
]

HEAD = """<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{ogt}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alef:wght@400;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
"""

CSS = """
  :root{
    --ink:#0f1512;--paper:#f2efe7;--teal:#1f6f5c;--teal-lift:#2f8f78;
    --gold:#d9a441;--slate:#5c8fb3;--paper-dim:#e3ded2;--ink-soft:#3a443f;
    --line:rgba(15,21,18,.14);--font:"Alef",system-ui,sans-serif;
  }
  *{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font);
    font-size:18px;line-height:1.6;-webkit-font-smoothing:antialiased}
  a{color:inherit}
  .wrap{max-width:1080px;margin:0 auto;padding:0 24px}
  .bar{background:var(--ink);color:var(--paper)}
  .bar .wrap{display:flex;align-items:center;gap:12px;height:60px}
  .bar .mark{font-weight:700;font-size:20px;letter-spacing:.2px;text-decoration:none;color:var(--paper)}
  .bar .scale{color:var(--gold);font-size:22px;line-height:1}
  .bar .eyebrow{margin-inline-start:auto;font-size:13px;letter-spacing:.14em;
    text-transform:uppercase;color:var(--paper-dim);opacity:.8}
  .hero{background:var(--ink);color:var(--paper);padding:22px 0 56px;position:relative;overflow:hidden}
  .hero::after{content:"";position:absolute;inset-inline:0;bottom:0;height:1px;
    background:linear-gradient(90deg,transparent,var(--gold),transparent);opacity:.5}
  .kick{display:inline-flex;align-items:center;gap:10px;font-size:13px;font-weight:700;
    letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}
  .kick .n{font-size:15px;color:var(--paper)}
  .kick .bar-sm{width:34px;height:1px;background:var(--gold);opacity:.6}
  h1{font-weight:700;line-height:1.04;margin:.34em 0 .2em;
    font-size:clamp(40px,7.5vw,88px);letter-spacing:-.4px}
  .dek{max-width:44ch;font-size:clamp(17px,2.3vw,21px);color:var(--paper-dim);line-height:1.55;margin:0 0 22px}
  .chips{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:30px}
  .chip{font-size:13.5px;font-weight:700;padding:6px 13px;border-radius:999px;
    border:1px solid rgba(242,239,231,.28);color:var(--paper-dim)}
  .chip.on{background:rgba(217,164,65,.14);border-color:rgba(217,164,65,.5);color:var(--gold)}
  .player{background:rgba(242,239,231,.06);border:1px solid rgba(242,239,231,.16);
    border-radius:16px;padding:20px 22px;max-width:640px}
  .player .lbl{display:flex;align-items:center;gap:9px;font-size:13px;font-weight:700;
    letter-spacing:.12em;text-transform:uppercase;color:var(--teal-lift);margin-bottom:14px}
  .player .lbl::before{content:"\\25B6";font-size:11px}
  audio{width:100%;height:44px}
  .dl{display:flex;flex-wrap:wrap;gap:12px;margin-top:18px}
  .btn{display:inline-flex;align-items:center;gap:8px;font-size:14.5px;font-weight:700;
    padding:11px 18px;border-radius:10px;text-decoration:none;transition:transform .12s ease,background .18s ease,border-color .18s ease,color .18s ease}
  .btn:hover{transform:translateY(-1px)}
  .btn:focus-visible{outline:2px solid var(--gold);outline-offset:3px}
  .btn.solid{background:var(--teal);color:var(--paper)}
  .btn.solid:hover{background:var(--teal-lift)}
  .btn.ghost{background:transparent;color:var(--paper);border:1px solid rgba(242,239,231,.32)}
  .btn.ghost:hover{border-color:var(--gold);color:var(--gold)}
  section.pad{padding:64px 0}
  .grid{display:grid;grid-template-columns:1.15fr .85fr;gap:52px;align-items:start}
  .eyebrow2{font-size:12.5px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--teal);margin:0 0 14px}
  .lede{font-weight:700;font-size:clamp(21px,2.6vw,26px);line-height:1.45;margin:0 0 18px}
  .body-txt{font-size:17.5px;line-height:1.75;color:var(--ink-soft)}
  .body-txt b{color:var(--ink);font-weight:700}
  .short-col{position:sticky;top:24px}
  .short-frame{background:var(--ink);border-radius:18px;padding:12px;box-shadow:0 24px 60px -28px rgba(15,21,18,.7)}
  video{display:block;width:100%;border-radius:10px;background:#000;aspect-ratio:9/16}
  .short-cap{display:flex;justify-content:space-between;align-items:center;margin-top:12px;font-size:13.5px;color:var(--paper-dim)}
  .short-cap a{color:var(--gold);text-decoration:none;font-weight:700}
  .short-cap a:hover{text-decoration:underline}
  .essay{background:var(--ink);color:var(--paper)}
  .essay .grid2{display:grid;grid-template-columns:auto 1fr;gap:34px;align-items:center}
  .essay .big{font-weight:700;font-size:clamp(56px,10vw,104px);line-height:.9;color:var(--gold)}
  .essay h3{font-weight:700;font-size:clamp(22px,3vw,30px);margin:0 0 8px}
  .essay p{color:var(--paper-dim);margin:0 0 20px;max-width:52ch}
  .back{display:inline-block;margin:26px 0 0;font-size:14.5px;font-weight:700;color:var(--teal);text-decoration:none}
  .back:hover{text-decoration:underline}
  footer{padding:44px 0 56px;border-top:1px solid var(--line);font-size:15px;color:var(--ink-soft)}
  footer .wrap{display:flex;flex-wrap:wrap;gap:14px 26px;align-items:baseline}
  footer .fmark{font-weight:700;color:var(--ink);font-size:17px}
  footer .sp{margin-inline-start:auto}
  footer a{color:var(--teal);text-decoration:none;font-weight:700}
  footer a:hover{text-decoration:underline}
  /* homepage cards */
  .about{font-size:clamp(18px,2.2vw,22px);color:var(--ink-soft);max-width:60ch;margin:0 0 8px}
  .cards{display:grid;grid-template-columns:1fr 1fr;gap:26px}
  .card{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);
    border-radius:18px;padding:26px 26px 22px;transition:transform .14s ease,box-shadow .2s ease;text-decoration:none;color:inherit}
  .card:hover{transform:translateY(-3px);box-shadow:0 20px 44px -26px rgba(15,21,18,.5)}
  .card .cnum{font-weight:700;font-size:40px;line-height:1;color:var(--gold)}
  .card .ckick{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);margin:14px 0 8px}
  .card h2{font-weight:700;font-size:clamp(22px,2.6vw,27px);line-height:1.2;margin:0 0 10px}
  .card p{font-size:16px;line-height:1.6;color:var(--ink-soft);margin:0 0 18px}
  .card .go{margin-top:auto;font-weight:700;color:var(--teal)}
  @media (max-width:760px){
    .grid{grid-template-columns:1fr;gap:36px}
    .short-col{position:static;max-width:360px}
    .essay .grid2{grid-template-columns:1fr;gap:16px}
    .cards{grid-template-columns:1fr}
    section.pad{padding:48px 0}
  }
  @media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

def esc(s): return html.escape(s, quote=True)

BARTOP = ('<div class="bar"><div class="wrap">'
          '<span class="scale">⚖</span>'
          '<a class="mark" href="{home}">חדלות בגובה העיניים</a>'
          '<span class="eyebrow">פודקאסט לנאמנים</span>'
          '</div></div>\n')

FOOTER = ('<footer><div class="wrap">'
          '<span class="fmark">⚖ חדלות בגובה העיניים</span>'
          '<span>נהלים ופסיקה בחדלות פירעון — לנאמנים, בגובה העיניים</span>'
          '<span class="sp"><a href="https://nivsimon.space" rel="me">@nivsimon.space</a></span>'
          '</div></footer>\n</body>\n</html>\n')

def episode_page(ep):
    chips = "".join(f'<span class="chip{" on" if i==0 and ep["chips"][0][0]!="נ" else ""}">{esc(c)}</span>'
                    for i, c in enumerate(ep["chips"]))
    head = HEAD.format(title=esc(ep["title"] + " — חדלות בגובה העיניים"),
                       desc=esc(ep["dek"]), ogt=esc(ep["title"]), css=CSS)
    return head + BARTOP.format(home="../../") + f"""
<header class="hero"><div class="wrap">
  <span class="kick"><span class="n">פרק {esc(ep['num'])}</span><span class="bar-sm"></span> {esc(ep['kicker'].split('·')[-1].strip())}</span>
  <h1>{esc(ep['title'])}</h1>
  <p class="dek">{esc(ep['dek'])}</p>
  <div class="chips">{chips}</div>
  <div class="player">
    <div class="lbl">האזנה לפרק</div>
    <audio controls preload="metadata" src="episode.mp3"></audio>
    <div class="dl">
      <a class="btn solid" href="episode.mp3" download>⬇ הורדת הפרק (MP3)</a>
      <a class="btn ghost" href="short.mp4" download>⬇ הורדת הסרטון (MP4)</a>
    </div>
  </div>
</div></header>

<section class="pad"><div class="wrap grid">
  <div>
    <p class="eyebrow2">על הפרק</p>
    <p class="lede">{esc(ep['lede'])}</p>
    <p class="body-txt">{esc(ep['body'])}</p>
    <a class="back" href="../../">← כל הפרקים</a>
  </div>
  <div class="short-col">
    <div class="short-frame">
      <video controls preload="metadata" playsinline src="short.mp4"></video>
      <div class="short-cap"><span>הסרטון הקצר</span><a href="short.mp4" download>הורדה ↓</a></div>
    </div>
  </div>
</div></section>

<section class="essay"><div class="wrap pad">
  <div class="grid2">
    <div class="big">{esc(ep['glyph'])}</div>
    <div>
      <p class="eyebrow2" style="color:var(--gold)">סיכום גרפי</p>
      <h3>{esc(ep['essay_title'])}</h3>
      <p>גרסה אינטראקטיבית של הפרק: הגרפיקה משתנה תוך כדי גלילה ומראה בדיוק היכן נותר שיקול הדעת של הנאמן, והיכן הנוהל כובל אותו.</p>
      <a class="btn solid" href="essay.html">קריאת הסיכום הגרפי ←</a>
    </div>
  </div>
</div></section>
""" + FOOTER

def homepage():
    cards = ""
    for ep in EPISODES:
        cards += f"""<a class="card" href="ep/{esc(ep['slug'])}/">
      <span class="cnum">{esc(ep['num'])}</span>
      <span class="ckick">{esc(ep['kicker'])}</span>
      <h2>{esc(ep['title'])}</h2>
      <p>{esc(ep['dek'])}</p>
      <span class="go">האזנה ←</span>
    </a>\n    """
    head = HEAD.format(title="חדלות בגובה העיניים — פודקאסט לנאמנים",
                       desc="פודקאסט לנאמנים בהליכי חדלות פירעון ושיקום כלכלי: ניתוח מקצועי, קליל ומדויק של נהלים, הנחיות ופסיקה.",
                       ogt="חדלות בגובה העיניים", css=CSS)
    return head + BARTOP.format(home=".") + f"""
<header class="hero"><div class="wrap">
  <span class="kick">פודקאסט לנאמנים</span>
  <h1>חדלות בגובה העיניים</h1>
  <p class="dek">נהלים, הנחיות ופסיקה בחדלות פירעון ושיקום כלכלי — ניתוח מקצועי, קליל ומדויק, לנאמנים שמנהלים את ההליך בפועל.</p>
</div></header>

<section class="pad"><div class="wrap">
  <p class="eyebrow2">כל הפרקים</p>
  <div class="cards">
    {cards.strip()}
  </div>
  <p style="margin-top:30px"><a class="back" href="ab/">🎧 השוואת מנועי קול (A/B) — v3 מול multilingual_v2 ←</a></p>
</div></section>
""" + FOOTER

def main():
    (SITE / "index.html").write_text(homepage(), encoding="utf-8")
    for ep in EPISODES:
        d = SITE / "ep" / ep["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(episode_page(ep), encoding="utf-8")
    print(f"built homepage + {len(EPISODES)} episode pages")

if __name__ == "__main__":
    main()
