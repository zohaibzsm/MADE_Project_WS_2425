
import os

class Test():
    def __init__(self, kaggle_username):
        self.kaggle_username = kaggle_username
        
    def test_pipeline(self):
        num_of_output_files = 2
        for i in range(num_of_output_files):
            try:
                assert os.path.exists(f"../data/{self.kaggle_username}{i}.sqlite"), f"Failed to verify output file {i+1}"
            except:
                print("Error in verifying output file", i+1, "\n\n")
            finally:
                print("\n")
                os.remove(f"../data/{self.kaggle_username}{i}.sqlite")
                print("\n")
