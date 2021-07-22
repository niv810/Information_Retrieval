import sys
from creation import create
from question import query
# from pip._internal.operations import freeze

if sys.argv[1] == 'create_index':
    create(sys.argv[2])
elif sys.argv[1] == "query":
    query(sys.argv[2], sys.argv[3])

# file = open("requirements.txt", "w")
# file.write('\n'.join(freeze.freeze()))
# file.close()
# print('\n'.join(freeze.freeze()))
