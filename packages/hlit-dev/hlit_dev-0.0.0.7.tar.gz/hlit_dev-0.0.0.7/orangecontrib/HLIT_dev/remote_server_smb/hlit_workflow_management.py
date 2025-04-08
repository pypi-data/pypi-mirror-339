import sys
import json
import os
import psutil
from pathlib import Path
if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils import MetManagement,subprocess_management
else:
    from orangecontrib.AAIT.utils import MetManagement,subprocess_management



def load_json_and_check_json_agregate(fichier_json, montab = []):
    try:
        with open(fichier_json, 'r', encoding='utf-8') as file:
            data = json.load(file)


        required_fields = {"name", "ows_file", "html_file", "description"}

        for item in data:
            if not required_fields.issubset(item.keys()):
                return 1  # Erreur si un champ manque
            montab.append(item)

        return 0  # Tout est bon
    except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
        print(f"Erreur: {e}")
        return 1  # Erreur lors de la lecture du fichier


def read_config_ows_html_file_as_dict(out_put_tab=[]):
    del out_put_tab[:]
    folder_path = Path(MetManagement.get_path_linkHTMLWorkflow())
    le_tab=[]
    for file_path in folder_path.glob('*.json'):
        if 0!=load_json_and_check_json_agregate(file_path,le_tab):
            print("error reading ",file_path)
            return 1
    if len(le_tab)==0:
        print("error no json loaded from", folder_path)
        return 1
    # crate absolute path
    for idx,_ in enumerate(le_tab):
        le_tab[idx]['html_file']=MetManagement.TransfromStorePathToPath(le_tab[idx]['html_file'])
        le_tab[idx]['ows_file']=MetManagement.TransfromStorePathToPath(le_tab[idx]['ows_file'])

    # on verifie que l on a pas deux fois le meme nom
    seen_names = set()
    for item in le_tab:
        if item["name"] in seen_names:
            print("error in json several use of :"+str(item["name"]))
            return 1
        seen_names.add(item["name"])
    for element in le_tab:
        out_put_tab.append(element)
    return 0


def open_local_html(list_config_html_ows,name):
    if os.name != "nt":
        print("only available on windows")
        return 1
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    a_lancer=""
    try:
        for element in list_config_html_ows:
            if element["name"]==name:
                a_lancer='"'+edge_path+'" "'+element['html_file']+'"'
    except Exception as e:
        print(e)
        return 1
    if a_lancer=="":
        print("aucun html trouvé")
        return 1
    result,PID=subprocess_management.execute_command(a_lancer,hidden=True)
    return result


def write_PID_to_file(name: str, number: int) -> int:
    """
    Writes an integer to a file named "name.txt" inside a folder named "name".
    Handles exceptions related to file operations.
    Returns 0 if successful, 1 if an error occurs.
    """
    try:
        # Create directory if it does not exist

        dirname=MetManagement.get_api_local_folder_admin()
        os.makedirs(dirname, exist_ok=True)
        # Define file path
        file_path = os.path.join(dirname, f"{name}.txt")

        # Write the integer to the file
        with open(file_path, 'w') as file:
            file.write(str(number))

        return 0  # Success
    except Exception as e:
        print(f"Error: {e}")
        return 1  # Error


def check_file_and_process(name: str) -> int:
    """
    Checks if "name.txt" exists in the "name" directory.
    If it exists, reads its content as an integer.
    If a process with that integer as PID exists, returns 2.
    If not, deletes the file and returns the integer.
    If the file does not exist return 0
    If an error occurs, returns 1.
    """
    try:
        dirname=MetManagement.get_api_local_folder_admin()
        # Define file path
        file_path = os.path.join(dirname, f"{name}.txt")

        # Check if file exists
        if not os.path.isfile(file_path):
            return 0
        print(file_path+ " existe")
        # Read the integer from the file
        with open(file_path, 'r') as file:
            content = file.read().strip()

        if not content.isdigit():
            return 1

        process_id = int(content)
        print(process_id)
        # Check if a process with this PID exists
        if process_id in [p.pid for p in psutil.process_iter()]:
            print("process deja en existant")
            return 2

        # If no such process exists, delete the file
        os.remove(file_path)

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def start_workflow(list_config_html_ows,name, with_terminal=True,gui=True):
    """Launch a workflow using the command line and store the process information.
    retun 1 -> erro
    return 0 ->> ok
    retrun 2 -> workflow alrwready used"""
    workflow_path=""
    try:
        for element in list_config_html_ows:
            if element["name"]==name:
                workflow_path=element['ows_file']
    except Exception as e:
        print(e)
        return 1
    if workflow_path=="":
        print("no ows file found in json config")
        return 1
    if not os.path.isfile(workflow_path):
        print(workflow_path+" doesn t existe")
        return 1
    res=check_file_and_process(name)
    if res==1:
        return 1
    if res==2:
        return 2
    workflow_directory=Path(os.path.dirname(workflow_path))
    # clean file to aviod erreor
    for file in workflow_directory.glob("*.ows.swp.*"):
        file.unlink()

    # 2. Construct the command to run the workflow
    python_path = Path(sys.executable)
    workflow_path=str(workflow_path)
    workflow_path=workflow_path.replace('/','\\')

    command = str(python_path)+ ' -m Orange.canvas '+ workflow_path
    PID=None
    try:
        if with_terminal:
            PID=subprocess_management.open_terminal(command, with_qt=gui)
        else:
            PID=subprocess_management.open_hide_terminal(command, with_qt=gui)
    except Exception as e:
        print(e)
        return 1

    print("le PID",PID)
    return write_PID_to_file(name,PID)




if __name__ == "__main__":
    list_config_html_ows=[]
    if 0!= read_config_ows_html_file_as_dict(list_config_html_ows):
        print("an error occurs")
        exit(1)
    print(list_config_html_ows)
    # if 0!=open_local_html(list_config_html_ows,"nom simpathique2"):
    #     print("an error occurs")
    #     exit(1)

    pid = os.getpid()
    print(f"Le PID du processus Python en cours est : {pid}")
    if None!=start_workflow(list_config_html_ows,"nom simpathique2", with_terminal=True,gui=True):
        print("ok")
