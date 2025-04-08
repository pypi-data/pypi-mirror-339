# SignalWire Prompt Object Model (POM)

A lightweight Python library for structured prompt management that helps organize and manipulate prompts for large language models.

## Installation

```bash
pip install signalwire-pom
```

## Usage

```python
from signalwire_pom import PromptObjectModel

# Create a new POM
pom = PromptObjectModel()

# Add sections with content
overview = pom.add_section("Overview", body="This is an overview of the project.")
overview.add_bullets(["Point 1", "Point 2", "Point 3"])

# Add subsections
details = overview.add_subsection("Details", body="More detailed information.")
details.add_bullets(["Detail 1", "Detail 2"])

# Generate markdown
markdown = pom.render_markdown()
print(markdown)

# Generate JSON representation
json_data = pom.to_json()
print(json_data)
```

## Features

- Create structured hierarchical prompts
- Add sections, subsections, body text, and bullet points
- Export to markdown or JSON
- Find sections by title

## License

MIT 