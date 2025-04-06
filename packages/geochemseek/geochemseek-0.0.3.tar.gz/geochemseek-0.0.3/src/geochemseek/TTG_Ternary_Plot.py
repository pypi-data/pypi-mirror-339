import ternary
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def normalize_data(data: pd.DataFrame | np.ndarray, columns: list[str] = None) -> np.ndarray:
    """
    Normalize input data so that the sum of each row equals 100.
    Parameters:
    - data (numpy.ndarray or pandas.DataFrame): Input data.
    - columns (list or None): Column names for DataFrame inputs. Defaults to all columns.
    Returns:
    - numpy.ndarray: Normalized data.
    """
    if isinstance(data, pd.DataFrame):
        if columns is None:
            columns = data.columns
        data = data[columns].values
    elif not isinstance(data, np.ndarray):
        raise ValueError("Input data must be a numpy array or pandas DataFrame.")

    row_sums = np.sum(data, axis=1).reshape(-1, 1)
    normalized_data = np.divide(data, row_sums, where=row_sums != 0) * 100
    return normalized_data


def configure_ternary_plot(
    tax,
    fontsize: int = 8,
    labels: dict = None,
    grid_color: str = "blue",
    grid_alpha: float = 0.5,
    grid_multiple: int = 10,
    tick_offset: float = 0.015,
) -> None:
    """
    Configure basic ternary plot settings.
    """
    tax.boundary(linewidth=1.0)
    tax.gridlines(color=grid_color, multiple=grid_multiple, linewidth=0.5, alpha=grid_alpha)

    default_labels = {"left": "Ab", "right": "Or", "top": "An"}
    if labels:
        if not all(key in default_labels for key in labels):
            raise ValueError("Labels dictionary must contain keys: 'left', 'right', 'top'")
        default_labels.update(labels)

    tax.left_corner_label(default_labels["left"], fontsize=fontsize)
    tax.right_corner_label(default_labels["right"], fontsize=fontsize)
    tax.top_corner_label(default_labels["top"], fontsize=fontsize)

    tax.ticks(axis="lbr", multiple=grid_multiple, linewidth=1, offset=tick_offset, fontsize=fontsize - 3)
    tax.get_axes().axis("off")
    tax.clear_matplotlib_ticks()


def create_ternary_plot(data, columns, output_file, scale, plot_type="Barker", sample_names=None):
    """
    Create a ternary plot for the specified plot type (Barker or O'Connor).
    """
    normalized_data = normalize_data(data, columns)
    figure, tax = ternary.figure(scale=scale)
    figure.set_size_inches(8 / 2.54, 8 / 2.54)

    # Use columns as axis labels
    labels = {"left": columns[2], "right": columns[0], "top": columns[1]}
    configure_ternary_plot(tax, labels=labels)

    if plot_type == "Barker":
        bg_data = np.array([
            [0, 30, 70], [20, 20, 60], [20, 32, 48],
            [20, 20, 60], [25, 17.5, 57.5], [30, 0, 70],
            [25, 17.5, 57.5], [35, 15, 50], [35, 26, 39]
        ])
        tax.plot(bg_data, lw=0.5, color='k', alpha=0.75)
        tax.annotate('Trondhjemite', (2, 10, 88), fontsize=6)
        tax.annotate('Granite', (30, 10, 60), fontsize=6)
        tax.annotate('Tonalite', (10, 30, 60), rotation=60, fontsize=6)
        tax.annotate('Granodiorite', (25, 20, 55), rotation=60, fontsize=6)
    elif plot_type == "O'Connor":
        lines_1 = [
            [(0, 25, 75), (50, 12.5, 37.5)],
            [(30, 17.5, 52.5), (30, 0, 0)],
            [(20, 20, 60), (20, 45, 35)],
        ]
        lines_2 = [
            [(50, 12.5, 37.5), (100, 0, 0)],
            [(35, 16.25, 48.75), (35, 38, 27)],
            [(50, 12.5, 37.5), (50, 30, 20)]
        ]
        for p1, p2 in lines_1:
            tax.line(p1, p2, linewidth=0.5, color='k', linestyle='-', alpha=0.75)
        for p1, p2 in lines_2:
            tax.line(p1, p2, linewidth=0.5, color='k', linestyle='--', alpha=0.75)
        tax.annotate('Trondhjemite', (4, 8, 88), fontsize=6)
        tax.annotate('Granite', (35, 8, 57), fontsize=6)
        tax.annotate('Tonalite', (10, 25, 65), rotation=60, fontsize=6)
        tax.annotate('Granodiorite', (25, 22, 53), rotation=60, fontsize=6)
        tax.annotate('Quartz monzonite', (40, 18, 42), rotation=60, fontsize=6)
    else:
        raise ValueError(f"Unknown plot type: {plot_type}")

    tax.scatter(normalized_data, s=5, color='r', alpha=0.8)
    
    # 新增样本标注功能
    if sample_names is not None:
        for i, (a, b, c) in enumerate(normalized_data):
            tax.annotate(sample_names[i], (a, b, c), fontsize=2, ha='left', va='bottom', xytext=(3, 3), textcoords='offset points')

    plt.savefig(output_file, format='svg', bbox_inches='tight')
    print(f"{plot_type} plot saved as {output_file}")
    plt.show()
    plt.close()




if __name__ == "__main__":
    file_name = "data.xlsx"
    sheet_name = "Sheet1"

    try:
        # Load data from Excel
        raw_data = pd.read_excel(file_name, sheet_name=sheet_name)
        plot_columns = ["Or", "An", "Ab"]
        sample_names = raw_data["sample name"].tolist()  # 新增样本名称列
    except FileNotFoundError:
        print(f"File {file_name} not found. Ensure the file is in the correct directory.")
        exit()

    create_ternary_plot(raw_data, columns=plot_columns, 
                       output_file="TTG_ternary_plot_Barker.svg", 
                       scale=100, plot_type="Barker",
                       sample_names=sample_names)  # 添加样本名称参数

    create_ternary_plot(raw_data, columns=plot_columns, output_file="TTG_ternary_plot_OConnor.svg", scale=100, plot_type="O'Connor", sample_names=sample_names)
