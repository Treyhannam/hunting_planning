import json
from pathlib import Path
import pandas as pd
import geopandas as gpd


def load_otc_data(otc_dict: dict, gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """Loads OTC data from a json file and converts it to a DataFrame. JSON file is copy and
    pasted from the CPW big game brochure.
    """
    all_data = []
    for k, v in otc_dict.items():
        data = v.split(",")
        data = [int(d) for d in data if d.strip().isdigit()]
        pub_private, sex = k.split("_", 1)
        all_data.append(
            pd.DataFrame(
                {
                    "gmu": data,
                    "public_or_private": [pub_private] * len(data),
                    "sex": [sex] * len(data),
                }
            )
        )

    all_df = pd.concat(all_data)

    otc_df = all_df.pivot_table(
        index="gmu",
        columns=["public_or_private", "sex"],
        aggfunc=lambda x: True,
        fill_value=False,
    ).reset_index()

    otc_df.columns = [
        "_".join(col).strip() if col[1] else col[0] for col in otc_df.columns.values
    ]
    otc_df = otc_df.rename(columns={"gmu_": "gmu"})

    complete_df = (
        gdf[["GMUID"]]
        .merge(otc_df, left_on="GMUID", right_on="gmu", how="left")
        .fillna(False)
    )

    complete_df["no_over_the_counter"] = ~complete_df[
        ["private_either_sex", "private_female", "public_either_sex", "public_female"]
    ].any(axis=1)

    complete_df.drop(columns=["gmu"], inplace=True)

    return complete_df


if __name__ == "__main__":
    data_directory = Path(__file__).parent.parent / "assets" / "data"

    json_fpath = data_directory / "otc.json"

    geo_fpath = data_directory / "cpw_gmu.geojson"

    gdf = gpd.read_file(geo_fpath)

    with open(json_fpath, "r") as file:
        otc_dict = json.load(file)

    df = load_otc_data(otc_dict, gdf)

    fpath = data_directory / "otc.csv"

    df.to_csv(fpath, index=False)
