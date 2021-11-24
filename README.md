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

## How to use
To test this program you need to follow this steps:
<ol>
<li> Open a terminal and go to the directory where you created the python files. </li>
<li> Run the program "color_segmenter.py" to choose limits (b, g, r) for the color that you want to detect. After you chose the color, press "w" to save the current limits. Use the following command to run this program: </li>
<code>./color_segmenter.py</code>
<li> Now, run the program "ar_paint.py" to start drawing. For the basic functionality write the following command on the terminal:</li>
<code>./ar_paint.py -j limits.json</code> <br>
- While you are running the program, you can interact with the program by pressing the keys shown in the next table:<br>

| Key         | Action                                          |
| ----------- | -----------                                     |
| b           | Start painting with the color blue              |
| g           | Start painting with the color green             |
| r           | Start painting with the color red               |
| +           | Increase the pencil size                        |
| -           | Decrease the pencil size                        |
| c           | Clear the window                                |
| w           | Save the current image on a PNG file            |
| m           | Start painting with the mouse                   |
| n           | Start painting with the mask                    |
| v           | Switch to draw on the white canvas/real frame   |
| s           | Draw a rectangle                                |
| o           | Draw a circle                                   |
| q           | Exit the program                                |

<li> You can also use two advanced functionalities by using input arguments.<br>
If you want to use the advanced functionality 1, write the following command: <br>
<code>./ar_paint.py -j limits.json -usp</code> </li>
<li> If you want to use the advanced functionality 4, write the following command: <br>
<code>./ar_paint.py -j limits.json -unp</code> </li>
</ol>

## Functionalities
### Basic Functionality
When the user runs the program in this functionality, it's possible to paint with the mask or with the mouse.<br><br>
In this mode the user can:
<ul>
<li>Choose the color that it's used to draw (blue, green or red);</li> 
<li>Increase or decrease the pencil size;</li>
<li>Clear the window;</li>
<li>Save the current image as a PNG file;</li>
<li>Switch between the white canvas/real frame;</li>
<li>Draw rectangles or circles.</li>
</ul>

#### Default
The default mode is painting with the mouse, in color blue and with pencil size 5.

### Advanced Functionality 1
#### Shake Prevention
Sometimes the color detection might fail and the object detected with the biggest area can oscillate around the area of the window. When this happens the lines are drawn across all the window. <br><br>
To prevent this from happening, you may use this functionality.
### Advanced Functionality 4
#### Numeric Painting
On this functionality, the program divides the window in zones. The user must paint the zones accordingly to the colors atributed to the zones (The colors are atributed randomly by the program). <br><br>
In the end, the user can make an evaluation of the drawing, by pressing the space bar.

## Contributors
<ul>
<li>Lucas Rodrigues Dal'Col</li>
<li>Manuel Alberto Silva Gomes</li>
<li>Emanuel Krzysztoń</li>
<li>João Pedro Tira Picos Costa Nunes</li>
</ul>