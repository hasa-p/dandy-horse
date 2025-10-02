import os
import argparse
import fitparse
from datetime import datetime


def analyze_fit_structure(input_file, output_file=None):
    """
    Analyze FIT file structure with clean output to file and console summary.
    """
    # Set default output filename if not provided
    if output_file is None:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"fit_analysis_{base_name}_{timestamp}.txt"

    # Load the FIT file
    fitfile = fitparse.FitFile(input_file)
    message_count = 0
    field_count = 0
    unique_messages = set()
    unique_fields = set()

    print(f"Analyzing {input_file}...")

    with open(output_file, 'w') as f:
        # Write header
        f.write(f"FIT File Analysis Report\n")
        f.write(f"File: {input_file}\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write("=" * 80 + "\n\n")

        # Process messages with progress feedback
        for i, message in enumerate(fitfile.get_messages()):
            message_count += 1
            unique_messages.add(message.name)

            f.write(f"Message #{i + 1}: {message.name}\n")
            f.write("-" * 60 + "\n")

            # Get message number if available
            msg_num = 'N/A'
            if hasattr(message, 'def_mesg'):
                if hasattr(message.def_mesg, 'global_mesg_num'):
                    msg_num = message.def_mesg.global_mesg_num

            f.write(f"Type: {message.mesg_type}\n")
            f.write(f"Global Message #: {msg_num}\n\n")

            # Process fields
            f.write("Fields:\n")
            for field in message:
                field_count += 1
                unique_fields.add(field.name)

                try:
                    value = field.value
                    if isinstance(value, bytes):
                        value = f"<bytes: {value.hex()}>"
                    elif isinstance(value, list):
                        value = [v.hex() if isinstance(v, bytes) else v for v in value]

                    f.write(f"  {field.name}:\n")
                    f.write(f"    Type: {field.type}\n")
                    f.write(f"    Value: {value}\n")
                    if field.units:
                        f.write(f"    Units: {field.units}\n")
                    f.write("\n")
                except Exception as e:
                    f.write(f"  [Error processing field: {str(e)}]\n\n")

            f.write("\n")  # Extra space between messages

            # Print progress every 50 messages
            if (i + 1) % 50 == 0:
                print(f"  Processed {i + 1} messages...")

    # Print summary to console
    print("\nAnalysis complete!")
    print(f"Results saved to: {output_file}")
    print(f"\nSummary Statistics:")
    print(f"- Total messages processed: {message_count}")
    print(f"- Unique message types: {len(unique_messages)}")
    print(f"- Total fields processed: {field_count}")
    print(f"- Unique field names: {len(unique_fields)}")
    print("\nTip: Use 'less' or a text editor to view the output file:")
    print(f"    less {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze FIT file structure with clean output')
    parser.add_argument('input_file', help='Path to the input FIT file')
    parser.add_argument('-o', '--output', help='Custom output file path (optional)')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        exit(1)

    analyze_fit_structure(args.input_file, args.output)
