import matplotlib.pyplot as plt
import pandas as pd
import argparse
import os

def map_to_new_range(c, a, b):
    new_c = 3.14 - (((c - a) / (b - a)) * (3.14 - 0) + 0)
    return new_c

def gauge_design(value, ref_range, unit, parameter,save_dir):

    diff = ref_range[1] - ref_range[0]

    if ref_range[0] - diff >= value:
        if value - diff < 0 and value >= 0:
            a = 0
        else:
            a = value - diff
    elif ref_range[0] - diff >= 0:
        a = ref_range[0] - diff
    else:
        a = 0

    if ref_range[1] + diff <= value:
        b = value + diff
    elif a == 0:
        b = ref_range[1] + ref_range[0] - a
        if value > b:
            b = value + diff 
    else:
        b = ref_range[1] + diff

    low_range = [a, ref_range[0]]
    high_range = [ref_range[1], b]

    val_rad = map_to_new_range(value, a, b)
    one_unit = 3.14 / (b - a)

    low_range_diff = low_range[1] - low_range[0]
    high_range_diff = high_range[1] - high_range[0]

    values = [b, ref_range[1], ref_range[0], a]

    low_width = one_unit * low_range_diff
    high_width = one_unit * high_range_diff

    x_axis_vals = [0, high_width, (one_unit * diff + high_width), 3.14]

    fig = plt.figure(figsize=(10, 5))

    ax = fig.add_subplot(projection="polar")

    ax.set_aspect('equal')

    ax.set_thetamin(0)
    ax.set_thetamax(180)

    ax.bar(x=0, width=high_width, height=0.5, bottom=2,
           edgecolor='white', color="#ee4d55", align='edge', linewidth=3)

    ax.bar(x=high_width, width=(3.14 - low_width - high_width), height=0.5, bottom=2,
           edgecolor='white', color='#4dab6d', align='edge', linewidth=3)

    ax.bar(x=(one_unit * diff + high_width), width=low_width, height=0.5, bottom=2,
           edgecolor='white', color="#f6ee54", align='edge', linewidth=3)

    for loc, val in zip(x_axis_vals, values):
        plt.annotate(val, fontweight="bold", fontsize=15, xy=(loc, 2.5), ha='right' if val <= (b + a) / 2 else "left")

    plt.annotate(" ",xytext=(0, 0), xy=(val_rad, 2.0),
                 arrowprops=dict(arrowstyle="wedge", color="black"),
                 bbox=dict(boxstyle="circle", facecolor="black", linewidth=2.0),
                 fontsize=20, fontweight='bold', color="white")

    plt.text(-1.57, 0.5, str(value), fontsize=20, fontweight="bold",ha='center', va='center')
    plt.text(-1.57, 0.85, "Units: " + unit, fontsize=18,  ha='center', va='center')

    ax.set_axis_off()
    attr_save_path = os.path.join(save_dir, f"{parameter}_gauge.png")
    plt.savefig(attr_save_path, transparent=True)

    # return fig


def create_gauges(csv_file,save_dir):
    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():
        parameter = row['Para.']
        value_str = str(row['Result'])
        unit = row['Unit']
        ref_range_str = row['Ref.Ranges']

        if '.' in value_str and not value_str.endswith('.0'):
            value = float(value_str)
        else:
            value = int(float(value_str))

        ref_range = [int(float(value)) if '.' in value and not value.endswith('.0') else int(value) for value in ref_range_str.split("-")]

        gauge_design(value, ref_range, unit, parameter,save_dir)

# def create_gauges(csv_file):
#     df = pd.read_csv(csv_file)
#     gauge_data = {}

#     for index, row in df.iterrows():
#         parameter = row['Para.']
#         value_str = str(row['Result'])
#         unit = row['Unit']
#         ref_range_str = row['Ref.Ranges']

#         if '.' in value_str and not value_str.endswith('.0'):
#             value = float(value_str)
#         else:
#             value = int(float(value_str))

#         ref_range = [int(float(value)) if '.' in value and not value.endswith('.0') else int(value) for value in ref_range_str.split("-")]

#         fig = gauge_design(value, ref_range, unit, parameter)
#         gauge_data[parameter] = fig
#     return gauge_data

# Usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate gauge images from a csv file')
    parser.add_argument('--csv_file', type=str, help='Path to the csv file containing the data', required=True)
    parser.add_argument('--save_dir', type=str, help='Path to save the generated images', required=True)
    args = parser.parse_args()
    init_dir = os.path.join(args.save_dir,os.path.basename(args.csv_file)[:-4])
    
    if not os.path.exists(init_dir):
        os.makedirs(init_dir, exist_ok=True)
        
    create_gauges(args.csv_file,init_dir)
