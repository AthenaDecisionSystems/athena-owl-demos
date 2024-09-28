import getopt, sys
import requests




def process_args(argv):
    """
    need a query
    """
    query="""Hi IBU, I am on the phone with one of my very important customer. Her name is Sonya Smith. She has a problem with her claim 2 for their water damage. She told me that the carpet is expensive. She is surprised of the current coverage. Sonya finds this very disappointing. What would be the next best action?"""
    try:
      opts, args = getopt.getopt(argv,"hq",["query"])
    except getopt.GetoptError:
        help_str = "queryTheAgent.py -q <the query as string>"
        print (help_str)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (help_str)
            sys.exit()
        elif opt in ("-q", "--query"):
            query = arg
    return query

IBU_BASE_URL="http://localhost:8002/api/v1"
AGENT_REF="ibu_agent"
if __name__ == "__main__":
    print("---> Welcome to query the agent tool")
    theQuery = process_args(sys.argv[1:])
    data='{ "locale": "en",\
                  "query": "' + theQuery + '", \
                  "chat_history": [],\
                  "agent_id": "' + AGENT_REF + '",  \
                  "user_id" : "remote_test", \
                  "thread_id" : "3" \
              }'
    print(data)
    rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}, timeout = 10).content.decode()
    print(f"\n@@@> {rep}")