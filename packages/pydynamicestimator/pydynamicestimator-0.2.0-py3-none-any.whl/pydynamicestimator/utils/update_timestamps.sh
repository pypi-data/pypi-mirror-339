#!/bin/bash
for file in $(find C:/Users/mkatanic/Documents/Research/PowerDynamicEstimator/pydynamicestimator/ \( -name '*.py' -o -name '*.txt' \)); do
    DATE=$(date '+%Y-%m-%d')  # Only date, without time
    # Update the second line to reflect the new Last Modified date
    sed -i "2s|# Last Modified:.*|# Last Modified: $DATE|" "$file"
done
