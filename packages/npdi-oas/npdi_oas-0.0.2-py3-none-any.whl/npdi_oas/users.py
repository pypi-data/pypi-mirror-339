from pydantic import BaseModel, Field
from typing import Any
from pagination import PaginatedResponse


class BaseUser(BaseModel):
    first_name: str | None = Field(None, description="The first name of the user.")
    last_name: str | None = Field(None, description="The last name of the user.")
    primary_email: str | None = Field(None, description="The primary email address of the user. This is the email address used for login.")
    contact_info: dict[str, Any] | None = Field(None, description="Contact information for the user.")
    website: str | None = Field(None, description="The user's website.")
    location: dict[str, Any] | None = None
    employment: dict[str, Any] | None = Field(None, description="Employment information for the user.")
    bio: str | None = Field(None, description="A short biography of the user.")
    profile_image: str | None = Field(None, description="URL to the user's profile image.")
    social_media: dict[str, Any] | None = Field(None, description="The user's social media profiles.")


class UpdateUser(BaseUser, BaseModel):
    first_name: str | None = Field(None, description="The first name of the user.")
    last_name: str | None = Field(None, description="The last name of the user.")
    primary_email: str | None = Field(None, description="The primary email address of the user. This is the email address used for login.")
    contact_info: dict[str, Any] | None = Field(None, description="Contact information for the user.")
    website: str | None = Field(None, description="The user's website.")
    location: dict[str, Any] | None = None
    employment: dict[str, Any] | None = Field(None, description="Employment information for the user.")
    bio: str | None = Field(None, description="A short biography of the user.")
    profile_image: str | None = Field(None, description="URL to the user's profile image.")
    social_media: dict[str, Any] | None = Field(None, description="The user's social media profiles.")


class User(BaseUser, BaseModel):
    first_name: str | None = Field(None, description="The first name of the user.")
    last_name: str | None = Field(None, description="The last name of the user.")
    primary_email: str | None = Field(None, description="The primary email address of the user. This is the email address used for login.")
    contact_info: dict[str, Any] | None = Field(None, description="Contact information for the user.")
    website: str | None = Field(None, description="The user's website.")
    location: dict[str, Any] | None = None
    employment: dict[str, Any] | None = Field(None, description="Employment information for the user.")
    bio: str | None = Field(None, description="A short biography of the user.")
    profile_image: str | None = Field(None, description="URL to the user's profile image.")
    social_media: dict[str, Any] | None = Field(None, description="The user's social media profiles.")
    uid: str | None = Field(None, description="Unique identifier for the user.")


class UserList(PaginatedResponse, BaseModel):
    results: list[User] | None = None


