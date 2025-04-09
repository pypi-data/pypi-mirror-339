from .stock_data import *

def MA(df_raw, feature, period):
    df = df_raw[['R_Symbol',feature]].copy()
    try:
        return df.groupby('R_Symbol')[feature].rolling(window = period, min_periods=None, closed= 'right').mean(engine = 'cython').values
    except:
        print('Error in MA function with feature: ', feature)
        return None

def MAX(df_raw, feature, period):
    df = df_raw[['R_Symbol',feature]].copy()
    try:
        return df.groupby('R_Symbol')[feature].rolling(window = period, min_periods=None, closed= 'right').max(engine = 'cython').values
    except:
        print('Error in MAX function with feature: ', feature)
        return None
    
def MIN(df_raw, feature, period):
    df = df_raw[['R_Symbol',feature]].copy()
    try:
        return df.groupby('R_Symbol')[feature].rolling(window = period, min_periods=None, closed= 'right').min(engine = 'cython').values
    except:
        print('Error in MIN function with feature: ', feature)
        return None

def STD(df_raw, feature, period):
    df = df_raw[['R_Symbol',feature]].copy()
    try:
        return df.groupby('R_Symbol')[feature].rolling(window = period, min_periods=None, closed= 'right').std(ddof=0).values
    except:
        print('Error in STD function with feature: ', feature)
        return None
    
def OVER(df_raw, numerator, denominator, period = None):
    df = df_raw.copy()
    df['num'] = df[numerator]
    df['den'] = df[denominator]
    if period is None:
        return (df['num'] - df['den'] )/ df['den']
    else:
        df['den'] = df.groupby('R_Symbol').shift(period)['den']
        return (df['num'] - df['den'] )/ df['den']