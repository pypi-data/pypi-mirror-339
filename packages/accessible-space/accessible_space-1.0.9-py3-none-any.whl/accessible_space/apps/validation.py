import functools
import gc
import importlib
import math
import sys
import os
import subprocess
import uuid
import netcal.metrics.confidence

import matplotlib.patches

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import matplotlib.pyplot as plt
import mplsoccer
# import psutil
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import sklearn.model_selection
import streamlit as st
import xmltodict
import kloppy.metrica

from accessible_space.utility import get_unused_column_name, progress_bar
from accessible_space.interface import per_object_frameify_tracking_data, get_expected_pass_completion, get_dangerous_accessible_space, plot_expected_completion_surface
from accessible_space.core import PARAMETER_BOUNDS


cache_dir = os.path.join(os.path.dirname(__file__), ".joblib-cache")
memory = joblib.Memory(verbose=0)

metrica_open_data_base_dir = "https://raw.githubusercontent.com/metrica-sports/sample-data/refs/heads/master/data"

# PREFIT_PARAMS = {"a_max": 34.98577765329907, "b0": 14.307280169228356, "b1": -231.7861293805111,
#                  "exclude_passer": True, "inertial_seconds": 1.1354178248836497,
#                  "keep_inertial_velocity": True, "n_v0": 7.454954615235632, "normalize": False,
#                  "pass_start_location_offset": -0.7978801423524864,
#                  "player_velocity": 31.023509491980597, "radial_gridsize": 5.456708513777949,
#                  "time_offset_ball": -0.6530280473299319, "tol_distance": 6.730245091897855,
#                  "use_approx_two_point": True, "use_efficient_sigmoid": True, "use_fixed_v0": True,
#                  "use_max": False, "use_poss": True, "v0_max": 27.829349276867582,
#                  "v0_min": 4.142039313955755, "v0_prob_aggregation_mode": "mean",
#                  "v_max": 7.055841492280175}
PREFIT_PARAMS = {"a_max": 19.942472316273097, "b0": 13.260772123749703, "b1": -127.09674547384373,
                 "exclude_passer": True, "inertial_seconds": 1.3395881692600928, "keep_inertial_velocity": True,
                 "n_v0": 12.247054481867808, "normalize": False, "pass_start_location_offset": -1.8511411034901555,
                 "player_velocity": 20.15065924009609, "radial_gridsize": 3.711704666931358,
                 "time_offset_ball": -0.5271934355925483, "tol_distance": 10.46499802361764,
                 "use_approx_two_point": True, "use_efficient_sigmoid": True, "use_fixed_v0": True, "use_max": False,
                 "use_poss": True, "v0_max": 26.574734241456405, "v0_min": 12.008983050682373,
                 "v0_prob_aggregation_mode": "mean", "v_max": 8.337625232516878}
# PREFIT_PARAMS = {"a_max":15.320522976441866,"b0":7.652265667897893,"b1":-387.0112850702951,"exclude_passer":True,"inertial_seconds":0.8409501339936791,"keep_inertial_velocity":True,"n_v0":11.891555158694638,"normalize":False,"pass_start_location_offset":0.9120646929315286,"player_velocity":35.05882750031251,"radial_gridsize":3.767212990186012,"time_offset_ball":-0.2590790006707344,"tol_distance":13.736206935581796,"use_approx_two_point":True,"use_efficient_sigmoid":True,"use_fixed_v0":True,"use_max":False,"use_poss":True,"v0_max":35.27727379709076,"v0_min":13.163066579023884,"v0_prob_aggregation_mode":"mean","v_max":21.845468713434915}
# PREFIT_PARAMS = {"a_max":41.90193498181908,"b0":-14.690056100552695,"b1":-148.88001744880762,"exclude_passer":True,"inertial_seconds":0.2250365781096205,"keep_inertial_velocity":True,"n_v0":14.54322577016436,"normalize":False,"pass_start_location_offset":1.9777702688754788,"player_velocity":17.57480218475458,"radial_gridsize":4.022150910529389,"time_offset_ball":-0.2329821187407557,"tol_distance":18.531430660435102,"use_approx_two_point":False,"use_efficient_sigmoid":True,"use_fixed_v0":True,"use_max":True,"use_poss":True,"v0_max":38.10728919164311,"v0_min":6.915469083830606,"v0_prob_aggregation_mode":"max","v_max":29.708163108996636}


def bootstrap_metric_ci(y_true, y_pred, fnc, n_iterations=1000, conf_level=0.95, **kwargs):
    bs_loglosses = []
    for _ in range(n_iterations * 10):
        indices = np.random.choice(len(y_true), size=len(y_true), replace=True)
        y_true_sample = y_true[indices]
        y_pred_sample = y_pred[indices]
        res = fnc(y_true_sample, y_pred_sample, **kwargs)
        if res is not None:
            bs_loglosses.append(res)
        if len(bs_loglosses) >= n_iterations:
            break

    bs_loglosses = np.array(sorted(bs_loglosses))

    logloss = fnc(y_true, y_pred, **kwargs)

    if len(bs_loglosses) == 0:
        return logloss, None, None

    percentile_alpha = ((1 - conf_level) / 2) * 100
    ci_lower = np.percentile(bs_loglosses, percentile_alpha)
    ci_higher = np.percentile(bs_loglosses, 100 - percentile_alpha)

    return logloss, ci_lower, ci_higher



def bootstrap_logloss_ci(y_true, y_pred, n_iterations=1000, all_labels=np.array([0, 1]), conf_level=0.95):
    return bootstrap_metric_ci(y_true, y_pred, sklearn.metrics.log_loss, n_iterations, conf_level, labels=all_labels)


def bootstrap_brier_ci(y_true, y_pred, n_iterations=1000, conf_level=0.95):
    return bootstrap_metric_ci(y_true, y_pred, sklearn.metrics.brier_score_loss, n_iterations, conf_level)


def ece(y_true, y_pred, bins=10):
    ece = netcal.metrics.confidence.ECE(bins=int(bins))
    return ece.measure(y_pred, y_true)


def ece_ci(y_true, y_pred, n_iterations=1000, conf_level=0.95):
    return bootstrap_metric_ci(y_true, y_pred, ece, n_iterations, conf_level)


def bootstrap_auc_ci(y_true, y_pred, n_iterations=1000, conf_level=0.95):
    def error_handled_auc(y_true, y_pred):
        try:
            return sklearn.metrics.roc_auc_score(y_true, y_pred)
        except ValueError:
            return None
    return bootstrap_metric_ci(y_true, y_pred, error_handled_auc, n_iterations, conf_level)


@memory.cache
def get_metrica_tracking_data(dataset_nr, limit=None):
    dataset = kloppy.metrica.load_open_data(dataset_nr, limit=None)
    df_tracking = dataset.to_df()
    return df_tracking


# TODO rename
@st.cache_resource
def get_kloppy_events(dataset_nr):
    if dataset_nr in [1, 2]:
        # df = pd.read_csv(f"C:/Users/Jonas/Desktop/ucloud/Arbeit/Spielanalyse/soccer-analytics/football1234/datasets/metrica/sample-data-master/data/Sample_Game_{dataset_nr}/Sample_Game_{dataset_nr}_RawEventsData.csv")
        df = pd.read_csv(f"{metrica_open_data_base_dir}/Sample_Game_{dataset_nr}/Sample_Game_{dataset_nr}_RawEventsData.csv")
        df["body_part_type"] = df["Subtype"].where(df["Subtype"].isin(["HEAD"]), None)
        df["set_piece_type"] = df["Subtype"].where(
            df["Subtype"].isin(["THROW IN", "GOAL KICK", "FREE KICK", "CORNER KICK"]), None).map(
            lambda x: x.replace(" ", "_") if x is not None else None
        )
        df["Type"] = df["Type"].str.replace(" ", "_")
        df["Start X"] = (df["Start X"] - 0.5) * 105
        df["Start Y"] = -(df["Start Y"] - 0.5) * 68
        df["End X"] = (df["End X"] - 0.5) * 105
        df["End Y"] = -(df["End Y"] - 0.5) * 68
        df = df.rename(columns={
            "Type": "event_type",
            "Period": "period_id",
            "Team": "team_id",
            "From": "player_id",
            "To": "receiver_player_id",
            "Start X": "coordinates_x",
            "Start Y": "coordinates_y",
            "End X": "end_coordinates_x",
            "End Y": "end_coordinates_y",
            "Start Frame": "frame_id",
            "End Frame": "end_frame_id",
        })
        player_id_to_column_id = {}
        column_id_to_team_id = {}
        for team_id in df["team_id"].unique():
            df_players = df[df["team_id"] == team_id]
            team_player_ids = set(
                df_players["player_id"].dropna().tolist() + df_players["receiver_player_id"].dropna().tolist())
            player_id_to_column_id.update(
                {player_id: f"{team_id.lower().strip()}_{player_id.replace('Player', '').strip()}" for player_id in
                 team_player_ids})
            column_id_to_team_id.update({player_id_to_column_id[player_id]: team_id for player_id in team_player_ids})

        df["player_id"] = df["player_id"].map(player_id_to_column_id)
        df["receiver_player_id"] = df["receiver_player_id"].map(player_id_to_column_id)
        df["receiver_team_id"] = df["receiver_player_id"].map(column_id_to_team_id)

        df["tmp_next_player"] = df["player_id"].shift(-1)
        df["tmp_next_team"] = df["team_id"].shift(-1)
        df["tmp_receiver_player"] = df["receiver_player_id"].where(df["receiver_player_id"].notna(), df["tmp_next_player"])
        df["tmp_receiver_team"] = df["tmp_receiver_player"].map(column_id_to_team_id)

        df["success"] = df["tmp_receiver_team"] == df["team_id"]

        df["is_pass"] = (df["event_type"].isin(["PASS", "BALL_LOST", "BALL_OUT"])) \
                        & (~df["Subtype"].isin(["CLEARANCE", "HEAD-CLEARANCE", "HEAD-INTERCEPTION-CLEARANCE"])) \
                        & (df["frame_id"] != df["end_frame_id"])

        df["is_high"] = df["Subtype"].isin([
            "CROSS",
            # "CLEARANCE",
            "CROSS-INTERCEPTION",
            # "HEAD-CLEARANCE",
            # "HEAD-INTERCEPTION-CLEARANCE"
        ])

        #     df_passes["xc"], _, _ = dangerous_accessible_space.get_expected_pass_completion(
        #         df_passes, df_tracking, event_frame_col="td_frame", tracking_frame_col="frame", event_start_x_col="start_x",
        #         event_start_y_col="start_y", event_end_x_col="end_x", event_end_y_col="end_y",
        #         event_player_col="tracking_player_id",
        #     )

        return df.drop(columns=["tmp_next_player", "tmp_next_team", "tmp_receiver_player", "tmp_receiver_team"])
    else:
        # dataset = kloppy.metrica.load_event(
        #     event_data="C:/Users/Jonas/Desktop/ucloud/Arbeit/Spielanalyse/soccer-analytics/football1234/datasets/metrica/sample-data-master/data/Sample_Game_3/Sample_Game_3_events.json",
        #     # meta_data="https://raw.githubusercontent.com/metrica-sports/sample-data/refs/heads/master/data/Sample_Game_3/Sample_Game_3_metadata.xml",
        #     meta_data="C:/Users/Jonas/Desktop/ucloud/Arbeit/Spielanalyse/soccer-analytics/football1234/datasets/metrica/sample-data-master/data/Sample_Game_3/Sample_Game_3_metadata.xml",
        #     coordinates="secondspectrum",
        # )
        # json_data = json.load(open("C:/Users/Jonas/Desktop/ucloud/Arbeit/Spielanalyse/soccer-analytics/football1234/datasets/metrica/sample-data-master/data/Sample_Game_3/Sample_Game_3_events.json"))
        # json_data = json.loads(open(f"{metrica_open_data_base_dir}/Sample_Game_3/Sample_Game_3_events.json"))
        json_data = requests.get(f"{metrica_open_data_base_dir}/Sample_Game_3/Sample_Game_3_events.json").json()

        df = pd.json_normalize(json_data["data"])

        expanded_df = pd.DataFrame(df['subtypes'].apply(pd.Series))
        expanded_df.columns = [f'subtypes.{col}' for col in expanded_df.columns]

        new_dfs = []
        for expanded_col in expanded_df.columns:
            expanded_df2 = pd.json_normalize(expanded_df[expanded_col])
            expanded_df2.columns = [f'{expanded_col}.{col}' for col in expanded_df2.columns]
            new_dfs.append(expanded_df2)

        expanded_df = pd.concat(new_dfs, axis=1)

        df = pd.concat([df, expanded_df], axis=1)

        i_subtypes_nan = ~df["subtypes.name"].isna()
        i_subtypes_0_nan = ~df["subtypes.0.name"].isna()

        # check if the True's are mutually exclusive
        assert not (i_subtypes_nan & i_subtypes_0_nan).any()

        df.loc[i_subtypes_nan, "subtypes.0.name"] = df.loc[i_subtypes_nan, "subtypes.name"]
        df.loc[i_subtypes_nan, "subtypes.0.id"] = df.loc[i_subtypes_nan, "subtypes.id"]
        df = df.drop(columns=["subtypes.name", "subtypes.id", "subtypes"])
        subtype_cols = [col for col in df.columns if col.startswith("subtypes.") and col.endswith("name")]

        player2team = df[['from.id', 'team.id']].set_index('from.id')['team.id'].to_dict()
        df["receiver_team_id"] = df["to.id"].map(player2team)
        # df["tmp_next_player"] = df["player_id"].shift(-1)
        # df["tmp_next_team"] = df["team_id"].shift(-1)
        # df["tmp_receiver_player"] = df["receiver_player_id"].where(df["receiver_player_id"].notna(), df["tmp_next_player"])
        # df["tmp_receiver_team"] = df["tmp_receiver_player"].map(column_id_to_team_id)
        df["success"] = df["receiver_team_id"] == df["team.id"]

        df["success"] = df["success"].astype(bool)

        df["is_pass"] = (df["type.name"].isin(["PASS", "BALL LOST", "BALL OUT"])) \
                        & ~df[subtype_cols].isin(["CLEARANCE"]).any(axis=1) \
                        & (df["start.frame"] != df["end.frame"])

        # df[df[['Name', 'Age']].isin(['Alice', 30]).any(axis=1)]
        df["is_high"] = df[subtype_cols].isin(["CROSS"]).any(axis=1)

        df = df.rename(columns={
            "type.name": "event_type",
            "from.id": "player_id",
            "team.id": "team_id",
            "to.id": "receiver_player_id",
            "period": "period_id",
            "start.frame": "frame_id",
            "end.frame": "end_frame_id",
            "start.x": "coordinates_x",
            "start.y": "coordinates_y",
            "end.x": "end_coordinates_x",
            "end.y": "end_coordinates_y",
        }).drop(columns=[
            "to",
        ])
        df["coordinates_x"] = (df["coordinates_x"] - 0.5) * 105
        df["coordinates_y"] = (df["coordinates_y"] - 0.5) * 68
        df["end_coordinates_x"] = (df["end_coordinates_x"] - 0.5) * 105
        df["end_coordinates_y"] = (df["end_coordinates_y"] - 0.5) * 68

        meta_data = xmltodict.parse(requests.get(f"{metrica_open_data_base_dir}/Sample_Game_3/Sample_Game_3_metadata.xml").text)

        df_player = pd.json_normalize(meta_data, record_path=["main", "Metadata", "Players", "Player"])
        player2team = df_player[["@id", "@teamId"]].set_index("@id")["@teamId"].to_dict()
        df["team_id"] = df["player_id"].map(player2team)

        return df


@st.cache_resource
def get_metrica_data(dummy=False):
    datasets = []
    dfs_event = []
    st.write(" ")
    st.write(" ")
    progress_bar_text = st.empty()
    st_progress_bar = st.progress(0)
    dataset_nrs = [1, 2, 3] if not dummy else [1, 3]
    for dataset_nr in dataset_nrs:
    # for dataset_nr in [3]:
        progress_bar_text.text(f"Loading dataset {dataset_nr}")
        # dataset = kloppy.metrica.load_tracking_csv(
        #     home_data=f"https://raw.githubusercontent.com/metrica-sports/sample-data/master/data/Sample_Game_{dataset_nr}/Sample_Game_{dataset_nr}_RawTrackingData_Home_Team.csv",
        #     away_data=f"https://raw.githubusercontent.com/metrica-sports/sample-data/master/data/Sample_Game_{dataset_nr}/Sample_Game_{dataset_nr}_RawTrackingData_Away_Team.csv",
        #     # sample_rate=1 / 5,
        #     # limit=100,
        #     coordinates="secondspectrum"
        # )
        # df_events1 = pd.read_csv(f"https://raw.githubusercontent.com/metrica-sports/sample-data/refs/heads/master/data/Sample_Game_{dataset_nr}/Sample_Game_{dataset_nr}_RawEventsData.csv")
        # df_passes1 = df_events1[df_events1["Type"] == "PASS"]

        with st.spinner(f"Downloading events from dataset {dataset_nr}"):
            df_events = get_kloppy_events(dataset_nr).copy()
        event_frames = df_events["frame_id"].unique()

        delta_frames_to_load = 5

        frames_to_load = [set(range(event_frame, event_frame + delta_frames_to_load)) for event_frame in event_frames]
        frames_to_load = sorted(list(set([frame for frames in frames_to_load for frame in frames])))

        with st.spinner(f"Downloading tracking data from dataset {dataset_nr}"):
            df_tracking = get_metrica_tracking_data(dataset_nr)

        df_tracking = df_tracking[df_tracking["frame_id"].isin(frames_to_load)]

        df_tracking[[col for col in df_tracking.columns if col.endswith("_x")]] = (df_tracking[[col for col in df_tracking.columns if col.endswith("_x")]].astype(float) - 0.5) * 105
        df_tracking[[col for col in df_tracking.columns if col.endswith("_y")]] = (df_tracking[[col for col in df_tracking.columns if col.endswith("_y")]].astype(float) - 0.5) * 68

        df_tracking = df_tracking.drop(columns=[col for col in df_tracking.columns if col.endswith("_d") or col.endswith("_s")])

        players = [col.replace("_x", "") for col in df_tracking.columns if col.endswith("_x")]
        x_cols = [f"{player}_x" for player in players]
        y_cols = [f"{player}_y" for player in players]
        vx_cols = [f"{player}_vx" for player in players]
        vy_cols = [f"{player}_vy" for player in players]
        v_cols = [f"{player}_velocity" for player in players]
        frame_col = "frame_id"

        # dt = df_tracking["timestamp"].diff().mean()

        # df_tracking["ball_vx"] = df_tracking["ball_x"].diff() / df_tracking["timestamp"].dt.total_seconds().diff()
        # df_tracking["ball_vy"] = df_tracking["ball_y"].diff() / df_tracking["timestamp"].dt.total_seconds().diff()
        # df_tracking["ball_velocity"] = np.sqrt(df_tracking["ball_vx"]**2 + df_tracking["ball_vy"]**2)
        for player in players:
            df_tracking[f"{player}_x"] = df_tracking[f"{player}_x"].astype(float)
            xdiff = df_tracking[f"{player}_x"].diff().fillna(method="bfill")
            xdiff2 = -df_tracking[f"{player}_x"].diff(periods=-1).fillna(method="ffill")
            tdiff = df_tracking["timestamp"].diff().dt.total_seconds().fillna(method="bfill")
            tdiff2 = -df_tracking["timestamp"].diff(periods=-1).dt.total_seconds().fillna(method="ffill")
            vx = (xdiff + xdiff2) / (tdiff + tdiff2)
            df_tracking[f"{player}_vx"] = vx

            df_tracking[f"{player}_y"] = df_tracking[f"{player}_y"].astype(float)
            ydiff = df_tracking[f"{player}_y"].diff().fillna(method="bfill")
            ydiff2 = -df_tracking[f"{player}_y"].diff(periods=-1).fillna(method="ffill")
            vy = (ydiff + ydiff2)  # / (tdiff + tdiff2)
            df_tracking[f"{player}_vy"] = vy
            df_tracking[f"{player}_velocity"] = np.sqrt(vx ** 2 + vy ** 2)

            i_nan_x = df_tracking[f"{player}_x"].isna()
            df_tracking.loc[i_nan_x, f"{player}_vx"] = np.nan
            i_nan_y = df_tracking[f"{player}_y"].isna()
            df_tracking.loc[i_nan_y, f"{player}_vy"] = np.nan
            df_tracking.loc[i_nan_x | i_nan_y, f"{player}_velocity"] = np.nan

        player_to_team = {}
        if dataset_nr in [1, 2]:
            for player in players:
                if "home" in player:
                    player_to_team[player] = "Home"
                elif "away" in player:
                    player_to_team[player] = "Away"
                else:
                    player_to_team[player] = None
        else:
            player_to_team = df_events[['player_id', 'team_id']].set_index('player_id')['team_id'].to_dict()

        df_tracking_obj = per_object_frameify_tracking_data(
            df_tracking, frame_col,
            coordinate_cols=[[x_cols[i], y_cols[i], vx_cols[i], vy_cols[i], v_cols[i]] for i, _ in enumerate(players)],
            players=players, player_to_team=player_to_team,
            new_coordinate_cols=["x", "y", "vx", "vy", "v"],
            new_team_col="team_id", new_player_col="player_id",
        )

        # get ball control
        fr2control = df_events.set_index("frame_id")["team_id"].to_dict()
        df_tracking_obj["ball_possession"] = df_tracking_obj["frame_id"].map(fr2control)
        df_tracking_obj = df_tracking_obj.sort_values("frame_id")
        df_tracking_obj["ball_possession"] = df_tracking_obj["ball_possession"].ffill()

        if dummy:
            df_events = df_events.iloc[:100]
            df_tracking_obj = df_tracking_obj[df_tracking_obj["frame_id"].isin(df_events["frame_id"].unique())]

        datasets.append(df_tracking_obj)
        dfs_event.append(df_events)

        st_progress_bar.progress(dataset_nr / 3)

    return datasets, dfs_event


def check_synthetic_pass(p4ss, df_tracking_frame_attacking, v_receiver, v_receiver_threshold=4, v_players=10, pass_duration_threshold=0.5, pass_length_threshold=15, distance_to_origin_threshold=7.5):
    """ Checks whether a synthetic pass is guaranteed to be unsuccessful according to the criteria of our validation """

    p4ss["angle"] = math.atan2(p4ss["end_coordinates_y"] - p4ss["coordinates_y"], p4ss["end_coordinates_x"] - p4ss["coordinates_x"])

    if v_receiver > v_receiver_threshold:
        return False  # Criterion 1: Receiver is not too fast

    v0_pass = p4ss["v0"]
    v0x_pass = v0_pass * math.cos(p4ss["angle"])
    v0y_pass = v0_pass * math.sin(p4ss["angle"])
    x0_pass = p4ss["coordinates_x"]
    y0_pass = p4ss["coordinates_y"]

    pass_length = math.sqrt((p4ss["coordinates_x"] - p4ss["end_coordinates_x"]) ** 2 + (p4ss["coordinates_y"] - p4ss["end_coordinates_y"]) ** 2)
    pass_duration = pass_length / v0_pass
    if pass_duration < pass_duration_threshold or pass_length < pass_length_threshold:
        return False  # Criterion 2: Pass is not too short

    df_tracking_frame_attacking = df_tracking_frame_attacking[
        (df_tracking_frame_attacking["team_id"] == p4ss["team_id"]) &
        (df_tracking_frame_attacking["player_id"] != p4ss["player_id"])
    ]
    for _, row in df_tracking_frame_attacking.iterrows():
        x_player = row["x"]
        y_player = row["y"]

        distance_to_target = math.sqrt((x_player - p4ss["end_coordinates_x"]) ** 2 + (y_player - p4ss["end_coordinates_y"]) ** 2)
        necessary_speed_to_reach_target = distance_to_target / pass_duration
        distance_to_origin = math.sqrt((x_player - p4ss["coordinates_x"]) ** 2 + (y_player - p4ss["coordinates_y"]) ** 2)

        def can_intercept(x0b, y0b, vxb, vyb, x_A, y_A, v_A, duration):
            # Constants
            C = (x0b - x_A) ** 2 + (y0b - y_A) ** 2
            B = 2 * ((x0b - x_A) * vxb + (y0b - y_A) * vyb)
            A = v_A ** 2 - (vxb ** 2 + vyb ** 2)

            if A <= 0:
                # If A is non-positive, agent A cannot intercept object B
                return False

            # Calculate the discriminant of the quadratic equation
            discriminant = B ** 2 + 4 * A * C

            # Check if the discriminant is non-negative and if there are real, positive roots
            if discriminant >= 0:
                # Roots of the quadratic equation
                sqrt_discriminant = math.sqrt(discriminant)
                t1 = (B - sqrt_discriminant) / (2 * A)
                t2 = (B + sqrt_discriminant) / (2 * A)

                # Check if any of the roots are non-negative
                if t1 >= 0 or t2 >= 0 and t1 < duration and t2 < duration:
                    return True

            return False

        # st.write("distance_to_origin", distance_to_origin, distance_to_target)
        if necessary_speed_to_reach_target < v_players or distance_to_origin < distance_to_origin_threshold or can_intercept(x0_pass, y0_pass, v0x_pass, v0y_pass, x_player, y_player, v_players, pass_duration):
            # st.write("False")
            return False  # Criterion 3: Pass cannot be received by any teammate

    return True


def add_synthetic_passes(
    df_passes, df_tracking, n_synthetic_passes=5, event_frame_col="frame_id", tracking_frame_col="frame_id",
    event_team_col="team_id", tracking_team_col="team_id", event_player_col="player_id",
    tracking_player_col="player_id", x_col="x", y_col="y",
    new_is_synthetic_col="is_synthetic"
):
    st.write("n_synthetic_passes", n_synthetic_passes)
    df_passes[new_is_synthetic_col] = False
    synthetic_passes = []

    teams = df_tracking[tracking_team_col].unique()

    for _, p4ss in df_passes.sample(frac=1).iterrows():
        # for attacking_team in df_tracking[tracking_team_col].unique():
        for attacking_team in teams:
            df_frame_players = df_tracking[
                (df_tracking[event_frame_col] == p4ss[event_frame_col]) &
                (df_tracking[x_col].notna()) &
                (df_tracking[event_team_col].notna())  # ball
            ]
            df_frames_defenders = df_frame_players[df_frame_players[tracking_team_col] != attacking_team]
            df_frame_attackers = df_frame_players[df_frame_players[tracking_team_col] == attacking_team]

            for _, attacker_frame in df_frame_attackers.iterrows():
                for _, defender_frame in df_frames_defenders.iterrows():
                    for v0 in [10]:  # [5, 10, 15, 20]:
                        synthetic_pass = {
                            "frame_id": p4ss[event_frame_col],
                            "coordinates_x": attacker_frame[x_col],
                            "coordinates_y": attacker_frame[y_col],
                            "end_coordinates_x": defender_frame[x_col],
                            "end_coordinates_y": defender_frame[y_col],
                            "event_type": None,
                            "Subtype": None,
                            "period": None,
                            "end_frame_id": None,
                            "v0": v0,
                            "player_id": attacker_frame[tracking_player_col],
                            "team_id": attacker_frame[tracking_team_col],
                            "success": False,
                            new_is_synthetic_col: True,
                        }
                        # assert p4ss[event_team_col] == attacker_frame[tracking_team_col]
                        # i += 1
                        # if i > 15:
                        #     st.stop()

                        if check_synthetic_pass(synthetic_pass, df_frame_players, v_receiver=defender_frame["v"]):
                            synthetic_passes.append(synthetic_pass)
                            if len(synthetic_passes) >= n_synthetic_passes:
                                break
                    if len(synthetic_passes) >= n_synthetic_passes:
                        break
                if len(synthetic_passes) >= n_synthetic_passes:
                    break
            if len(synthetic_passes) >= n_synthetic_passes:
                break
        if len(synthetic_passes) >= n_synthetic_passes:
            break

    df_synthetic_passes = pd.DataFrame(synthetic_passes)

    assert len(df_synthetic_passes) == n_synthetic_passes, f"len(df_synthetic_passes)={len(df_synthetic_passes)} != n_synthetic_passes={n_synthetic_passes}, (len(synthetic_passes)={len(synthetic_passes)}"

    return pd.concat([df_passes, df_synthetic_passes], axis=0)

# TODO change definition of impossible pass to exclude passes where opponent is around passer (e.g. 5 meter radius)
def get_scores(_df, baseline_accuracy, outcome_col="success", add_confidence_intervals=True):
    df = _df.copy()

    data = {}

    # Descriptives
    data["average_accuracy"] = df[outcome_col].mean()
    data["synthetic_share"] = df["is_synthetic"].mean()

    # Baselines
    data["baseline_brier"] = sklearn.metrics.brier_score_loss(df[outcome_col], [baseline_accuracy] * len(df))
    try:
        data["baseline_logloss"] = sklearn.metrics.log_loss(df[outcome_col], [baseline_accuracy] * len(df))
    except ValueError:
        data["baseline_logloss"] = np.nan
    try:
        data["baseline_auc"] = sklearn.metrics.roc_auc_score(df[outcome_col], [baseline_accuracy] * len(df))
    except ValueError:
        data["baseline_auc"] = np.nan

    if "xc" in df.columns:
        data["avg_xc"] = df["xc"].mean()
        # Model scores
        data["brier_score"] = (df[outcome_col] - df["xc"]).pow(2).mean()

        data["ece"] = ece(df[outcome_col].values, df["xc"].values)

        if add_confidence_intervals:
            logloss_from_ci, logloss_ci_lower, logloss_ci_upper = bootstrap_logloss_ci(df[outcome_col].values, df["xc"].values)
            data["logloss_ci_lower"] = logloss_ci_lower
            data["logloss_ci_upper"] = logloss_ci_upper
            _, brier_ci_lower, brier_ci_upper = bootstrap_brier_ci(df[outcome_col].values, df["xc"].values)
            data["brier_ci_lower"] = brier_ci_lower
            data["brier_ci_upper"] = brier_ci_upper
            _, auc_ci_lower, auc_ci_upper = bootstrap_auc_ci(df[outcome_col].values, df["xc"].values)
            data["auc_ci_lower"] = auc_ci_lower
            data["auc_ci_upper"] = auc_ci_upper
            _, ecll_ci_lower, ecll_ci_upper = ece_ci(df[outcome_col].values, df["xc"].values)
            data["ece_ci_lower"] = ecll_ci_lower
            data["ece_ci_upper"] = ecll_ci_upper

        # data["brier_score"] = sklearn.metrics.brier_score_loss(df[outcome_col], df["xc"])

        try:
            data["logloss"] = sklearn.metrics.log_loss(df[outcome_col], df["xc"], labels=np.array([0, 1]))
        except ValueError:
            data["logloss"] = np.nan
        try:
            data["auc"] = sklearn.metrics.roc_auc_score(df[outcome_col], df["xc"], labels=np.array([0, 1]))
        except ValueError:
            data["auc"] = np.nan
    else:
        data["brier_score"] = np.nan
        data["logloss"] = np.nan
        data["auc"] = np.nan

    # Model scores by syntheticness
    for is_synthetic in [False, True]:
        synth_str = "synthetic" if is_synthetic else "real"
        df_synth = df[df["is_synthetic"] == is_synthetic]

        baseline_accuracy_synth = df_synth[outcome_col].mean()

        if "xc" in df.columns:
            try:
                data[f"brier_score_{synth_str}"] = sklearn.metrics.brier_score_loss(df_synth[outcome_col], df_synth["xc"])
            except ValueError:
                data[f"brier_score_{synth_str}"] = np.nan
            try:
                data[f"logloss_{synth_str}"] = sklearn.metrics.log_loss(df_synth[outcome_col], df_synth["xc"], labels=np.array([0, 1]))
            except ValueError:
                data[f"logloss_{synth_str}"] = np.nan
            try:
                data[f"auc_{synth_str}"] = sklearn.metrics.roc_auc_score(df_synth[outcome_col], df_synth["xc"], labels=np.array([0, 1]))
            except ValueError:
                data[f"auc_{synth_str}"] = np.nan
            try:
                data[f"ece_{synth_str}"] = ece(df_synth[outcome_col].values, df_synth["xc"])
            except (ValueError, AssertionError):
                data[f"ece_{synth_str}"] = np.nan

            if add_confidence_intervals:
                logloss_from_ci, logloss_ci_lower, logloss_ci_upper = bootstrap_logloss_ci(df_synth[outcome_col].values, df_synth["xc"].values)
                data[f"logloss_ci_lower_{synth_str}"] = logloss_ci_lower
                data[f"logloss_ci_upper_{synth_str}"] = logloss_ci_upper
                _, brier_ci_lower, brier_ci_upper = bootstrap_brier_ci(df_synth[outcome_col].values, df_synth["xc"].values)
                data[f"brier_ci_lower_{synth_str}"] = brier_ci_lower
                data[f"brier_ci_upper_{synth_str}"] = brier_ci_upper
                _, auc_ci_lower, auc_ci_upper = bootstrap_auc_ci(df_synth[outcome_col].values, df_synth["xc"].values)
                data[f"auc_ci_lower_{synth_str}"] = auc_ci_lower
                data[f"auc_ci_upper_{synth_str}"] = auc_ci_upper
                _, ecll_ci_lower, ecll_ci_upper = ece_ci(df[outcome_col].values, df["xc"].values)
                data["ece_ci_lower"] = ecll_ci_lower
                data["ece_ci_upper"] = ecll_ci_upper

        data[f"average_accuracy_{synth_str}"] = df_synth[outcome_col].mean()
        data[f"synthetic_share_{synth_str}"] = df_synth["is_synthetic"].mean()
        try:
            data[f"baseline_brier_{synth_str}"] = sklearn.metrics.brier_score_loss(df_synth[outcome_col], [baseline_accuracy_synth] * len(df_synth))
        except ValueError:
            data[f"baseline_brier_{synth_str}"] = np.nan
        try:
            data[f"baseline_loglos_{synth_str}"] = sklearn.metrics.log_loss(df_synth[outcome_col], [baseline_accuracy_synth] * len(df_synth))
        except ValueError:
            data[f"baseline_loglos_{synth_str}"] = np.nan
        try:
            data[f"baseline_auc_{synth_str}"] = sklearn.metrics.roc_auc_score(df_synth[outcome_col], [baseline_accuracy_synth] * len(df_synth))
        except ValueError:
            data[f"baseline_auc_{synth_str}"] = np.nan
        try:
            data[f"ece_{synth_str}"] = np.nan  # ece(df_synth[outcome_col].values, [baseline_accuracy_synth] * len(df_synth))
        except ValueError:
            data[f"ece_{synth_str}"] = np.nan

    return data


def calibration_histogram(df, hist_col="xc", synth_col="is_synthetic", n_bins=None, binsize=None, add_text=True, use_boken_axis=True):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.style.use("seaborn-v0_8")
    plt.figure()

    # reset style

    if use_boken_axis:
        import brokenaxes
        bax = brokenaxes.brokenaxes(xlims=((0, 1),), ylims=((0, 400), (1600, 1650)), hspace=0.125)
    else:
        bax = plt.gca()
    plt.title("Distribution of predicted pass success rates in training set")

    # x = np.linspace(0, 1, 100)
    # bax.plot(x, np.sin(10 * x), label='sin')
    # bax.plot(x, np.cos(10 * x), label='cos')
    # bax.legend(loc=3)
    # bax.set_xlabel('time')
    # bax.set_ylabel('value')

    # if binsize is None and n_bins is not None:
    #     df[bin_col] = pd.qcut(df[hist_col], n_bins, labels=False, duplicates="drop")
    # elif binsize is not None and n_bins is None:
    #     min_val = df[hist_col].min()
    #     max_val = df[hist_col].max()
    #     bin_edges = [min_val + i * binsize for i in range(int((max_val - min_val) / binsize) + 2)]
    #     df[bin_col] = pd.cut(df[hist_col], bins=bin_edges, labels=False, include_lowest=True)
    # else:
    #     raise ValueError("Either n_bins or binsize must be specified")
    custom_style = {
        'axes.edgecolor': 'gray',
        'axes.facecolor': 'whitesmoke',
        'axes.grid': True,
        'grid.color': 'lightgray',
        'grid.linestyle': '--',
        'axes.spines.right': False,
        'axes.spines.top': False,
    }
    plt.rcParams.update({
        'axes.facecolor': 'gray',
        'axes.edgecolor': 'black',
        'axes.grid': True,
        'grid.color': '.8',
        'grid.linestyle': '-',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'xtick.bottom': True,
        'ytick.left': True,
        'axes.titlesize': 16,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.frameon': False,
        'legend.fontsize': 12,
        'figure.facecolor': 'gray',
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans'],
        'lines.linewidth': 1.5,
        'lines.markersize': 6,
    })
    plt.rcParams.update(custom_style)

    # plt.hist(data, bins=30, stacked=True, label=['Data 1', 'Data 2', 'Data 3'], color=['blue', 'green', 'red'])
    import matplotlib.cm
    cmap = matplotlib.cm.get_cmap('viridis')  # or 'plasma', 'inferno', etc.

    groups = [(is_synthetic, df) for is_synthetic, df in df.groupby(synth_col)]
    dfs = [group[1] for group in groups]
    # plt.hist([df["xc"] for df in dfs], stacked=True, bins=n_bins, label=[f"Synthetic={group[0]}" for group in groups])
    bax.hist([df[hist_col] for df in dfs], stacked=True, bins=n_bins, density=False,
             label=[f"{'Synthetic passes' if group[0] else 'Real passes'}" for group in groups],
             color=[cmap(i / len(groups)) for i in range(len(groups))]
             )

    # set x limit
    bax.set_xlim(0, 1)
    # plt.ylim(0, 400)

    # set xticks
    bax.set_xticks(np.arange(0, 1.1, 0.1))
    plt.gca().set_xticks(np.arange(0, 1.1, 0.1))
    plt.gca().set_xticklabels([f"{i:.1f}" for i in np.arange(0, 1.1, 0.1)])

    # thin y grid


    # plt.gca().set_xlabel("X Axis", labelpad=20)  # Move X label down
    # plt.gca().set_ylabel("Y Axis", labelpad=20)  # Move Y label left

    bax.set_xlabel("Predicted pass success probability", labelpad=7)
    bax.set_ylabel("Number of passes in training set", labelpad=35)

    # bax.annotate('xxxx (synthetic passes)', xy=(0.1, 400), xytext=(0.1, 300),
    #             arrowprops=dict(facecolor='yellow', arrowstyle='->', lw=2, ls='dashed', color='yellow'),
    #             fontsize=12, color='yellow', ha='center', va='center')

    bax.set_axisbelow(True)
    plt.gca().xaxis.grid(color='gray', linestyle='dashed', alpha=0.5)
    plt.gca().yaxis.grid(color='gray', linestyle='dashed', alpha=0.5)

    bax.legend(loc='upper right', fontsize=12, frameon=True)

    plt.rcParams.update(plt.rcParamsDefault)

    return plt.gcf()


# df = pd.DataFrame({"xc": np.random.sample(size=1000), "is_synthetic": [True, False] * 500, "success": [True, False] * 500})
# st.write("df")
# st.write(df)
# st.write(calibration_histogram(df, "xc", n_bins=10))
# st.stop()


def get_bins(df, prediction_col="xc", outcome_col="success", new_bin_col="bin", n_bins=None, binsize=None):
    if binsize is None and n_bins is not None:
        df[new_bin_col] = pd.qcut(df[prediction_col], n_bins, labels=False, duplicates="drop")
    elif binsize is not None and n_bins is None:
        min_val = df[prediction_col].min()
        max_val = df[prediction_col].max()
        bin_edges = [min_val + i * binsize for i in range(int((max_val - min_val) / binsize) + 2)]
        df[new_bin_col] = pd.cut(df[prediction_col], bins=bin_edges, labels=False, include_lowest=True)
    else:
        raise ValueError("Either n_bins or binsize must be specified")

    df_calibration = df.groupby(new_bin_col).agg({outcome_col: "mean", prediction_col: "mean"}).reset_index()
    df_calibration[new_bin_col] = df_calibration[new_bin_col]
    return df_calibration


def bin_nr_calibration_plot(df, prediction_col="xc", outcome_col="success", n_bins=None, binsize=None, add_text=True, style="seaborn-v0_8", add_interval=True, interval_confidence_level=0.95, n_bootstrap_samples=1000):
    bin_col = get_unused_column_name(df.columns, "bin")

    df_calibration = get_bins(df, prediction_col, outcome_col, bin_col, n_bins, binsize)

    plt.style.use(style)
    fig, ax = plt.subplots()

    ax.plot(df_calibration[prediction_col], df_calibration[outcome_col], marker="o")
    ax.plot([0, 1], [0, 1], linestyle="--", color="black")

    if add_interval:
        avg_predictions = []
        uppers = []
        lowers = []
        avg_avg_outcomes = []
        for bin, df_bin in df.groupby(bin_col):
            avg_outcomes = []
            for i in range(n_bootstrap_samples):
                df_sample = df_bin.sample(n=len(df_bin), replace=True)
                avg_outcomes.append(df_sample[outcome_col].mean())

            avg_outcome_lower = np.percentile(avg_outcomes, 100 * (1 - interval_confidence_level) / 2)
            avg_outcome_upper = np.percentile(avg_outcomes, 100 * (1 - (1 - interval_confidence_level) / 2))
            avg_predictions.append(df_calibration.loc[df_calibration[bin_col] == bin, prediction_col].iloc[0])
            avg_avg_outcomes.append(np.mean(avg_outcomes))
            uppers.append(avg_outcome_upper)
            lowers.append(avg_outcome_lower)

        avg_predictions = np.array(avg_predictions)
        uppers = np.array(uppers)
        lowers = np.array(lowers)

        df_bootstrap = pd.DataFrame({"avg_prediction": avg_predictions, "avg_outcome": avg_avg_outcomes, "upper": uppers, "lower": lowers})

        plt.fill_between(avg_predictions, lowers, uppers, color='grey', alpha=0.3, label='Uncertainty Area')

    # Annotate each point with the number of samples
    if add_text:
        for i, row in df_calibration.iterrows():
            count = len(df[df[bin_col] == row[bin_col]])  # Count of samples in the bin
            ax.annotate(
                f"n={count}",
                (row[prediction_col], row[outcome_col] - 0.03),  # Position of the text
                bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='lightblue'),
                fontsize=7, ha='center', va='center'
            )

    # xticks every 0.1
    ax.set_xticks(np.arange(0, 1.1, 0.1))
    ax.set_xticklabels([f"{i:.1f}" for i in np.arange(0, 1.1, 0.1)])
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.set_yticklabels([f"{i:.1f}" for i in np.arange(0, 1.1, 0.1)])

    ax.set_xlabel("Predicted pass success probability")
    ax.set_ylabel("Observed pass success rate")
    ax.set_title("Calibration curve of our model on the test data")
    return fig


def plot_pass(p4ss, df_tracking, add_legend=True, add_as=False, add_das=False, flip=False, legend_loc="best",
              legend_bbox_to_anchor=None, use_green_background=True, add_pass_to_legend=True):
    # from mplsoccer import Pitch, VerticalPitch

    if use_green_background:
        pitch = mplsoccer.Pitch(pitch_type="secondspectrum", pitch_length=105, pitch_width=68, pitch_color='#aabb97', line_color='white',
                  stripe_color='#c2d59d', stripe=True)
    else:
        pitch = mplsoccer.Pitch(pitch_type="secondspectrum", pitch_length=105, pitch_width=68, pitch_color="white", shade_color="white")

#    pitch = mplsoccer.Pitch(pitch_type="secondspectrum", pitch_length=105, pitch_width=68, pitch_color="white", shade_color="white")
    # specifying figure size (width, height)
    fig, ax = pitch.draw(figsize=(8, 4))

    plt.style.use("seaborn-v0_8-white")  # ?

    # plt.title(f"Pass: {p4ss['success']}")

    df_frame = df_tracking[df_tracking["frame_id"] == p4ss["frame_id"]].copy()

    red_color = "#ff6666"
    red_color_pass = "#b30000"
    blue_color = "#6864b0"

    if flip:
        df_frame["x"] = -df_frame["x"]
        df_frame["y"] = -df_frame["y"]
        df_frame["vx"] = -df_frame["vx"]
        df_frame["vy"] = -df_frame["vy"]

        if "coordinates_x" in p4ss:
            p4ss["coordinates_x"] = -p4ss["coordinates_x"]
            p4ss["coordinates_y"] = -p4ss["coordinates_y"]
            p4ss["end_coordinates_x"] = -p4ss["end_coordinates_x"]
            p4ss["end_coordinates_y"] = -p4ss["end_coordinates_y"]

    if add_das or add_as:
        assert len(df_frame) > 0
        df_frame["ball_owning_team_id"] = p4ss["team_id"]
        n_angles = 117  #  st.number_input("n_angles", 1, 200, 117, key=str(uuid.uuid4()))
        radial_gridsize = 2.7 # st.number_input("radial_gridsize", 0.1, 10.0, 2.7, key=str(uuid.uuid4()))
        das = get_dangerous_accessible_space(df_frame, team_in_possession_col="ball_owning_team_id", period_col=None, tol_distance=2.6, inertial_seconds=0.24, radial_gridsize=radial_gridsize, n_angles=n_angles, n_v0=100, v0_max=52.5)
        if add_das:
            plot_expected_completion_surface(das.dangerous_result, color="red", plot_gridpoints=False)
        if add_as:
            plot_expected_completion_surface(das.simulation_result, color="red", plot_gridpoints=False)

    try:
        arrow = matplotlib.patches.FancyArrowPatch(
            (p4ss["coordinates_x"], p4ss["coordinates_y"]), (p4ss["end_coordinates_x"], p4ss["end_coordinates_y"]),
            arrowstyle="->", mutation_scale=30, color=red_color_pass, linewidth=2, ec=red_color_pass, fc=red_color_pass

        )
        plt.gca().add_artist(arrow)
    except KeyError:
        pass
    # plt.scatter(p4ss["coordinates_x"], p4ss["coordinates_y"], c=red_color_pass, marker="x", s=150, label="Pass origin (event data)")

    # df_frame = df_tracking[df_tracking["frame_id"] == p4ss["frame_id"]]
    for team_nr, team in enumerate(df_frame["team_id"].unique()):
        team_color = red_color if team == p4ss["team_id"] else blue_color
        team_name = "Attacking team" if team == p4ss["team_id"] else "Defending team"

        if team is None:
            continue
        df_frame_team = df_frame[df_frame["team_id"] == team]

        df_frame_team["player_name"] = df_frame_team["player_id"].map(lambda x: f"Player{str(x).replace('home_', '').replace('away_', '').replace('PlayerP', 'P')}")

        x = df_frame_team["x"].tolist()
        y = df_frame_team["y"].tolist()

        vx = df_frame_team["vx"].tolist()
        vy = df_frame_team["vy"].tolist()

        player_names = df_frame_team["player_name"].tolist()

        for i in range(len(x)):
            label = None if i == 0 and team_nr == 0 else None
            if vx[i] ** 2 + vy[i] ** 2 > 0:
                plt.arrow(x=x[i], y=y[i], dx=vx[i]/2, dy=vy[i]/2, width=0.425/1.5, head_width=1.5/1.5, head_length=1.5/1.5, fc="black", ec="black", label=label)

            # plot names
            # if i == 0:
            plt.text(x[i], y[i] - 2.65, player_names[i], fontsize=8, color=team_color, ha="center", va="center")

        plt.scatter(x, y, c=team_color, label=team_name, edgecolors="black", s=50, linewidth=1)

    # plot ball position
    df_frame_ball = df_frame[df_frame["player_id"] == "ball"]
    x_ball = df_frame_ball["x"].iloc[0]
    y_ball = df_frame_ball["y"].iloc[0]
    plt.scatter(x_ball, y_ball, c="black", marker="x", s=100, label="Ball position (tracking data)")

    if add_legend:
        plt.legend(frameon=True, loc=legend_loc, bbox_to_anchor=legend_bbox_to_anchor)

    # handles, labels = plt.gca().get_legend_handles_labels()

    plt.scatter([], [], marker=r'$\rightarrow$', label='Velocity', color='black', s=100)  # dummy scatter to add an item to the legend
    if add_pass_to_legend:
        plt.scatter([], [], marker=r'$\rightarrow$', label='Pass', color=red_color_pass, s=100)  # dummy scatter to add an item to the legend

    # handles[0] = matplotlib.patches.FancyArrowPatch((0, 0), (1, 0), color="blue", mutation_scale=0.0000, mutation_aspect=0.0)
    # handles.append(matplotlib.lines.Line2D([], [], color=red_color_pass, marker='>', markersize=10, label="Arrow"))
    # handles.append(matplotlib.patches.FancyArrowPatch((0, 0), (1, 0), color="blue", mutation_scale=0.0000, mutation_aspect=0.0))
    # labels.append(None)
    # arrow =
    # plt.legend(handles=handles, labels=labels, frameon=True)
    if add_legend:
        plt.legend(frameon=True, prop={'size': 9}, loc=legend_loc, bbox_to_anchor=legend_bbox_to_anchor)

    # st.write(handles)
    # st.write(labels)

    # plt.xlim(-52.5, 52.5)
    # plt.ylim(-34, 34)

    st.write(plt.gcf())

    if add_legend:
        filename = f"{p4ss['frame_id']}_legend_{add_das}_{add_as}"
    else:
        filename = f"{p4ss['frame_id']}_{add_das}_{add_as}"

    # plt.savefig(os.path.join(os.path.dirname(__file__), f"{filename}.png"), dpi=300, bbox_inches="tight")
    # plt.savefig(os.path.join(os.path.dirname(__file__), f"{filename}.pdf"), bbox_inches="tight")

    plt.close()

    return plt.gcf()


def _choose_random_parameters(parameter_to_bounds):
    random_parameters = {}
    for param, bounds in parameter_to_bounds.items():
        # st.write("B", param, bounds, str(type(bounds[0])), str(type(bounds[-1])), "bool", isinstance(bounds[0], bool), isinstance(bounds[0], int), isinstance(bounds[0], float))
        if isinstance(bounds[0], bool):  # order matters, bc bool is also int
            random_parameters[param] = np.random.choice([bounds[0], bounds[-1]])
        elif isinstance(bounds[0], int) or isinstance(bounds[0], float):
            random_parameters[param] = np.random.uniform(bounds[0], bounds[-1])
        elif isinstance(bounds[0], str):
            random_parameters[param] = np.random.choice(bounds)
        else:
            raise NotImplementedError(f"Unknown type: {type(bounds[0])}")
    return random_parameters


def simulate_parameters(df_training, dfs_tracking, use_prefit, seed, add_confidence_intervals, chunk_size=200, outcome_col="success", calculate_passes_json=False):
    np.random.seed(seed)
    gc.collect()

    data = {
        # "brier_score": [],
        # "logloss": [],
        # "auc": [],
        # "brier_score_synthetic": [],
        # # "logloss_synthetic": [],
        # # "auc_synthetic": [],
        # "brier_score_real": [],
        # "logloss_real": [],
        # "auc_real": [],
        # "passes_json": [],
        # "parameters": [],
    }

    # progress_bar_text.text(f"Simulation {i + 1}/{n_steps}")
    # progress_bar.progress((i + 1) / n_steps)

    if use_prefit:
        parameter_assignment = PREFIT_PARAMS
    else:
        parameter_assignment = _choose_random_parameters(PARAMETER_BOUNDS)

    data_simres = {
        "xc": [],
        "success": [],
        "is_synthetic": [],
    }
    dfs_training_passes = []
    for dataset_nr, df_training_passes in df_training.groupby("dataset_nr"):
        df_training_passes = df_training_passes.copy()
        # df_training_passes = df_training_passes[df_training_passes["event_type"] == "PASS"]
        df_tracking = dfs_tracking[dataset_nr].copy()
        ret = get_expected_pass_completion(
            df_training_passes, df_tracking, event_frame_col="frame_id", tracking_frame_col="frame_id",
            event_start_x_col="coordinates_x",
            event_start_y_col="coordinates_y", event_end_x_col="end_coordinates_x",
            event_end_y_col="end_coordinates_y",
            event_team_col="team_id",
            event_player_col="player_id", tracking_player_col="player_id", tracking_team_col="team_id",
            ball_tracking_player_id="ball",
            tracking_x_col="x", tracking_y_col="y", tracking_vx_col="vx", tracking_vy_col="vy", tracking_v_col="v",
            tracking_team_in_possession_col="ball_possession",

            n_frames_after_pass_for_v0=5, fallback_v0=10,
            chunk_size=chunk_size,
            use_progress_bar=False,
            use_event_coordinates_as_ball_position=True,  # necessary because validation uses duplicate frames (artificial passes)

            **parameter_assignment,
        )
        xc = ret.xc
        df_training_passes["xc"] = xc
        data_simres["xc"].extend(xc.tolist())
        data_simres["success"].extend(df_training_passes[outcome_col].tolist())
        data_simres["is_synthetic"].extend(df_training_passes["is_synthetic"].tolist())

        # print(dataset_nr, "lens data_simres", {k: len(v) for k, v in data_simres.items()})

        dfs_training_passes.append(df_training_passes.copy())

    # print("B")
    df_training_passes = pd.concat(dfs_training_passes)
    training_passes_json = df_training_passes.to_json(orient="records")
    if calculate_passes_json:
        data["passes_json"] = training_passes_json
    else:
        data["passes_json"] = ""
    # print("C")

    df_simres = pd.DataFrame(data_simres)
    data["parameters"] = parameter_assignment
    for key, value in parameter_assignment.items():
        data[key] = value
    # print("D")

    scores = get_scores(df_simres, df_training[outcome_col].mean(), outcome_col=outcome_col, add_confidence_intervals=add_confidence_intervals)
    for key, value in scores.items():
        # data[key].append(value)
        data[key] = value
    # print("E")

    # df_to_display = pd.DataFrame(data).sort_values("logloss", ascending=True)
    # df_to_display.iloc[1:, df_to_display.columns.get_loc("passes_json")] = np.nan
    # df_to_display.iloc[1:, df_to_display.columns.get_loc("parameters")] = np.nan
    # display_df.write(df_to_display.head(20))

    gc.collect()

    return data


def validate_multiple_matches(
    dfs_tracking, dfs_passes, n_steps=100, training_size=0.7, use_prefit=True,
    outcome_col="success", tracking_team_col="team_id", event_team_col="team_id",
):
    @st.fragment
    def frag_plot_das():
        dataset_nr = st.number_input("Dataset nr", value=0, min_value=0, max_value=len(dfs_tracking) - 1, key="frag_plot_das2")
        # max_frame = dfs_tracking[dataset_nr]["frame_id"].max()
        # frame = st.number_input("Frame", value=0, min_value=0, max_value=max_frame, key="frag_plot_das")
        default_frame = 7404
        frames = dfs_tracking[dataset_nr]["frame_id"].unique().tolist()
        frame = st.selectbox("Frame", frames, key="frag_plot_das", index=frames.index(default_frame))

        teams = dfs_tracking[dataset_nr]["team_id"].dropna().unique()
        selected_team = st.selectbox("Team", teams, key="frag_plot_das3")

        # df_frame = dfs_tracking[dataset_nr][dfs_tracking[dataset_nr]["frame_id"] == frame].copy()
        # assert len(df_frame) > 0
        # # plot pitch
        # df_frame["ball_owning_team_id"] = selected_team
        #
        # das = get_dangerous_accessible_space(df_frame, team_in_possession_col="ball_owning_team_id", period_col=None)
        # plot_expected_completion_surface(das.simulation_result)

        for das in ["das", "as"]:
            plot_pass({"frame_id": frame, "team_id": selected_team}, dfs_tracking[dataset_nr], add_legend=True,
                      legend_loc="lower left", add_as=das == "as", add_das=das == "das", flip=True, use_green_background=False,
                      legend_bbox_to_anchor=(0.05, 0.0), add_pass_to_legend=False)
            st.write(plt.gcf())


    frag_plot_das()

    random_state = 1893

    exclude_synthetic_passes_from_training_set = st.checkbox("Exclude synthetic passes from training set", value=False)
    exclude_synthetic_passes_from_test_set = st.checkbox("Exclude synthetic passes from test set", value=False)
    chunk_size = st.number_input("Chunk size", value=50, min_value=1, max_value=None)
    max_workers = st.number_input("Max workers", value=5, min_value=1, max_value=None)

    ## Add synthetic passes
    @st.cache_resource
    def _get_dfs_passes_with_synthetic():
        dfs_passes_with_synthetic = []
        for df_tracking, df_passes in progress_bar(zip(dfs_tracking, dfs_passes)):
            # n_synthetic_passes = 5
            n_synthetic_passes = len(df_passes[df_passes["success"]]) - len(df_passes[~df_passes["success"]])

            with st.spinner(f"Adding synthetic passes to dataset ({n_synthetic_passes} synthetic passes)"):
                df_passes = add_synthetic_passes(df_passes, df_tracking, n_synthetic_passes=n_synthetic_passes, tracking_frame_col="frame_id", event_frame_col="frame_id")
                dfs_passes_with_synthetic.append(df_passes)

            # if plot_synthetic_passes:
            #     columns = st.columns(2)
            #     for pass_nr, (_, synthetic_pass) in enumerate(df_passes[df_passes["is_synthetic"]].iterrows()):
            #         df_frame = df_tracking[df_tracking["frame_id"] == synthetic_pass["frame_id"]]
            #         fig = plt.figure()
            #         plt.arrow(synthetic_pass["coordinates_x"], synthetic_pass["coordinates_y"], synthetic_pass["end_coordinates_x"] - synthetic_pass["coordinates_x"], synthetic_pass["end_coordinates_y"] - synthetic_pass["coordinates_y"], head_width=1, head_length=1, fc='k', ec='k')
            #
            #         plt.plot([-52.5, -52.5], [-34, 34], color="black", alpha=0.5)
            #         plt.plot([52.5, 52.5], [-34, 34], color="black", alpha=0.5)
            #         plt.plot([-52.5, 52.5], [-34, -34], color="black", alpha=0.5)
            #         plt.plot([-52.5, 52.5], [34, 34], color="black", alpha=0.5)
            #
            #         df_frame_home = df_frame[df_frame[tracking_team_col] == synthetic_pass[event_team_col]]
            #         plt.scatter(df_frame_home["x"], df_frame_home["y"], color="red", alpha=1)
            #         df_frame_def = df_frame[(df_frame[tracking_team_col] != synthetic_pass[event_team_col]) & (df_frame[tracking_team_col].notna())]
            #         plt.scatter(df_frame_def["x"], df_frame_def["y"], color="blue", alpha=1)
            #         df_frame_ball = df_frame[df_frame[tracking_team_col].isna()]
            #         plt.scatter(df_frame_ball["x"], df_frame_ball["y"], color="black", alpha=1, marker="x", s=100)
            #
            #         columns[pass_nr % 2].write(f"Pass {pass_nr} (frame {synthetic_pass['frame_id']})")
            #         columns[pass_nr % 2].write(fig)
            #
            #         plt.close()

        return dfs_passes_with_synthetic

    dfs_passes_with_synthetic = _get_dfs_passes_with_synthetic()

    ##
    dfs_training = []
    dfs_test = []
    for dataset_nr, df_passes in enumerate(dfs_passes_with_synthetic):
        df_passes = df_passes.copy()
        dataset_nr_col = get_unused_column_name(df_passes.columns, "dataset_nr")
        df_passes[dataset_nr_col] = dataset_nr
        df_passes["stratification_var"] = df_passes[outcome_col].astype(str) + "_" + df_passes["is_synthetic"].astype(str)

        df_passes = df_passes.reset_index(drop=True)

        df_passes["identifier"] = df_passes["dataset_nr"].astype(str) + "_" + df_passes.index.astype(str)

        assert len(df_passes["identifier"]) == len(set(df_passes["identifier"]))
        assert len(df_passes.index) == len(set(df_passes.index))

        df_training, df_test = sklearn.model_selection.train_test_split(
            df_passes, stratify=df_passes["stratification_var"], train_size=training_size, random_state=random_state
        )

        if exclude_synthetic_passes_from_training_set:
            df_training = df_training[~df_training["is_synthetic"]]
        if exclude_synthetic_passes_from_test_set:
            df_test = df_test[~df_test["is_synthetic"]]

        assert len(set(df_training.index).intersection(set(df_test.index))) == 0
        assert len(set(df_training["identifier"]).intersection(set(df_test["identifier"]))) == 0

        dfs_training.append(df_training.copy())
        dfs_test.append(df_test.copy())

    df_training = pd.concat(dfs_training).reset_index(drop=True).copy()
    st.write("df_training", df_training.shape)
    df_test = pd.concat(dfs_test).reset_index(drop=True).copy()
    st.write("df_test", df_test.shape)

    # assert no duplicate "identifier"
    assert len(df_training["identifier"]) == len(set(df_training["identifier"]))
    assert len(df_test["identifier"]) == len(set(df_test["identifier"]))
    # assert no overlapping "identifier"
    assert len(set(df_training["identifier"]).intersection(set(df_test["identifier"]))) == 0

    st.write("Number of training passes", len(df_training), f"avg. accuracy={df_training[outcome_col].mean():.1%}")
    st.write("Number of test passes", len(df_test), f"avg. accuracy={df_test[outcome_col].mean():.1%}")

    training_scores = get_scores(df_training, df_training[outcome_col].mean(), outcome_col=outcome_col, add_confidence_intervals=False)

    # test_scores = get_scores(df_test, df_training[outcome_col].mean(), outcome_col=outcome_col)
    # st.write("Training scores")
    # st.write(training_scores)
    # st.write("Test scores")
    # st.write(test_scores)

    data = {
        "brier_score": [],
        "logloss": [],
        "auc": [],
        "brier_score_synthetic": [],
        # "logloss_synthetic": [],
        # "auc_synthetic": [],
        "brier_score_real": [],
        "logloss_real": [],
        "auc_real": [],
        "passes_json": [],
    }
    data.update({key: [] for key in training_scores.keys()})
    data["parameters"] = []
    # progress_bar_text = st.empty()
    # progress_bar = st.progress(0)
    display_df = st.empty()

    import concurrent.futures
    df = None
    expensive_cols = ["passes_json", "parameters"]
    # very_expensive_cols = ["passes_json"]

    simulate_params_partial = functools.partial(simulate_parameters, df_training, dfs_tracking, use_prefit, chunk_size=chunk_size, outcome_col=outcome_col, calculate_passes_json=False, add_confidence_intervals=False)

    use_parallel_processing = st.checkbox("Use parallel processing", value=False)

    optimization_target = st.selectbox("Select optimization target", [
        "logloss", "brier_score", "auc", "logloss_real", "brier_score_real", "auc_real", "logloss_synthetic", "brier_score_synthetic", "auc_synthetic",
    ])

    if not use_prefit:
        if use_parallel_processing:
            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
                tasks = [executor.submit(simulate_params_partial, seed=np.random.randint(0, 2**16 - 1)) for _ in range(n_steps)]

                for i, future in enumerate(progress_bar(concurrent.futures.as_completed(tasks), total=n_steps, desc="MP Simulation")):
                    # process = psutil.Process(os.getpid())
                    # process_id = os.getpid()
                    # print(f"MAIN PROCESS {process_id}: Memory usage (MB): {process.memory_info().rss / 1024 ** 2:.2f} MB")
                    # st.write(f"MAIN PROCESS {process_id}: Memory usage (MB): {process.memory_info().rss / 1024 ** 2:.2f} MB")

                    data = future.result()
                    df_data = pd.Series(data).to_frame().T
                    df_data["step_nr"] = i
                    front_cols = ["step_nr", "logloss", "brier_score", "auc", "brier_score_synthetic", "logloss_synthetic", "auc_synthetic", "brier_score_real", "logloss_real", "auc_real"]
                    cols = front_cols + [col for col in df_data.columns if col not in front_cols]
                    df_data = df_data[cols]

                    if df is None:
                        df = df_data
                    else:
                        df = pd.concat([df, df_data], axis=0)
                        df = df.sort_values(optimization_target, ascending=True).reset_index(drop=True)
                        # if len(df) > 20:
                        #     df.loc[20:, expensive_cols] = np.nan
                        if len(df) > 1:
                            df.loc[1:, expensive_cols] = np.nan

                    display_df.write(df.head(20))

                try:
                    del data
                    del df_data
                except Exception as e:
                    st.write(e)

                # memory_bytes = df.memory_usage(deep=True).sum()
                # memory_mb = memory_bytes / (1024 ** 2)
                # st.write(f"Memory usage of df (MB): {memory_mb:.2f} MB")

                future = None
                del future

                # debug_memory_usage()

                gc.collect()
        else:
            for i in progress_bar(range(n_steps), desc="Simulation", total=n_steps):
                data = simulate_params_partial(seed=np.random.randint(0, 2**16 - 1))
                df_data = pd.Series(data).to_frame().T
                df_data["step_nr"] = i
                front_cols = ["step_nr", "logloss", "brier_score", "auc", "brier_score_synthetic", "logloss_synthetic",
                              "auc_synthetic", "brier_score_real", "logloss_real", "auc_real"]
                cols = front_cols + [col for col in df_data.columns if col not in front_cols]
                df_data = df_data[cols]

                if df is None:
                    df = df_data
                else:
                    df = pd.concat([df, df_data], axis=0)
                    df = df.sort_values(optimization_target, ascending=True).reset_index(drop=True)
                    # if len(df) > 20:
                    #     df.loc[20:, expensive_cols] = np.nan
                    if len(df) > 1:
                        df.loc[1:, expensive_cols] = np.nan

                display_df.write(df.head(20))

            try:
                del data
                del df_data
            except Exception as e:
                st.write(e)

            # memory_bytes = df.memory_usage(deep=True).sum()
            # memory_mb = memory_bytes / (1024 ** 2)
            # st.write(f"Memory usage of df (MB): {memory_mb:.2f} MB")

            future = None
            del future

            # debug_memory_usage()

            gc.collect()

    else:
        ret = simulate_parameters(df_training, dfs_tracking, use_prefit, np.random.randint(0, 2**16 - 1), add_confidence_intervals=True, chunk_size=chunk_size, outcome_col=outcome_col, calculate_passes_json=True)
        data = ret
        df_data = pd.Series(data).to_frame().T
        df_data["step_nr"] = 0
        front_cols = ["step_nr", "logloss", "brier_score", "auc", "brier_score_synthetic", "logloss_synthetic", "auc_synthetic", "brier_score_real", "logloss_real", "auc_real"]
        cols = front_cols + [col for col in df_data.columns if col not in front_cols]
        df_data = df_data[cols]
        df = df_data
        display_df.write(df.head(20))

    df_training_results = df.sort_values(optimization_target, ascending=True).reset_index(drop=True)

    training_data_simres = df_training_results["passes_json"][0]
    df_training_passes = pd.read_json(training_data_simres).copy()

    # move logloss column and brier and auc etc to front
    cols = df_training_results.columns.tolist()
    front_cols = ["step_nr", "logloss", "brier_score", "auc", "brier_score_synthetic", "logloss_synthetic", "auc_synthetic", "brier_score_real", "logloss_real", "auc_real"]
    df_training_results[front_cols] = df_training_results[front_cols].astype(float)
    cols = front_cols + [col for col in cols if col not in front_cols]
    df_training_results = df_training_results[cols]
    st.write("df_training_results")
    st.write(df_training_results)

    df_training_results.to_csv("df_training_results.csv", sep=";")
    st.write(f"Wrote results to {os.path.abspath('df_training_results.csv')}")

    best_index = df_training_results[optimization_target].idxmin()
    best_parameters = df_training_results["parameters"][best_index]
    best_passes = df_training_results["passes_json"][best_index]
    df_best_passes = pd.read_json(best_passes).copy()
    df_best_passes["error"] = (df_best_passes["success"] - df_best_passes["xc"]).abs()

    st.write("### Training results")

    @st.fragment
    def frag1():
        n_bins = st.number_input("Number of bins for calibration plot", value=10, min_value=1, max_value=None, key="frag1")
        add_text = st.checkbox("Add text to calibration plot", value=True, key="add_text1")
        style = st.selectbox("Style", plt.style.available, index=plt.style.available.index("seaborn-v0_8"), key="style1")
        st.write(bin_nr_calibration_plot(df_best_passes, outcome_col=outcome_col, n_bins=n_bins, add_text=add_text, style=style))

    @st.fragment
    def frag2():
        binsize = st.number_input("Binsize for calibration plot", value=0.1, min_value=0.01, max_value=None, key="frag2")
        add_text = st.checkbox("Add text to calibration plot", value=True, key="add_text2")
        style = st.selectbox("Style", plt.style.available, index=plt.style.available.index("seaborn-v0_8"), key="style2")
        st.write(bin_nr_calibration_plot(df_best_passes, outcome_col=outcome_col, binsize=binsize, add_text=add_text, style=style))

    @st.fragment
    def frag3():
        use_boken_axis = st.checkbox("Use broken axis", value=True, key="frag3")
        st.write(calibration_histogram(df_best_passes, n_bins=40, use_boken_axis=use_boken_axis))
        # plt.savefig(os.path.join(os.path.dirname(__file__), "frag3_training.png"), dpi=300)
        # plt.savefig(os.path.join(os.path.dirname(__file__), "frag3_training.pdf"))

    frag1()
    frag2()
    frag3()

    # st.stop()

    if st.toggle("Show example passes", value=True):
        for (text, df) in [
            ("Random synthetic passes", df_best_passes[df_best_passes["is_synthetic"]].sample(frac=1).reset_index(drop=True)),
            ("Worst synthetic predictions", df_best_passes[df_best_passes["is_synthetic"]].sort_values("error", ascending=False)),
            ("Best synthetic predictions", df_best_passes[df_best_passes["is_synthetic"]].sort_values("error", ascending=True)),
            ("Worst real predictions", df_best_passes[~df_best_passes["is_synthetic"]].sort_values("error", ascending=False)),
            ("Best real predictions", df_best_passes[~df_best_passes["is_synthetic"]].sort_values("error", ascending=True)),
        ]:
            with st.expander(text):
                for pass_nr, (_, p4ss) in enumerate(df.iterrows()):
                    st.write("#### Pass", pass_nr, "xc=", p4ss["xc"], "success=", p4ss["success"], "error=", p4ss["error"],
                             "is_synthetic=", p4ss["is_synthetic"])
                    st.write(p4ss)
                    for add_legend in [True, False]:
                        plot_pass(p4ss, dfs_tracking[p4ss["dataset_nr"]], add_legend=add_legend, use_green_background=False)

    #             plot_pass({"frame_id": frame, "team_id": selected_team}, dfs_tracking[dataset_nr], add_legend=True,
                    #                       legend_loc="lower left", add_as=das == "as", add_das=das == "das", flip=True, use_green_background=False,
                    #                       legend_bbox_to_anchor=(0.05, 0.0), add_pass_to_legend=False)

                    if pass_nr > 20:
                        break

    # with st.expander("Worst predictions"):
    #     for pass_nr, (_, p4ss) in enumerate(df_best_passes.sort_values("error", ascending=False).iterrows()):
    #         # st.write("Pass", pass_nr, "xc=", p4ss["xc"], "success=", p4ss["success"], "error=", p4ss["error"], "is_synthetic=", p4ss["is_synthetic"])
    #         st.write("#### Pass", pass_nr, "xc=", p4ss["xc"], "success=", p4ss["success"], "error=", p4ss["error"], "is_synthetic=", p4ss["is_synthetic"])
    #         plot_pass(p4ss, dfs_tracking[p4ss["dataset_nr"]])
    #
    #         if pass_nr > 1:
    #             break
    #
    # with st.expander("Best predictions"):
    #     for pass_nr, (_, p4ss) in enumerate(df_best_passes.sort_values("error", ascending=True).iterrows()):
    #         st.write("#### Pass", pass_nr, "xc=", p4ss["xc"], "success=", p4ss["success"], "error=", p4ss["error"], "is_synthetic=", p4ss["is_synthetic"])
    #         plot_pass(p4ss, dfs_tracking[p4ss["dataset_nr"]])
    #
    #         if pass_nr > 1:
    #             break

    data_simres = {
        "xc": [],
        "success": [],
        "is_synthetic": [],
    }
    for dataset_nr, df_test_passes in df_test.groupby("dataset_nr"):
        df_test_passes = df_test_passes.copy()
        df_tracking = dfs_tracking[dataset_nr].copy()
        ret = get_expected_pass_completion(
            df_test_passes, df_tracking, event_frame_col="frame_id", tracking_frame_col="frame_id",
            event_start_x_col="coordinates_x",
            event_start_y_col="coordinates_y", event_end_x_col="end_coordinates_x", event_end_y_col="end_coordinates_y",
            event_team_col="team_id",
            event_player_col="player_id", tracking_player_col="player_id", tracking_team_col="team_id",
            ball_tracking_player_id="ball",
            tracking_team_in_possession_col="ball_possession",
            tracking_x_col="x", tracking_y_col="y", tracking_vx_col="vx", tracking_vy_col="vy", tracking_v_col="v",
            n_frames_after_pass_for_v0=5, fallback_v0=10, chunk_size=chunk_size,

            use_event_coordinates_as_ball_position=True,

            **best_parameters,
        )
        data_simres["xc"].extend(ret.xc)
        data_simres["success"].extend(df_test_passes[outcome_col].tolist())
        data_simres["is_synthetic"].extend(df_test_passes["is_synthetic"].tolist())

    df_simres_test = pd.DataFrame(data_simres).copy()

    df_simres_total = pd.concat([df_training_passes, df_test_passes]).reset_index(drop=True)
    df_simres_total_only_success = df_simres_total[df_simres_total["success"]].copy()
    st.write("df_simres_total_only_success")
    st.write(df_simres_total_only_success)
    st.write(df_simres_total_only_success["xc"].mean())

    test_scores = get_scores(df_simres_test.copy(), df_test[outcome_col].mean(), outcome_col=outcome_col, add_confidence_intervals=True)
    st.write("### Test scores")
    df_test_scores = pd.DataFrame(test_scores, index=[0])

    # order cols like training
    df_test_scores = df_test_scores[[col for col in df_training_results.columns if col in df_test_scores.columns]]

    st.write("df_test_scores")
    st.write(df_test_scores)

    df_test_scores.to_csv("df_test_scores.csv", sep=";")
    st.write(f"Wrote test scores to {os.path.abspath('df_test_scores.csv')}")

    st.write("df_simres_test")
    st.write(df_simres_test)

    @st.fragment
    def frag1_test():
        n_bins = st.number_input("Number of bins for calibration plot", value=10, min_value=1, max_value=None, key="frag1_test")
        add_text = st.checkbox("Add text to calibration plot", value=True, key="add_text1_test")
        st.write(bin_nr_calibration_plot(df_simres_test, outcome_col=outcome_col, n_bins=n_bins, add_text=add_text))
        # plt.savefig(os.path.join(os.path.dirname(__file__), "frag1_test.png"), dpi=300)
        # plt.savefig(os.path.join(os.path.dirname(__file__), "frag1_test.pdf"))

    @st.fragment
    def frag2_test():
        binsize = st.number_input("Binsize for calibration plot", value=0.1, min_value=0.01, max_value=None, key="frag2_test")
        add_text = st.checkbox("Add text to calibration plot", value=True, key="add_text2_test")
        st.write(bin_nr_calibration_plot(df_simres_test, outcome_col=outcome_col, binsize=binsize, add_text=add_text))
        # plt.savefig(os.path.join(os.path.dirname(__file__), "frag2_test.pdf"))

    @st.fragment
    def frag3_test():
        use_boken_axis = st.checkbox("Use broken axis", value=True, key="frag4_test")
        st.write(calibration_histogram(df_simres_test, n_bins=40, use_boken_axis=use_boken_axis))

    frag1_test()
    frag2_test()
    frag3_test()
    # st.write(bin_nr_calibration_plot(df_simres_test, outcome_col=outcome_col, n_bins=10))
    # st.write(bin_nr_calibration_plot(df_simres_test, outcome_col=outcome_col, n_bins=20))

    # for n_bins in [5, 10, 20]:
    #     st.write(f"Calibration plot with {n_bins} bins")
    #     fig = bin_nr_calibration_plot(df_simres_test, outcome_col=outcome_col, n_bins=n_bins)
    #     st.pyplot(fig)
    #
    # for binsize in [0.2, 0.1, 0.05]:
    #     st.write(f"Calibration plot with binsize {binsize}")
    #     fig = bin_nr_calibration_plot(df_simres_test, outcome_col=outcome_col, binsize=binsize)
    #     st.pyplot(fig)
    #
    # st.stop()

    # brier = sklearn.metrics.brier_score_loss(df_simres_test["success"], df_simres_test["xc"])
    # logloss = sklearn.metrics.log_loss(df_simres_test["success"], df_simres_test["xc"], labels=[0, 1])
    # try:
    #     auc = sklearn.metrics.roc_auc_score(df_simres_test["success"], df_simres_test["xc"])
    # except ValueError as e:
    #     auc = e
    #
    # # brier = sklearn.metrics.brier_score_loss(df_test[outcome_col], df_test["xc"])
    # # logloss = sklearn.metrics.log_loss(df_test[outcome_col], df_test["xc"])
    # # auc = sklearn.metrics.roc_auc_score(df_test[outcome_col], df_test["xc"])
    # st.write("#### Test results")
    # st.write(f"Brier: {brier}")
    # st.write(f"Logloss: {logloss}")
    # st.write(f"AUC: {auc}")
    #
    # # brier_skill_score = 1 - brier / baseline_brier
    # # st.write(f"Brier skill score: {brier_skill_score}")
    #
    # for is_synthetic in [True, False]:
    #     df_synth = df_simres_test[df_simres_test["is_synthetic"] == is_synthetic]
    #     brier = sklearn.metrics.brier_score_loss(df_synth["success"], df_synth["xc"])
    #     logloss = sklearn.metrics.log_loss(df_synth["success"], df_synth["xc"], labels=[0, 1])
    #     try:
    #         auc = sklearn.metrics.roc_auc_score(df_synth["success"], df_synth["xc"])
    #     except ValueError as e:
    #         auc = e
    #     st.write(f"#### Test results (synthetic={is_synthetic})")
    #     st.write(f"Brier (synthetic={is_synthetic}): {brier}")
    #     st.write(f"Logloss (synthetic={is_synthetic}): {logloss}")
    #     st.write(f"AUC (synthetic={is_synthetic}): {auc}")
    #
    # return


def validation_dashboard(dummy=False):
    dfs_tracking, dfs_event = get_metrica_data(dummy=dummy)

    ### DAS vs x_norm
    # for df_tracking, df_event in zip(dfs_tracking, dfs_event):
    #     das_vs_xnorm(df_tracking, df_event)
    #     break

    ### Validation
    dfs_passes = []
    for i, (df_tracking, df_events) in enumerate(zip(dfs_tracking, dfs_event)):
        df_events["player_id"] = df_events["player_id"].str.replace(" ", "")
        df_events["receiver_player_id"] = df_events["receiver_player_id"].str.replace(" ", "")

        ### Prepare data -> TODO put into other function
        dataset_nr = i + 1
        st.write(f"### Dataset {dataset_nr}")
        # if dataset_nr == 1 or dataset_nr == 2:
        #     continue
        # df_tracking = dataset
        # st.write(f"Getting events...")
        # df_events = get_kloppy_events(dataset_nr)

        st.write("Pass %", f'{df_events[df_events["is_pass"]]["success"].mean():.2%}',
                 f'Passes: {len(df_events[df_events["is_pass"]])}')

        st.write("df_tracking", df_tracking.shape)
        st.write(df_tracking.head())
        st.write("df_events", df_events.shape)
        st.write(df_events)

        ### Do validation with this data
        dfs_event.append(df_events)
        df_passes = df_events[(df_events["is_pass"]) & (~df_events["is_high"])]

        df_passes = df_passes.drop_duplicates(subset=["frame_id"])

        dfs_passes.append(df_passes)

        for _, p4ss in df_passes.iloc[:1].iterrows():
            plot_pass(p4ss, df_tracking)

    validate_das(dfs_tracking, dfs_passes)

    n_steps = st.number_input("Number of simulations", value=25000)
    use_prefit = st.checkbox("Use prefit parameters", value=True)

    return validate_multiple_matches(
        dfs_tracking=dfs_tracking, dfs_passes=dfs_passes, outcome_col="success", n_steps=n_steps, use_prefit=use_prefit
    )


def validate_das(dfs_tracking, dfs_passes):
    from accessible_space.interface import get_das_gained

    @st.cache_resource
    def _get_das(dataset_nr):
        df_passes = dfs_passes[dataset_nr]
        df_tracking = dfs_tracking[dataset_nr]
        das_result = get_das_gained(df_passes, df_tracking, event_success_col="success",
                                    event_target_frame_col="end_frame_id", event_start_x_col="coordinates_x",
                                    event_start_y_col="coordinates_y", event_target_x_col="end_coordinates_x",
                                    event_target_y_col="end_coordinates_y", tracking_period_col="period_id",
                                    )  # default -> 0.7603557334416071 mean, 0.7106466261420992
        return das_result

    dfs = []
    for dataset_nr in progress_bar([0, 1, 2], total=3):
        das_result = _get_das(dataset_nr)

        phi_grid = das_result.simulation_result.phi_grid[0]
        r_grid = das_result.simulation_result.r_grid

        dr = r_grid[1] - r_grid[0]

        df_passes = dfs_passes[dataset_nr]
        df_passes["frame_index"] = das_result.frame_index

        target_densities = []
        for pass_index, p4ss in progress_bar(dfs_passes[dataset_nr].iterrows(), total=len(dfs_passes[dataset_nr])):
            p4ss["angle"] = (2*math.pi + math.atan2(p4ss["end_coordinates_y"] - p4ss["coordinates_y"], p4ss["end_coordinates_x"] - p4ss["coordinates_x"])) % (2*math.pi)
            p4ss["distance"] = np.sqrt((p4ss["end_coordinates_y"] - p4ss["coordinates_y"])**2 + (p4ss["end_coordinates_x"] - p4ss["coordinates_x"])**2)
            phi_index = np.abs(phi_grid - p4ss["angle"]).argmin()
            r_index = np.abs(r_grid - p4ss["distance"]).argmin()
            F = p4ss["frame_index"]
            target_density = das_result.simulation_result.attack_poss_density[F, phi_index, r_index] * dr
            target_densities.append(target_density)

        df_passes["target_density"] = target_densities
        df_passes = df_passes[df_passes["success"]]
        df_passes["dataset_nr"] = dataset_nr
        dfs.append(df_passes)

    df_passes = pd.concat(dfs)

    # write target density mean
    st.write("Target density mean")
    st.write(df_passes["target_density"].mean())
    st.write(df_passes)
    st.write(df_passes.groupby("dataset_nr")["target_density"].mean())

def main(run_as_streamlit_app=True, dummy=False):
    if run_as_streamlit_app:
        key_argument = "run_dashboard"
        if len(sys.argv) == 2 and sys.argv[1] == key_argument:
            validation_dashboard(dummy=dummy)
        else:  # if script is called directly, call it again with streamlit
            subprocess.run(['streamlit', 'run', os.path.abspath(__file__), key_argument], check=True)
    else:
        validation_dashboard(dummy=dummy)


if __name__ == '__main__':
    main()
