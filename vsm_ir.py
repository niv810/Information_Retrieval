import sys
from creation import create
from question import query

if sys.argv[1] == 'create_index':
    create(sys.argv[2])
elif sys.argv[1] == "query":
    query(sys.argv[2], sys.argv[3])
