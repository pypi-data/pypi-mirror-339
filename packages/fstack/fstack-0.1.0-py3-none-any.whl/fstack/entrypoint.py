#!/usr/bin/env python3

import click
import subprocess
from pipeline.utils import get_yml
import pipeline.git_pipeline as git
import pipeline.docker_pipeline as docker

import pipeline.api as pipe

@click.group()
def cli():
    pass

@cli.command()
def deploy():
    datos = get_yml()
        
    comandos = [
        git.git_add(),
        git.git_commit(), 
        git.git_push(),
        docker.docker_build(datos["params"]["docker_image"])
        # cloud_provider.login()
        # cloud_provider.push()
    ]

    
    print(comandos)

    for comando in comandos:
        try: 
            print(f"\nEjecutando: {' '.join(comando)}")
            proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            for linea in iter(proceso.stdout.readline, ""):
                print(linea, end="")  

            proceso.stdout.close()
            proceso.stderr.close()
            proceso.wait() 
        except Exception as e :
            print(f"Ha ocurrido un error: {e} - {e.__class__}")

@cli.command()
def create_repo():
    datos = get_yml()
    response, status_code,text = pipe.create_repo(
        key_id= datos["x-key-id"],
        api_key= datos["x-api-key"],
        provider_id= datos["provider"],
        service= datos["service"],
        space_id= ["space"]
    )
    print (response, status_code, text)
    

if __name__ == "__main__":
    cli()