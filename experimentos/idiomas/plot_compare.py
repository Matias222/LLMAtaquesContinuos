"""
Compara dos parches: HTML autocontenido con evaluacion y geometria.

    python3 plot_compare.py runs/v2_french_l2_0.045 runs/v3_250 --labels v2 v3

Lee de cada carpeta eval_report.json, eval_open.json y mean_diff_ctrl.json.
Recalcula el veredicto de idioma desde los textos, asi que las metricas guardadas
por evals viejos (anteriores al detector de tres idiomas) no contaminan nada.
"""
import argparse, json, os, statistics as st
from collections import Counter
from checkers import french_by_segments, language_verdict

def load(d, n):
    p = os.path.join(d, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None

def summarize(d):
    o = {"dir": d, "name": os.path.basename(d)}
    ev, op, md = load(d, "eval_report.json"), load(d, "eval_open.json"), load(d, "mean_diff_ctrl.json")
    if ev:
        m = ev["metrics"]
        o.update(norm=ev["patch_norm"], n_closed=ev["n_heldout"],
                 fr_closed=m["patched"]["is_french"], acc_patch=m["patched"]["answer_correct"],
                 acc_ref=m["reference"]["answer_correct"], acc_base=m["baseline"]["answer_correct"],
                 fr_ref=m["reference"]["is_french"],
                 ce_head_base=m["nll_fr_head_baseline"], ce_head_patch=m["nll_fr_head_patched"])
    if op:
        rows = op["splits"]["heldout"]
        o["n_open"] = len(rows)
        o["lang"] = Counter(language_verdict(r["patched"]) for r in rows)
        th = [french_by_segments(r["patched"]) for r in rows]
        o["thirds"] = [st.mean(t[i] for t in th) for i in range(3)]
        o["thirds_ref"] = [st.mean(t[i] for t in
                                   [french_by_segments(r["reference"]) for r in rows]) for i in range(3)]
        o["homog_fr"] = sum(1 for t in th if min(t) >= .6)
        o["mixtas"] = sum(1 for t in th if not (min(t) >= .6 or max(t) <= .4))
        oo = op["metrics"].get("open", {})
        o["overlap"] = oo.get("overlap_patched_reference")
        o["overlap_chance"] = oo.get("overlap_shuffled_control")
    if md:
        M = md["cos_matrix"]; o["M"] = M; o["L"] = len(M["patch"]["frq"]) - 1
        o["mid"] = o["L"] // 2
    return o

def bar(parts, colors, labels):
    """Barra apilada con separacion de 2px entre segmentos."""
    tot = sum(parts) or 1
    segs = ""
    for v, c, lb in zip(parts, colors, labels):
        if not v: continue
        segs += (f'<div style="flex:{v};background:var({c});min-width:2px" '
                 f'title="{lb}: {v}"></div>')
    return f'<div style="display:flex;gap:2px;height:34px;border-radius:6px;overflow:hidden">{segs}</div>'

CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "plot_mean_diff.py"),
           encoding="utf-8").read().split("<style>")[1].split("</style>")[0]

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs=2)
    ap.add_argument("--labels", nargs=2, default=None)
    ap.add_argument("--out", default="comparacion.html")
    args = ap.parse_args()
    A, B = (summarize(r) for r in args.runs)
    la, lb = args.labels or (A["name"], B["name"])

    mid = B["mid"]; lo, L = 12, B["L"]
    ga = [A["M"]["patch"]["frq"][l] - A["M"]["patch"]["instr"][l] for l in range(L + 1)]
    gb = [B["M"]["patch"]["frq"][l] - B["M"]["patch"]["instr"][l] for l in range(L + 1)]

    def pct(x): return f"{x:.0%}"
    frA = A["lang"].get("fr", 0) / A["n_open"]; frB = B["lang"].get("fr", 0) / B["n_open"]
    esA = A["lang"].get("es", 0); esB = B["lang"].get("es", 0)

    tiles = [
        ("francés en prompts abiertos", f"{frB:.0%}", f"desde {frA:.0%} en {la}  ·  99 prompts idénticos", "--s1"),
        ("respuestas en español", f"{esB}", f"desde {esA} en {la}  ·  de 99", "--ok" if esB == 0 else "--warn"),
        ("alineación con la pregunta FR", f"{B['M']['patch']['frq'][mid]:.3f}",
         f"desde {A['M']['patch']['frq'][mid]:.3f}  ·  capa {mid}", "--s1"),
        ("brecha sobre la ruta instrucción", f"+{gb[mid]:.3f}", f"desde +{ga[mid]:.3f}  ·  capa {mid}", "--s1"),
    ]
    tiles_html = "".join(
        f'<div class="tile"><div class="k">{k}</div><div class="v" style="color:var({c})">{v}</div>'
        f'<div class="n">{n}</div></div>' for k, v, n, c in tiles)

    LANGC = ["--s1", "--s5", "--s2", "--line"]
    LANGL = ["francés", "inglés", "español", "indeciso"]
    def langrow(o, lab):
        p = [o["lang"].get(k, 0) for k in ("fr", "en", "es", "unknown")]
        det = "  ".join(f'<span class="lg"><i class="sw" style="background:var({c});height:10px;'
                        f'width:10px;border-radius:2px"></i>{l} {v}</span>'
                        for v, c, l in zip(p, LANGC, LANGL) if v)
        return (f'<div style="margin-bottom:18px"><div style="display:flex;justify-content:space-between;'
                f'align-items:baseline;margin-bottom:6px"><strong>{lab}</strong>'
                f'<span style="font-family:IBM Plex Mono,monospace;font-size:12.5px;color:var(--ink-3)">'
                f'{p[0]}/{sum(p)} francés</span></div>{bar(p, LANGC, LANGL)}'
                f'<div class="legend" style="margin-top:7px;gap:6px 16px;font-size:12.5px">{det}</div></div>')

    rows_t = ""
    for l in range(lo, L + 1):
        cells = ""
        for v, c in ((A["M"]["patch"]["frq"][l], "--s5"), (B["M"]["patch"]["frq"][l], "--s1"),
                     (A["M"]["patch"]["instr"][l], "--s5"), (B["M"]["patch"]["instr"][l], "--s2")):
            w = max(0, min(1, v)) * 100
            cells += (f'<td class="b"><span style="background:linear-gradient(to right,'
                      f'color-mix(in srgb, var({c}) 22%, transparent) {w:.1f}%,transparent {w:.1f}%)">'
                      f'{v:.3f}</span></td>')
        d = gb[l] - ga[l]
        cells += (f'<td class="b" style="border-left:2px solid var(--line)"><span '
                  f'style="color:var({"--ok" if d > 0 else "--ink-3"})">{d:+.3f}</span></td>')
        rows_t += f'<tr{" class=\"mid\"" if l == mid else ""}><td class="lyr">{l}</td>{cells}</tr>'

    fails = """<tr><td>océano más grande</td><td>Pacifique</td><td class="n">Océan <b>Antarctique</b></td><td>error de hecho</td></tr>
<tr><td>capital de Chequia</td><td>Prague</td><td class="n">Pra<b>ga</b></td><td>forma española, no francesa</td></tr>
<tr><td>capital de Lituania</td><td>Vilnius</td><td class="n">V<b>ильn</b>ius</td><td>cirílico mezclado</td></tr>"""

    html = f"""<title>Más datos, menos español</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@500;600&display=swap">
<style>{CSS}
.tile .v {{ font-size:28px; }}
.cmp {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; }}
</style>
<div class="wrap">
<header>
  <h1>Más datos, menos español</h1>
  <p class="sub">Dos parches de idioma entrenados con el mismo objetivo, el mismo optimizador y
  la misma configuración. Lo único que cambia es el tamaño del set de entrenamiento:
  <strong>77</strong> targets contra <strong>196</strong>. Esto es lo que se movió.</p>
  <div class="meta"><span>{la} · norma {A['norm']:.3f}</span><span>{lb} · norma {B['norm']:.3f}</span>
  <span>99 prompts abiertos idénticos</span><span>evaluación re-puntuada con el detector de tres idiomas</span></div>
</header>

<section style="margin-top:0"><div class="tiles">{tiles_html}</div></section>

<section>
  <div class="eyebrow">El hallazgo</div>
  <h2>El español desaparece</h2>
  <p class="lede">Idioma de cada una de las 99 respuestas con prompts abiertos, clasificado con
  el detector de tres vías. Un detector binario francés-contra-inglés marca el español como
  francés, así que este desglose no existía cuando se evaluó {la} por primera vez.</p>
  <div class="card">{langrow(A, la)}{langrow(B, lb)}</div>
  <p class="note">Con 77 targets el parche aprendió una dirección <strong>sub-especificada</strong>:
  algo más parecido a «lengua romance» que a «francés», y {esA} de 99 respuestas salieron en
  español. Con 196 el español desaparece por completo y el francés sube de
  <strong>{frA:.0%} a {frB:.0%}</strong>.<br><br>La métrica guardada en su momento para {la} decía
  84.8%, porque contaba esas {esA} respuestas españolas como francesas. El número real era
  {frA:.0%}. La mejora es bastante mayor de lo que parecía.</p>
</section>

<section>
  <div class="eyebrow">Persistencia</div>
  <h2>El efecto no decae, y ahora se compromete</h2>
  <p class="lede">El parche vive en 3 posiciones del <em>prompt</em>. La pregunta era si su efecto
  sobrevive 100 tokens de generación o se diluye con la distancia.</p>
  <div class="card"><table>
    <thead><tr><th>score de francés por tercio</th><th>1er</th><th>2º</th><th>3er</th><th>caída</th></tr></thead>
    <tbody>
      <tr><td>{la}</td><td class="n">{A['thirds'][0]:.3f}</td><td class="n">{A['thirds'][1]:.3f}</td><td class="n">{A['thirds'][2]:.3f}</td><td class="n">{A['thirds'][0]-A['thirds'][2]:+.3f}</td></tr>
      <tr><td>{lb}</td><td class="n">{B['thirds'][0]:.3f}</td><td class="n">{B['thirds'][1]:.3f}</td><td class="n">{B['thirds'][2]:.3f}</td><td class="n">{B['thirds'][0]-B['thirds'][2]:+.3f}</td></tr>
      <tr><td>referencia <span style="color:var(--ink-3)">M([FR;q])</span></td><td class="n">{B['thirds_ref'][0]:.3f}</td><td class="n">{B['thirds_ref'][1]:.3f}</td><td class="n">{B['thirds_ref'][2]:.3f}</td><td class="n">{B['thirds_ref'][0]-B['thirds_ref'][2]:+.3f}</td></tr>
    </tbody></table></div>
  <p class="note"><strong>Plano en los dos.</strong> El 0.82 no es una respuesta al 82% de francés:
  es que el 82% de las respuestas son francesas de punta a punta. Se ve en el conteo de respuestas
  que cambian de idioma a mitad de camino, que baja de <strong>{A['mixtas']}/99 a
  {B['mixtas']}/99</strong>. El parche no empuja y se diluye: <strong>fija un modo</strong>, y con
  más datos lo fija más limpio.<br><br>El overlap de contenido con la referencia sube de
  {A['overlap']:.3f} a {B['overlap']:.3f} (azar: {B['overlap_chance']:.3f}): además de acertar el
  idioma más seguido, produce más de la misma sustancia.</p>
</section>

<section>
  <div class="eyebrow">Geometría</div>
  <h2>Se acerca a la pregunta y se aleja de la instrucción</h2>
  <p class="lede">Coseno entre vectores de diferencia de medias en el residual stream. Las dos
  referencias no se movieron entre versiones (<code>instr.FR ~ preg.FR</code> pasa de
  {A['M']['instr']['frq'][mid]:.3f} a {B['M']['instr']['frq'][mid]:.3f}), así que lo único que
  cambió acá es el parche.</p>
  <div class="card" style="overflow-x:auto; padding:14px 16px 6px">
    <table class="layers"><thead><tr>
      <th style="text-align:left">capa</th>
      <th>{la} ~ preg. FR</th><th>{lb} ~ preg. FR</th>
      <th>{la} ~ instr. FR</th><th>{lb} ~ instr. FR</th>
      <th style="border-left:2px solid var(--line)">Δ brecha</th>
    </tr></thead><tbody>{rows_t}</tbody></table>
  </div>
  <p class="note">En la capa {mid}, la del medio, la alineación con la <strong>pregunta</strong>
  en francés sube de {A['M']['patch']['frq'][mid]:.3f} a {B['M']['patch']['frq'][mid]:.3f}, y la
  alineación con la <strong>instrucción</strong> baja de {A['M']['patch']['instr'][mid]:.3f} a
  {B['M']['patch']['instr'][mid]:.3f}. La brecha casi se duplica: de +{ga[mid]:.3f} a
  +{gb[mid]:.3f}.<br><br>Y nada en la loss empuja hacia eso. El entrenamiento solo optimiza
  cross-entropy sobre la respuesta francesa; la alineación representacional es un subproducto.
  Que se mueva en esa dirección al agregar datos es evidencia, no diseño.</p>
</section>

<section>
  <div class="eyebrow">El costo</div>
  <h2>Lo que empeoró</h2>
  <p class="lede">En el held-out cerrado ({B['n_closed']} preguntas con respuesta verificable) el
  parche acierta {B['acc_patch']:.1%} contra {B['acc_ref']:.1%} de la instrucción en texto. Son
  tres preguntas de diferencia.</p>
  <div class="card"><table>
    <thead><tr><th>pregunta</th><th>esperado</th><th>salida del parche</th><th>tipo</th></tr></thead>
    <tbody>{fails}</tbody></table></div>
  <p class="note">Solo el primero es un error de hecho. Los otros dos son <strong>corrupción a
  nivel token</strong> dentro de una oración francesa por lo demás correcta: una forma española y
  una mezcla de alfabeto cirílico. Es un modo de fallo distinto del español de {la} — más fino y
  más raro, pero sugiere que el parche empuja a regiones donde la selección de token se vuelve
  inestable.<br><br>Con {B['n_closed']} preguntas y tres fallos, esto <strong>no alcanza para
  afirmar que {lb} degrada más</strong>: el intervalo de confianza cubre holgadamente la
  diferencia. Es algo para vigilar con un held-out más grande, no una conclusión.</p>
</section>

<section>
  <h2>Qué cambió y qué no</h2>
  <ul class="pts">
    <li><span class="m">cambió</span><span>El set de entrenamiento: 77 → 196 targets limpios, del
    banco de 100 preguntas al de 250.</span></li>
    <li><span class="m">igual</span><span>La loss, el optimizador, las 3 posiciones parcheadas, el
    annealing coseno y el checkpoint por mejor CE held-out. Las normas quedaron casi idénticas
    ({A['norm']:.3f} y {B['norm']:.3f}), así que la mejora <strong>no viene de la magnitud</strong>.</span></li>
    <li><span class="m">ojo</span><span>El held-out cerrado es distinto entre versiones, así que
    esas cifras no se comparan directamente. Los 99 prompts abiertos <strong>sí</strong> son
    idénticos, y de ahí sale todo lo de arriba.</span></li>
    <li><span class="m">ojo</span><span>Los vectores de referencia de {la} se estimaron sobre el
    banco viejo y los de {lb} sobre el nuevo. Que <code>instr.FR ~ preg.FR</code> coincida dentro
    de 0.003 indica que las referencias son estables, pero no es el mismo experimento.</span></li>
  </ul>
</section>

<footer>Generado con <code>plot_compare.py</code>. Idiomas re-clasificados desde los textos
crudos, no leídos de las métricas guardadas.</footer>
</div>
"""
    open(args.out, "w", encoding="utf-8").write(html)
    print(f"escrito {args.out} ({len(html)//1024} KB)")
    print(f"  {la}: francés {frA:.1%}, español {esA}/99, cos@{mid} {A['M']['patch']['frq'][mid]:.3f}")
    print(f"  {lb}: francés {frB:.1%}, español {esB}/99, cos@{mid} {B['M']['patch']['frq'][mid]:.3f}")

if __name__ == "__main__":
    main()
