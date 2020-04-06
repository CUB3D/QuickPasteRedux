import os
import aiofiles


class NoteStorage:
    async def get(self, file_name, default=""):
        pass

    async def set(self, file_name, data):
        pass


class LocalNoteStorage(NoteStorage):
    async def get(self, file_name, default=""):
        file_path = os.path.join("files", file_name)

        if os.path.exists(file_path):
            async with aiofiles.open(file_path) as f:
                content = await f.read()
            return content
        else:
            return default

    async def set(self, file_name, data):
        async with aiofiles.open(os.path.join("files", file_name), "w") as f:
            await f.write(data)
