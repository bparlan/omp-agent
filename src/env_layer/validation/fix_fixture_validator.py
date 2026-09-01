with open("fixture_validator.py", "r") as f:
    content = f.read()

# Fix the hardcoded M11 reference in line 75 (schema_dir construction)
content = content.replace(
    'schema_dir = self.fixtures_dir.parent / "milestones" / "M11"',
    'schema_dir = self.fixtures_dir.parent / "milestones" / milestone_id',
)

# Update docstring to be more generic
content = content.replace(
    "This module validates fixture contracts as specified in the M11S1 specification.",
    "This module validates fixture contracts as specified in milestone specifications.",
)

content = content.replace(
    "as specified in the M11S1 Environment Layer specification.",
    "as specified in Environment Layer specifications.",
)

with open("fixture_validator.py", "w") as f:
    f.write(content)

print("Fixed fixture_validator.py to be milestone-agnostic")
