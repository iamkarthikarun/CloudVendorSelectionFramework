from pathlib import Path

class Config:
    """
    Configuration class to store all configurable parameters for the project.
    """

    def __init__(self):
        self.output_dir = "Folder/" #Replace with output files directory
        self.num_experts = 4  # Number of experts
        self.num_alternatives = 7  # Number of alternatives
        self.num_attributes = 8  # Number of attributes

        self.qrofn = [
            (0.98, 0.01), (0.9, 0.6), (0.8, 0.65), (0.75, 0.6),
            (0.5, 0.5), (0.6, 0.7), (0.7, 0.8), (0.6, 0.9), (0.01, 0.98)
        ]

        self.output_file = Path(self.output_dir+"opfile.txt")
        self.image_dir = Path(self.output_dir+"images/")
        
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self.image_dir.mkdir(parents=True, exist_ok=True)
