# this will run the api/service.py file with the instantiated app FastAPI
# NOTE: This runs the DEV versions with Hotreload: --reload --reload-dir api/ "$@"
# uvicorn_server() {
#     uvicorn api.service:app --host 0.0.0.0 --port 9000 --log-level debug --reload --reload-dir api/ "$@"
# }
# 
# 
# export -f uvicorn_server
# 
# echo -en "\033[92m
# The following commands are available:
#     uvicorn_server
#         Run the Uvicorn Server
# \033[0m
# "
# 

uvicorn api.service:app --host 0.0.0.0 --port 9000 --log-level debug --reload --reload-dir api/ "$@"
