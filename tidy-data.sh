#!/bin/bash
echo "Removing all CSV data in /output"
rm "${PWD}"/output/*.csv
rm "${PWD}"/output/plots/*.png
echo "Old data removed"