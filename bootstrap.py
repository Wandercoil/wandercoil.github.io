"""One-off: copy the Lens It website from the public repo and point its links at this repo."""
import re, shutil
from pathlib import Path

SRC, DST = Path("src/docs"), Path("lensit")
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("_test"))
for f in ("LICENSE", "SECURITY.md"):
    shutil.copy(Path("src") / f, f)
shutil.copytree("src/.github/ISSUE_TEMPLATE", ".github/ISSUE_TEMPLATE")
SITE = "https://github.com/Wandercoil/wandercoil.github.io"
OLD = "https://github.com/Wandercoil/lensit"

def edit(name, pairs):
    p = DST / name
    s = p.read_text(encoding="utf-8")
    for a, b in pairs:
        assert a in s, f"{name}: {a[:50]}"
        s = s.replace(a, b)
    for sub in ("/releases", "/issues", "/blob/main/LICENSE", "/blob/main/SECURITY.md"):
        s = s.replace(OLD + sub, SITE + sub)
    s = s.replace("github.com/Wandercoil/lensit/issues", "github.com/Wandercoil/wandercoil.github.io/issues")
    s = s.replace(OLD, "https://github.com/Wandercoil")
    p.write_text(s, encoding="utf-8")

edit("index.html", [
    ("matched offline on the photographer's laptop. Free and open source.", "matched offline on the photographer's laptop. Free to use."),
    ("For event photographers · Free &amp; open source", "For event photographers · Free to use"),
    ("<td>Can you change how it works?</td><td>Yes, it's open source</td>", "<td>Are the AI models open?</td><td>Yes, open-weight models</td>"),
    ("Yes. Lens It is open source. There's no subscription", "Yes. Lens It is free to use. There's no subscription"),
    ("<li><b>04</b> Open source</li>", "<li><b>04</b> Open models</li>"),
    (' · Mac/Linux and developers: <a href="https://github.com/Wandercoil/lensit">run from source</a>', ""),
    ('<h4>Open source</h4><a href="https://github.com/Wandercoil/lensit">GitHub</a>', "<h4>Open models</h4>"),
])
p = DST / "index.html"
s = p.read_text(encoding="utf-8")
s, n = re.subn(r'\s*<div class="term reveal" aria-label="Install commands">.*?</div>\s*</div>(?=\s*</div>\s*\n)', "\n", s, count=1, flags=re.S)
assert n == 1, "install block"
assert "pip install" not in s, "install text left"
p.write_text(s, encoding="utf-8")
edit("try.html", [('<a href="https://github.com/Wandercoil/lensit">Source code</a> · ', "")])
edit("privacy.html", [("Lens It is free, open-source software. It has three parts:", "Lens It is free to use. It has three parts:")])
edit("terms.html", [
    ("Lens It is free and open source. Use it", "Lens It is free to use. Use it"),
    ('Its code is free, open-source software released under the <a href="https://github.com/Wandercoil/lensit/blob/main/LICENSE">GNU Affero General Public License v3.0</a>. If you distribute Lens It, or run a modified version for others to use, you must make your full source code available under the same licence and keep our copyright notice. The face models',
     'Version 0.2.8 and earlier were released under the <a href="https://github.com/Wandercoil/lensit/blob/main/LICENSE">GNU Affero General Public License v3.0</a>, and you keep the rights that licence gives you for those versions. Newer development is private. The face models'),
    ("The open-source licence covers the code only. You may not", "No licence covers these names or logos. You may not"),
])
fb = DST / "feedback.js"
s = fb.read_text(encoding="utf-8")
assert OLD + "/issues/new" in s
fb.write_text(s.replace(OLD + "/issues/new", SITE + "/issues/new"), encoding="utf-8")
sec = Path("SECURITY.md")
s = sec.read_text(encoding="utf-8")
assert "- Code: " + OLD in s
sec.write_text(s.replace("- Code: " + OLD, "- Downloads: " + SITE + "/releases"), encoding="utf-8")
cfg = Path(".github/ISSUE_TEMPLATE/config.yml")
cfg.write_text(cfg.read_text(encoding="utf-8").replace(OLD, SITE), encoding="utf-8")
Path("index.html").write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/lensit/"><title>Wandercoil</title><a href="/lensit/">Lens It</a>\n', encoding="utf-8")
Path(".nojekyll").write_text("")
Path("README.md").write_text("# Wandercoil\n\nWebsite and downloads for [Lens It](https://wandercoil.github.io/lensit/). A Wandercoil product.\n", encoding="utf-8")
left = [str(f) for f in DST.rglob("*") if f.suffix in {".html", ".js"} and "Wandercoil/lensit" in f.read_text(encoding="utf-8")]
assert not left, left
print("site ready")
