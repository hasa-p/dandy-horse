import fitparse
import pandas as pd
import argparse
from datetime import datetime


def parse_fit_file(file_path):
    """Parse a FIT file and extract key activity data including heart rate."""
    try:
        fitfile = fitparse.FitFile(file_path)
        records = []

        for record in fitfile.get_messages("record"):
            record_data = {}
            for field in record:
                if field.name in [
                    'timestamp', 'distance', 'enhanced_speed',
                    'altitude', 'cadence', 'temperature',
                    'position_lat', 'position_long', 'heart_rate'
                ]:
                    record_data[field.name] = field.value

            if 'timestamp' in record_data:
                record_data['timestamp'] = record_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

            records.append(record_data)

        df = pd.DataFrame(records)

        # Calculate derived metrics
        if 'enhanced_speed' in df.columns:
            df['speed_kmh'] = df['enhanced_speed'] * 3.6  # Convert m/s to km/h

        return df

    except Exception as e:
        print(f"Error parsing FIT file: {e}")
        return None


if __name__ == '__main__':
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Parse a FIT file and extract activity data.')
    parser.add_argument('file_path', type=str, help='Path to the FIT file')

    current_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    parser.add_argument('--output', type=str, default=f'activity_data_{current_timestamp}.csv',
                        help='Output CSV file path (default: activity_data.csv)')
    args = parser.parse_args()

    # Parse the file
    activity_data = parse_fit_file(args.file_path)

    if activity_data is not None:
        # Save to CSV
        activity_data.to_csv(args.output, index=False)
        print(f"Success! Data saved to {args.output}")
        print("\nSample data with heart rate:")
        print(activity_data[['timestamp', 'heart_rate', 'speed_kmh', 'cadence']].head())
    else:
        print("Failed to parse the FIT file.")