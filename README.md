simple-manga-visor
==================

A comic and manga viewer multiplatform made with kivy

Here is a simple app made with kivy 1.7 about one year ago.
The app is a image viewer created for viewing manga or comic.
It works on Linux (with python and kivy), MAC, Windows (with python and kivy or may be compiled), Android (compiled with python for android).

In the version 0.1.7 it reads only folders with images or zip like files (zip and cbz). I added a previous version (0.1.5) that reads rar too (with a library named rarfile.py, not created by me, but the rar files only work in linux with unrar installed), but its a unupdated version, so it has some issues (some files are readed in random order, because no sorting, it was fixed for the 0.1.7 version).

For android I give you a compiled version (debug-version), for testing. It have some issues with some images because the pygame (used for rendering images) is not well supported on android.

I dropped the development few weeks after I started, because I use "Perfect Viewer" Now, and I'm not motivated to follow the development. It is a experiments.
I realease this app under the MIT License, so you can use and read and learn freely. It's useful to learn some characteristics of kivy.

For run the application:
1.- First install kivy, in linux with pip (install python and pip before):
sudo pip install kivy

then go to the folder and run
python main.py

And that's all. You can fork this project (please) or use snippets from this app.

Ah! For the 0.1.5 you must download the rarfile.py from: https://github.com/markokr/rarfile as is said in the file. I don't own that library.
