ReadMe – PremiereSilenceCutter

This program uses your mouse, keyboard, and a series of updating screenshots to cut the silence out of clips in adobe premiere pro. This leaves the user the option to expand silences back where needed. I wrote this in a weekend so don't be suprised if it's buggier than code Adobe would send out.

In order for it to work:
	•For best results, add your footage to the beginning of the timeline (with no space ahead of it), and zoom in until it fills the entire timeline. Click off the track to deselect (no white box around clip) once done.
	•currently if the playhead is not at the very front when you start, the program won't work. Will fix that at some point.
	•You'll need to nest your footage so that it appears green (this also ensures there's no premade cuts), and make sure your Premiere color scheme is set to default - these colors are how it finds the timeline automatically
	•Make sure the tracks that you want to have cut are selected (meaning V1 and A1 are in blue boxes), and that the audio and video are linked (“linked selection” is on). Don’t try to do this on multiple layers of clips at the same time - if you need something cut along with your audio, first nest them.
	•Make sure your audio is showing as dual channel on the timeline
	•You’ll need to make sure your hotkeys are the same as this program expects
		q = ripple trim previous edit to playhead (I think this is the default)
		z = add edit (I think this is the default)
		h = hand tool (this is the default)
		v = selection tool (this is the default)
		= = zoom in (this is the default)
		- = zoom out (this is the default)
		n = go to sequence-clip start
	•Don’t use your mouse or keyboard while the program is running, unless it starts to malfunction or you want to stop it. Then quickly move your mouse to one of the corners of your screen and it should exit automatically. 

Recommendations:
	•I recommend you expand your audio track so the waveform is taller. It helps the program to see the audio with more precision
	•It’s probably easiest to play around with the variables it asks for and then write down what works well for you. If you understand Python, you could just hard-code your values in. They all do slightly different things:
		•Leftmost X, Rightmost X, Top Y, and Bottom Y are the coordinates of the sides of the display with premiere on it. This tells the computer where to look to intially find the timeline. For me, this was 0, 3440, 0, 1439, respectively. If you have one 1080p monitor, they should be 0, 1920, 0, 1080. If you have multiple monitors, this can change your mouse coordinates. If you're unsure, you can use the included executable "MouseTracker.exe" to read out the coordinates of your mouse in real time.
		•minSilence is the minimum amount of silence you want the program to cut out, in pixels. If you enter 5, and there’s a silence 10 pixels long, it won’t cut it. 20-60 was a good range for me. Enter numbers less than 1 at your own risk
		•gap is the amount of space you want before and after your “good” audio, in pixels. 5-15 was a good range for me. Enter numbers more or less at your own risk
		•Audio Level is how high up the audio track you want the program to search when looking for light and dark pixels (audio and silence, respectively), from 1-20. I had good results around 8-12. 10 is half-way up, 20 would be at the very top and would only leave huge peaks, 0 would leave everything untouched.
	•If Premiere is being slower than the program and screwing things up, try proxying your footage.
	•The code can be found on my github at https://github.com/CopperPanMan/Premiere-Pro-Silence-Cutter


