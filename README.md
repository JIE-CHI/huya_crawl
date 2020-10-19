# Huya scraper
This repository contains my python implementation of a simple huya-livestream scraper. You can also find a Chinese version of README [here](./README_CH.md)
## Installation
Please make sure the following modules are installed:

selenium is used to automate the web browser (Firefox in this case)
```bash
pip install selenium 
```
From some reason, we are intereseted to know the number of kills in each game, so we use tesseract to recognise the text from the video.

```bash
sudo apt-get install tesseract-ocr
```
As we are working with Chinese characters, we also need to download the language specific data and move it to /usr/share/tesseract-ocr/4.00/tessdata/
```bash
wget https://github.com/tesseract-ocr/tessdata/blob/master/chi_sim.traineddata ./
sudo mv chi_sim.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
pip install pytesseract
```

## To do
* gift retrieval
* plot function
* auto login
