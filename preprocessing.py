import pandas as pd
from datetime import datetime, timedelta
idx = pd.IndexSlice

def to_timedelta(str, format = '%M:%S.%fs'):
    if str == '-':
        return pd.NA
    parsed_time = datetime.strptime(str, format)
    return timedelta(
        minutes=parsed_time.minute,
        seconds=parsed_time.second,
        microseconds=parsed_time.microsecond
    )

def clean_pits(path, out):
    pits = pd.read_pickle(path)
    pits['Pit'] = pd.to_numeric(pits['Pit'].str.split().str[-1].str[:-1])
    pits['Tyres condition'] = pd.to_numeric(pits['Tyres condition'].str[:-1])/100
    pits['Fuel left'] = pd.to_numeric(pits['Fuel left'].str[:-1])/100
    pits['Pit time'] = pd.to_numeric(pits['Pit time'].str[:-1])
    pits['Refilled to'] = (pd.to_numeric(pits['Refilled to'].str.split().str[0], 'coerce')/180).fillna(pits['Fuel left'])
    pits['Fuel used'] = pits['Refilled to'].shift(1) - pits['Fuel left']
    pits.loc[idx[:, 0], 'Fuel used'] = pd.NA
    pits['Tyres used'] = 1 - pits['Tyres condition']
    pits.to_pickle(out)

def clean_laps(path, out):
    laps = pd.read_pickle(path)
    laps['Pos'] = pd.to_numeric(laps['Pos'])
    laps['Temp'] = pd.to_numeric(laps['Temp'].str[:-1])
    laps['Hum'] = pd.to_numeric(laps['Hum'].str[:-1])/100
    laps['Lap time'] = laps['Lap time'].apply(lambda t: to_timedelta(t, '%M:%S.%f'))
    laps.to_pickle(out)

def clean_tracks(path, out):
    tracks = pd.read_pickle(path)
    tracks.index += 1
    tracks['Lap distance'] = pd.to_numeric(tracks['Lap distance'].str.split().str[0])
    tracks.to_pickle(out)

def clean_practice(path, out):
    practice = pd.read_pickle(path)
    practice['Net time'] = practice['Net time'].apply(lambda t: to_timedelta(t).total_seconds())
    practice['Lap time'] = practice['Lap time'].apply(lambda t: to_timedelta(t).total_seconds())
    practice['Driver mistake'] = pd.to_numeric(practice['Driver mistake'].str[:-1])
    practice.to_pickle(out)

clean = {'pits': clean_pits, 'laps': clean_laps, 'tracks': clean_tracks, 'practice': clean_practice}