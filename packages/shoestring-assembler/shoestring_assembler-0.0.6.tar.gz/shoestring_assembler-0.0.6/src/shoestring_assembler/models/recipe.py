from pathlib import Path

import json
import sys
import hashlib
from pathlib import Path
from shoestring_assembler.display import Display
from shoestring_assembler.schemas import RecipeSchema, SchemaValidationError

try:
    from pathlib import UnsupportedOperation
except ImportError:
    UnsupportedOperation = NotImplementedError

try:
    import tomllib as toml
except ImportError:
    import tomli as toml

import yaml

class Recipe:
    def __init__(self, recipe_filepath,recipe,hash):
        self._filepath_provided = recipe_filepath
        self._recipe = recipe
        self._hash = hash

    #
    # Methods for loading and validation
    #

    @classmethod
    def load(cls,recipe_filepath):
        recipe_location = Path.resolve(Path(recipe_filepath))
        Display.print_header("Get Recipe")
        try:
            # check file type is supported and find parser
            ext = recipe_location.suffix

            if ext == ".yml" or ext == ".yaml":
                parser = cls._parse_yaml
            elif ext == ".toml":
                parser = cls._parse_toml
            elif ext == ".json":
                parser = cls._parse_json
            else:
                Display.print_error(
                    f"Recipe format unsupported - expects a json, yaml or toml file"
                )
                sys.exit(255)

            # parse file
            with Display.open_file(
                recipe_location, "rb", description="Loading Recipe..."
            ) as file:
                recipe_content = parser(file)
                file.seek(0)  # reset file
                hash_fn = hashlib.sha256()
                hash_fn.update(file.read())
                recipe_hash = hash_fn.hexdigest()

            recipe_obj = cls(recipe_filepath, recipe_content, recipe_hash)
            recipe_obj.validate()

        except FileNotFoundError:
            Display.print_error(
                f"Unable to find recipe file. Expected to find it at: {recipe_location}"
            )
            sys.exit(255)

        Display.print_complete("Recipe loaded")
        return recipe_obj

    @classmethod
    def _parse_json(self, file):
        return json.load(file)

    @classmethod
    def _parse_yaml(self, file):
        return yaml.safe_load(file)

    @classmethod
    def _parse_toml(self, file):
        return toml.load(file)

    def validate(self):
        Display.print_log("Validating Recipe")

        try:
            RecipeSchema.validate(self._recipe)
        except SchemaValidationError as v_err:
            Display.print_error(
                f"Recipe error at {v_err.json_path}:\n\n{v_err.message}"
            )
            Display.print_error(
                "Recipe is not valid -- unable to start the solution -- please correct the issues flagged above and try again."
            )
            sys.exit(255)

        Display.print_log("Recipe valid")

    #
    # Methods for recipe access
    #

    @property
    def sources(self) -> dict:
        return self._recipe["source"]

    @property
    def service_modules(self) -> dict:
        return self._recipe.get("service_module",{})
    @property
    def infrastructure(self) -> dict:
        return self._recipe.get("infrastructure", {})

    @property
    def solution(self) -> dict:
        return self._recipe["solution"]
