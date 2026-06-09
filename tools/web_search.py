from ddgs import DDGS

# Creating a function which will search the web basically for web surfing

def web_search(query: str) -> str:

    try:
    
        # Searching and taking the top 3 results 

        with DDGS() as dgs:
            results = list(dgs.text(query,max_results = 3))

        if not results:
             
            return "I could not find any results for that sir."

        # Now combining all the three top results for a better optimized answer

        combined = ""
        for i,result in enumerate(results):
            title = result.get("title", "")
            body = result.get("body", "")
            combined += f"{title}, {body}"  

        return combined.strip()

    except Exception as e:
        print(f"Exception error: {e}")
        

# Testing block

if __name__ == "__main__":
    result = web_search("What happened in the bengal elections 2026? ")
    print(result)
    