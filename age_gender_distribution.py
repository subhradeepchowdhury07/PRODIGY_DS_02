import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import os

# ── Output folder ─────────────────────────────────────────────────────────────
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Styling ───────────────────────────────────────────────────────────────────
BG    = "#F8F7F4"
PANEL = "#FFFFFF"
TEXT  = "#2C2C2A"
MUTED = "#888780"
GRID  = "#E5E3DC"
MALE_COLOR   = "#378ADD"
FEMALE_COLOR = "#D4537E"

plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "axes.facecolor":    PANEL,
    "figure.facecolor":  BG,
    "axes.edgecolor":    GRID,
    "axes.grid":         True,
    "grid.color":        GRID,
    "grid.linewidth":    0.6,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "text.color":        TEXT,
    "axes.labelcolor":   TEXT,
    "xtick.color":       MUTED,
    "ytick.color":       MUTED,
})

SOURCE = "Source: UN World Population Prospects 2024 (estimates)"

def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"  Saved → {path}")
    plt.close(fig)

# ── UN WPP 2024 — World estimates (millions), 5-year age groups ───────────────
# https://population.un.org/wpp/
AGE_GROUPS = [
    "0–4","5–9","10–14","15–19","20–24","25–29",
    "30–34","35–39","40–44","45–49","50–54","55–59",
    "60–64","65–69","70–74","75–79","80–84","85–89","90–94","95–99","100+"
]

# Population in millions (World, 2024 estimate)
MALE = np.array([
    341.5, 327.8, 316.2, 310.1, 309.4, 307.6,
    295.8, 277.4, 258.2, 241.6, 220.5, 196.4,
    168.7, 139.2, 107.3,  75.8,  48.2,  24.6,
      9.1,   2.6,   0.5
])
FEMALE = np.array([
    326.1, 313.2, 302.4, 296.7, 296.2, 294.8,
    284.1, 267.3, 250.4, 236.0, 218.2, 197.2,
    173.8, 147.3, 118.2,  89.4,  62.4,  35.7,
     15.4,   5.2,   1.4
])

# Gender share by region (%) — Male / Female
REGION_GENDER = {
    "World":                        (49.7, 50.3),
    "Africa":                       (50.1, 49.9),
    "Asia":                         (50.5, 49.5),
    "Europe":                       (48.5, 51.5),
    "Latin America & Caribbean":    (49.3, 50.7),
    "Northern America":             (49.4, 50.6),
    "Oceania":                      (49.8, 50.2),
}

# Broad age group share (%) — World 2024
BROAD_AGES = {
    "0–14 (Children)":   25.4,
    "15–24 (Youth)":     15.6,
    "25–64 (Working age)": 48.3,
    "65+ (Older adults)": 10.7,
}

# Historical median age (World)
YEARS_MED   = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2024]
MEDIAN_AGES = [23.6, 23.0, 22.0, 22.5, 24.2, 26.1, 28.4, 30.9, 31.7]

# ═══════════════════════════════════════════════════════════════════════════════
# Chart 1 — Population Pyramid (Age & Gender Distribution)
# ═══════════════════════════════════════════════════════════════════════════════
print("Chart 1: Population Pyramid …")
fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor(BG)
ax.set_facecolor(PANEL)

y = np.arange(len(AGE_GROUPS))
ax.barh(y, -MALE,  color=MALE_COLOR,   height=0.75, edgecolor="none", label="Male")
ax.barh(y,  FEMALE, color=FEMALE_COLOR, height=0.75, edgecolor="none", label="Female")

ax.set_yticks(y)
ax.set_yticklabels(AGE_GROUPS, fontsize=10)
ax.set_xlabel("Population (millions)", fontsize=11, labelpad=8)
ax.set_title("World population pyramid by age & gender — 2024",
             fontsize=14, fontweight="500", pad=16, color=TEXT, loc="left")

max_val = max(MALE.max(), FEMALE.max())
ax.set_xlim(-max_val * 1.15, max_val * 1.15)
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{abs(x):.0f}M")
)

ax.axvline(0, color=GRID, linewidth=1.2)
ax.text(-max_val * 0.57, len(AGE_GROUPS) - 0.3, "Male",
        fontsize=12, color=MALE_COLOR, fontweight="500")
ax.text( max_val * 0.35, len(AGE_GROUPS) - 0.3, "Female",
        fontsize=12, color=FEMALE_COLOR, fontweight="500")

fig.text(0.99, 0.01, SOURCE, ha="right", fontsize=8, color=MUTED)
plt.tight_layout()
save(fig, "01_population_pyramid.png")

# ═══════════════════════════════════════════════════════════════════════════════
# Chart 2 — Gender Distribution by Region (stacked bar)
# ═══════════════════════════════════════════════════════════════════════════════
print("Chart 2: Gender Distribution by Region …")
regions = list(REGION_GENDER.keys())
male_pct   = [v[0] for v in REGION_GENDER.values()]
female_pct = [v[1] for v in REGION_GENDER.values()]

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(PANEL)

x = np.arange(len(regions))
ax.bar(x, male_pct,   color=MALE_COLOR,   width=0.55, edgecolor="none", label="Male")
ax.bar(x, female_pct, color=FEMALE_COLOR,  width=0.55, edgecolor="none",
       bottom=male_pct, label="Female")

ax.axhline(50, color=TEXT, linewidth=0.8, linestyle="--", alpha=0.4)
ax.text(len(regions) - 0.45, 50.3, "50 %", fontsize=8, color=MUTED)

for i, (m, f) in enumerate(zip(male_pct, female_pct)):
    ax.text(i, m / 2,       f"{m:.1f}%", ha="center", va="center",
            fontsize=9, color="white", fontweight="500")
    ax.text(i, m + f / 2,   f"{f:.1f}%", ha="center", va="center",
            fontsize=9, color="white", fontweight="500")

ax.set_xticks(x)
ax.set_xticklabels(regions, fontsize=9, rotation=15, ha="right")
ax.set_ylabel("Share of population (%)", fontsize=11, labelpad=8)
ax.set_ylim(0, 105)
ax.set_title("Male vs female share by world region — 2024",
             fontsize=14, fontweight="500", pad=16, color=TEXT, loc="left")

legend_handles = [
    mpatches.Patch(color=MALE_COLOR,   label="Male"),
    mpatches.Patch(color=FEMALE_COLOR, label="Female"),
]
ax.legend(handles=legend_handles, loc="upper right", fontsize=10,
          frameon=True, framealpha=0.9, edgecolor=GRID)

fig.text(0.99, 0.01, SOURCE, ha="right", fontsize=8, color=MUTED)
plt.tight_layout()
save(fig, "02_gender_by_region.png")

# ═══════════════════════════════════════════════════════════════════════════════
# Chart 4 — Age Distribution: Male vs Female overlay
# ═══════════════════════════════════════════════════════════════════════════════
print("Chart 4: Age Distribution Overlay …")
fig, ax = plt.subplots(figsize=(11, 5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(PANEL)

x = np.arange(len(AGE_GROUPS))
w = 0.38
ax.bar(x - w/2, MALE,   width=w, color=MALE_COLOR,   alpha=0.9,
       edgecolor="none", label="Male")
ax.bar(x + w/2, FEMALE, width=w, color=FEMALE_COLOR,  alpha=0.9,
       edgecolor="none", label="Female")

ax.set_xticks(x)
ax.set_xticklabels(AGE_GROUPS, fontsize=9, rotation=35, ha="right")
ax.set_ylabel("Population (millions)", fontsize=11, labelpad=8)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}M"))
ax.set_title("Male vs female population by age group — World 2024",
             fontsize=14, fontweight="500", pad=16, color=TEXT, loc="left")

legend_handles = [
    mpatches.Patch(color=MALE_COLOR,   label=f"Male   (total {MALE.sum():.0f}M)"),
    mpatches.Patch(color=FEMALE_COLOR, label=f"Female (total {FEMALE.sum():.0f}M)"),
]
ax.legend(handles=legend_handles, loc="upper right", fontsize=10,
          frameon=True, framealpha=0.9, edgecolor=GRID)

fig.text(0.99, 0.01, SOURCE, ha="right", fontsize=8, color=MUTED)
plt.tight_layout()
save(fig, "04_age_gender_overlay.png")

# ═══════════════════════════════════════════════════════════════════════════════
# Chart 5 — Rising Median Age Over Time
# ═══════════════════════════════════════════════════════════════════════════════
print("Chart 5: Median Age Trend …")
fig, ax = plt.subplots(figsize=(10, 4))
fig.patch.set_facecolor(BG)
ax.set_facecolor(PANEL)

ax.fill_between(YEARS_MED, MEDIAN_AGES, alpha=0.12, color="#7F77DD")
ax.plot(YEARS_MED, MEDIAN_AGES, color="#7F77DD", linewidth=2.5, marker="o",
        markersize=6, markerfacecolor=PANEL, markeredgewidth=2)

for yr, age in zip(YEARS_MED, MEDIAN_AGES):
    ax.text(yr, age + 0.35, f"{age}", ha="center", fontsize=9,
            color="#7F77DD", fontweight="500")

ax.set_xlim(1945, 2028)
ax.set_ylim(18, 36)
ax.set_xlabel("Year", fontsize=11, labelpad=8)
ax.set_ylabel("Median age (years)", fontsize=11, labelpad=8)
ax.set_title("World median age is rising — 1950 to 2024",
             fontsize=14, fontweight="500", pad=16, color=TEXT, loc="left")
ax.tick_params(labelsize=9)

fig.text(0.99, 0.01, SOURCE, ha="right", fontsize=8, color=MUTED)
plt.tight_layout()
save(fig, "05_median_age_trend.png")

print("\nAll 5 charts saved to the 'output/' folder.")
print("Libraries needed: matplotlib, numpy  (pip install matplotlib numpy)")
