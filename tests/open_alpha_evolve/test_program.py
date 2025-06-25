import pytest
import tempfile
from pathlib import Path
from open_alpha_evolve.program import Program

class TestProgram:
    @pytest.fixture(scope="class")
    def test_file(self):
        test_file = tempfile.NamedTemporaryFile(suffix=".py")
        test_file.write(b"print('Hello World')")
        test_file.flush()

        yield test_file
        # cleanup the file after the test
        test_file.close()
    
    def test_program_init(self, test_file: tempfile.NamedTemporaryFile):
        assert Program(test_file.name) is not None
        assert Program(Path(test_file.name)) is not None

    def test_program_str(self, test_file: tempfile.NamedTemporaryFile):
        program = Program(test_file.name)
        assert str(program) == program.to_markdown()
        
    def test_program_to_markdown(self, test_file: tempfile.NamedTemporaryFile):
        program = Program(test_file.name)
        assert program.to_markdown() == """
        ```python
        print('Hello World')
        ```
        """.strip()

    def test_program_id_is_unique(self, test_file: tempfile.NamedTemporaryFile):
        program1 = Program(test_file.name)
        program2 = Program(test_file.name)
        assert program1.id != program2.id