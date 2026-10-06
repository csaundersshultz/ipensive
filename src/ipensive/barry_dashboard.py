import logging
from pathlib import Path
import jinja2
from copy import deepcopy
import matplotlib as m
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib import rcParams
import pandas as pd
import json
import numpy as np
from datetime import date




rcParams.update({"font.size": 10})  # Set default font size for plots
m.use("Agg")  # Use a non-interactive backend for matplotlib
################################

my_log = logging.getLogger(__name__)


def write_barry_dashboard_html(config=None):
    """Render the Barry Arm dashboard page into the web output directory."""
    template_file = Path(__file__).parent / "templates" / "barry_dashboard.template"
    with open(template_file, "r") as f:
        template = jinja2.Template(f.read())

    out_dir = Path(config["OUT_WEB_DIR"]) if config else Path.cwd() / "output/html"
    out_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    plot_path = (Path("Landslides") / "Barry Arm East" / "velaz_plots" / f"barry_arm_velaz_{today}.png").as_posix()
    out_file = out_dir / "barry_dashboard.html"
    with open(out_file, "w") as f:
        f.write(template.render(plot_path=plot_path))
    my_log.info("Barry Arm dashboard html written")

def correct_velocity_for_temp():
    pass

def plot_zones_json(json_path, figax, zone_tag="zones", 
                    colrs=['green', 'blue', 'red', 'yellow', 'purple'], ls='-'):
    """
    Add kinematic zones to an existing plot
    """
    fig, ax = figax
    with open(json_path, "r") as f:
        data = json.load(f)
# Loop through each polygon entry
    for i, zone_data in enumerate(data[zone_tag]):
        lbl = zone_data['zone']
        xs = np.array(zone_data["x"])
        xs = np.where(xs<180, xs+360, xs) #loop around 360 for az values below 180
        ys = 1000 * np.array(zone_data["y"])

        coords = list(zip(xs, ys))

        poly = Polygon(
            coords,
            closed=True,
            fill=False,
            edgecolor=colrs[i % len(colrs)],
            linestyle=ls,
            linewidth=1,
            label=lbl
        )
        ax.add_patch(poly)
    return (fig,ax)


def is_barry_ascii_file_complete(config, plot_date):
    """Return whether the Barry Arm ASCII file has its expected 5,762 lines."""
    ascii_dir = Path(config["OUT_ASCII_DIR"])
    plot_day = plot_date.isoformat()
    data_file = ascii_dir / "Barry_Arm_East" / plot_day[:7] / f"Barry_Arm_East_{plot_day}.txt"
    if not data_file.exists():
        return False

    with open(data_file, "r") as f:
        return sum(1 for _ in f) == 5762


def barry_arm_plot(config=None, plot_date=None):
    """
    Locate the requested day's ASCII file, add kinematic elements overlay, and save it.
    """
    ascii_dir = Path(config["OUT_ASCII_DIR"]) if config else Path.cwd() / "output/ascii_output"
    plot_day = (plot_date or date.today()).isoformat()
    data_file = ascii_dir / "Barry_Arm_East" / plot_day[:7] / f"Barry_Arm_East_{plot_day}.txt"
    if not data_file.exists():
        my_log.warning("No Barry Arm ASCII file found for %s: %s", plot_day, data_file)
        return None
    df = pd.read_csv(data_file, sep="\t", parse_dates=["Time"])
    #df = df.dropna(subset=["Azimuth", "Velocity", "Sigma_tau", "Vel_err", "Baz_err"])
    df = df.loc[df["Sigma_tau"] <= 0.03]
    df = df.loc[(df["Azimuth"]>= 270) & (df["Azimuth"] <= 360)]

    #output filename
    plot_dir = (Path(config["OUT_WEB_DIR"]) if config else Path.cwd() / "output"/"html") / "Landslides" / "Barry Arm East" / "velaz_plots"
    plot_dir.mkdir(parents=True, exist_ok=True)
    plot_file = plot_dir / f"barry_arm_velaz_{plot_day}.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    zones_json_path = Path.cwd() / "data" / "barry_data" / "barry_zones_AzVel.json"
    plot_zones_json(zones_json_path, (fig,ax))
    ymin, ymax = 300, 380
    clipped_velocity = df["Velocity"].clip(lower=ymin, upper=ymax)
    scatter = ax.scatter(
        df["Azimuth"],
        clipped_velocity,
        c=df["MCCM"],
        cmap="RdYlBu_r",
        vmin=0.2,
        vmax=1.0,
        edgecolors="k",
        linewidths=0.3,
        s=10,
        alpha=0.5,
        clip_on=False
    )
    #ax.errorbar( df["Azimuth"], df['Velocity'], xerr=df["Baz_err"], yerr=df["Vel_err"], fmt="none", ecolor="black", elinewidth=0.7, capsize=2, alpha=0.1)

    # labels ec.
    ax.set_title(f"Barry Arm infrasound - {plot_day} \nSigmaTau<=0.3, n={len(df)}")
    ax.set_xlabel("Back-Azimuth [degrees]")
    ax.set_ylabel("Velocity [m/s]")

    ax.set_ylim(ymin, ymax)
    yticks = np.arange(ymin, ymax+1, 10)
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"<{yticks[0]}"] + [str(tick) for tick in yticks[1:-1]] + [f">{yticks[-1]}"])
    ax.set_xlim(270,360)
    ax.grid(True, alpha=0.25)
    fig.colorbar(scatter, ax=ax, label="MCCM")
    fig.tight_layout()

    plt.legend()

    #Saving
    fig.savefig(plot_file, dpi=120)
    plt.close(fig)

    my_log.info("Barry Arm plot created from %s", data_file)
    return plot_file


if __name__ == "__main__":
    pf = barry_arm_plot()
    print(f"Test barry arm plot created - {pf}")