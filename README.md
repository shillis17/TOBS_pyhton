# OBS Web Socket Python Wrapper

## Getting Started

You must add a config.toml unless you edit obsController yourself to add Host, Port, and password from OBS.

The .toml should look like this 

```toml
[connection]
host = "localhost"
port = 4455
password = "obs server password"
```
located in your home directory (C:\Users{you_user_name}\config.toml)

All sources in OBS must be in groups\folders for this program to see them otherwise the program will skip the source.

Make sure you enable the websocket in OBS>tools>WebSocketServerSettngs to allow the program to make changes to OBS.

## Usage

The code is OOP and currently has 1 class ObsController, to use the function in the class you must first create a class object:

```python
obsctl = ObsController() # Makes controller object
```

From here you can use any of the methods the class owns, a summary of each method is avalible after this section.

This following code creates the class object then uses the object to find the sources and scenes of an OBS setup.

*Example*
```python
#initiating the class
obsctl = ObsController() # Makes controller object

#using the class
print(obsctl.get_version()) # checks version of OBS and web socket
print(f"Scenes found: {obsctl.get_scenes()}")
print(f"Sources found: {obsctl.get_sources()}")
print(f"Audio Sources found: {obsctl.get_input_names()}")
```

## Methods


### get_version

This method takes no arguments.  

This method returns a string.

This method finds and reports the current version of OBS and the websocket server in a human readable string.

*Example*

```python
obsctl = ObsController()
obsctl.get_version()
```

Might show this in the terminal:

```text
OBS version: 31.1.2
obs-websocket version: 5.6.2
```

---

### get_scenes

This method takes no arguments.  

This method returns a list of strings.

This method gets all scene names from the current OBS profile and returns them as a Python list.

*Example*

```python
obsctl = ObsController()
scenes = obsctl.get_scenes()
print(scenes)
```

Might show this in the terminal:

```text
['Stream', 'BRB', 'Starting Soon', 'Just Chatting']
```

---

### get_current_scene

This method takes no arguments.  

This method returns a string.

This method gets the name of the current program (live) scene in OBS.

*Example*

```python
obsctl = ObsController()
current = obsctl.get_current_scene()
print(current)
```

Might show this in the terminal:

```text
Stream
```

---

### change_scene

This method takes one argument, `name` (string).  

This method returns a boolean.

This method switches the current program scene to the given scene name if it exists. It returns `True` if the scene was changed, or `False` if the scene name was not found.

*Example*

```python
obsctl = ObsController()
success = obsctl.change_scene("BRB")
print(success)
```

Might show this in the terminal:

```text
True
```

If `"BRB"` does not exist, it would show:

```text
False
```

---

### get_sources

This method takes no arguments.  

This method returns a list of strings.

This method finds all visual sources that are children of groups (folders) in the current program scene and returns their names as a list. Top-level items that are not groups are ignored.

*Example*

```python
obsctl = ObsController()
sources = obsctl.get_sources()
print(sources)
```

Might show this in the terminal:

```text
['Web Cam', 'Game Capture', 'Cat Jam', 'Overlay', 'Chat Box']
```

---

### toggle_source

This method takes one argument, `source_name` (string).  

This method returns a boolean.

This method looks for a source with the given name inside any group in the current program scene and toggles its visibility (enabled/disabled). It returns `True` if the source was found and toggled, or `False` if it was not found.

*Example*

```python
obsctl = ObsController()
toggled = obsctl.toggle_source("Cat Jam")
print(toggled)
```

Might show this in the terminal:

```text
True
```

If no child source named `"Cat Jam"` exists in any group, it would show:

```text
False
```

---

### get_inputs

This method takes no arguments.  

This method returns a list of dictionaries.

This method retrieves all OBS inputs (things like Mic, Music, Game Capture, Desktop, etc.) and returns the raw info for each as a dictionary containing fields such as `inputName`, `inputKind`, and `inputKindCaps`.

*Example*

```python
obsctl = ObsController()
inputs = obsctl.get_inputs()
for info in inputs:
    print(info)
```

Might show this in the terminal:

```text
{'inputName': 'Mic', 'inputKind': 'wasapi_input_capture', 'inputKindCaps': 130, ...}
{'inputName': 'Music', 'inputKind': 'wasapi_output_capture', 'inputKindCaps': 642, ...}
{'inputName': 'Game Capture', 'inputKind': 'game_capture', 'inputKindCaps': 32907, ...}
...
```

---

### get_input_names

This method takes no arguments.  

This method returns a list of strings.

This method is a convenience wrapper over `get_inputs`. It returns just the `inputName` for each input in OBS.

*Example*

```python
obsctl = ObsController()
names = obsctl.get_input_names()
print(names)
```

Might show this in the terminal:

```text
['Mic', 'Music', 'Game Capture', 'Web Cam', 'Desktop', 'Cat Jam']
```

---

### get_input_info

This method takes one argument, `input_name` (string).  

This method returns a dictionary or `None`.

This method searches the current list of inputs for one whose `inputName` matches `input_name`. If found, it returns that input’s info dictionary. If no input is found, it returns `None`.

*Example*

```python
obsctl = ObsController()
info = obsctl.get_input_info("Mic")
print(info)
```

Might show this in the terminal:

```text
{'inputName': 'Mic', 'inputKind': 'wasapi_input_capture', 'inputKindCaps': 130, ...}
```

If the input does not exist:

```python
print(obsctl.get_input_info("Not A Real Input"))
```

Would show:

```text
None
```

---

### is_audio_input

This method takes one argument, `input_name` (string).  

This method returns a boolean.

This method checks whether a given input supports audio, using the `inputKindCaps` bitfield from OBS. It returns `True` if the input supports audio, and `False` if it does not or if the input name does not exist.

*Example*

```python
obsctl = ObsController()
print(obsctl.is_audio_input("Mic"))
print(obsctl.is_audio_input("Game Capture"))
print(obsctl.is_audio_input("Some Image"))
```

Might show this in the terminal:

```text
True
True
False
```

---

### mute_input

This method takes one argument, `input_name` (string).  

This method returns a boolean.

This method mutes the given input if it exists and supports audio. It returns `True` if the input was successfully muted, or `False` if the input name does not exist or is not audio-capable.

*Example*

```python
obsctl = ObsController()
muted = obsctl.mute_input("Mic")
print(muted)
```

Might show this in the terminal:

```text
True
```

If `"Mic"` does not exist or has no audio:

```text
False
```

---

### unmute_input

This method takes one argument, `input_name` (string).  

This method returns a boolean.

This method unmutes the given input if it exists and supports audio. It returns `True` if the input was successfully unmuted, or `False` if the input name does not exist or is not audio-capable.

*Example*

```python
obsctl = ObsController()
unmuted = obsctl.unmute_input("Music")
print(unmuted)
```

Might show this in the terminal:

```text
True
```

If `"Music"` does not exist or has no audio:

```text
False
```

---

### toggle_input_mute

This method takes one argument, `input_name` (string).  

This method returns a boolean.

This method toggles the mute state of the given input if it exists and supports audio. It returns `True` if the input was found and toggled, or `False` otherwise.

*Example*

```python
obsctl = ObsController()
toggled = obsctl.toggle_input_mute("Desktop")
print(toggled)
```

Might show this in the terminal:

```text
True
```

If `"Desktop"` does not exist or has no audio:

```text
False
```

---

### mute_all_audio

This method takes one optional argument, `except_inputs` (list of strings), which defaults to `None`.  

This method returns nothing (`None`).

This method mutes all audio-capable inputs in OBS. If `except_inputs` is provided, any inputs whose names are in that list will be skipped and left unchanged.

*Example*

```python
obsctl = ObsController()

# Mute every audio-capable input:
obsctl.mute_all_audio()

# Mute all audio-capable inputs except Mic:
obsctl.mute_all_audio(except_inputs=["Mic"])
```

There is no direct terminal output unless you add your own `print` calls.

---

### unmute_all_audio

This method takes one optional argument, `only_inputs` (list of strings), which defaults to `None`.  

This method returns nothing (`None`).

This method unmutes audio-capable inputs. If `only_inputs` is `None`, it unmutes all audio-capable inputs. If `only_inputs` is a list, it unmutes only those named inputs (and ignores non-audio inputs).

*Example*

```python
obsctl = ObsController()

# Unmute all audio-capable inputs:
obsctl.unmute_all_audio()

# Unmute only Mic and Music:
obsctl.unmute_all_audio(only_inputs=["Mic", "Music"])
```

Again, there is no direct terminal output unless you print something yourself.

---

### mute_all_but

This method takes one argument, `keep_inputs` (list of strings).  

This method returns nothing (`None`).

This method mutes all audio-capable inputs except the ones specified in `keep_inputs`. Inputs in `keep_inputs` are explicitly unmuted so they remain on, and all other audio-capable inputs are muted.

*Example*

```python
obsctl = ObsController()

# Keep Mic unmuted, mute all other audio-capable inputs:
obsctl.mute_all_but(["Mic"])
```

No terminal output is produced by default.

---

### unmute_only

This method takes one argument, `inputs` (list of strings).  

This method returns nothing (`None`).

This method unmutes only the given audio-capable inputs and mutes all other audio-capable inputs. It is effectively the inverse of `mute_all_but`.

*Example*

```python
obsctl = ObsController()

# Only keep Mic and Music unmuted:
obsctl.unmute_only(["Mic", "Music"])
```

No terminal output is produced by default.

---

### start_record

This method takes no arguments.  

This method returns nothing (`None`).

This method sends a request to OBS to start recording, as if you pressed the “Start Recording” button. OBS must be configured correctly for recording or this may fail.

*Example*

```python
obsctl = ObsController()
obsctl.start_record()
```

You would see recording start in OBS (no automatic terminal output).

---

### stop_record

This method takes no arguments.  

This method returns nothing (`None`).

This method sends a request to OBS to stop recording, as if you pressed the “Stop Recording” button.

*Example*

```python
obsctl = ObsController()
obsctl.stop_record()
```

You would see recording stop in OBS (no automatic terminal output).

---

### start_stream

This method takes no arguments.  

This method returns nothing (`None`).

This method sends a request to OBS to start streaming, as if you pressed the “Start Streaming” button. OBS must have valid streaming settings configured.

*Example*

```python
obsctl = ObsController()
obsctl.start_stream()
```

You would see streaming start in OBS (no automatic terminal output).

---

### stop_stream

This method takes no arguments. 

This method returns nothing (`None`).

This method sends a request to OBS to stop streaming, as if you pressed the “Stop Streaming” button.

*Example*

```python
obsctl = ObsController()
obsctl.stop_stream()
```

You would see recording stop in OBS (no automatic terminal output).

