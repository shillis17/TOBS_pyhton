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

Get a human-readable string describing the OBS and obs-websocket versions.

*Example*
```python
obsctl = ObsController()
obsctl.get_version()
```

Would show this in the terminal

```text
OBS version: xx.x.x
obs-websocket version: x.x.x
```
### get_scenes
### get_current_scene
### change_scene
### get_sources
### toggle_source
### get_inputs
### get_input_names
### get_input_info
### is_audio_input
### mute_input
### unmute_input
### toggle_input_mute
### mute_all_audio
### unmute_all_audio
### mute_all_but
### unmute_only
### start_record
### stop_record
### start_stream
### stop_stream
