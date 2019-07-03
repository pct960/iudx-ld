from pyld import jsonld
import json
import requests
import sys



def ctxtResolver(contextInput, contextOutput):
    if(isinstance(contextInput, (list,))):
        for ct in contextInput:
            if(isinstance(ct, (str,))):
                c = requests.get(ct).json()["@context"]
                ctxtResolver(c, contextOutput)
            elif(isinstance(ct, (dict,))):
                contextOutput.update(ct)
    elif(isinstance(contextInput, (dict,))):
        contextOutput.update(contextInput)


def main():
    itemFile = sys.argv[1]
    with open(itemFile, "r") as f:
        item = json.load(f)
    numItems = len(item.keys())-2 # -2 for context and id
    context = {}
    ctxtResolver(item["@context"], context)
    doc = {k:v for k,v in item.items() if k not in "@context"}
    item = {}
    item["@context"] = context
    item.update(doc)


    expanded = jsonld.expand(item)
    print("Expanded")
    print(json.dumps(expanded, indent=2))
    print("\n\n")
    compacted = jsonld.compact(expanded,context)
    print("Compacted")
    print(json.dumps(compacted, indent=2))
    print("\n\n")
    flattened = jsonld.flatten(compacted, context)
    print("Flattened")
    print(json.dumps(flattened, indent=2))
    print("\n\n")
    normalized = jsonld.normalize(
        item, {'algorithm': 'URDNA2015', 'format': 'application/n-quads'})
    print("Normalized")
    print(json.dumps(normalized, indent=2))
    print("\n\n")


    print("Input length\t" + str(numItems))
    print("Expanded length\t" + str(len(expanded[0])-1))
    inpPropNames = list(item.keys())
    expPropNames = [k.split("/")[-1] for k in expanded[0].keys()]
    print(type(inpPropNames))
    print(type(expPropNames))
    missing = list( set(inpPropNames) - set(expPropNames) )
    print(missing)




if __name__ == "__main__":
    main()
