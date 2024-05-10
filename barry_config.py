# SYSTEM PARAMETERS
# HOSTNAME	  = '137.227.224.220' #AVO waveserver?
# PORT		  = 16002

# TESTING!!!
HOSTNAME = "IRIS"  # waveserver to get data from  old="pubavo1.wr.usgs.gov"
PORT = 420  # No port for IRIS #old=16022
OUT_WEB_DIR = "C:/Users/csaunders-shultz/Documents/ipensive/output/pngs"
OUT_ASCII_DIR = "C:/Users/csaunders-shultz/Documents/ipensive/output/ascii"
LOGS_DIR = "C:/Users/csaunders-shultz/Documents/ipensive/output/logs"

# DEFAUlT PROCESSING PARAMETERS
DURATION = 600  # DON'T CHANGE THIS!
LATENCY = 60  # how long to pause and wait for data latency to catch up before processing (seconds)
EXTRA_PAUSE = 0  # extra pause in case some arrays are extra latent (Dillingham)
FREQMIN = 0.8  # minimum frequency
FREQMAX = 5.0  # maximum frequency
TAPER = 5.0  # seconds to taper beginning and end of trace before filtering
WINDOW_LENGTH = 30  # window length for each calculation [seconds]
OVERLAP = 15  # amount of overlap between windows [seconds]
MIN_CHAN = 3  # minimum number of channels needed to perform inversion

# DEFAULT PLOTTING PARAMETERS
MCTHRESH = 0.6  # where to draw the threshold line in MCCM plot
AZ_MIN = 0  # minimum azimuth to plot
AZ_MAX = 360  # maximum azimuth to plot
VEL_MIN = 0.25  # minimum sound speed range
VEL_MAX = 0.45  # maximum sound speed range
ARRAY_LABEL = "Infrasound"

# Infrasound channels list
NETWORKS = [
    {
        "Name": "AVO",
        "ARRAYS": [
            dict(
                {
                    "Name": "Barry Arm East",
                    "SCNL": [
                        {
                            "scnl": "BAEI.HDF.AV.01",
                            "sta_lat": 61.132675,
                            "sta_lon": -148.1219,
                        },
                        {
                            "scnl": "BAEI.HDF.AV.02",
                            "sta_lat": 61.132085,
                            "sta_lon": -148.12107,
                        },
                        {
                            "scnl": "BAEI.HDF.AV.03",
                            "sta_lat": 61.13173,
                            "sta_lon": -148.121985,
                        },
                        {
                            "scnl": "BAEI.HDF.AV.04",
                            "sta_lat": 61.131875,
                            "sta_lon": -148.122915,
                        },
                        {
                            "scnl": "BAEI.HDF.AV.05",
                            "sta_lat": 61.132405,
                            "sta_lon": -148.12281,
                        },
                        {
                            "scnl": "BAEI.HDF.AV.06",
                            "sta_lat": 61.13218,
                            "sta_lon": -148.12206,
                        },
                    ],
                    "digouti": (1 / 400000)
                    / 0.0275,  # convert counts to Pressure in Pa 01-Jun-2021
                    "volcano": [
                        {
                            "name": "Barry Glacier / Tail",
                            "v_lat": 61.145313,
                            "v_lon": -148.137882,
                        },
                        {"name": "Core", "v_lat": 61.150054, "v_lon": -148.148203},
                        {"name": "Prow", "v_lat": 61.141487, "v_lon": -148.153993},
                        {"name": "Kite", "v_lat": 61.139483, "v_lon": -148.168980},
                        {
                            "name": "Cascade Glacier",
                            "v_lat": 61.119845,
                            "v_lon": -148.171899,
                        },
                    ],
                    "AZ_MIN": 220,
                    "AZ_MAX": 340,
                }
            ),
        ],
    }
]
