import toml

class Settings:
    def __init__(self):
        self.config = {}

    def load_config(self, path):
        try:
            self.config = toml.load(path)
            print("Loaded configuration:", self.config)  # Debug output
        except Exception as e:
            print(f"Error loading configuration: {e}")
            self.config = {}

# Test the configuration loading
settings = Settings()
settings.load_config('config.toml')

# Print config structure
print("Settings config:", settings.config)

# Debugging: Accessing specific keys
try:
    settings_section = settings.config.get("settings", {})
    tts_section = settings_section.get("tts", {})
    tiktok_sessionid = tts_section.get("tiktok_sessionid", "")
    voice_choice = tts_section.get("voice_choice", "")

    print("Settings Section:", settings_section)
    print("TTS Section:", tts_section)
    print("TikTok Session ID:", tiktok_sessionid)
    print("Voice Choice:", voice_choice)
except KeyError as e:
    print(f"Missing expected configuration key: {e}")
