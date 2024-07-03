import unittest
import os
import filecmp

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

    def test_compare_directories(self):
        dir1 = DIR1
        dir2 = DIR2

        files1 = list(self.list_files(dir1))
        files2 = list(self.list_files(dir2))

        # Convert file paths to relative paths for comparison
        rel_files1 = {os.path.relpath(f, dir1) for f in files1}
        rel_files2 = {os.path.relpath(f, dir2) for f in files2}

        # Check if both directories have the same set of files
        self.assertSetEqual(rel_files1, rel_files2, "Directories do not have the same files")

        matched_files_count = 0
        # For each file in directory 1, compare its contents with the corresponding file in directory 2
        for file_rel_path in rel_files1:
            file1 = os.path.join(dir1, file_rel_path)
            file2 = os.path.join(dir2, file_rel_path)
            if self.compare_file_contents(file1, file2):
                matched_files_count += 1
            else:
                print(f"File contents do not match for {file_rel_path}")

        print(f"Number of matched files: {matched_files_count}")
        self.assertEqual(len(rel_files1), matched_files_count, "Not all files matched in content")

if __name__ == '__main__':
    unittest.main()