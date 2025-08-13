# services/notifications.py
import asyncio

async def send_notification(task_name: str):
    # Simulate sending an email or logging
    await asyncio.sleep(3)  # non-blocking wait
    print(f"[Background Task] Notification sent for task: {task_name}")
