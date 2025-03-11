from car.autonomous.program import AutonomousDrivingProgram
from car.autonomous.program_alpha import AutnomousDrivingProgramAlpha

# think about making it singleton
class ProgramsRegistry:
    def __init__(self):
        self.programs: dict[str, AutonomousDrivingProgram] = {}

    def register_program(self, program: AutonomousDrivingProgram):
        if program.name not in self.programs:
            self.programs[program.name] = program

    def get_program(self, program_name: str) -> AutonomousDrivingProgram | None:
        if program_name not in self.programs:
            return None
        return self.programs[program_name]
    
programs_registry_instance = ProgramsRegistry()
programs_registry_instance.register_program(AutnomousDrivingProgramAlpha())