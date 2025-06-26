import pytest
import tempfile

from open_alpha_evolve.program import Program
from open_alpha_evolve.program_database import ProgramDatabase, SamplingStrategy

class TestProgramDatabase:
    @pytest.fixture(scope="class")
    def test_file(self):
        test_file = tempfile.NamedTemporaryFile(suffix=".py")
        test_file.write(b"print('Hello World')")
        test_file.flush()

        yield test_file
        # cleanup the file after the test
        test_file.close()

    def test_sample_returns_program_and_list_of_programs(self, test_file: tempfile.NamedTemporaryFile):
        database = ProgramDatabase()

        program1 = Program(test_file.name)
        program2 = Program(test_file.name)
        program3 = Program(test_file.name)

        database.add(program1)
        database.add(program2)
        database.add(program3)

        parent_program, inspirations = database.sample()

        assert isinstance(parent_program, Program)
        assert isinstance(inspirations, list)
        assert all(isinstance(program, Program) for program in inspirations)

    def test_get_by_id_returns_program(self, test_file: tempfile.NamedTemporaryFile):
        database = ProgramDatabase()

        program = Program(test_file.name)
        program_id = database.add(program)

        assert database.get(program_id) == program

    def test_add_saves_program(self, test_file: tempfile.NamedTemporaryFile):
        database = ProgramDatabase()
        
        program = Program(test_file.name)
        program_id = database.add(program)

        assert database.get(program_id) == program

    def test_sample_parent_randomly_returns_program(self, test_file: tempfile.NamedTemporaryFile):
        database = ProgramDatabase()
        
        program = Program(test_file.name)
        program_id = database.add(program)

        parent_program = database._sample_parent(sampling_strategy=SamplingStrategy.RANDOM)
        assert parent_program.id == program_id

    def test_sample_inspirations_randomly_returns_list_of_n_programs(self, test_file: tempfile.NamedTemporaryFile):
        database = ProgramDatabase()
        
        program1 = Program(test_file.name)
        program2 = Program(test_file.name)
        program3 = Program(test_file.name)

        database.add(program1)
        database.add(program2)
        database.add(program3)

        n = 2
        inspirations = database._sample_inspirations(program1, n=n)
        assert len(inspirations) == n
        assert all(isinstance(program, Program) for program in inspirations)
    
    def test_sample_inspirations_randomly_returns_all_programs_if_n_is_greater_than_number_of_programs(self, test_file: tempfile.NamedTemporaryFile):
        database = ProgramDatabase()
        
        program1 = Program(test_file.name)
        program2 = Program(test_file.name)
        program3 = Program(test_file.name)

        database.add(program1)
        database.add(program2)
        database.add(program3)

        n = 4
        inspirations = database._sample_inspirations(program1, n=n, sampling_strategy=SamplingStrategy.RANDOM)
        assert len(inspirations) == len(database._programs) - 1 # parent program should not be included
        assert all(isinstance(program, Program) for program in inspirations)    

    def test_sample_inspirations_randomly_does_not_include_parent_program(self, test_file: tempfile.NamedTemporaryFile):
        database = ProgramDatabase()
        
        program1 = Program(test_file.name)
        program2 = Program(test_file.name)
        program3 = Program(test_file.name)

        database.add(program1)
        database.add(program2)
        database.add(program3)

        parent_program = database._sample_parent(sampling_strategy=SamplingStrategy.RANDOM)
        inspirations = database._sample_inspirations(parent_program, n=3, sampling_strategy=SamplingStrategy.RANDOM)
        assert parent_program not in inspirations   

    def test_sample_inspirations_randomly_returns_unique_programs(self, test_file: tempfile.NamedTemporaryFile):
        database = ProgramDatabase()
        
        program1 = Program(test_file.name)
        program2 = Program(test_file.name)
        program3 = Program(test_file.name)

        database.add(program1)
        database.add(program2)
        database.add(program3)

        parent_program = database._sample_parent(sampling_strategy=SamplingStrategy.RANDOM)
        inspirations = database._sample_inspirations(parent_program, n=3, sampling_strategy=SamplingStrategy.RANDOM)
        assert len(inspirations) == len(set(inspirations))