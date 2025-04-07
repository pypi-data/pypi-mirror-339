import typer
from pathlib import Path

app = typer.Typer(help="""
Initialize a new Quantum Machine with a predefined folder structure.

This command creates the following files:
- main.py
- project.json
- requirements.txt
- Dockerfile

Example:
    quantum init machine HelloWorld
""")

@app.command()
def machine(name: str):
    """
    Initialize a new Quantum Machine with the given name.
    
    This command creates a folder with basic boilerplate files:
    - main.py
    - project.json
    - requirements.txt
    - Dockerfile

    Example:
        quantum init machine HelloWorld
    """
    
    project_dir = Path(name)
    project_dir.mkdir(parents=True, exist_ok=True)

    (project_dir / "main.py").write_text(
        "from quantum.CoreEngine import CoreEngine\n\n"
        "class MyMachine(CoreEngine):\n"
        "    def receiving(self, input_data, dependent_machine_data, callback):\n"
        "        \"\"\"Receiving\n"
        "        :param input_data: Configure parameter values\n"
        "        :param dependent_machine_data: Dependant/Previous machine data values\n"
        "        :return: callback method to pass data and error into next step\n"
        "        \"\"\"\n"
        "        data = {}\n"
        "        error_list = []\n"
        "        try:\n"
        "            # Check Input data\n"
        "            self.machine_logger.info(f\'Input data :: {input_data}\')\n\n"
        "            # Check dependant data\n"
        "            self.machine_logger.info(f\'Dependent Machine Data :: {dependent_machine_data}\')\n\n"
        "            # Review Final data and Error list\n"
        "            data = self.get_final_data()\n"
        "            error_list = self.get_error_list()\n\n\n"
        "        except Exception as e:\n"
        "            err_msg = f\"This is error log {str(e)}\"\n"
        "            self.machine_logger.error(\"This is info log\")\n"
        "            error_list.append(err_msg)\n"
        "        finally:\n"
        "            self.machine_logger.info(\"This is info log\")\n"
        "            callback(data, error_list)\n\n"
        "    def pre_processing(self, callback):\n"
        "        \"\"\"Pre-Processing\n"
        "        :return: callback method to pass data and error into next step\n"
        "        \"\"\"\n"
        "        data = {}\n"
        "        error_list = []\n"
        "        try:\n"
        "            # Updated Final data and Error list\n"
        "            data = self.get_final_data()\n"
        "            error_list = self.get_error_list()\n\n\n"
        "        except Exception as e:\n"
        "            err_msg = f\"This is error log {str(e)}\"\n"
        "            self.machine_logger.error(\"This is info log\")\n"
        "            error_list.append(err_msg)\n"
        "        finally:\n"
        "            self.machine_logger.info(\"This is info log\")\n"
        "            callback(data, error_list)\n\n"
        "    def processing(self, callback):\n"
        "        \"\"\"Processing\n"
        "        :return: callback method to pass data and error into next step\n"
        "        \"\"\"\n"
        "        data = {}\n"
        "        error_list = []\n"
        "        try:\n"
        "            # Updated Final data and Error list\n"
        "            data = self.get_final_data()\n"
        "            error_list = self.get_error_list()\n\n\n"
        "        except Exception as e:\n"
        "            err_msg = f\"This is error log {str(e)}\"\n"
        "            self.machine_logger.error(\"This is info log\")\n"
        "            error_list.append(err_msg)\n"
        "        finally:\n"
        "            self.machine_logger.info(\"This is info log\")\n"
        "            callback(data, error_list)\n\n"
        "    def post_processing(self, callback):\n"
        "        \"\"\"Post-Processing\n"
        "        :return: callback method to pass data and error into next step\n"
        "        \"\"\"\n"
        "        data = {}\n"
        "        error_list = []\n"
        "        try:\n"
        "            # Updated Final data and Error list\n"
        "            data = self.get_final_data()\n"
        "            error_list = self.get_error_list()\n\n\n"
        "        except Exception as e:\n"
        "            err_msg = f\"This is error log {str(e)}\"\n"
        "            self.machine_logger.error(\"This is info log\")\n"
        "            error_list.append(err_msg)\n"
        "        finally:\n"
        "            self.machine_logger.info(\"This is info log\")\n"
        "            callback(data, error_list)\n\n"
        "    def packaging_shipping(self, callback):\n"
        "        \"\"\"Packaging & Shipping\n"
        "        :return: callback method to pass data and error into next step, This is final data to use into next machine\n"
        "        \"\"\"\n"
        "        data = {}\n"
        "        error_list = []\n"
        "        try:\n"
        "            # Updated Final data and Error list\n"
        "            data = self.get_final_data()\n"
        "            error_list = self.get_error_list()\n\n\n"
        "        except Exception as e:\n"
        "            err_msg = f\"This is error log {str(e)}\"\n"
        "            self.machine_logger.error(\"This is info log\")\n"
        "            error_list.append(err_msg)\n"
        "        finally:\n"
        "            self.machine_logger.info(\"This is info log\")\n"
        "            callback(data, error_list)\n\n"
        "if __name__ == '__main__':\n"
        "    # Create a machine instance and start the process\n"
        "    machine = MyMachine()\n"
        "    machine.start()\n"
    )

    (project_dir / "project.json").write_text(
        '{\n  "name": "' + name + '",\n'
        '  "version": "1.0.0",\n'
        '  "title": "' + name + '",\n'
        '  "author": "",\n'
        '  "license": "",\n'
        '  "short_description": "",\n'
        '  "long_description": "",\n'
        '  "specification": {\n'
        '    "input": "",\n'
        '    "output": ""\n'
        '  },\n'
        '  "infrastructure": {\n'
        '    "os": "",\n'
        '    "storage": "",\n'
        '    "memory": "",\n'
        '    "cpu": "",\n'
        '    "cloud": ""\n'
        '  },\n'
        '  "parameters": [],\n'
        '  "faq": [\n'
        '    {\n'
        '      "question": "",\n'
        '      "answer": ""\n'
        '    },\n'
        '    {\n'
        '      "question": "",\n'
        '      "answer": ""\n'
        '    },\n'
        '    {\n'
        '      "question": "",\n'
        '      "answer": ""\n'
        '    }\n'
        '  ]\n'
        '}'
    )

    (project_dir / "requirements.txt").write_text(
        "git+https://github.com/QuantumDatalytica-LLC/quantum-core-engine.git@main"
    )

    (project_dir / "Dockerfile").write_text(
        "FROM python:3.10-buster\n\n"
        "# Creating Application Source Code Directory\n"
        "# RUN mkdir -p /usr/src/app\n\n"
        "# Setting Home Directory for containers\n"
        "WORKDIR /usr/src/app/\n\n"
        "# Installing python dependencies\n"
        "COPY requirements.txt .\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n\n"
        "# Copying src code to Container\n"
        "COPY . .\n\n"
        "# Execute code under Container\n"
        "CMD [\"python\", \"main.py\"]\n"
    )

    tests_dir = project_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "test_main.py").write_text(
        "import unittest\n"
        "from main import MyMachine\n\n"
        "class TestMyMachine(unittest.TestCase):\n"
        "    def test_run(self):\n"
        "        machine = MyMachine()\n"
        "        #machine.set_input('input_data', 'quantum')\n"
        "        machine.start()\n"
        "        #self.assertEqual(machine.get_output('result'), 'QUANTUM')\n\n"
        "if __name__ == '__main__':\n"
        "    unittest.main()\n"
    )

    typer.secho(f"✅ Quantum Machine '{name}' scaffolded!", fg=typer.colors.GREEN)