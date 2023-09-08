#!/usr/bin/env python

import argparse
import json
import csv
from io import StringIO


def parse_spdx_file(spdx_file):
    with open(spdx_file, "r") as f:
        data = json.load(f)

    dependencies = []
    for package in data["packages"]:
        name = package["name"]
        ecosystem, _, name = name.partition(
            ":"
        )  # Split by ":" to separate ecosystem and name
        if (ecosystem != "") and (name == ""):
            name = ecosystem
            ecosystem = ""
        dependency = {
            "name": name.strip(),  # Remove leading/trailing whitespace
            "version": package["versionInfo"],
            "ecosystem": ecosystem,
            "license": package.get("licenseConcluded", "NOASSERTION"),
        }
        dependencies.append(dependency)

    return dependencies


def print_dependencies(dependencies, output_format):
    if output_format == "text":
        print("Dependency Details:")
        for dependency in dependencies:
            print(f"Name: {dependency['name']}")
            print(f"Version: {dependency['version']}")
            print(f"Ecosystem: {dependency['ecosystem']}")
            print(f"License: {dependency['license']}")
            print()

        # Print the total number of dependencies
        print(f"Total Dependencies: {len(dependencies)}")

    elif output_format == "markdown" or output_format == "md":
        print("| Name | Version | Ecosystem | License |")
        print("|------|---------|-----------|---------|")
        for dependency in dependencies:
            print(
                f"| {dependency['name']} | {dependency['version']} | {dependency['ecosystem']} | {dependency['license']} |"
            )
            
    elif output_format == "csv":
        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)
        csv_writer.writerow(["Name", "Version", "Ecosystem", "License"])
        for dependency in dependencies:
            csv_writer.writerow(
                [
                    dependency["name"],
                    dependency["version"],
                    dependency["ecosystem"],
                    dependency["license"],
                ]
            )
        print(csv_output.getvalue())


def sort_dependencies(dependencies, sort_by):
    if sort_by == "name":
        return sorted(dependencies, key=lambda x: x["name"])
    elif sort_by == "version":
        return sorted(dependencies, key=lambda x: x["version"])
    elif sort_by == "ecosystem":
        return sorted(dependencies, key=lambda x: x["ecosystem"])
    elif sort_by == "license":
        return sorted(dependencies, key=lambda x: x["license"])
    else:
        return dependencies


def main():
    parser = argparse.ArgumentParser(
        description="Parse SPDX files and extract dependency details."
    )
    parser.add_argument("spdx_files", nargs="+", help="One or more SPDX files to parse")
    parser.add_argument(
        "-o", "--output-format",
        choices=["text", "markdown", "md", "csv"],
        default="text",
        help="Output format (text/markdown/csv)",
    )
    parser.add_argument(
        "-s", "--sort-by",
        choices=["name", "version", "ecosystem", "license"],
        default=None,
        help="Sort dependencies by specified field",
    )

    args = parser.parse_args()

    all_dependencies = []
    for spdx_file in args.spdx_files:
        dependencies = parse_spdx_file(spdx_file)
        all_dependencies.extend(dependencies)

    if args.sort_by:
        all_dependencies = sort_dependencies(all_dependencies, args.sort_by)

    print_dependencies(all_dependencies, args.output_format)


if __name__ == "__main__":
    main()
