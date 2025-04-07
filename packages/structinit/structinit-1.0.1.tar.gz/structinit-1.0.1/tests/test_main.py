# tests/test_main.py

import os
import shutil
import json
import subprocess
import tempfile
# from projinit.Main import parse_structure, create_structure

def test_create_structure(tmp_path):
    sample_md = tmp_path / "structure.md"
    sample_md.write_text
    (
    """
    Projinit/
    ├── projinit/
    │   ├── __init__.py
    │   └── main.py
    ├── tests/
    │   └── test_main.py
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    ├── requirements.txt
    └── setup.py
    """
    )
    
    # structure = parse_structure(str(sample_md))
    # create_structure(structure)

    assert (tmp_path / "projinit").is_dir()
    assert (tmp_path / "projinit" / "__init__.py").exists()
    assert (tmp_path / "tests" / "test_main.py").exists()
    assert (tmp_path / ".gitignore").exists()
    assert (tmp_path / "LICENSE").exists()

def test_main():
    """
    Test the main.py script by providing input dynamically and storing output in the tests folder.
    """
    # Create a temporary directory inside the tests folder
    tests_dir = os.path.dirname(__file__)  # Get the path to the tests folder
    with tempfile.TemporaryDirectory(dir=tests_dir) as tmp_dir:
        # Create a temporary .md file
        md_path = os.path.join(tmp_dir, "structure.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(
                """
                Projinit/
                ├── projinit/
                │   ├── __init__.py
                │   └── main.py
                ├── tests/
                │   └── test_main.py
                ├── .gitignore
                ├── LICENSE
                ├── README.md
                ├── requirements.txt
                └── setup.py
                """
            )

        # Create a temporary test input JSON file
        test_input = {
            "project_name": "Projinit",
            "md_path": md_path,
            "language": "Python",
            "init_git": True,
            "add_license": True,
            "skip_name": False,
        }
        test_input_path = os.path.join(tmp_dir, "test_input.json")
        with open(test_input_path, "w", encoding="utf-8") as f:
            json.dump(test_input, f)

        # Set the TEST_INPUT_PATH environment variable
        os.environ["TEST_INPUT_PATH"] = test_input_path

        # Run main.py in test mode
        result = subprocess.run(
            ["python", "d:\\Structure\\ML\\Project Structure\\projinit\\projinit\\main.py", "--test"],
            capture_output=True,
            text=True,
        )

        # Check the output
        print(result.stdout)
        assert "✅ Project structure created successfully." in result.stdout

        # Verify the structure was created inside the temporary directory
        assert os.path.isdir(os.path.join(tmp_dir, "Projinit"))
        assert os.path.isfile(os.path.join(tmp_dir, "Projinit", "projinit", "__init__.py"))
        assert os.path.isfile(os.path.join(tmp_dir, "Projinit", "projinit", "main.py"))
        assert os.path.isfile(os.path.join(tmp_dir, "Projinit", "tests", "test_main.py"))
        assert os.path.isfile(os.path.join(tmp_dir, "Projinit", ".gitignore"))
        assert os.path.isfile(os.path.join(tmp_dir, "Projinit", "LICENSE"))

        print(f"✅ Test output stored in: {tmp_dir}")


if __name__ == "__main__":
    test_main()
