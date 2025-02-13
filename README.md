# flacue

Lossless FLAC splitter using CUE sheets, powered by ffmpeg/ffcuesplitter.

### Description

A super simple command line tool that splits large lossless audio files (like FLAC, APE etc.) into individual tracks based on information from a CUE sheet.

### Features
*   It is a simple wrapper around `ffcuesplitter`
*   Supports common lossless audio formats
*   Easy to use from the terminal
*   Option to remove original file and cleanup your audio library after splitting

### Depends on:
*   ffmpeg - download it from https://ffmpeg.org/


### Installation

    pip install flacue

### Usage from terminal:

    ~$ flacue "path/to/cuefile.cue"  
    ~$ flacue "path/to/cuefile.cue" -ro  # removes the original audio file

