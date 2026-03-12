# Explanation of the Dockerfile:
#  - `FROM`: Base image (Python 3.13)
# - `RUN`: Execute commands during build
# - `WORKDIR`: Set working directory
# - `COPY`: Copy files into the image
# - `ENTRYPOINT`: Default command to run

# To run this pipeline, you would typically build the Docker image and then run a container with the appropriate argument for the day. For example:
# 1. Build the Docker image:
#    docker build -t my_pipeline_image .
# 2. Run the container with the day argument:
#    docker run --rm my_pipeline_image 1


import sys
import pandas as pd

print("arguments", sys.argv)

day = int(sys.argv[1])
print(f"Running pipeline for day {day}")

df = pd.DataFrame({"A": [1,2], "B": [3,4]})
print(df.head())

df.to_parquet(f"output_day_{day}.parquet")

