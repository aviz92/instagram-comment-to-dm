---
description: Python async patterns — asyncio, async/await, concurrency, task management, blocking calls, and common pitfalls.
globs:
  - "**/*.py"
alwaysApply: false
---

# Scope Control
- Apply rules **only** to async code you add or modify.
- Do NOT convert existing sync code to async unless explicitly asked.

# Basic Rules
- Never mix sync and async code in the same execution context without isolation.
- Never call a coroutine without `await` — it silently does nothing:
```python
  # bad — coroutine created but never executed
  process_order(order_id)

  # good
  await process_order(order_id)
```
- Never use `time.sleep()` in async code — use `asyncio.sleep()`.
- Never run blocking I/O in an async function — offload to a thread executor.

# Blocking Calls
- Wrap all blocking calls with `asyncio.to_thread()`:
```python
  # good — blocking I/O offloaded to thread pool
  result = await asyncio.to_thread(blocking_db_call, user_id)

  # bad — blocks the entire event loop
  result = blocking_db_call(user_id)
```
- Treat any sync library call as potentially blocking — file I/O, `requests`, `psycopg2`, etc.
- Use async-native libraries where available: `httpx` over `requests`, `asyncpg` over `psycopg2`.

# Concurrency
- Use `asyncio.gather()` to run independent coroutines concurrently:
```python
  # good — runs concurrently
  user, orders = await asyncio.gather(
      get_user(user_id),
      get_orders(user_id),
  )

  # bad — runs sequentially
  user = await get_user(user_id)
  orders = await get_orders(user_id)
```
- Use `asyncio.gather(*tasks, return_exceptions=True)` when partial failure is acceptable.
- Use `asyncio.TaskGroup` (Python 3.11+) for structured concurrency:
```python
  async with asyncio.TaskGroup() as tg:
      task_a = tg.create_task(fetch_data())
      task_b = tg.create_task(process_queue())
```

# Task Management
- Always store task references — tasks not referenced can be garbage collected mid-execution:
```python
  # bad — task may be garbage collected
  asyncio.create_task(background_job())

  # good — keep reference
  task = asyncio.create_task(background_job())
  background_tasks.add(task)
  task.add_done_callback(background_tasks.discard)
```
- Always handle task cancellation gracefully — catch `asyncio.CancelledError` and clean up:
```python
  try:
      await long_running_task()
  except asyncio.CancelledError:
      await cleanup()
      raise  # always re-raise CancelledError
```
- Set timeouts on all async operations — never await indefinitely:
```python
  async with asyncio.timeout(30):
      result = await external_api_call()
```

# Async Context Managers & Generators
- Use `async with` for async context managers — never manually call `__aenter__`/`__aexit__`.
- Use `async for` for async generators — never manually call `__anext__`.
- Prefer `asynccontextmanager` for simple async context managers:
```python
  from contextlib import asynccontextmanager

  @asynccontextmanager
  async def managed_connection():
      conn = await create_connection()
      try:
          yield conn
      finally:
          await conn.close()
```

# Common Pitfalls
- Never create a new event loop manually — use `asyncio.run()` at the entry point only.
- Never use `loop.run_until_complete()` inside an already-running loop.
- Avoid sharing mutable state between concurrent tasks — use `asyncio.Lock` when necessary.
- Do NOT use `async def` for functions that have no `await` — it adds overhead with no benefit.
