import json
from typing import Annotated

import yfinance as yf
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from yfinance.const import SECTOR_INDUSTY_MAPPING

from yfmcp.types import Sector

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = FastMCP("Yahoo Finance MCP Server", log_level="ERROR")


@mcp.tool()
def get_ticker_info(symbol: Annotated[str, Field(description="The stock symbol")]) -> str:
    """Retrieve information about a specific stock symbol using Yahoo Finance API."""
    ticker = yf.Ticker(symbol)
    return json.dumps(ticker.info, ensure_ascii=False)


@mcp.tool()
def get_ticker_news(symbol: Annotated[str, Field(description="The stock symbol")]) -> str:
    """Fetches news articles for a given stock ticker symbol."""
    ticker = yf.Ticker(symbol)
    news = ticker.get_news()
    return str(news)


@mcp.tool()
def search_quote(
    query: Annotated[str, Field(description="The search query")],
    max_results: Annotated[int, Field(description="The maximum number of results")] = 8,
) -> str:
    """Search for quotes using a query string."""
    search = yf.Search(query, max_results=max_results)
    return str(search.quotes)


@mcp.tool()
def search_news(
    query: Annotated[str, Field(description="The search query")],
    news_count: Annotated[int, Field(description="The number of news articles")] = 8,
) -> str:
    """Search for news articles using a query string."""
    search = yf.Search(query, news_count=news_count)
    assert len(search.news) == news_count, f"Expected {news_count} news articles, but got {len(search.news)}"
    return str(search.news)


@mcp.tool()
def get_top_etfs(sector: Annotated[Sector, Field(description="The sector to get")]) -> str:
    """Retrieve the top ETFs in a specific sector."""
    s = yf.Sector(sector)
    return "\n".join(f"{symbol}: {name}" for symbol, name in s.top_etfs.items())


@mcp.tool()
def get_top_mutual_funds(sector: Annotated[Sector, Field(description="The sector to get")]) -> str:
    """Retrieve the top mutual funds in a specific sector."""
    s = yf.Sector(sector)
    return "\n".join(f"{symbol}: {name}" for symbol, name in s.top_mutual_funds.items())


@mcp.tool()
def get_top_companies(
    sector: Annotated[Sector, Field(description="The sector to get")],
    top_n: Annotated[int, Field(description="Number of top companies to retrieve")],
) -> str:
    """Retrieve the top companies in a specific sector."""
    s = yf.Sector(sector)
    df = s.top_companies
    if df is None:
        return f"No top companies available for {sector} sector."

    return df.iloc[:top_n].to_json(orient="records")


@mcp.tool()
def get_top_growth_companies(
    sector: Annotated[Sector, Field(description="The sector to get")],
    top_n: Annotated[int, Field(description="Number of top growth companies to retrieve")],
) -> str:
    """Retrieve the top growth companies in a specific sector."""
    results = []

    for industry_name in SECTOR_INDUSTY_MAPPING[sector]:
        industry = yf.Industry(industry_name)

        df = industry.top_growth_companies
        if df is None:
            continue

        results.append(
            {
                "industry": industry_name,
                "top_growth_companies": df.iloc[:top_n].to_json(orient="records"),
            }
        )
    return json.dumps(results, ensure_ascii=False)


@mcp.tool()
def get_top_performing_companies(
    sector: Annotated[Sector, Field(description="The sector to get")],
    top_n: Annotated[int, Field(description="Number of top performing companies to retrieve")],
) -> str:
    """Retrieve the top performing companies in a specific sector."""
    results = []

    for industry_name in SECTOR_INDUSTY_MAPPING[sector]:
        industry = yf.Industry(industry_name)

        df = industry.top_performing_companies
        if df is None:
            continue

        results.append(
            {
                "industry": industry_name,
                "top_performing_companies": df.iloc[:top_n].to_json(orient="records"),
            }
        )
    return json.dumps(results, ensure_ascii=False)


def main():
    mcp.run()
