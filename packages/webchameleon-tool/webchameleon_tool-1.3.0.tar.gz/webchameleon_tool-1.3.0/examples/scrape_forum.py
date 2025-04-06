import asyncio
from webchameleon import WebChameleon


async def main():
    auth_config = {
        "headers": {"Authorization": "Bearer your_api_key"},
    }
    chameleon = WebChameleon(
        target="https://scrapepark.org",
        disguise_as="mobile_app",
        auto_learn=True,
        max_concurrent=5,
        auth_config=auth_config,
        custom_settings={"max_depth": 5},
    )

    structure = await chameleon.analyze_structure()
    print("Structure:", structure)

    data = await chameleon.scrape(
        target_elements={"title": ".text", "content": ".quote", "author": ".author"},
        depth=3,
        adaptive_depth=True,
    )
    await chameleon.save(data, "forum_data.json", format="json", compress=True)

    api_data = await chameleon.reverse_api(
        use_playwright=True, max_depth=4, interactive_mode=True
    )
    if api_data:
        await chameleon.save(api_data, "api_data.json", format="json")
        print("API Data:", api_data)
    else:
        print("No API detected.")

    relations = await chameleon.map_relations(
        data, "forum_relations.graphml", weight_threshold=0.6
    )
    print("Status:", chameleon.status())


if __name__ == "__main__":
    asyncio.run(main())
