# InstantMD

Instant MD is a Investigation, Medication and Chief complaint recognition application using NLP

### Installation

### Setting up

##### Clone the repository 

```
$ git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
$ cd REPO_NAME
```

##### Initialize a virtual environment

Windows:
```
$ python -m venv venv
$ venv\Scripts\activate.bat
```

Unix/MacOS:
```
$ python -m venv venv
$ source venv/bin/activate
```
##### Install the dependencies

```
$ pip install -r requirements.txt
```

## Running the app

```
$ python app.py
```

## Problem Statement
### Abstract
Being able to have machines understand unstructured textual content already plays a big part nowadays in our life. NLP can contribute largely to the advancement of medical science. NLP is used to extract information from free text narratives written by a variety of healthcare providers. Here we approach natural language processing algorithm where we

* Evaluate the free text and compare it with the dataset of NLP Dictionary.
* Annotated the important textual content from the text like Medication, Investigation (Pathology, Radiology), Chief Complaint.
* After Segregation the highlighted data should automatically enter the flow of EMR.

### Problem Definition
To develop a solution, the first step is to understand the problem. Develop an NLP module to identify the keywords related to a patient's investigation, medication and chief complaint from a free text in the text box. Highlight the extracted content and feed them as input in EMR’s Chief complaint, Investigation and Medication module.

