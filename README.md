# Blemish removal tool

This project was part of the official openCV computer vision I course (https://opencv.org/courses)

The goal is to remove skin irregularities. The approach is to analyze neighboring patches 
of where the blemish is. Then find the one with the least noise by analyzing the frequency domain
and copy it onto the blemish by using seamless cloning.