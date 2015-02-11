#simple-manga-visor

A comic and manga viewer multiplatform made with kivy 1.7 and python 2.7

#This is the unstable version, it don't work properly

## I will copy the readme from master:

##Description

Here is a simple app made with kivy 1.7 about one year ago.

The app is a image viewer created for viewing manga or comic.

It works on Linux (with python and kivy), MAC, Windows (with python and kivy or may be compiled), Android (compiled with python for android).

Originaly the proyect was in google code, you can see at: 

https://code.google.com/p/simple-manga-and-comic-visor

##Run

* First install kivy, in linux with pip (install python and pip before):

```
sudo pip install kivy
```

* then go to the folder and run

```
python main.py
```

##Tested

* It's tested on linux, windows and android 2.3.3 in 2013.

###Known Bugs

* The stable version only works with "/" (root) path. In Unix it's fine, but in Windows, it only will work for C:\
There are a unstable version that I tried to fix, but it doesn't open anything. see unstable branch.

* On android some images doesn't open and make the app to close unexpectedly. Probably because pygame on android is dropped.

##Acknowledgements

* Thanks to the documentation of kivy.

* And the snippets that I copied from the forums and google.

##All

And that's all. You can fork this project or use snippets from this app, it's licensed in MIT license, see the LICENCE file.
