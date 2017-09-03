#!/usr/local/bin/python3

import docker
import argparse

def criar_container(args):
    client = conect_docker()
    executando = client.containers.run(args.imagem, args.comando)
    print(executando)
    return(executando)

def listar_containers(args):
    client = conect_docker()
    get_all = todos_container()
    for cada_container in get_all:
        conectando = client.containers.get(cada_container.id)
        print ("O container da vez é o %s e ele utiliza a imagem %s e o comando %s" %(conectando.short_id, conectando.attrs['Config']['Image'], conectando.attrs['Config']['Cmd']))

def procurar_container(args):
    client = conect_docker()
    get_all = todos_container()
    for cada_container in get_all:
        conectando = client.containers.get(cada_container.id)
        imagem_container = conectando.attrs['Config']['Image'].lower()
        if str(args.imagem) in str(imagem_container):
	#if set('alpine').intersection(conectando.attrs['Config']['Image'].lower()):
            print("Achei o container %s que contem a palavra %s no nome de sua imagem" %(conectando.short_id, conectando.attrs['Config']['Image']))

def remover_container(args):
    #remover containers bindando abaixo de 1024
    client = conect_docker()
    get_all = todos_container()
    for cada_container in get_all:
        conectando = client.containers.get(cada_container.id)
        portas = conectando.attrs['HostConfig']['PortBindings']
        if isinstance(portas,dict):
            for porta, porta1 in portas.items():
                porta1 = str(porta1)
                porta2 = ''.join(filter(str.isdigit, porta1))
                if int(porta2) <= 1024:
                    print("Removendo o container %s que esta escutando na porta %s e bindando no host %s" %(str(cada_container.short_id) , str(porta1), str(porta2)))
                    removendo = cada_container.remove(force=True)
                    return(removendo)

def conect_docker():
   client = docker.from_env()
   return(client)

def todos_container():
    client = conect_docker()
    get_all = client.containers.list(all)
    return(get_all)

parser = argparse.ArgumentParser(description="Docker-cli criado na aula de python")
subparser = parser.add_subparsers()

#criar
criar_opt = subparser.add_parser('criar')
criar_opt.add_argument('--imagem', required=True)
criar_opt.add_argument('--comando', required=True)
criar_opt.set_defaults(func=criar_container)

#listar
listar_opt = subparser.add_parser('ls')
listar_opt.set_defaults(func=listar_containers)

#Procurar
procurar_opt = subparser.add_parser('procurar')
procurar_opt.add_argument('--imagem', required=True)
procurar_opt.set_defaults(func=procurar_container)

#remover_container
remover_opt = subparser.add_parser('rm')
remover_opt.set_defaults(func=remover_container)

cmd = parser.parse_args()
cmd.func(cmd)

