# audio_search
In this project, we are taking an audio input (keyword) from the user and trying to find this keyword in a audio book.

# Organization of the Repository

## Code

In order to be able to run the code follow the following steps:

1. Clone this repo to your local machine.

2. Create a new environment and use `requirements.txt` for dependencies.

3. Download an audio book from [Librevox Recordings](https://librivox.org/)

If you want to just test the code you can get [Alice's Advantures](http://www.archive.org/download/alices_adventures/alices_adventures_64kb_mp3.zip) which is relatively small in size.

4. Unzip the audio book and make sure that you put it under `data` directory and deleted the zipped file.

5. Run `main.py` and follow the directions. Note initial set-up might take approximately 15 minutes. after the first run, you can skip the set-up then you can start searching keywords. 

## Notebooks

Under the notebooks directory you will find the notebook `report` where we explained some technical aspects of the project. It will give you more in dept and step by step explanation of the projects. 

## Limitations and Further Research

- In this project, I used `speech_recognition` library where they provide public access to the Google Cloud Speech API. But their public service has the limitations. For example they don't process longer audio files. This is the reason that we divide the audio file into smaller chunks and then process them which extends the set-up time significantly. 

- When we match the keyword with the part of the audio we first converted everthing into text and then search match. More direct approach could be more efficient and quick. However, right now I don't how this can be achievable.

- Text matching is a very strict process and we tried to loosen this with `fuzzywuzzy` library. With this library we make sure that more flexible search is possible. However, ideally for such app we could add search from the context and relevancy. I think this can be achievable but I didn't experimented such feature yet. 

- Right now silent detection is mechanical (We give the minimum dFBS number and min_silence parameters by hand). Unfortunately, this leads that for each chapter, we should find the best parameters. It might be very interesting to see ML solving this problem. 
- Instead of keyword search for some book context search might be interesting.
