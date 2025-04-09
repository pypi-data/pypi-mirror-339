import asyncio

from sthg_fastapi_logs.log_wrapper import service_log


@service_log()
async def b(data):
    print(data)


async def main():
    await b(data=123)


if __name__ == '__main__':
    asyncio.run(main())
