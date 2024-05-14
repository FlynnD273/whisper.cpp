import math
import subprocess
import librosa
import datetime
import re

progressWidth = 50

NONE = "\033[0m"
GREEN = "\033[32m"

class TimedText:
    def __init__(self, start: str, end: str, text: str) -> None:
        self.start = start
        self.end = end
        self.text = text

    def __str__(self) -> str:
        return f"{GREEN}[{self.start}]{NONE} {self.text} {GREEN}[{self.end}]{NONE}"

def printProgress(progress: float) -> None:
    count = math.floor(progress*progressWidth)
    print(f"\r[{'#'*count}{' '*(progressWidth - count)}]", end="")

timeExp = re.compile(r"\[([0-9:.]+) --> ([0-9:.]+)\][\s]*(.*)")

file = "./samples/gb0.wav"
totalTime = librosa.get_duration(path=file)

cmd = [ "./main", "-m", "models/ggml-base.bin", file ]
proc = subprocess.Popen(cmd, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True)

transcript: list[TimedText] = []

printProgress(0)
for line in iter(proc.stdout.readline, ''): # type: ignore
    strline = line.rstrip()
    # print(">>> ", end="")
    # print(strline)


    if strline != "":
        matches = timeExp.match(strline)
        if matches is None:
            continue

        grps = matches.groups()
        if len(grps) == 3:
            latestTime = datetime.datetime.strptime(grps[1], "%H:%M:%S.%f") - datetime.datetime(1900, 1, 1)
            progress = latestTime.total_seconds()/totalTime
            printProgress(progress)
            transcript.append(TimedText(grps[0], grps[1], grps[2]))
            # print("Start: " + grps[0])
            # print("End: " + grps[1])
            # print("Text: " + grps[2])

print("\r" + " " * (progressWidth + 2), end="\r")
for text in transcript:
    print(text)
