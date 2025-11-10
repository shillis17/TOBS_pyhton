import obsws_python as obs


class ObsController:
    """
    High-level convenience wrapper around obsws_python.ReqClient.

    This class assumes:
      - OBS is running
      - obs-websocket is enabled and reachable (config.toml or manual settings)
      - All visual sources you care about live inside groups (folders),
        e.g. 'Audio', 'Video', 'Chaos'.
    """

    def __init__(self) -> None:
        """
        Initialize the OBS websocket client.

        Raises:
            SystemExit: if a connection to OBS cannot be established.
        """
        try:
            self.client = obs.ReqClient()
        except Exception as e:
            print("ERROR: Unable to log into OBS, check config.toml has proper details.")
            print("Reason:", e)
            raise SystemExit()
        
    def _find_source_in_groups(self, source_name: str) -> tuple[str | None, int | None]:
        """
        Find a source that lives inside a group in the current scene.

        Returns (group_name, scene_item_id) or (None, None) if not found.
        """
        scene_name = self.get_current_scene()
        items = self.client.get_scene_item_list(scene_name)

        for item in items.scene_items: # type: ignore
            group_name = item["sourceName"]

            try:
                group_items = self.client.get_group_scene_item_list(group_name)
            except Exception:
                continue

            for child in group_items.scene_items: # type: ignore
                if child["sourceName"] == source_name:
                    return group_name, child["sceneItemId"]

        return None, None

    # Info
    def get_version(self) -> str:
        """
        Get a human-readable string describing the OBS and obs-websocket versions.
        """
        v = self.client.get_version()
        return (
            f"OBS version: {v.obs_version}\n" # type: ignore
            f"obs-websocket version: {v.obs_web_socket_version}" # type: ignore
        )
    


    # Scenes
    def get_scenes(self) -> list[str]:
        """
        Return a list of all scene names in the current OBS profile.
        """
        resp = self.client.get_scene_list()
        return [scene["sceneName"] for scene in resp.scenes]  # type: ignore

    def get_current_scene(self) -> str:
        """
        Get the name of the current program (live) scene.
        """
        resp = self.client.get_current_program_scene()
        return resp.current_program_scene_name  # type: ignore

    def change_scene(self, name: str) -> bool:
        """
        Switch the current program scene, if it exists.

        Returns:
            bool: True if the scene was changed, False otherwise.
        """
        scenes = self.get_scenes()
        if name in scenes:
            self.client.set_current_program_scene(name)
            return True
        else:
            return False
        


    # Visual Sources (must be in groups)
    def get_sources(self) -> list[str]:
        """
        Get a list of source names that live inside groups in the current scene.

        This method:
          - enumerates top-level scene items in the current program scene
          - treats each top-level item as a potential group
          - for items that are groups, returns the names of their children

        Top-level items that are *not* groups are ignored.
        """
        scene_name = self.get_current_scene()
        items = self.client.get_scene_item_list(scene_name)

        names: list[str] = []

        for item in items.scene_items: # type: ignore
            group_name = item["sourceName"]
            try:
                group_items = self.client.get_group_scene_item_list(group_name)
            except Exception:
                # Not a group
                continue

            for child in group_items.scene_items: # type: ignore
                names.append(child["sourceName"])

        return names

    def toggle_source(self, source_name: str) -> bool:
        """
        Toggle visibility of a source that lives inside a group.
        """
        container, scene_item_id = self._find_source_in_groups(source_name)
        if scene_item_id is None:
            return False

        info = self.client.get_scene_item_enabled(container, scene_item_id)
        new_state = not info.scene_item_enabled # type: ignore

        self.client.set_scene_item_enabled(container, scene_item_id, new_state)
        return True
    


    # Inputs / Audio (using inputKindCaps)
    def get_inputs(self) -> list[dict]:
        """
        Get the list of all inputs (sources) in OBS.

        Returns:
            list[dict]: Each dict typically has 'inputName', 'inputKind',
                        'inputKindCaps', etc.
        """
        resp = self.client.get_input_list()
        return list(resp.inputs) # type: ignore

    def get_input_names(self) -> list[str]:
        """
        Get the list of all input names.
        """
        return [i["inputName"] for i in self.get_inputs()]

    def get_input_info(self, input_name: str) -> dict | None:
        """
        Look up the info dict for a given input name.

        Returns:
            dict or None if not found.
        """
        for info in self.get_inputs():
            if info["inputName"] == input_name:
                return info
        return None

    def is_audio_input(self, input_name: str) -> bool:
        """
        Check whether an input supports audio, using inputKindCaps.

        According to the obs-websocket protocol, the InputKindCapability
        flag for "supports audio" is bit 1 (value 2). So we check:

            bool(inputKindCaps & 2)
        """
        info = self.get_input_info(input_name)
        if info is None:
            return False

        caps = info.get("inputKindCaps", 0)
        SUPPORTS_AUDIO = 1 << 1  # == 2
        return bool(caps & SUPPORTS_AUDIO)

    def mute_input(self, input_name: str) -> bool:
        """
        Mute a specific input by name.

        Returns:
            bool: True if muted, False if the input name doesn't exist
                  or doesn't support audio.
        """
        if not self.is_audio_input(input_name):
            return False

        self.client.set_input_mute(input_name, True)
        return True

    def unmute_input(self, input_name: str) -> bool:
        """
        Unmute a specific input by name.

        Returns:
            bool: True if unmuted, False if the input name doesn't exist
                  or doesn't support audio.
        """
        if not self.is_audio_input(input_name):
            return False

        self.client.set_input_mute(input_name, False)
        return True

    def toggle_input_mute(self, input_name: str) -> bool:
        """
        Toggle the mute state of a specific input by name.

        Returns:
            bool: True if toggled, False if the input name doesn't exist
                  or doesn't support audio.
        """
        if not self.is_audio_input(input_name):
            return False

        self.client.toggle_input_mute(input_name)
        return True

    def mute_all_audio(self, except_inputs: list[str] | None = None) -> None:
        """
        Mute all audio-capable inputs, optionally skipping some by name.

        Args:
            except_inputs: list of input names that should NOT be muted.
        """
        skip = set(except_inputs or [])
        for info in self.get_inputs():
            name = info["inputName"]
            if name in skip:
                continue
            if self.is_audio_input(name):
                self.mute_input(name)

    def unmute_all_audio(self, only_inputs: list[str] | None = None) -> None:
        """
        Unmute audio-capable inputs.

        Args:
            only_inputs:
                - If None: unmute ALL audio-capable inputs.
                - If list: unmute ONLY those audio-capable inputs whose names are in the list.
        """
        targets: list[str]
        if only_inputs is None:
            targets = [i["inputName"] for i in self.get_inputs() if self.is_audio_input(i["inputName"])]
        else:
            targets = [name for name in only_inputs if self.is_audio_input(name)]

        for name in targets:
            self.unmute_input(name)

    def mute_all_but(self, keep_inputs: list[str]) -> None:
        """
        Mute all audio-capable inputs except those in keep_inputs.

        Any kept inputs will be ensured unmuted.
        """
        keep = set(keep_inputs)
        for info in self.get_inputs():
            name = info["inputName"]
            if not self.is_audio_input(name):
                continue
            if name in keep:
                self.unmute_input(name)
            else:
                self.mute_input(name)

    def unmute_only(self, inputs: list[str]) -> None:
        """
        Unmute only the given audio-capable inputs; mute all other audio-capable ones.

        Args:
            inputs: list of input names to keep unmuted.
        """
        keep = set(inputs)
        for info in self.get_inputs():
            name = info["inputName"]
            if not self.is_audio_input(name):
                continue
            if name in keep:
                self.unmute_input(name)
            else:
                self.mute_input(name)



    # Stream / Record
    def start_record(self) -> None:
        """Start OBS recording."""
        self.client.start_record()

    def stop_record(self) -> None:
        """Stop OBS recording."""
        self.client.stop_record()

    def start_stream(self) -> None:
        """Start OBS streaming."""
        self.client.start_stream()

    def stop_stream(self) -> None:
        """Stop OBS streaming."""
        self.client.stop_stream()