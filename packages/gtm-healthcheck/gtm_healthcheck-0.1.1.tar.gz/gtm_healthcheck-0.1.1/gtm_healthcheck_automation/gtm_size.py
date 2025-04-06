import json
import csv
import argparse
import os

def healthcheck(json_object):
    stringlength = json.dumps(json_object, separators=(",", ":"))
    size_kb = len(stringlength.encode()) / 1024
    return size_kb

def generate_healthcheck_csv(json_input_file, csv_output_file="healthcheck.csv"):
    with open(json_input_file, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    tags = data["containerVersion"].get("tag", [])
    triggers = data["containerVersion"].get("trigger", [])
    variables = data["containerVersion"].get("variable", [])

    tag_sizes = [(tag["name"], healthcheck(tag)) for tag in tags]
    trigger_sizes = [(trigger["name"], healthcheck(trigger)) for trigger in triggers]
    variable_sizes = [(variable["name"], healthcheck(variable)) for variable in variables]

    total_tag_size = sum(size for _, size in tag_sizes)
    total_trigger_size = sum(size for _, size in trigger_sizes)
    total_variable_size = sum(size for _, size in variable_sizes)

    with open(csv_output_file, mode="w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Type", "Name", "Size (KB)", "% Occupied"])

        for name, size in tag_sizes:
            percent = (size / total_tag_size * 100) if total_tag_size > 0 else 0
            csv_writer.writerow(["Tag", name, f"{size:.2f}", f"{percent:.1f}%"])

        for name, size in trigger_sizes:
            percent = (size / total_trigger_size * 100) if total_trigger_size > 0 else 0
            csv_writer.writerow(["Trigger", name, f"{size:.2f}", f"{percent:.1f}%"])

        for name, size in variable_sizes:
            percent = (size / total_variable_size * 100) if total_variable_size > 0 else 0
            csv_writer.writerow(["Variable", name, f"{size:.2f}", f"{percent:.1f}%"])

    print(f"✅ Healthcheck file generated: {os.path.abspath(csv_output_file)}")

def main():
    parser = argparse.ArgumentParser(description="GTM Healthcheck JSON Analyzer")
    parser.add_argument("filename", help="Path to GTM container JSON file")
    args = parser.parse_args()

    generate_healthcheck_csv(args.filename)

if __name__ == "__main__":
    main()
