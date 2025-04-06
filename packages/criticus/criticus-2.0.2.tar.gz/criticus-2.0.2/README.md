# Criticus
This is a collection of computer tools for aiding the text critical workflow from transcription to collation to analysis.
Some of the tools already exist as CLI's that I have made, but here are are collected into one place and converted to user-friendly GUI applications.

## The Problem I'm trying to Solve
The standard tool for transcribing ancient New Testament manuscripts ([ITSEE's OTE](https://itsee-wce.birmingham.ac.uk/ote/transcriptiontool)) produces files in an entirely different format from that required by the standard tool for collating these transcriptions ([the WCE Collation Editor](https://github.com/itsee-birmingham/standalone_collation_editor)).

Moving from transcription to collation to analysis requires several steps of intermediate conversion of the data along the way. Criticus is a collection of tools to help 'connect' these three basic tasks.

## What Criticus Does
Criticus is a desktop app with ten distinct tools:
1. Convert a plain text transcription of a chapter or other unit into single-verse JSON files properly formatted for use in the Collation Editor. This is the simplest way to get data into the Collation Editor.
2. Convert a repurposed superset of Markdown to TEI XML. Included is a graphical user interface (GUI) to my CLI [MarkdownTEI](https://github.com/d-flood/MarkdownTEI). This is presented as simple and offline alternative to the [Online Transcription Editor (OTE)](https://itsee-wce.birmingham.ac.uk/ote/transcriptiontool). MarkdownTEI converted files can even be uploaded to the OTE.
3. Convert TEI transcriptions (from MarkdownTEI or the OTE) to single-verse JSON files for use in the Collation Editor. This is a GUI version of my [TEI to JSON](https://github.com/d-flood/TEI-to-JSON) CLI.
4. Combine any number of single-verse collation files produced by the Collation Editor.
5. Reformat the collation file output of the Collation Editor for use with the [open-cbgm](https://github.com/jjmccollum/open-cbgm-standalone) and with Apparatus Explorer (a [desktop](https://github.com/d-flood/apparatus-explorer) and [web app](https://davidaflood.com/appex/demo/)) for visualization and editing.
6. Provide a simple way to view TEI XML transcriptions offline.
7. Provide an interface to conveniently edit the standalone collation editor project configuration. This is how one chooses which witnesses to collate, and which witness should be the basetext.
8. Export the TEI XML output of the ITSEE Collation Editor to a Microsoft Word DOCX file suitable for print publication.

## Installation

### Run on any platform with Python 3.11+
- Install the latest version of Python from https://www.python.org/
- Open a terminal and type in the following commands, typing Enter/Return after each.
   - On Windows: 
      - `pip install criticus`
      - `python -m criticus`
   - On MacOS: 
      - `pip3 install criticus`
      - `python3 -m criticus`

To update simply call:
   - Windows: `python -m pip install criticus --upgrade`
   - MacOS: `python3 -m pip install criticus --upgrade`

[**See the additional dependencies for the Collation Editor**](#collation-editor-prerequisites)

### Download and run the source code

This project is managed with `hatch`. If you are familiar, clone this repository and call `hatch shell`, then `python -m criticus`.

## Brief Tutorial
Please [contact](https://www.davidaflood.com/contact/), message me on Twitter, or fill out a GitHub issue for help using these tools and to report bugs. There are certain to be untested edge cases especially when converting TEI to JSON.

![screenshot of Criticus's main window](images/criticus_home.png)

### Plain Text to JSON Files
![screenshot of plain text to json window](images/txt2json.png)
The structure of the plain text (.txt) file is important. Criticus assumes:
- One verse (or other unit) per line
- Each line begins with the verse number
- There is no more than one whole chapter (or other complete unit) per file

1. Choose whether to convert all verses in a text file or to convert a range of verses (can be one verse, e.g. '3 to 3').
   - If "Range of verses" is selected, than a first ('from') and last ('to') verse must be entered. These input values must match verse numbers in the file, e.g. '7 to 12' *not* '1:7 to 1:12'.
   - If "All verses in file" is selected, then every verse will be converted to a different JSON file.
2. Choose whether to provide Criticus with the witness siglum or to have Criticus try and get this information from the input text file name.
   - If "Manual" is selected, then Criticus will use the user provided siglum and unit prefix.
     - The siglum is an identifier for the witness, e.g. 'P52'
     - The unit prefix is whatever needs to be added to the verse number to make it a full reference. This is normally the book and chapter (*with no spaces*), e.g. "Rom14", "Rom_14", "R14", "B06K14V". With this information, Criticus can create the correct directories and filenames for every verse to be converted.
   - If "Auto from file name" is selected, then Criticus will get the siglum and unit prefix from the file name *if the following convention is observed:* `<siglum>_<unit prefix>.txt`. That is, the filename should consist of the siglum, followed by an underscore, followed by the book and chapter. E.g., `P46_Rom14.txt`.
3. Choose the output directory by clicking "Browse" and navigating to the right folder.
   - If you have downloaded the Collation Editor, go to that folder and to `/collation/data/textrepo/json/`. This is where the Collation Editor expects the transcription files to be.
4. Finally, click "Convert File".
   - You will be prompted to select a plain text file.
   - Upon selecting it Criticus will attempt to convert the specified verses from the file and save them into the chosen output directory.
   - Criticus creates a folder in the output directory named after the siglum and then deposits the converted verses from that witness into the folder.
   - Criticus also creates and places a `metadata.json` file that must exist for the Collation Editor to work.
5. Caution. If you have many plain text transcription files in the same folder, and all adhere to the naming convention required by "auto from file name", then all chapter files can be converted at once by clicking "Convert Directory". 
   - This can easily result in the creation of hundreds or thousands of JSON files (which may be what you want!). So, make sure to test one of the files to ensure that its format is compatible and that the result is satisfactory before converting an entire folder.

### MarkdownTEI
This tool began as a [CLI](https://github.com/d-flood/MarkdownTEI) but here it is much more user-friendly as a GUI.
![MarkdownTEI tool screenshot of window](images/md2tei.png)
1. Choose how Criticus should format the converted transcription file. All options can be read by a computer but they differ most in human-readability.
   - "Do not add extra whitespace"
    ![example of no added whitespace](images/markdown_to_tei/no_extra_whitespace.png)
   - "Keep transcription lines"
    ![example of lines kept together](images/markdown_to_tei/keep_lines_example.png)
   - "Pretty Print"
    ![example of pretty printed xml](images/markdown_to_tei/pretty_print.png)
2. Select the Markdown (.md) file to be converted by clicking "Browse".
   - You will then be prompted to choose the converted file's location and name.

### TEI to JSON
This is the most difficult task. The TEI XML produced by the WYSIWYG OTE is very flexible and it is difficult to predict all of the possible combinations and nested encodings. Please tell me about bugs and edge cases.
![screenshot of TEI to JSON window](images/tei2json.png)
1. Select the TEI transcription file to be converted.
   - This can be the output of MarkdownTEI (most reliable) or the OTE.
2. Choose whether to convert all of the TEI transcription file or one verse.
   - Converting one verse is useful for correcting errors discovered in transcriptions during the collation process.
   - When working with TEI transcriptions, the verse reference format follows the IGNTP/INTF style, e.g. "B06K13V1" (B06 = Romans, K13 = chapter 13, V1 = verse 1).
3. Select the output folder where chapter folders and verse files are created and saved.
   - This should be located by going to the root folder of the Collation Editor and navigating to `/collation/data/textrepo/json/`.
4. Then click "Convert".

### Combine Collation Files
I've found that the Collation Editor fails to process more than a dozen verses at one time and it is best used one verse at a time. For analysis, these individual verse collation files should be combined into chapter and book length files.
![screenshot of Combine Collation Files window](images/combine_collations.png)
1. Navigate to the folder that contains all of the files you want to combine by clicking "Browse".
2. Enter a bit of text to filter all files to be combined.
   - E.g., entering "Rom13" would combine "Rom13.1.xml" and "Rom13.2.xml" but not "Rom14.1.xml" while entering "Rom" would result in combining them all.
3. Click "Combine XML Files". You will then be prompted to select the name and location of the combined file.

### Reformat Collation File
The output of the Collation Editor has several redundancies and lacks some useful features that are needed for the file to be used as input for the open-cbgm or the Apparatus Explorer.
![screenshot of Reformat Collation File window](images/reformat_collation.png)
1. Select an XML collation file that was combined during the previous step by clicking "Browse".
2. Click "Convert". You will then be prompted to save the reformatted file.

### View TEI Transcriptions
This is a simple way to view TEI transcriptions.
![screenshot of TEI Viewer list view](images/tei_viewer_list.png)
1. Select a folder that has one or more TEI transcriptions in it.
2. Click a transcription file from the list. ![Example transcription](images/tei_viewer.png)

### Configure Collation Editor
The WCE Collation Editor is configured by manually editing a config file located at `<root>/collation/data/project/default/config.json`. The Collation Editor is launched by a convenient start up script distributed with the Collation Editor (`startup.sh` for MacOS and `startup.bat` for Windows). This module of Criticus provides convenient access to the important values in the config file. This module also contains a shortcut for launching the Collation Editor.

#### Collation Editor Prerequisites:
1. Download [my fork of the collation editor](https://github.com/d-flood/standalone_collation_editor) instead of the one directly from ITSEE. My fork has a few critical fixes and a few nice-to-haves.
2. Install [Java](https://www.java.com/en/download/).
3. Optional but highly recommended: Install FireFox. The Collation Editor is only tested on FireFox. You are likely going to be problem solving issues with the Collation Editor, so removing the issue of cross-browser differences is going to save you time.

#### How to configure the Collation Editor with Criticus

![screenshot of the collation editor configuration file editor window](images/collation_config.png)

1. Browse for the config file. Begin in the root folder of the Collation Editor and go to `/collation/data/project/default/config.json`. Once it is selected, click "Load".
2. The "Project Title" is not important. Change it to whatever you like. It will be displayed in the Collation Editor.
3. The "Basetext" is whichever witness you want all others to be collated against. The basetext must be prepared as json files just like any other witness.
4. The "Witnesses" section tells the Collation Editor which witnesses should be included in the collation. This might change from verse to verse, but most likely it will not, since missing witnesses will be interpreted as lacunose for the entire verse.
5. Add a witness to the list by typing its siglum or witness ID into the field and pressing "Enter" or clicking "Add Witness".
6. Select one or more witnesses from the list, then click "Delete Selected" to remove these from the configuration file.
7. "Start Collation Editor" will attempt to locate the appropriate start up script and execute it. It will also attempt to open Firefox (by far the best for working in the Collation Editor) to the right port.

#### Export XML Collation File to DOCX (Microsoft Word)
![screenshot of the "Export Collation" page](images/export_collation.png)

This module will take a the TEI output of the Standalone Collation Editor and generate a Microsoft Word DOCX critical apparatus suitable for publishing.
