# Augmented Reality Paint
Augmented Reality Paint is a program developed in the context of a university class. It replicates the basic functions 
of Microsoft Paint, with the added functionality of using the user's webcam to detect a color, be it the user's phone, 
the user's shirt, etc... as a pointer to paint the image. <br>
<TODO Add an image here>

## Program functionalities
The program consists of two main scripts: <br>
- color_segmenter.py - It is used to gather information from the user's webcam and create a mask. That mask will be used
as the pointer. The mask limits will be saved as a .json file; <br>
- ar_paint.py - Using the limits given by the previous script, transform the user's webcam into a pointer and painting 
in a white canvas. The user can also draw geometric shapes, draw with the mouse and play a coloring game!
