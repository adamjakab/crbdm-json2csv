#!/usr/bin/env python
#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#
import sys
import os
import re

in_filename = "data/test1.json"
out_filename = "data/test1.csv"

start_pattern = '.*"values":\\['
end_pattern = '\\],"partial":true\\}\\]\\}\\]\\}'

buffer = ""

full_fil_size = os.path.getsize(in_filename)
chunk_size = 10240
chunk_count = round(full_fil_size / chunk_size)
chunk_number = 0

out_file_stream = open(out_filename, "w")
out_file_stream.write('"time", "AP", "clients"' + "\n")


def handle_match(match):
    match = match.group(1)
    out_file_stream.write(match + "\n")
    # print("Match: '{0}'".format(match))
    return ""


def update_progress(title, progress):
    bar_length = 40  # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(bar_length*progress))
    text = "\r{0}[{1}] {2}% {3}".format(
        title, "#"*block + "-"*(bar_length-block), round(progress*100), status)
    sys.stdout.write(text)
    sys.stdout.flush()


with open(in_filename) as f:
    while True:
        # print("{0}/{1}".format(chunk_number, chunk_count))
        progress_percent = chunk_number / chunk_count
        update_progress("converting:", progress_percent)
        chunk_number += 1

        chunk = f.read(chunk_size)
        if not chunk:
            break
        # print("-" * 80 + ":buffer: {0}".format(buffer))
        if chunk_number == 1:
            chunk = re.sub(start_pattern, "", chunk)
        # chunk = re.sub(end_pattern, "", chunk)
        buffer = buffer + chunk
        buffer = re.sub("\\[([^]]*)\\],?", handle_match, buffer)
        if len(buffer) > 1024:
            # print("buffer overflow: '{0}'".format(buffer))
            buffer = buffer[-128:]
            # print("buffer fix: '{0}'".format(buffer))

#
# print("=" * 80)
# print("Done.")
# print("Leftover in buffer: '{0}'".format(buffer))
out_file_stream.close()
print("Output saved in: {0}".format(out_filename))

