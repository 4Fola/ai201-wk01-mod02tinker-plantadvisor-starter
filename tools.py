import json
import os
from datetime import datetime
from config import DATA_PATH

# Plant database and seasonal data are loaded once at module load.
# This mirrors how a real service would cache its data source in memory.
with open(os.path.join(DATA_PATH, "plants.json"), encoding="utf-8") as f:
    _plant_db = json.load(f)

with open(os.path.join(DATA_PATH, "seasons.json"), encoding="utf-8") as f:
    _season_data = json.load(f)

# Maps calendar months to seasons for auto-detection.
_MONTH_TO_SEASON = {
    12: "winter", 1: "winter", 2: "winter",
    3: "spring", 4: "spring", 5: "spring",
    6: "summer", 7: "summer", 8: "summer",
    9: "fall",  10: "fall",  11: "fall",
}


def lookup_plant(plant_name: str) -> dict:
    """
    Search the plant database for a plant by name and return its care information.

    TODO — Milestone 1:

    Right now this always returns a "not found" response. Your job is to implement
    the search logic so it can actually find plants.

    The plant database (_plant_db) is a dict where keys are lowercase slugs like
    "pothos", "snake_plant", "fiddle_leaf_fig". Each plant also has a "display_name"
    field and an "aliases" list with common alternate names.

    Your implementation should handle all three:
      1. Direct key match (e.g., "pothos" → finds "pothos")
      2. Display name match (e.g., "Pothos" → finds "pothos")
      3. Alias match (e.g., "devil's ivy" → finds "pothos")

    All matching should be case-insensitive. Strip whitespace from the input.

    Return format when found:
      {"found": True, "plant": <the full plant dict>}

    Return format when not found:
      {"found": False, "name": <original input>, "message": <helpful string>}

    The message in the not-found case matters — the agent will use it to decide
    what to tell the user. Your spec has a dedicated field for this — think about
    what information would actually be helpful to the agent.

    Before writing code, complete the lookup_plant section of specs/tool-functions-spec.md.
    """
    # Milestone 1: Input Normalization
    # Handling empty/invalid inputs and normalize casing and whitespace
    if not plant_name or not isinstance(plant_name, str):
        return {
            "found": False,
            "name": plant_name,
            "message": "Please provide a valid plant name to look up.",
        }
    normalized_input = plant_name.strip().lower()

    # Milestone 1: Search Order & Alias Matching
    # Iterates through _plant_db evaluating slugs, displa_name, and aliases
    for slug, plant_info in _plant_db.items():
        #1. Direct slug key match (e.g., 'snake_plant')
        if slug.lower() == normalized_input:
            return {"found": True, "plant": plant_info}

        #2. Display name match (e.g., 'Snake Plant')
        display_name = plant_info.get("display_name", "").lower()
        if display_name == normalized_input:
            return {"found": True, "plant": plant_info}

        #3. Alias list match (e.g., 'sansevieria', "mother-in-law's tongue")
        aliases = [alias.lower() for alias in plant_info.get("aliases", [])]
        if normalized_input in aliases:
            return{"found": True, "plant": plant_info}

    # Milestone 1 & 3: Not-Found Message Design & Graceful Degradation
    # Clear inofrmative message enabling the LLM to degrade gracefully
    return {
        "found" : False,
        "name": plant_name,
        "message": (
            f" No plant matching '{plant_name}' was found in the database. "
            "Acknowledge that this plant is missing from the database, offer general care tips"
            "if applicable based on plat type, and do not invent specific care instructions."
        ),
    }


def get_seasonal_conditions(season: str | None = None) -> dict:
    """
    Return current seasonal care context for houseplants.

    If season is provided and valid, returns that season's data.
    If season is None (or invalid), auto-detects from the current calendar month.

    Pre-implemented — read through this and the spec before working on lookup_plant().
    """
    VALID_SEASONS = {"spring", "summer", "fall", "winter"}

    if season and season.lower() in VALID_SEASONS:
        # Caller specified a valid season — use it directly
        season_key = season.lower()
        detected = False
    else:
        # Auto-detect from the current month using the _MONTH_TO_SEASON mapping
        current_month = datetime.now().month
        season_key = _MONTH_TO_SEASON[current_month]
        detected = True

    # Copy the season dict so we don't mutate the cached data
    result = dict(_season_data[season_key])
    result["detected_season"] = detected
    return result

    # Optional Challenge: Third Tool Implementation
    def get_plant_list() -> dict:
        """
        This returns a summuary list of all houseplants in the local database.
        Enables recommendations based on beginner-friendliness / difficulty level.
        """

    catalog = []
    for slug, info in _plant_db.items():
        catalog.appemd({
            "slug": slug,
            "display_name": info.get("display_name", slug),
            "care_level": info.get("care_level", info.get("difficulty", "easy")),
            "light_summary": info.get("light", "Inddirect light")
        })

    return {
        "count": len(catalog),
        "plants": catalog
    }
