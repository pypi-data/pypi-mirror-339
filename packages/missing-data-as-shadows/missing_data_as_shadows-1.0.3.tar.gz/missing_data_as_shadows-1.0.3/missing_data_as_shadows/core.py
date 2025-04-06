import pandas as pd
import seaborn as sns
import sys
import matplotlib.pyplot as plt
import numpy as np
import itertools
import matplotlib.patheffects as pe
import matplotlib.patches as patches
import math
from matplotlib.backends.backend_pdf import PdfPages
from functools import wraps

pdf_file = None

dpi = 1200


def require_name_if_save_true(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get('save', False) and kwargs.get('name') is None:
            raise ValueError("If save is True, the name must be specified.")
        return func(*args, **kwargs)

    return wrapper


def open_pdf(name):
    """Otvorí nový PDF súbor s daným menom."""
    global pdf_file
    if pdf_file is None:
        pdf_file = PdfPages(f"{name}.pdf")
    return pdf_file


def show_save_helper(save, name):
    """Pomocná funkcia na zobrazenie a/alebo uloženie obrázka."""
    global pdf_file

    if save:
        # Ak PDF ešte nie je otvorený, otvorí ho
        if pdf_file is None:
            pdf_file = PdfPages(f"{name}.pdf")
        # Pridá aktuálny obrázok do PDF
        pdf_file.savefig(plt.gcf())


def close_pdf():
    """Zatvorí otvorený PDF súbor."""
    global pdf_file
    if pdf_file is not None:
        pdf_file.close()
        pdf_file = None


@require_name_if_save_true
def create_correlation_matrix_flatten(data_set, save=False, name=None, method="pearson"):
    df_numeric = data_set.select_dtypes(include=[float, int])
    correlation_matrix = df_numeric.corr(method=method).abs()

    # Nastavenie hlavnej diagonály na 0
    np.fill_diagonal(correlation_matrix.values, 0)

    plt.figure(figsize=(16, 12))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")

    show_save_helper(save, name)

    return correlation_matrix


def prepare_data(df, attribute_one, attribute_two):
    df_copy = df.copy()
    results = []
    attribute_one_value = f'{attribute_one}_value'
    attribute_two_missing_count = f'missing_{attribute_two}_count'

    # Prejdeme cez každú unikátnu hodnotu pre attribute_one
    for value in df_copy[attribute_one].dropna().unique():
        # Filtrovanie riadkov kde je attribute_one rovný aktuálnej hodnote
        filtered_df = df_copy[df_copy[attribute_one] == value]

        # Spočítame, koľko z týchto riadkov má chýbajúce hodnoty pre attribute_two
        missing_in_attribute_two = filtered_df[attribute_two].isnull().sum()

        if missing_in_attribute_two != 0:
            results.append((value, int(missing_in_attribute_two)))

    # Spočítame riadky, kde sú oba atribúty null
    both_missing_count = df_copy[df_copy[attribute_one].isnull() & df_copy[attribute_two].isnull()].shape[0]

    # Ak existujú riadky s obidvomi chýbajúcimi hodnotami, pridáme ich do výsledkov
    if both_missing_count > 0:
        results.append(('Both missing', both_missing_count))

    # Vytvorenie DataFrame z výsledkov
    results_df = pd.DataFrame(results, columns=[attribute_one_value, attribute_two_missing_count])

    # Výpočet 3. kvartilu pre stĺpec 'missing_attribute_two_count'
    third_quartile = results_df[attribute_two_missing_count].quantile(0.75)

    # Filtrovanie riadkov, kde je 'missing_attribute_two_count' väčší ako 3. kvartil, s výnimkou 'Both missing'
    filtered_df = results_df[results_df[attribute_two_missing_count] > third_quartile]

    # Zoradenie výsledkov podľa 'missing_attribute_two_count' zostupne
    sorted_filtered_df = filtered_df.sort_values(by=attribute_two_missing_count, ascending=False)

    # Pridanie riadka s 'Both missing' na koniec (ak existuje)
    if both_missing_count > 0:
        both_missing_row = results_df[results_df[attribute_one_value] == 'Both missing']
        sorted_filtered_df = sorted_filtered_df[sorted_filtered_df[attribute_one_value] != 'Both missing']
        sorted_filtered_df = pd.concat([sorted_filtered_df, both_missing_row])

    return [sorted_filtered_df, attribute_one_value, attribute_two_missing_count]


def create_plot(df, value_name, missing_count_name, name=None, save=False, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
        own_figure = True
    else:
        fig = ax.figure
        own_figure = False

    ax.set_facecolor('white')
    fig.patch.set_alpha(1)
    for spine in ax.spines.values():
        spine.set_visible(False)

    df[value_name] = df[value_name].astype(str)

    ax.bar(df[value_name], df[missing_count_name], color='grey')

    ax.set_xlabel(value_name)
    ax.set_ylabel(missing_count_name)

    ax.grid(False)
    plt.xticks(rotation=45)
    plt.tight_layout()

    show_save_helper(save, name)


def create_plot_bar(data, attribute_one, attribute_two, name=None, save=False, ax=None):
    result = prepare_data(data, attribute_one, attribute_two)
    create_plot(result[0], result[1], result[2], name, save, ax)


@require_name_if_save_true
def plot_all_pairs_bar_charts(data, columns=None, num_cols=3, name=None, save=False):
    if columns is None:
        columns = data.columns

    pairs = list(itertools.permutations(columns, 2))
    valid_pairs = []

    # Predspracovanie: Vynechanie prázdnych grafov
    for attribute_one, attribute_two in pairs:
        results_df, attrib_one_val, attrib_two_missing_count = prepare_data(data, attribute_one, attribute_two)

        if results_df[attrib_two_missing_count].notna().sum() > 0:  # Ak existujú ne-null hodnoty
            valid_pairs.append((attribute_one, attribute_two, results_df, attrib_one_val, attrib_two_missing_count))

    num_pairs = len(valid_pairs)
    if num_pairs == 0:
        return  # Ak nie sú dáta, nevoláme plt.show()

    num_rows = math.ceil(num_pairs / num_cols)

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12 * num_cols, 4 * num_rows), squeeze=False)

    for i, (attribute_one, attribute_two, results_df, atrib_one_val, atrib_two_missing_count) in enumerate(valid_pairs):
        row = i // num_cols
        col = i % num_cols
        ax = axes[row, col]

        results_df[atrib_one_val] = results_df[atrib_one_val].astype(str)
        x_positions = range(len(results_df))

        ax.bar(x_positions, results_df[atrib_two_missing_count], color='grey')

        ax.set_xlabel(atrib_one_val)
        ax.set_ylabel(atrib_two_missing_count)

        ax.set_xticks(x_positions)
        ax.set_xticklabels(results_df[atrib_one_val], rotation=90, ha='center')

        # Odstránenie pozadia, spines a mriežky
        ax.set_facecolor('white')
        fig.patch.set_alpha(0)
        fig.subplots_adjust(hspace=0.5)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.grid(False)

    # Odstránenie nadbytočných subplotov
    total_subplots = num_rows * num_cols
    for j in range(num_pairs, total_subplots):
        row = j // num_cols
        col = j % num_cols
        fig.delaxes(axes[row, col])

    show_save_helper(save, name)


def scatter_with_shadows_rect_binned(
        df,
        col_a,
        col_b,
        marker_size_scatter=3,
        marker_size_rect=0.5,
        bins_count=10,
        fraction_of_range=0.5,
        color_missing_b='grey',
        color_missing_a='grey',
        alpha_main=0.3,
        outline_color='black',
        outline_width=0.5,
        ax=None,
        save=True,
        name="scatter_with_shadows",
        full_report = False
):
    # Ak nedostaneme ax, vytvoríme vlastnú figúru
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
        own_figure = True
    else:
        fig = ax.figure
        own_figure = False

    ax.set_facecolor('white')
    fig.patch.set_alpha(0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    df_non_missing = df.dropna(subset=[col_a, col_b]).copy()

    ax.scatter(
        df_non_missing[col_a],
        df_non_missing[col_b],
        s=marker_size_scatter,
        c='black',
        alpha=0.7,
    )

    fig.canvas.draw()

    def marker_diameter_in_data(ax_, s_points2):
        import math
        r_points = math.sqrt(s_points2)
        diameter_points = 2 * r_points
        diameter_inch = diameter_points / 72
        diameter_px = diameter_inch * ax_.figure.dpi
        pt0_data = ax_.transData.inverted().transform([(0, 0)])[0]
        pt1_data = ax_.transData.inverted().transform([(diameter_px, 0)])[0]
        width_data = pt1_data[0] - pt0_data[0]
        return width_data

    diameterA = marker_diameter_in_data(ax, marker_size_rect)
    diameterB = diameterA

    # Diskretizácia na osi A
    A_min_val = df_non_missing[col_a].min()
    A_max_val = df_non_missing[col_a].max()
    binsA = np.linspace(A_min_val, A_max_val, bins_count + 1)

    df_non_missing['binA'] = pd.cut(df_non_missing[col_a], bins=binsA, include_lowest=True)
    agg_B = df_non_missing.groupby('binA')[col_b].agg(['min', 'max']).dropna()

    # Diskretizácia na osi B
    B_min_val = df_non_missing[col_b].min()
    B_max_val = df_non_missing[col_b].max()
    binsB = np.linspace(B_min_val, B_max_val, bins_count + 1)

    df_non_missing['binB'] = pd.cut(df_non_missing[col_b], bins=binsB, include_lowest=True)
    agg_A = df_non_missing.groupby('binB')[col_a].agg(['min', 'max']).dropna()

    # Missing B
    df_missing_B = df[df[col_b].isna() & df[col_a].notna()].copy()
    if len(df_missing_B) > 0:
        df_missing_B['binA'] = pd.cut(df_missing_B[col_a], bins=binsA, include_lowest=True)

        for idx, row in df_missing_B.iterrows():
            bin_label = row['binA']
            if pd.isna(bin_label) or (bin_label not in agg_B.index):
                continue

            bmin = agg_B.loc[bin_label, 'min']
            bmax = agg_B.loc[bin_label, 'max']
            if pd.isna(bmin) or pd.isna(bmax):
                continue

            b_center = (bmin + bmax) / 2.0
            full_height = (bmax - bmin)
            rect_height = fraction_of_range * full_height
            bottom_y = b_center - rect_height / 2

            A_i = row[col_a]
            left_x = A_i - diameterA / 2
            rect_width = diameterA

            rect = patches.FancyBboxPatch(
                (left_x, bottom_y),
                rect_width,
                rect_height,
                boxstyle="round,pad=0.7",
                facecolor=color_missing_b,
                alpha=alpha_main,
                edgecolor=outline_color if outline_width > 0 else None,
                linewidth=outline_width
            )
            ax.add_patch(rect)

    # Missing A
    df_missing_A = df[df[col_a].isna() & df[col_b].notna()].copy()
    if len(df_missing_A) > 0:
        df_missing_A['binB'] = pd.cut(df_missing_A[col_b], bins=binsB, include_lowest=True)

        for idx, row in df_missing_A.iterrows():
            bin_label = row['binB']
            if pd.isna(bin_label) or (bin_label not in agg_A.index):
                continue

            amin_ = agg_A.loc[bin_label, 'min']
            amax_ = agg_A.loc[bin_label, 'max']
            if pd.isna(amin_) or pd.isna(amax_):
                continue

            a_center = (amin_ + amax_) / 2.0
            full_width = (amax_ - amin_)
            rect_width = fraction_of_range * full_width
            left_x = a_center - rect_width / 2

            B_i = row[col_b]
            bottom_y = B_i - diameterB / 2
            rect_height = diameterB

            rect = patches.FancyBboxPatch(
                (left_x, bottom_y),
                rect_width,
                rect_height,
                boxstyle="round,pad=0.7",
                facecolor=color_missing_a,
                alpha=alpha_main,
                edgecolor=outline_color if outline_width > 0 else None,
                linewidth=outline_width
            )
            ax.add_patch(rect)

    ax.set_xlabel(col_a)
    ax.set_ylabel(col_b)

    ax.grid(False)
    plt.tight_layout()

    # Zobrazíme len ak sme vytvorili vlastnú figúru
    # if own_figure and show:
    #     plt.show()

    show_save_helper(save, name)
    if full_report is not True:
        close_pdf()

def create_subplot_with_shadows(data, atr1, atr2, name="subplot_with_shadows", save=True,full_report=False ):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

    # 2) "Zrušíme" (remove) horné Axes, aby sme mohli spraviť JEDEN široký
    gs = axes[0, 0].get_gridspec()
    for ax_ in axes[0, :]:
        ax_.remove()

    # Teraz pridáme "ax_top" ako subplot, ktorý zaberie celú prvú (0.) riadku
    ax_top = fig.add_subplot(gs[0, :])  # riadok 0, všetky stĺpce

    # 3) Horný široký graf: scatter_with_shadows_rect_binned
    scatter_with_shadows_rect_binned(
        data,
        col_a=atr1,
        col_b=atr2,
        name =name,
        save = False,
        bins_count=10,
        marker_size_scatter=3,
        marker_size_rect=0.005,
        ax=ax_top,
        full_report=full_report,
    )

    # 4) V spodnej riadku (riadok index 1) nám ostali 2 Axes: axes[1,0] a axes[1,1].
    # Vykreslíme tam dva bar charty:
    create_plot_bar(
        data,
        attribute_one=atr1,
        attribute_two=atr2,
        ax=axes[1, 0],  # ľavý spodný subplot
    )

    create_plot_bar(
        data,
        attribute_one=atr2,
        attribute_two=atr1,
        ax=axes[1, 1],  # pravý spodný subplot
    )

    axes[1, 0].tick_params(axis='x', labelrotation=90)
    axes[1, 1].tick_params(axis='x', labelrotation=90)

    # 5) Celkové doladenie a zobrazenie
    plt.tight_layout()
    show_save_helper(save, name)

    if full_report is not True:
        close_pdf()


# %%
def make_full_analysis(dataset, output_name="complete_report", method="pearson"):
    open_pdf(output_name)

    try:
        # Generovanie korelačnej matice
        correlation_matrix = create_correlation_matrix_flatten(dataset, save=True, name=output_name, method=method)
        plot_all_pairs_bar_charts(dataset, save=True, name=output_name)

        max_correlation_partners = correlation_matrix.idxmax(axis=1)

        # Použitie množiny na odstránenie duplikátov
        max_correlation_pairs = set()

        for atr1, atr2 in zip(max_correlation_partners.index, max_correlation_partners.values):
            pair = tuple(sorted([atr1, atr2]))  # Zabezpečíme rovnaké poradie v tuple
            max_correlation_pairs.add(pair)

        # Konverzia na list, ak chceš výstup ako list dvojíc
        max_correlation_pairs = list(max_correlation_pairs)

        for pair_of_max_correlation in max_correlation_pairs:
            create_subplot_with_shadows(dataset, pair_of_max_correlation[0], pair_of_max_correlation[1], save=True,
                                        name=output_name, full_report=True)

    finally:
        # Uzavretie PDF súboru (dôležité volať vždy na konci!)
        close_pdf()
