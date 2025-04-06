import ../src/rapidinstall

my_tasks = [
	{'name': 'Pip', 'commands': 'pip install pip'},
	{'name': 'Download MyFile', 'commands': "wget -c https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/VAEs/orangemix.vae.pt"}
]

rapidinstall.install(my_tasks, update_interval=5)