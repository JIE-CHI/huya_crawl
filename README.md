# Huya scraper
This repository contains my python implementation of a simple huya-livestream scraper. You can also find a Chinese version of README [here](./README_CH.md)
## Installation
Please make sure the following modules are installed:

Selenium is used to automate the web browser (Firefox in this case)
```bash
pip install selenium 
```
If you get error message as follows when running the webdriver function, it is probable that your geckodriver is not setup correctly.
```
WebDriverException: Message: 'geckodriver' executable needs to be in PATH.
```
The easiest way to install it is with sudo privileges, but you can also try to add the path to your bashrc file or parse the path to the webdriver explicity if you don't have it.  
```bash
#download the latest geckodriver from the webpage
wget https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-linux64.tar.gz ./
tar -xvzf geckodriver*
sudo cp ./geckodriver-v0.27.0-linux64/geckodriver /usr/bin/
```

From some reason, we are intereseted to know the number of kills in each game, so we need to use OCR tools to recognise the text from the video. We tried [pytesseract](https://github.com/madmaze/pytesseract) and [cnocr](https://github.com/breezedeus/cnocr) here, you can install either of them as follows. (cnor works better in our case.)

```bash
sudo apt-get install tesseract-ocr

pip install cnocr
```
As we are working with Chinese characters, we also need to download the language specific data. Cnocr downloads it automatically the first time you use it, but for pytesseract you need to download it yourself and move it to /usr/share/tesseract-ocr/4.00/tessdata/
```bash
wget https://github.com/tesseract-ocr/tessdata/blob/master/chi_sim.traineddata ./
sudo mv chi_sim.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
pip install pytesseract
```
## Example

## To do
* more intelligent gift-msg
* plot function
* add example
* train my own OCR model