import click
import subprocess

@click.command()
def start():
    """Start your vm"""
    subprocess.run([
        "gcloud", "compute", "instances", "start",
        "--zone", "australia-southeast2-c", "lewagon-data-eng-vm-sprngbk"
    ])

@click.command()
def stop():
    """Stop your vm"""
    subprocess.run([
        "gcloud", "compute", "instances", "stop",
        "--zone", "australia-southeast2-c", "lewagon-data-eng-vm-sprngbk"
    ])

@click.command()
def connect():
    """Connect to your vm in vscode inside your ~/code/<user.lower_github_nickname>/folder """
    # code --folder-uri vscode-remote://ssh-remote+username@<vm ip>/<path inside vm>
    subprocess.run([
        "cursor", "--folder-uri", "vscode-remote://ssh-remote+adora@dataeng/home/adora/code/sprngbk/data-engineering-challenges"
    ])
