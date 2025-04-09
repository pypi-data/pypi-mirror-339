#!/usr/bin/env python
from mcp.server.fastmcp import FastMCP
from gpt_researcher import GPTResearcher
import asyncio

mcp = FastMCP("GeneOnline AI小編")


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"

async def write_report(query: str, report_type: str):
    researcher = GPTResearcher(query, report_type)
    research_result = await researcher.conduct_research()
    report = await researcher.write_report()
    
    # Get additional information
    research_context = researcher.get_research_context()
    research_costs = researcher.get_costs()
    research_images = researcher.get_research_images()
    research_sources = researcher.get_research_sources()
    
    return report, research_context, research_costs, research_images, research_sources

@mcp.tool()
async def get_report(query: str, report_type: str = "research_report") -> str:
    """AI will write a report for the topic you specified"""
    report, context, costs, images, sources = await write_report(query, report_type)
    return f"Report: {report}\nContext: {context}\nCosts: {costs}\nImages: {images}\nSources: {sources}"


@mcp.prompt()
def echo_prompt(message: str) -> str:
    """Create an echo prompt"""
    return f"Please write an news article for this topic: {message}"

if __name__ == "__main__":
    mcp.run()