import numpy as np
import pandas as pd

# Load dataset
df = pd.read_csv("dataset/smartphone_cleaned_v2.csv")

class PY():
    def brand_name(self):
        return df['brand_name'].unique().tolist()

    def model(self):
        return df['model'].unique().tolist()

    def rating(self):
        return {
            "min": float(df['rating'].min()),
            "max": float(df['rating'].max()),
            "default": float(df['rating'].median())
        }

    def has_5g(self):
        return df['has_5g'].unique().tolist()

    def has_nfc(self):
        return df['has_nfc'].unique().tolist()

    def has_ir_blaster(self):
        return df['has_ir_blaster'].unique().tolist()

    def processor_name(self):
        return df['processor_name'].unique().tolist()

    def processor_brand(self):
        return df['processor_brand'].unique().tolist()

    def num_cores(self):
        return df['num_cores'].unique().tolist()

    def processor_speed(self):
        return {
            "min": float(df['processor_speed'].min()),
            "max": float(df['processor_speed'].max()),
            "default": float(df['processor_speed'].median())
        }

    def battery_capacity(self):
        return {
            "min": int(df['battery_capacity'].min()),
            "max": int(df['battery_capacity'].max()),
            "default": int(df['battery_capacity'].median())
        }

    def fast_charging(self):
        return df['fast_charging'].unique().tolist()

    def ram_capacity(self):
        return {
            "min": int(df['ram_capacity'].min()),
            "max": int(df['ram_capacity'].max()),
            "default": int(df['ram_capacity'].median())
        }

    def internal_memory(self):
        return {
            "min": int(df['internal_memory'].min()),
            "max": int(df['internal_memory'].max()),
            "default": int(df['internal_memory'].median())
        }

    def screen_size(self):
        return {
            "min": float(df['screen_size'].min()),
            "max": float(df['screen_size'].max()),
            "default": float(df['screen_size'].median())
        }

    def refresh_rate(self):
        return df['refresh_rate'].unique().tolist()

    def resolution(self):
        return df['resolution'].unique().tolist()

    def num_rear_cameras(self):
        return df['num_rear_cameras'].unique().tolist()

    def num_front_cameras(self):
        return df['num_front_cameras'].unique().tolist()


