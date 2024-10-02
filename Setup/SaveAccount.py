from qiskit_ibm_runtime import QiskitRuntimeService

token = ''
try:
    with open('token.tmp', encoding='utf-8') as f:
        token = f.read()
except FileNotFoundError:
    token = input('Cannot find token.tmp file, please paste here your IBM token: ')

QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token=token,
    set_as_default=True,
    overwrite=True,
)