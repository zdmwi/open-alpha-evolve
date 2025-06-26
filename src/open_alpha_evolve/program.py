import re
import itertools
from pathlib import Path

class Program:
    _id_generator = itertools.count()
    id: int
    file_path: Path
    content: str
    language: str

    # evolve block markers
    evolve_start_marker: str
    evolve_end_marker: str

    parent_id: int | None = None

    def __init__(self, file_path: Path | str, *, evolve_start_marker: str = "# EVOLVE-BLOCK-START", evolve_end_marker: str = "# EVOLVE-BLOCK-END") -> None:
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        self.id = next(Program._id_generator)
        self.file_path = file_path
        self.content = file_path.read_text()
        self.language = file_path.suffix
        self.evolve_start_marker = evolve_start_marker
        self.evolve_end_marker = evolve_end_marker

    def get_evolve_blocks(self) -> list[str]:
        pattern = re.compile(rf"{self.evolve_start_marker}\s+(.*?)\s+{self.evolve_end_marker}", re.DOTALL)
        matches = pattern.findall(self.content)
        if matches:
            return matches
        
        return []
    
    def _get_markdown_syntax(self) -> str:
        if self.language == ".py":
            return "python"
        
        return ""

    def to_markdown(self) -> str:
        return f"```{self._get_markdown_syntax()}\n{self.content}\n```".strip()

    def __str__(self) -> str:
        return self.to_markdown()
