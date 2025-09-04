from time import sleep
import asyncio

class SyncSpongeBob:
  def cook_bread(self):
    sleep(3)
  
  def cook_hamburguer(self):
    sleep(5)
  
  def make_milkshake(self):
    sleep(10)
  
  def mount_sandwich(self):
    sleep(3)
  
  def cook(self):
    self.cook_bread()
    self.cook_hamburguer()
    self.make_milkshake()
    self.mount_sandwich()

class AsyncSpongeBob:
  async def cook_bread(self):
    await asyncio.sleep(3)
  
  async def cook_hamburguer(self):
    await asyncio.sleep(5)
  
  async def make_milkshake(self):
    await asyncio.sleep(10)
  
  async def mount_sandwich(self):
    await asyncio.sleep(3)
  
  async def cook(self):
    await asyncio.gather(
      self.cook_bread(),
      self.cook_hamburguer(),
      self.make_milkshake()
    )
    await self.mount_sandwich()

# sync_bob = SyncSpongeBob()
# sync_bob.cook()

async_bob = AsyncSpongeBob()
asyncio.run(async_bob.cook())