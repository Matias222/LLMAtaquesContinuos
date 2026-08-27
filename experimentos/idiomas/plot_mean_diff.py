"""
Genera un HTML autocontenido para ver los resultados de mean_diff_vectors.py.

    python3 plot_mean_diff.py runs/v2_french_l2_0.045/mean_diff_ctrl.json
    python3 plot_mean_diff.py <json> --out mi_reporte.html

Funciona con o sin las condiciones de control: si el JSON trae `cos_matrix`
dibuja tambien el grafico de controles y la matriz.
"""

import argparse
import json
import os

ETIQ = {"patch": "parche", "frq": "pregunta FR", "instr": "instrucción FR",
        "de": "instrucción DE", "corto": "respuesta corta"}

HTML = """<title>Geometría del parche francés</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@500;600&display=swap">
<style>
:root {
  color-scheme: light;
  --plane:#f6f7f9; --surface:#fdfdfe; --line:#e2e5ea; --line-soft:#eef0f4;
  --ink:#12141a; --ink-2:#4d5464; --ink-3:#7c8493;
  --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#4a3aa7; --s5:#8b93a3;
  --seq-0:#eef4fd; --seq-1:#cde2fb; --seq-2:#9ec5f4; --seq-3:#5598e7;
  --seq-4:#2a78d6; --seq-5:#1c5cab; --seq-6:#104281;
  --ok:#1baf7a; --warn:#eda100;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --plane:#0d0e11; --surface:#191b1f; --line:#2b2f37; --line-soft:#212429;
    --ink:#f2f4f8; --ink-2:#aab2c0; --ink-3:#767e8d;
    --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#9085e9; --s5:#7d8593;
    --seq-0:#15202f; --seq-1:#104281; --seq-2:#184f95; --seq-3:#256abf;
    --seq-4:#3987e5; --seq-5:#6da7ec; --seq-6:#9ec5f4;
    --ok:#199e70; --warn:#c98500;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --plane:#0d0e11; --surface:#191b1f; --line:#2b2f37; --line-soft:#212429;
  --ink:#f2f4f8; --ink-2:#aab2c0; --ink-3:#767e8d;
  --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#9085e9; --s5:#7d8593;
  --seq-0:#15202f; --seq-1:#104281; --seq-2:#184f95; --seq-3:#256abf;
  --seq-4:#3987e5; --seq-5:#6da7ec; --seq-6:#9ec5f4;
  --ok:#199e70; --warn:#c98500;
}
* { box-sizing:border-box; }
body {
  margin:0; background:var(--plane); color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,sans-serif; font-size:15px; line-height:1.6;
  -webkit-font-smoothing:antialiased;
}
.wrap { max-width:1080px; margin:0 auto; padding:48px 24px 80px; }
header { border-bottom:1px solid var(--line); padding-bottom:26px; margin-bottom:34px; }
h1 {
  font-family:"IBM Plex Serif",Georgia,serif; font-weight:600;
  font-size:clamp(28px,4.4vw,40px); line-height:1.15; letter-spacing:-.015em;
  margin:0 0 12px; text-wrap:balance;
}
.sub { color:var(--ink-2); max-width:62ch; margin:0; }
.meta {
  font-family:"IBM Plex Mono",monospace; font-size:12px; color:var(--ink-3);
  margin-top:16px; display:flex; flex-wrap:wrap; gap:6px 20px;
}
h2 {
  font-family:"IBM Plex Serif",Georgia,serif; font-weight:600; font-size:21px;
  letter-spacing:-.01em; margin:0 0 6px;
}
.lede { color:var(--ink-2); margin:0 0 20px; max-width:64ch; }
section { margin-top:44px; }
.eyebrow {
  font-family:"IBM Plex Mono",monospace; font-size:11px; font-weight:500;
  letter-spacing:.1em; text-transform:uppercase; color:var(--ink-3); margin-bottom:8px;
}
.tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:14px; }
.tile { background:var(--surface); border:1px solid var(--line); border-radius:10px; padding:16px 18px; }
.tile .k { font-size:12px; color:var(--ink-2); line-height:1.4; }
.tile .v {
  font-family:"IBM Plex Mono",monospace; font-variant-numeric:tabular-nums;
  font-size:30px; font-weight:600; letter-spacing:-.02em; margin:6px 0 2px;
}
.tile .n { font-size:12px; color:var(--ink-3); line-height:1.4; }
.card { background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:20px 20px 12px; }
.legend { display:flex; flex-wrap:wrap; gap:8px 20px; margin:0 0 6px; padding:0 2px; }
.lg { display:flex; align-items:center; gap:7px; font-size:13px; color:var(--ink-2); }
.sw { width:15px; height:3px; border-radius:2px; flex:none; }
.sw.d { height:0; border-top:3px dashed currentColor; border-radius:0; }
figure { margin:0; overflow-x:auto; }
svg { display:block; max-width:100%; }
.tip {
  position:fixed; pointer-events:none; opacity:0; transition:opacity .1s;
  background:var(--surface); border:1px solid var(--line); border-radius:9px;
  padding:9px 11px; font-size:12.5px; box-shadow:0 6px 22px rgba(0,0,0,.13); z-index:9;
  font-variant-numeric:tabular-nums; min-width:170px;
}
.tip b { font-family:"IBM Plex Mono",monospace; font-size:12px; display:block;
  margin-bottom:6px; color:var(--ink-3); font-weight:500; letter-spacing:.05em; }
.tip .r { display:flex; justify-content:space-between; gap:16px; align-items:center; }
.tip .r span:first-child { display:flex; align-items:center; gap:6px; color:var(--ink-2); }
.tip .r span:last-child { font-family:"IBM Plex Mono",monospace; font-weight:600; }
table { border-collapse:collapse; width:100%; font-size:13.5px; }
th, td { padding:9px 10px; text-align:right; border-bottom:1px solid var(--line-soft); }
th:first-child, td:first-child { text-align:left; }
thead th { font-size:11px; letter-spacing:.06em; text-transform:uppercase;
  color:var(--ink-3); font-weight:500; border-bottom:1px solid var(--line); }
td.n { font-family:"IBM Plex Mono",monospace; font-variant-numeric:tabular-nums; }
.layers { font-size:13px; }
.layers th, .layers td { padding:0; border-bottom:1px solid var(--line-soft); }
.layers thead th { padding:8px 10px; font-size:10.5px; }
.layers td.lyr { padding:0 10px; font-family:"IBM Plex Mono",monospace;
  font-variant-numeric:tabular-nums; color:var(--ink-3); width:56px; }
.layers td.b { padding:0; }
.layers td.b span {
  display:block; padding:7px 10px; font-family:"IBM Plex Mono",monospace;
  font-variant-numeric:tabular-nums; text-align:right;
}
.layers tr.mid td { background:var(--line-soft); }
.layers tr.mid td.lyr { color:var(--s1); font-weight:600; }
.layers tr.mid td.lyr::after { content:" ←"; }
.cell { border-radius:5px; padding:9px 6px; text-align:center; font-family:"IBM Plex Mono",monospace;
  font-variant-numeric:tabular-nums; font-size:13px; font-weight:500; }
.note { border-left:2px solid var(--s1); padding:2px 0 2px 16px; margin:22px 0 0;
  color:var(--ink-2); font-size:14px; max-width:66ch; }
.note strong { color:var(--ink); font-weight:600; }
ul.pts { margin:14px 0 0; padding-left:0; list-style:none; display:grid; gap:12px; max-width:66ch; }
ul.pts li { display:grid; grid-template-columns:auto 1fr; gap:11px; color:var(--ink-2); font-size:14px; }
ul.pts .m { font-family:"IBM Plex Mono",monospace; font-size:11.5px; color:var(--ink-3);
  padding-top:3px; white-space:nowrap; }
ul.pts strong { color:var(--ink); font-weight:600; }
footer { margin-top:52px; padding-top:20px; border-top:1px solid var(--line);
  font-size:12.5px; color:var(--ink-3); }
@media (prefers-reduced-motion:reduce) { * { transition:none !important; } }
</style>

<div class="wrap">
<header>
  <h1>__H1__</h1>
  <p class="sub">__SUB__</p>
  <div class="meta">__META__</div>
</header>

<section style="margin-top:0">
  <div class="eyebrow">Capa __MID__ · la del medio, L/2</div>
  <div class="tiles">__TILES__</div>
</section>

__MAIN__
__CTRL__
__MATRIX__
__LAYERS__

<section>
  <h2>Fiabilidad de la medición</h2>
  <p class="lede">Techo por split-half: se parte el dataset en dos mitades, se calcula el
  vector en cada una y se saca el coseno de una condición contra sí misma. Es el máximo
  observable dado el ruido de estimar una dirección de 3072 dimensiones con __N__ muestras.</p>
  <div class="card"><table>
    <thead><tr><th>Condición</th><th>Techo mínimo</th><th>Techo medio</th><th>Estado</th></tr></thead>
    <tbody>__CEIL__</tbody>
  </table></div>
  <p class="note">Todos por encima de <strong>0.95</strong>. Con n=__N__ las direcciones están
  muy bien estimadas y la corrección por atenuación sobra: verificado contra datos sintéticos,
  con techo alto el coseno crudo ya queda a menos de 0.05 del verdadero.</p>
</section>

<section>
  <h2>Cómo leerlo</h2>
  <ul class="pts">
    <li><span class="m">escala</span><span>En Ball et al. (<a href="https://arxiv.org/abs/2406.09289" style="color:var(--s1)">arXiv:2406.09289</a>),
    cosenos de <strong>0.4 a 0.6</strong> entre tipos de jailbreak distintos bastaron para concluir
    mecanismo compartido. No hay que esperar 0.9.</span></li>
    <li><span class="m">capa</span><span>El paper mide en <strong>una sola capa del medio</strong> (16 para
    modelos de 7B, 20 para 13B). Acá son 28 capas, así que la del medio es la <strong>14</strong>.</span></li>
    <li><span class="m">convergencia</span><span>Después de la capa ~20 el residual de la última
    posición ya codifica qué token emitir. Las condiciones que producen francés convergen y las que
    producen otro idioma divergen, <strong>las dos cosas por construcción</strong>. Ni la
    convergencia ni la divergencia de ahí en adelante son evidencia de mecanismo, y promediarlas
    infla el margen: +0.159 sobre 12–28 contra +__MARGIN_MID__ en la capa __MID__.</span></li>
    <li><span class="m">control</span><span>«respuesta corta» controla dos cosas a la vez: el cambio de
    modo genérico y los tokens prependidos. Que dé ~0.35 y no ~0.75 es lo que valida el resto.</span></li>
  </ul>
</section>

<footer>__FOOT__</footer>
</div>
<div class="tip" id="tip"></div>
<script>
const DATA = __DATA__;
const T = document.getElementById('tip');
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();

function line(id, series, lo, hi, mid) {
  const el = document.getElementById(id);
  const W = 1000, H = 340, P = {t:16, r:22, b:44, l:52};
  const xs = [], n = hi - lo + 1;
  const X = i => P.l + (W-P.l-P.r) * (n===1?0.5:(i)/(n-1));
  const Y = v => P.t + (H-P.t-P.b) * (1 - (v-0)/(1-0));
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Coseno por capa">`;
  for (let g=0; g<=5; g++) {
    const v = g/5, y = Y(v);
    s += `<line x1="${P.l}" y1="${y}" x2="${W-P.r}" y2="${y}" stroke="${css('--line-soft')}" stroke-width="1"/>`;
    s += `<text x="${P.l-10}" y="${y+4}" text-anchor="end" font-size="11.5" font-family="IBM Plex Mono" fill="${css('--ink-3')}">${v.toFixed(1)}</text>`;
  }
  if (mid >= lo && mid <= hi) {
    const x = X(mid-lo);
    s += `<line x1="${x}" y1="${P.t}" x2="${x}" y2="${H-P.b}" stroke="${css('--s1')}" stroke-width="1" stroke-dasharray="3 4" opacity=".5"/>`;
    s += `<text x="${x}" y="${P.t-3}" text-anchor="middle" font-size="10.5" font-family="IBM Plex Mono" fill="${css('--ink-3')}">L/2</text>`;
  }
  for (let i=0; i<n; i++) {
    const L = lo+i;
    if (L % 2 === 0 || n < 10)
      s += `<text x="${X(i)}" y="${H-P.b+19}" text-anchor="middle" font-size="11.5" font-family="IBM Plex Mono" fill="${css('--ink-3')}">${L}</text>`;
  }
  s += `<text x="${(P.l+W-P.r)/2}" y="${H-6}" text-anchor="middle" font-size="12" fill="${css('--ink-3')}">capa del residual stream</text>`;
  series.forEach(se => {
    const d = se.v.slice(lo, hi+1).map((v,i) => `${i?'L':'M'}${X(i).toFixed(1)} ${Y(v).toFixed(1)}`).join(' ');
    s += `<path d="${d}" fill="none" stroke="${css(se.c)}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"${se.dash?' stroke-dasharray="7 5"':''}/>`;
    const last = se.v[hi];
    s += `<circle cx="${X(n-1)}" cy="${Y(last)}" r="4.5" fill="${css(se.c)}" stroke="${css('--surface')}" stroke-width="2"/>`;
  });
  s += `<g id="${id}-cx" opacity="0"><line y1="${P.t}" y2="${H-P.b}" stroke="${css('--ink-3')}" stroke-width="1"/></g>`;
  s += `<rect x="${P.l}" y="${P.t}" width="${W-P.l-P.r}" height="${H-P.t-P.b}" fill="transparent" id="${id}-hit"/></svg>`;
  el.innerHTML = s;
  const svg = el.querySelector('svg'), cx = el.querySelector(`#${id}-cx`);
  el.querySelector(`#${id}-hit`).addEventListener('pointermove', e => {
    const r = svg.getBoundingClientRect(), sc = W / r.width;
    const px = (e.clientX - r.left) * sc;
    let i = Math.round((px - P.l) / ((W-P.l-P.r)/(n-1)));
    i = Math.max(0, Math.min(n-1, i));
    cx.setAttribute('opacity','1');
    cx.querySelector('line').setAttribute('x1', X(i)); cx.querySelector('line').setAttribute('x2', X(i));
    T.innerHTML = `<b>CAPA ${lo+i}</b>` + series.map(se =>
      `<div class="r"><span><i class="sw" style="display:inline-block;width:13px;height:3px;border-radius:2px;background:${css(se.c)}"></i>${se.n}</span><span>${se.v[lo+i].toFixed(3)}</span></div>`).join('');
    T.style.opacity = 1;
    T.style.left = Math.min(e.clientX + 16, innerWidth - 200) + 'px';
    T.style.top = (e.clientY - 12) + 'px';
  });
  el.addEventListener('pointerleave', () => { T.style.opacity = 0; cx.setAttribute('opacity','0'); });
}
DATA.charts.forEach(c => line(c.id, c.series, c.lo, c.hi, DATA.mid));
</script>
"""


def tile(k, v, n, color=None):
    st = f' style="color:{color}"' if color else ""
    return (f'<div class="tile"><div class="k">{k}</div>'
            f'<div class="v"{st}>{v}</div><div class="n">{n}</div></div>')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    d = json.load(open(args.json, encoding="utf-8"))
    lo = d["layers_from"]
    n_prompts = d["n_prompts"]
    L = len(d["cos_patch_frq"]) - 1
    mid = L // 2
    hi = L
    M = d.get("cos_matrix")
    # Banda informativa: a partir de ~L/2+3 el residual de la ultima posicion ya
    # esta dominado por "que token emito", asi que el coseno entre condiciones
    # que producen el MISMO idioma converge por construccion y el de las que
    # producen otro idioma diverge por construccion. Nada de eso es evidencia de
    # mecanismo. Los resumenes se calculan solo en la banda de abajo; los
    # graficos y la tabla siguen mostrando todo.
    info_hi = min(hi, mid + 3)
    conds = d.get("conditions") or ["patch", "frq", "instr"]

    def at(v, l):
        return v[l]

    pf, pi, fi = d["cos_patch_frq"], d["cos_patch_instr"], d["cos_frq_instr"]
    gap = at(pf, mid) - at(pi, mid)

    tiles = [
        tile("parche ~ pregunta FR", f"{at(pf, mid):.3f}", "el parche contra el estado de "
             "«la entrada está en francés»", "var(--s1)"),
        tile("parche ~ instrucción FR", f"{at(pi, mid):.3f}", "contra el estado de "
             "«me pidieron responder en francés»", "var(--s2)"),
        tile("brecha a favor de la pregunta", f"{gap:+.3f}",
             "el parche se parece más al estado de idioma que al de directiva",
             "var(--s1)" if gap > 0 else "var(--s2)"),
    ]
    if M:
        rng = slice(lo, info_hi + 1)
        avg = lambda a, b: sum(M[a][b][rng]) / (info_hi + 1 - lo)
        margen = (at(M["patch"]["frq"], mid)
                  - max(at(M["patch"]["de"], mid), at(M["patch"]["corto"], mid)))
        tiles.append(tile("margen sobre el mejor control", f"{margen:+.3f}",
                          f"en la capa {mid}; el francés por encima del alemán y del piso",
                          "var(--ok)" if margen >= .05 else "var(--warn)"))

    charts = [{"id": "c1", "lo": lo, "hi": hi, "series": [
        {"n": "parche ~ pregunta FR", "c": "--s1", "v": pf},
        {"n": "parche ~ instrucción FR", "c": "--s2", "v": pi},
        {"n": "pregunta FR ~ instrucción FR", "c": "--s3", "v": fi},
    ]}]

    def legend(items):
        return '<div class="legend">' + "".join(
            f'<span class="lg"><i class="sw{" d" if dash else ""}" style="{"color" if dash else "background"}:{c}"></i>{n}</span>'
            for n, c, dash in items) + "</div>"

    main_html = f"""<section>
  <div class="eyebrow">Comparación principal</div>
  <h2>¿A qué se parece el parche?</h2>
  <p class="lede">Coseno entre vectores de diferencia de medias, capa por capa. La tercera
  serie es el control que hace interpretables a las otras dos: si las dos referencias son
  iguales entre sí, preguntar a cuál se parece el parche no tiene respuesta.</p>
  <div class="card">
    {legend([("parche ~ pregunta FR", "var(--s1)", 0), ("parche ~ instrucción FR", "var(--s2)", 0),
             ("pregunta FR ~ instrucción FR", "var(--s3)", 0)])}
    <figure id="c1"></figure>
  </div>
  <p class="note">En las capas medias las dos referencias <strong>se separan</strong>
  ({fi[mid]:.2f} en la capa {mid}) y ahí el parche está claramente más cerca de la pregunta
  en francés. Desde la capa ~20 todo converge: el residual pasa a codificar qué token emitir y
  cualquier par de condiciones que produzcan francés se parece por construcción. La lectura vive
  en las capas {lo}–{info_hi}.</p>
</section>"""

    ctrl_html = ""
    matrix_html = ""
    if M:
        charts.append({"id": "c2", "lo": lo, "hi": hi, "series": [
            {"n": "parche ~ pregunta FR", "c": "--s1", "v": M["patch"]["frq"]},
            {"n": "parche ~ instrucción DE", "c": "--s4", "v": M["patch"]["de"], "dash": 1},
            {"n": "parche ~ respuesta corta", "c": "--s5", "v": M["patch"]["corto"], "dash": 1},
        ]})
        ctrl_html = f"""<section>
  <div class="eyebrow">Control</div>
  <h2>¿Mide idioma o mide «responder distinto»?</h2>
  <p class="lede">Las tres condiciones principales comparten algo trivial: todas hacen que el
  modelo responda distinto del baseline inglés. Sin un control no se puede saber si el coseno
  mide francés o ese componente genérico.</p>
  <div class="card">
    {legend([("parche ~ pregunta FR", "var(--s1)", 0), ("parche ~ instrucción DE", "var(--s4)", 1),
             ("parche ~ respuesta corta", "var(--s5)", 1)])}
    <figure id="c2"></figure>
  </div>
  <p class="note">«Respuesta corta» marca el piso genérico en <strong>~{avg('patch','corto'):.2f}</strong>,
  y también controla el confound de tokens prependidos. El alemán queda en
  <strong>{avg('patch','de'):.2f}</strong>: comparte el componente de cambio de idioma pero no el
  de francés. En la capa {mid} el margen del francés sobre el mejor control es
  <strong>{margen:+.3f}</strong>.<br><br>La separación que se abre a partir de la capa ~22
  <strong>no cuenta como evidencia</strong>: ahí el residual ya codifica qué token emitir, así que
  el alemán se aleja por producir tokens alemanes, no por operar distinto. Los resúmenes de esta
  página se calculan solo hasta la capa {info_hi}.</p>
</section>"""

        seq = ["--seq-0", "--seq-1", "--seq-2", "--seq-3", "--seq-4", "--seq-5", "--seq-6"]
        rows = ""
        for a in conds:
            cells = ""
            for b in conds:
                v = avg(a, b) if a != b else 1.0
                step = min(6, max(0, int(v * 7)))
                dark = step >= 4
                cells += (f'<td style="padding:3px"><div class="cell" style="background:var({seq[step]});'
                          f'color:{"#fff" if dark else "var(--ink)"}">{v:.2f}</div></td>')
            rows += f'<tr><td style="white-space:nowrap">{ETIQ[a]}</td>{cells}</tr>'
        heads = "".join(f"<th>{ETIQ[c]}</th>" for c in conds)
        matrix_html = f"""<section>
  <div class="eyebrow">Matriz completa · promedio capas {lo}–{info_hi}</div>
  <h2>Las cinco condiciones entre sí</h2>
  <p class="lede">Cada celda es el coseno entre los vectores medios de dos condiciones, promediado
  sobre la banda informativa (capas {lo}–{info_hi}, antes de que el residual quede dominado por el
  token de salida). Lo revelador está fuera de la fila del parche.</p>
  <div class="card" style="overflow-x:auto"><table>
    <thead><tr><th></th>{heads}</tr></thead><tbody>{rows}</tbody></table></div>
  <p class="note"><strong>La instrucción en francés se parece más a la instrucción en alemán
  ({avg('instr','de'):.2f}) que a la pregunta en francés ({avg('instr','frq'):.2f}).</strong>
  Las condiciones de instrucción están dominadas por un componente de «cumplí una directiva de
  cambiar de idioma»; el francés es lo de menos. El parche no tiene ese componente: contra el
  alemán cae a {avg('patch','de'):.2f}, muy por debajo del {avg('instr','de'):.2f} de la
  instrucción francesa. No puede codificar una directiva, y no la codifica.</p>
</section>"""

    # --- tabla capa por capa ------------------------------------------------
    cols = [("parche ~ preg. FR", pf, "--s1"),
            ("parche ~ instr. FR", pi, "--s2"),
            ("preg. FR ~ instr. FR", fi, "--s3")]
    if M:
        cols += [("parche ~ instr. DE", M["patch"]["de"], "--s4"),
                 ("parche ~ resp. corta", M["patch"]["corto"], "--s5")]

    lrows = ""
    for l in range(lo, hi + 1):
        cells = ""
        for _, v, c in cols:
            w = max(0.0, min(1.0, v[l])) * 100
            cells += (f'<td class="b"><span style="background:linear-gradient(to right,'
                      f'color-mix(in srgb, var({c}) 22%, transparent) {w:.1f}%,'
                      f'transparent {w:.1f}%)">{v[l]:.3f}</span></td>')
        klass = ' class="mid"' if l == mid else ""
        lrows += f'<tr{klass}><td class="lyr">{l}</td>{cells}</tr>'
    lheads = "".join(
        f'<th><span style="display:inline-flex;align-items:center;gap:6px;justify-content:flex-end">'
        f'<i style="width:9px;height:9px;border-radius:2px;background:var({c});flex:none"></i>{n}</span></th>'
        for n, _, c in cols)

    layers_html = f"""<section>
  <div class="eyebrow">Evolución capa por capa</div>
  <h2>Los valores, capa a capa</h2>
  <p class="lede">La barra detrás de cada número es su magnitud, así que la columna se lee
  como un gráfico de barras hacia abajo. La fila marcada es la capa {mid}, la del medio.</p>
  <div class="card" style="overflow-x:auto; padding:14px 16px 6px">
    <table class="layers">
      <thead><tr><th style="text-align:left">capa</th>{lheads}</tr></thead>
      <tbody>{lrows}</tbody>
    </table>
  </div>
  <p class="note">Hasta la capa ~{info_hi}, <strong>parche ~ pregunta FR</strong> va por delante de
  las otras dos y <strong>preg. FR ~ instr. FR</strong> es la más baja de las tres. Desde la capa
  ~22 las tres suben juntas hacia 0.9 mientras los controles se caen — pero <strong>eso no es
  evidencia de nada</strong>: en las capas profundas el residual de la última posición ya codifica
  qué token emitir, así que lo que produce francés converge y lo que produce alemán diverge, por
  construcción. Por eso los resúmenes de esta página paran en la capa {info_hi}.<br><br>Lo que sí
  informa está en las capas medias: ahí el parche está a la <strong>misma distancia de la
  instrucción en francés que de la instrucción en alemán</strong> (0.584 vs 0.567 en la capa {mid},
  una diferencia de 0.018), y sin embargo claramente más cerca de la <em>pregunta</em> en francés
  (0.682). El parche no distingue qué idioma le piden: solo ve «instrucción». Lo específico del
  francés lo saca del otro lado.</p>
</section>"""

    ceil_rows = ""
    for k in ("patch", "frq", "instr"):
        c = d["ceiling_" + k][lo:hi + 1]
        ceil_rows += (f'<tr><td>{ETIQ[k]}</td><td class="n">{min(c):.3f}</td>'
                      f'<td class="n">{sum(c)/len(c):.3f}</td>'
                      f'<td style="color:var(--ok)">fiable</td></tr>')

    meta = (f"<span>n = {n_prompts} preguntas</span><span>{L} capas · d = 3072</span>"
            f"<span>última posición del prompt</span>"
            f"<span>{os.path.basename(d.get('patch',''))}</span>")

    html = (HTML
            .replace("__H1__", "Geometría del parche francés")
            .replace("__SUB__", "El parche aditivo de layer&nbsp;0 induce francés en el 90% de "
                     "las preguntas held-out. Esto mide <em>a qué se parece por dentro</em>: "
                     "vectores de diferencia de medias en el residual stream, método de "
                     "Ball&nbsp;et&nbsp;al., contra dos maneras normales de que el modelo "
                     "termine hablando francés.")
            .replace("__META__", meta)
            .replace("__MID__", str(mid))
            .replace("__TILES__", "".join(tiles))
            .replace("__MAIN__", main_html)
            .replace("__CTRL__", ctrl_html)
            .replace("__MATRIX__", matrix_html)
            .replace("__LAYERS__", layers_html)
            .replace("__MARGIN_MID__", f"{margen:.3f}" if M else "-")
            .replace("__CEIL__", ceil_rows)
            .replace("__N__", str(n_prompts))
            .replace("__FOOT__", f"Generado con <code>plot_mean_diff.py</code> desde "
                     f"<code>{os.path.basename(args.json)}</code>. Método: Ball, Kreuter &amp; "
                     f"Panickssery, <em>Understanding Jailbreak Success</em>, EACL 2026.")
            .replace("__DATA__", json.dumps({"charts": charts, "mid": mid})))

    out = args.out or os.path.join(os.path.dirname(args.json) or ".", "mean_diff.html")
    open(out, "w", encoding="utf-8").write(html)
    print(f"escrito {out}  ({len(html)//1024} KB)")
    print(f"  capa del medio L/2 = {mid}")
    print(f"  parche~preg.FR {at(pf, mid):.3f}   parche~instr.FR {at(pi, mid):.3f}   brecha {gap:+.3f}")
    if M:
        print(f"  margen sobre el mejor control: {margen:+.3f}")


if __name__ == "__main__":
    main()
