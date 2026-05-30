from agents import build_search_agent, build_scrape_agent, writer_chain, critic_chain

def research_pipeline(topic: str) -> dict:
    state = {}

    # Step 1 - Search agent
    print("\n" + "=" * 50)
    print("Step 1 - Search agent is working...")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Conduct a web search to gather recent and reliable information on the topic: {topic}.")]
    })
    state['search_results'] = search_result["messages"][-1].content
    print("\nSearch Results:", state['search_results'])

    # Step 2 - Scrape agent
    print("\n" + "=" * 50)
    print("Step 2 - Scrape agent is working...")
    print("=" * 50)

    scrape_agent = build_scrape_agent()
    scrape_results = scrape_agent.invoke({
        "messages": [("user",
            f"Based on the search results, scrape the most relevant URLs for detailed info on: {topic}.\n\n"
            f"Search Results:\n{state['search_results'][:800]}")]
    })
    state['scrape_results'] = scrape_results["messages"][-1].content
    print("\nScraped Content:", state['scrape_results'])

    # Step 3 - Writer chain
    print("\n" + "=" * 50)
    print("Step 3 - Writer is drafting the report...")
    print("=" * 50)

    research_combined = (
        f"Search Results:\n{state['search_results']}\n\n"
        f"Detailed Scraped Content:\n{state['scrape_results']}"
    )
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    print("\nFinal Report:", state['report'])

    # Step 4 - Critic chain
    print("\n" + "=" * 50)
    print("Step 4 - Critic is reviewing the report...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state['report']
    })
    print("\nCritique:", state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    research_pipeline(topic)