import asyncio
from webchameleon import WebChameleon


async def main():
    chameleon = WebChameleon(
        target="https://instagram.com",  # Situs baru
        disguise_as="python_requests",  # Mode disguise sederhana untuk API
        auth_config={"headers": {"Authorization": "Bearer dummy_token"}},
    )

    api_data = await chameleon.reverse_api(
        use_playwright=True, max_depth=4, interactive_mode=True
    )
    if api_data:
        await chameleon.save(
            api_data, "reqres_api_data.json", format="json", compress=True
        )
        print("API Data:", api_data)
    else:
        print("No API detected.")


if __name__ == "__main__":
    asyncio.run(main())
