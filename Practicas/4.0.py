backend={"Python", "SQL", "Docker", "Linux"}
frontend={"HTML", "CSS", "JavaScript", "React"}
backend.add("Git")

comunes=backend&frontend
todas=backend|frontend
solo_backend=backend-frontend

accesos = ["Carlos", "Ana", "Carlos", "David", "Ana", "Elena"]
set_accesos=set(accesos)
len(set_accesos)

print(f"frontend: {frontend}")
print(f"backend: {backend}")
print(f"comunes: {comunes}")
print(f"todas: {todas}")
print(f"solo_backend: {solo_backend}")
print(f"accesos únicos: {set_accesos}")
print(f"número de accesos únicos: {len(set_accesos)}")