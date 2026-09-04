import glob, json, os, torch

def load(c):
    p = max(glob.glob(f"runs/_act_cache/acts_{c}_*.pt"), key=os.path.getmtime)
    return {i: s.float() for i, s in torch.load(p, map_location="cpu")["states"].items()}

cl, fr, ins = load("clean"), load("frq"), load("instr")
idx = sorted(cl)[:40]   # mean_diff_vectors usa usables.head(40)
d_fr  = torch.stack([fr[i]  - cl[i] for i in idx]).mean(0)
d_ins = torch.stack([ins[i] - cl[i] for i in idx]).mean(0)
cos = torch.nn.functional.cosine_similarity(d_fr, d_ins, dim=1)
ref = json.load(open("runs/v3_250/mean_diff_ctrl.json"))["cos_frq_instr"]

print(f"{'capa':>5}{'hooks':>10}{'json':>10}{'delta':>9}")
for l in (12, 14, 16, 20, 24):
    print(f"{l:>5}{cos[l-1]:>10.4f}{ref[l]:>10.4f}{cos[l-1]-ref[l]:>+9.4f}")