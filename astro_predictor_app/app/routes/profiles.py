from fastapi import APIRouter, HTTPException, Path
from typing import List
from astro_predictor_app.app.schemas import Profile
from astro_predictor_app.app.services.profile_manager import profile_manager

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.get("/", response_model=List[Profile])
def get_profiles():
    """List all saved profiles"""
    return profile_manager.get_all_profiles()

@router.post("/", response_model=Profile)
def create_profile(profile: Profile):
    """Save a new profile"""
    return profile_manager.create_profile(profile)

@router.get("/{profile_id}", response_model=Profile)
def get_profile(profile_id: str = Path(..., title="The ID of the profile to get")):
    """Get a specific profile"""
    profile = profile_manager.get_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.delete("/{profile_id}")
def delete_profile(profile_id: str = Path(..., title="The ID of the profile to delete")):
    """Delete a profile"""
    success = profile_manager.delete_profile(profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted successfully"}
