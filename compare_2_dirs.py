import unittest
import os

DIR1 = "/home/biraj/bids_parsing/outputs/working/pipeline_cpac_anat/anna_raw/sub-PA001/ses-V1W1"
DIR2 = "/home/biraj/bids_parsing/dataset/anna/raw/sub-PA001/ses-V1W1"

class DirectoryComparisonTest(unittest.TestCase):
    def list_files(self, directory):
        """Recursively list all files in a directory."""
        for root, _, files in os.walk(directory):
            for file in files:
                yield os.path.join(root, file)

    def compare_file_contents(self, file1, file2):
        """Compare the contents of two files in binary mode."""
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            return f1.read() == f2.read()

    def test_matching_file_names(self):
        """Test if both directories have the same set of files."""
        files1 = list(self.list_files(DIR1))
        files2 = list(self.list_files(DIR2))

        rel_files1 = {os.path.relpath(f, DIR1) for f in files1}
        rel_files2 = {os.path.relpath(f, DIR2) for f in files2}

        self.assertSetEqual(rel_files1, rel_files2, "Directories do not have the same files")

    def test_matching_file_contents(self):
        """Test if the contents of matching files are the same."""
        files1 = list(self.list_files(DIR1))
        rel_files1 = {os.path.relpath(f, DIR1) for f in files1}

        for file_rel_path in rel_files1:
            file1 = os.path.join(DIR1, file_rel_path)
            file2 = os.path.join(DIR2, file_rel_path)

            with self.subTest(file=file_rel_path):
                self.assertTrue(self.compare_file_contents(file1, file2), f"File contents do not match for {file_rel_path}")

if __name__ == '__main__':
    unittest.main()