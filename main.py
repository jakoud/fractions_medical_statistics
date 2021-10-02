import matplotlib.pyplot as plt
import pandas as pd
from preparations import prepare_normalization, blood_separation, normalization, fraction_types, read_database, dataframe_info
import seaborn as sns


def combined():
    fig, ax = plt.subplots()
    df = read_database()
    ax.set_box_aspect(1)
    minimum, maximum = prepare_normalization(df)
    krew_no, krew_post, krew_rest = blood_separation(df)

    x = normalization(krew_no['Hgb0'], minimum, maximum)
    y = normalization(krew_no['Hgb1'], minimum, maximum)
    ax.scatter(x, y, color='cyan', marker='o', label='NO')

    x = normalization(krew_post['Hgb0'], minimum, maximum)
    y = normalization(krew_post['Hgb1'], minimum, maximum)
    ax.scatter(x, y, color='orange', marker='s', label='POST')

    x = normalization(krew_rest['Hgb0'], minimum, maximum)
    y = normalization(krew_rest['Hgb1'], minimum, maximum)
    ax.scatter(x, y, color='grey', marker='^', label='YES')

    plt.axis([0, 1, 0, 1])
    plt.plot([0, 1], [0, 1], transform=ax.transAxes, c='black', alpha=0.5)
    plt.title('All patients by blood transfusion')
    plt.axhline(0.5, color='red', alpha=0.3)
    plt.axvline(0.5, color='red', alpha=0.3)
    plt.xlabel('Hgb0')
    plt.ylabel('Hgb1')
    plt.legend(loc='best')
    plt.show()


def single(fraction_type):
    fig, ax = plt.subplots()
    ax.set_box_aspect(1)
    df, colors = read_database()
    minimum, maximum = prepare_normalization(df)
    helper_df = df[df['wzórLET'] == fraction_type]
    krew_no, krew_post, krew_rest = blood_separation(helper_df)

    x = normalization(krew_no['Hgb0'], minimum, maximum)
    y = normalization(krew_no['Hgb1'], minimum, maximum)
    plt.scatter(x, y, c='blue', label='NO')

    x = normalization(krew_post['Hgb0'], minimum, maximum)
    y = normalization(krew_post['Hgb1'], minimum, maximum)
    plt.scatter(x, y, c='orange', label='POST')

    x = normalization(krew_rest['Hgb0'], minimum, maximum)
    y = normalization(krew_rest['Hgb1'], minimum, maximum)
    plt.scatter(x, y, c='pink', label='REST')

    plt.axis([0, 1, 0, 1])
    plt.plot([0, 1], [0, 1], transform=ax.transAxes, c='green', alpha=0.5, label='EQUALITY AXIS')

    plt.axhline(0.5, color='red', alpha=0.3, label='DIVISION QUARTERS')
    plt.axvline(0.5, color='red', alpha=0.3)

    plt.xlabel('Hgb0')
    plt.ylabel('Hgb1')
    plt.title(fraction_type)
    plt.legend(loc='upper left')
    plt.show()


def grid():
    fig, ax = plt.subplots()
    df = read_database()
    minimum, maximum = prepare_normalization(df)
    fractions = fraction_types(df, 'wzórLET')

    for value in range(len(fractions)):
        helper_df = df[df['wzórLET'] == fractions[value]]
        krew_no, krew_post, krew_rest = blood_separation(helper_df)
        ax = plt.subplot(5, 4, value + 1)

        x = normalization(krew_no['Hgb0'], minimum, maximum)
        y = normalization(krew_no['Hgb1'], minimum, maximum)
        ax.scatter(x, y, color='cyan', marker='o', label='NO')

        x = normalization(krew_post['Hgb0'], minimum, maximum)
        y = normalization(krew_post['Hgb1'], minimum, maximum)
        ax.scatter(x, y, color='orange', marker='s', label='POST')

        x = normalization(krew_rest['Hgb0'], minimum, maximum)
        y = normalization(krew_rest['Hgb1'], minimum, maximum)
        ax.scatter(x, y, color='grey', marker='^', label='YES')

        ax.axis([0, 1, 0, 1])
        plt.plot([0, 1], [0, 1], transform=ax.transAxes, c='green', alpha=0.3)
        ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False,
                       labelleft=False)
        ax.axhline(0.5, color='red', alpha=0.3)
        ax.axvline(0.5, color='red', alpha=0.3)
        plt.title(fractions[value])

    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper left')
    fig.text(0.5, 0.04, 'Hgb0', ha='center')
    fig.text(0.04, 0.5, 'Hgb1', va='center', rotation='vertical')
    plt.show()


def histograms():
    df = read_database()
    krew_no, krew_post, krew_rest = blood_separation(df)
    df = pd.concat([krew_no, krew_post])
    sns.histplot(df['Hgb1-Hgb0'], bins=20, kde=True)
    plt.show()


def boxplots():
    df = read_database()
    krew_no, krew_post, krew_rest = blood_separation(df)
    df = pd.concat([krew_no, krew_post])
    ax = sns.boxplot(x="wzórLET", y="Hgb1-Hgb0", data=df, order=fraction_types(df, 'wzórLET'))
    # Calculate number of obs per group & median to position labels
    nobs = [str(len(df[df['wzórLET'] == fraction])) for fraction in fraction_types(df, 'wzórLET')]

    # Add it to the plot
    pos = range(len(nobs))
    for tick, label in zip(pos, ax.get_xticklabels()):
        ax.text(pos[tick],
                -9.2,
                nobs[tick],
                horizontalalignment='center',
                size='x-small',
                color='b',
                weight='semibold')

    plt.show()

df = read_database()
dataframe_info(df)
