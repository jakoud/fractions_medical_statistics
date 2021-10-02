import pandas as pd


def read_database():
    df = pd.read_csv("Documents/VS Code/fractions_medical_statistics/data.csv", sep=";")

    return df


def prepare_normalization(df):
    min_h0 = df['Hgb0'].min()
    max_h0 = df['Hgb0'].max()
    min_h1 = df['Hgb1'].min()
    max_h1 = df['Hgb1'].max()

    return min_h0, max_h0, min_h1, max_h1


def blood_separation(helper_df):
    blood_no = helper_df[helper_df["KrewStatus"] == 'KrewNo']
    blood_post = helper_df[helper_df["KrewStatus"] == "KrewPost"]
    blood_pre = helper_df[helper_df['KrewStatus'] == 'KrewPre']
    blood_both = helper_df[helper_df['KrewStatus'] == 'KrewPrePost']
    blood_rest = pd.concat([blood_pre, blood_both])

    return blood_no, blood_post, blood_rest


def fraction_types(df, column_name):
    return sorted(list(set(df[column_name])))


def normalization(df, minimum, maximum):
    return (df - minimum) / (maximum - minimum)


def dataframe_info(df):
    print(df.info())
    print(len(df))
