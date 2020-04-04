import subprocess
def get_submodule_commit_date():
    out = subprocess.run(["git", "--no-pager", "show", "-s", "--format=%ci"], cwd="COVID-19", capture_output=True)
    return out.stdout.decode('utf-8').replace('\n','')

