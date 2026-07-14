#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lesson-files-consolidate — consolidate course/lesson files into templated
per-chapter (he/en) folders + exams folder. See SKILL.md.

Usage:
  consolidate.py --base "<BASE>" [--out "<OUT>"] [--lang en|he]
                 [--ignore "old"] [--skip-dirs "a b"] [--skip-prefix r"^\d+_"]
                 [--dry-run]
"""
import os, re, sys, shutil, time, hashlib, argparse, unicodedata, zipfile
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    return ''.join(ch for ch in s if unicodedata.category(ch)[0] != 'C')

def md5(p):
    h = hashlib.md5()
    with open(p,'rb') as f:
        for b in iter(lambda: f.read(65536), b''):
            h.update(b)
    return h.hexdigest()

# chapter keyword -> (en folder, he folder). ORDER MATTERS: more specific first.
CHAPTERS = [
    ('אגרות חוב', 'bonds', 'אגרות חוב'),
    ('אגח', 'bonds', 'אגרות חוב'),
    ('השקעות בניירות ערך סחירים', 'investments-tradable-securities', 'השקעות בניירות ערך סחירים'),
    ('השקעות בנ', 'investments-tradable-securities', 'השקעות בניירות ערך סחירים'),
    ('שיטת שווי מאזני', 'equity-method', 'שיטת שווי מאזני'),
    ('מאזני', 'equity-method', 'שיטת שווי מאזני'),
    ('התחייבויות לזמן ארוך', 'long-term-liabilities-loans', 'התחייבויות לזמן ארוך'),
    ('הלוואות', 'long-term-liabilities-loans', 'התחייבויות לזמן ארוך'),
    ('הון עצמי', 'equity', 'הון עצמי'),
    ('תזרים מזומנים', 'cash-flow', 'דוח תזרים מזומנים'),
    ('תזרים', 'cash-flow', 'דוח תזרים מזומנים'),
]

def chapter_for(c):
    for kw, en, he in CHAPTERS:
        if kw in c:
            return en, he
    return None

DOCX_RE = re.compile(r'<[^>]+>')
def docx_text(path):
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read('word/document.xml').decode('utf-8','ignore')
        return re.sub(r'\s+',' ', DOCX_RE.sub(' ', xml))
    except Exception:
        return ''

def exam_year(text, dd, mm):
    pat = re.compile(rf'{re.escape(dd)}\s*\.\s*{re.escape(mm)}\s*\.\s*((?:19|20)\d{{2}})')
    m = pat.search(text)
    if m: return m.group(1)
    yrs = re.findall(r'(?:19|20)\d{2}', text[:2000])
    return yrs[0] if yrs else 'YYYY'

def classify(raw, full, exam_years):
    c = norm(raw)
    ext = os.path.splitext(raw)[1].lower()
    # course-general
    if 'דף נוסחאות' in c: return ('course-general','כללי הקורס', 'course-general-material-formula-sheet','חומר-דף-נוסחאות')
    if 'חוברת עבודה' in c: return ('course-general','כללי הקורס', 'course-general-material-workbook','חומר-חוברת-עבודה')
    if 'מערך שיעור' in c: return ('course-general','כללי הקורס', 'course-general-material-lesson-plan','חומר-מערך-שיעור')
    if 'סילבוס' in c or 'תוכנית לימודים' in c: return ('course-general','כללי הקורס','course-general-material-syllabus','חומר-סילבוס')
    if 'סיכום מנטור' in c or 'סיכום מנטורית' in c: return ('course-general','כללי הקורס','course-general-material-mentor-summary','חומר-סיכום-מנטורית')
    # exams
    m = re.search(r'(\d{1,2})\.(\d{1,2})', c)
    if 'חשבונאות ב' in c and m:
        dd, mm = m.group(1), m.group(2)
        yr = exam_year(docx_text(full), dd, mm) if ext == '.docx' else exam_years.get((dd,mm),'YYYY')
        is_sol = (ext == '.xlsx') or ('פתרון' in c)
        comment = '-management-economics' if 'ניהול וכלכלה' in c else ''
        comment_he = '-ניהול-וכלכלה' if 'ניהול וכלכלה' in c else ''
        kind, kind_he = ('solution','פתרון') if is_sol else ('exam','מבחן')
        return ('exams','מבחנים',
                f'accounting-b-{kind}-{yr}-{dd}-{mm}{comment}',
                f'חשבונאות-ב-{kind_he}-{yr}-{dd}-{mm}{comment_he}')
    # bare D.D pair (no course word) -> inspect
    if m and ext in ('.docx','.xlsx'):
        dd, mm = m.group(1), m.group(2)
        yr = exam_year(docx_text(full), dd, mm) if ext == '.docx' else exam_years.get((dd,mm),'YYYY')
        is_sol = (ext == '.xlsx')
        kind, kind_he = ('solution','פתרון') if is_sol else ('exam','מבחן')
        return ('exams','מבחנים',
                f'accounting-b-{kind}-{yr}-{dd}-{mm}-management-economics',
                f'חשבונאות-ב-{kind_he}-{yr}-{dd}-{mm}-ניהול-וכלכלה')
    # V lecture material
    if c.startswith('V '):
        ch = chapter_for(c)
        if ch:
            return (ch[0], ch[1], f'{ch[0]}-material', f'{ch[1]}-חומר')
    # cash-flow statement / template
    if 'דוח תזרים מזומנים ממולא' in c: ch=chapter_for(c); return (ch[0],ch[1],f'{ch[0]}-material-statement-filled',f'{ch[1]}-חומר-ממולא')
    if 'דוח תזרים מזומנים' in c:
        ch=chapter_for(c)
        qual = '-פשוט' if 'פשוט' in c else ''
        return (ch[0],ch[1],f'{ch[0]}-material-statement{qual}',f'{ch[1]}-חומר-דוח{qual}')
    if 'שבלונה' in c or 'תבנית' in c:    ch=chapter_for(c); return (ch[0],ch[1],f'{ch[0]}-material-template',f'{ch[1]}-חומר-תבנית')
    # topic-named materials (e.g. אגח.pdf, שיטת שווי מאזני.pdf)
    ch = chapter_for(c)
    if ch:
        if 'תרגיל' in c:
            em = re.search(r'תרגיל\s*(\d+)', c)
            num = em.group(1) if em else 'prac'
            return (ch[0],ch[1],f'{ch[0]}-exercise-{num}-source',f'{ch[1]}-תרגיל-{num}-מקור')
        qual = '-בלי-תריגלים' if 'בלי' in c else ''
        return (ch[0],ch[1],f'{ch[0]}-material-summary{qual}',f'{ch[1]}-חומר-סיכום{qual}')
    # exercises
    ch = chapter_for(c)
    if ch:
        em = re.search(r'תרגיל\s*(\d+)', c)
        num = em.group(1) if em else None
        comment=''
        if 'קו ישר' in c: comment='straight-line'
        elif 'מסכם' in c: comment='summary'
        elif 'פשוט' in c: comment='simple'
        elif 'איתי' in c: comment='ithai'
        elif 'צמאים לחופש' in c: comment='thirsty-for-freedom'
        elif 'יובנטוס' in c: comment='juvenus'
        comment_he = {'straight-line':'קו-ישר','summary':'מסכם','simple':'פשוט','ithai':'איתי','thirsty-for-freedom':'צמאים-לחופש','juvenus':'יובנטוס'}.get(comment,'')
        slug = f'{ch[0]}-exercise-{num}' if num else f'{ch[0]}-exercise-practice'
        slug_he = f'{ch[1]}-תרגיל-{num}' if num else f'{ch[1]}-תרגיל-תרגול'
        if comment: slug += f'-{comment}'
        if comment_he: slug_he += f'-{comment_he}'
        if ext == '.doc': slug += '-legacy'; slug_he += '-ישן'
        return (ch[0],ch[1],slug,slug_he)
    return ('_UNMAPPED','_UNMAPPED',None,None)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True)
    ap.add_argument('--out', default=None)
    ap.add_argument('--lang', choices=['en','he'], default='en')
    ap.add_argument('--ignore', default='')
    ap.add_argument('--skip-dirs', default='')
    ap.add_argument('--skip-prefix', default='')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    OUT = a.out or a.base
    ignores = set(a.ignore.split())
    skip_dirs = set(a.skip_dirs.split())
    skip_pre = re.compile(a.skip_prefix) if a.skip_prefix else None

    files = []  # (full, rel, raw)
    for r, dirs, fs in os.walk(a.base):
        rel_r = os.path.relpath(r, a.base)
        prune = [d for d in dirs if d in ignores or d in skip_dirs or (skip_pre and skip_pre.match(d))]
        for d in prune:
            dirs.remove(d)
        for f in fs:
            if f.startswith('~$'): continue
            full = os.path.join(r, f)
            rel = os.path.relpath(full, a.base)
            files.append((full, rel, f))

    # Pass 1: extract exam years from every .docx so solutions can inherit them
    exam_years = {}
    for full, rel, raw in files:
        if not raw.lower().endswith('.docx'): continue
        c = norm(raw)
        mm = re.search(r'(\d{1,2})\.(\d{1,2})', c)
        if mm:
            dd, mo = mm.group(1), mm.group(2)
            yr = exam_year(docx_text(full), dd, mo)
            if yr != 'YYYY':
                exam_years[(dd, mo)] = yr

    groups = {}
    unmapped = []
    for full, rel, raw in files:
        en_f, he_f, en_s, he_s = classify(raw, full, exam_years)
        if en_f == '_UNMAPPED':
            unmapped.append(rel); continue
        folder = he_f if a.lang=='he' else en_f
        slug = he_s if a.lang=='he' else en_s
        ext = os.path.splitext(raw)[1].lower()
        groups.setdefault(folder, []).append((slug, ext, rel, full))

    print(f"=== {'DRY RUN' if a.dry_run else 'EXECUTE'} | lang={a.lang} | base={a.base} ===")
    print(f"Files collected: {len(files)}  Mapped: {len(files)-len(unmapped)}  Unmapped: {len(unmapped)}")
    if unmapped:
        print("!!! UNMAPPED:", unmapped)
        with open(r'C:/Users/Tiger/AppData/Local/hermes/scripts/_unmapped_dbg.txt','w',encoding='utf-8') as dbg:
            for rel in unmapped:
                full = os.path.join(a.base, rel)
                raw = os.path.basename(full)
                n = norm(raw)
                dbg.write(f"RAW : {raw!r}\nNORM: {n!r}\n")
                dbg.write('codepoints: ' + ' '.join(f'U+{ord(c):04X}' for c in n) + '\n\n')
    for folder in sorted(groups):
        items = sorted(groups[folder], key=lambda x: x[2])
        print(f"\n[{folder}] ({len(items)})")
        for slug, ext, rel, full in items:
            print(f"  {slug}{ext}\n      <- {rel}")
            if a.dry_run: continue
            dst_dir = os.path.join(OUT, folder)
            os.makedirs(dst_dir, exist_ok=True)
            dst = os.path.join(dst_dir, f"{slug}{ext}")
            if os.path.abspath(full) == os.path.abspath(dst): continue
            if os.path.exists(dst):
                if md5(full) == md5(dst):
                    try: os.unlink(full); print("      (dup, removed)"); continue
                    except: pass
                i=1
                while os.path.exists(dst):
                    dst = os.path.join(dst_dir, f"{slug}-{i}{ext}"); i+=1
            shutil.move(full, dst); print("      moved")

if __name__ == '__main__':
    main()
