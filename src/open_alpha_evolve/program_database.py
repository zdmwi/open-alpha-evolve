import enum
import random
from open_alpha_evolve.program import Program


class SamplingStrategy(enum.Enum):
    RANDOM = "random"
    

class ProgramDatabase:
    _programs: dict[str, Program]
    
    def __init__(self) -> None:
        self._programs = {}

    def sample(self) -> tuple[Program, list[Program]]:
        parent = self._sample_parent()
        inspirations = self._sample_inspirations(parent)

        return parent, inspirations

    def _sample_parent(self, *, sampling_strategy: SamplingStrategy = SamplingStrategy.RANDOM) -> Program:
        if not self._programs:
            raise ValueError("No programs in database")

        match sampling_strategy:
            case SamplingStrategy.RANDOM:
                return random.choice(list(self._programs.values()))

    def _sample_inspirations(self, parent: Program, n: int = 3, *, sampling_strategy: SamplingStrategy = SamplingStrategy.RANDOM) -> list[Program]:
        if not self._programs:
            raise ValueError("No programs in database")

        match sampling_strategy:
            case SamplingStrategy.RANDOM:
                programs = list(self._programs.values())
                programs.remove(parent)

                if n > len(programs):
                    return programs

                inspirations = []
                while len(inspirations) < n:
                    inspiration = random.choice(programs)
                    if inspiration not in inspirations:
                        inspirations.append(inspiration)

                return inspirations

    def add(self, program: Program) -> str:
        self._programs[program.id] = program
        return program.id

    def get(self, program_id: int) -> Program | None:
        return self._programs.get(program_id)