"""

"""

from __future__ import absolute_import, unicode_literals



import asyncio

async def hello(a, b):
    print(a)
    await asyncio.sleep(1)  # 模拟耗时操作
    print(b)

async def main():
    await asyncio.gather(hello(1, 2), hello(3,4), hello(5,6))

asyncio.run(main())