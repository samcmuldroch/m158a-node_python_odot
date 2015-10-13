# Sending OSC to Max

Disclaimer -- it's super late now, but I think a lot of you are interested in this, so here goes...

### IMPORTANT

You don't need to use these modules specifically. I tested the basics for you, but if you Google things like Node OSC or Python OSC you will find a lot of libraries. You can try out other ones if these don't work for you.

### MAX

Please open `OPEN_ME.maxpat` before doing anything else. 

Seriously, if I get one email about "What should I open in Max" Imma ban you 4 life. 

### Node

You need Node installed. That comes with `npm` -- which used to stand for Node Package Manager but I've read that it doesn't anymore... Computer Scientists of the future, please try to keep it real and stop with this nonsense. 

The `osc` module appears to be the best supported -- I have no way of testing on Windows at the moment. If it doesn't work, try to find another OSC library that does...

```
cd nodejs
npm install osc
node send.js
```

Note that I did copy/paste the example code that makes odot bundles sent out of Max print to a Node console -- see the code for `send.js` for that.

### Python

One thing I forgot about Python is how exciting it is to answer a students' question about a Python library without knowing if you need Python 2 or Python 3. COMPUTER SCIENTISTS, YO, LET'S TRY TO KEEP IT REAL!

Anyway, this pyOSC thing does the trick, though as you can see I just copy/pasted OSC.py in both python2 and python3 folders...

```
cd python/python3
python send.py
```

Read the readme in `/python` for stuffs.

### SUMMARY

Let's try to keep it real for reals.
