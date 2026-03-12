import json
import os
import uuid
from typing import List, Optional
from astro_predictor_app.app.schemas import Profile

class ProfileManager:
    def __init__(self, storage_file="profiles.json"):
        self.storage_file = storage_file
        self._ensure_storage()

    def _ensure_storage(self):
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump([], f)

    def _load_profiles(self) -> List[dict]:
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _save_profiles(self, profiles: List[dict]):
        with open(self.storage_file, 'w') as f:
            json.dump(profiles, f, indent=4)

    def create_profile(self, profile: Profile) -> Profile:
        profiles = self._load_profiles()
        profile.id = str(uuid.uuid4())
        profiles.append(profile.model_dump())
        self._save_profiles(profiles)
        return profile

    def get_all_profiles(self) -> List[Profile]:
        data = self._load_profiles()
        return [Profile(**item) for item in data]

    def get_profile(self, profile_id: str) -> Optional[Profile]:
        profiles = self.get_all_profiles()
        for p in profiles:
            if p.id == profile_id:
                return p
        return None

    def delete_profile(self, profile_id: str) -> bool:
        profiles = self._load_profiles()
        initial_len = len(profiles)
        profiles = [p for p in profiles if p.get('id') != profile_id]
        if len(profiles) < initial_len:
            self._save_profiles(profiles)
            return True
        return False

profile_manager = ProfileManager()
