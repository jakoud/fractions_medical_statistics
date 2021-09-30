import matplotlib.pyplot as plt
import pandas as pd


def prepare_normalization(df):
    min_h0 = df['Hgb0'].min()
    max_h0 = df['Hgb0'].max()
    min_h1 = df['Hgb1'].min()
    max_h1 = df['Hgb1'].max()

    return min_h0, max_h0, min_h1, max_h1


def read_database():
    df = pd.read_csv("/home/cyfronet/Downloads/data.csv")
    colors = pd.read_csv("/home/cyfronet/Downloads/colors.csv", header=None).values.tolist()

    return df, colors


def blood_separation(helper_df):
    blood_no = helper_df[helper_df["KrewStatus"] == 'KrewNo']
    blood_post = helper_df[helper_df["KrewStatus"] == "KrewPost"]
    blood_pre = helper_df[helper_df['KrewStatus'] == 'KrewPre']
    blood_both = helper_df[helper_df['KrewStatus'] == 'KrewPrePost']
    blood_rest = pd.concat([blood_pre, blood_both])

    return blood_no, blood_post, blood_rest


def fraction_types(df, column_name):
    return sorted(list(set(df[column_name])))


def normalization(dataframe, minimum, max):
    return (dataframe - minimum) / (max - minimum)


def combined():
    fig, ax = plt.subplots()
    df, colors = read_database()
    ax.set_box_aspect(1)
    min_h0, max_h0, min_h1, max_h1 = prepare_normalization(df)
    krew_no, krew_post, krew_rest = blood_separation(df)

    x = normalization(krew_no['Hgb0'], min_h0, max_h0)
    y = normalization(krew_no['Hgb1'], min_h1, max_h1)
    ax.scatter(x, y, color='cyan', marker='o', label='NO')

    x = normalization(krew_post['Hgb0'], min_h0, max_h0)
    y = normalization(krew_post['Hgb1'], min_h1, max_h1)
    ax.scatter(x, y, color='orange', marker='s', label='POST')

    x = normalization(krew_rest['Hgb0'], min_h0, max_h0)
    y = normalization(krew_rest['Hgb1'], min_h1, max_h1)
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
    df, colors = read_database()
    min_h0, max_h0, min_h1, max_h1 = prepare_normalization(df)
    helper_df = df[df['wzórLET'] == fraction_type]
    krew_no, krew_post, krew_rest = blood_separation(helper_df)

    x = normalization(krew_no['Hgb0'], min_h0, max_h0)
    y = normalization(krew_no['Hgb1'], min_h1, max_h1)
    plt.scatter(x, y, c='blue', label='NO')

    x = normalization(krew_post['Hgb0'], min_h0, max_h0)
    y = normalization(krew_post['Hgb1'], min_h1, max_h1)
    plt.scatter(x, y, c='orange', label='POST')

    x = normalization(krew_rest['Hgb0'], min_h0, max_h0)
    y = normalization(krew_rest['Hgb1'], min_h1, max_h1)
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
    df, colors = read_database()
    min_h0, max_h0, min_h1, max_h1 = prepare_normalization(df)
    fractions = fraction_types(df, 'wzórLET')

    for value in range(len(fractions)):
        helper_df = df[df['wzórLET'] == fractions[value]]
        krew_no, krew_post, krew_rest = blood_separation(helper_df)
        ax = plt.subplot(5, 4, value + 1)

        x = normalization(krew_no['Hgb0'], min_h0, max_h0)
        y = normalization(krew_no['Hgb1'], min_h1, max_h1)
        ax.scatter(x, y, color='cyan', marker='o', label='NO')

        x = normalization(krew_post['Hgb0'], min_h0, max_h0)
        y = normalization(krew_post['Hgb1'], min_h1, max_h1)
        ax.scatter(x, y, color='orange', marker='s', label='POST')

        x = normalization(krew_rest['Hgb0'], min_h0, max_h0)
        y = normalization(krew_rest['Hgb1'], min_h1, max_h1)
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


combined()