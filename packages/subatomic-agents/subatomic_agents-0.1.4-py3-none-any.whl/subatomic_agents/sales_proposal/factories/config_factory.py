from abc import ABC, abstractmethod
from helpers.files_and_folders import build_config_with_multithreading, create_random_folder, remove_folder

class ConfigFactory(ABC):
    @abstractmethod
    def create_config(self) -> dict:
        pass

class SalesProposalConfigFactory(ConfigFactory):
    def __init__(self, prompt_config_keys: list):
        self.prompt_config_keys = prompt_config_keys

    def create_config(self) -> dict:
        config = build_config_with_multithreading(self.prompt_config_keys)

        config['configurable']['vector_store_folder_name'] = create_random_folder()
        config['configurable']['meeting_transcript_vector_store_folder_name'] = create_random_folder()

        return config

    def cleanup(self, config: dict):
        remove_folder(config['configurable']['vector_store_folder_name'])
        remove_folder(config['configurable']['meeting_transcript_vector_store_folder_name'])
