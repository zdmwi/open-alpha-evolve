import itertools
from pathlib import Path

class Program:
    _id_generator = itertools.count()
    id: int
    file_path: Path
    content: str
    language: str

    parent_id: int | None = None

    def __init__(self, file_path: Path | str) -> None:
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        self.id = next(Program._id_generator)
        self.file_path = file_path
        self.content = file_path.read_text()
        self.language = file_path.suffix
    
    def _get_markdown_syntax(self) -> str:
        if self.language == ".py":
            return "python"
        
        return ""

    def to_markdown(self) -> str:
        return f"""
        ```{self._get_markdown_syntax()}
        {self.content}
        ```
        """.strip()

    def __str__(self) -> str:
        return self.to_markdown()
