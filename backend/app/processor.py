# backend/app/processor.py
import asyncio, os, tempfile, json
from typing import AsyncGenerator
from app.storage import S3Client
from app.mapping import CMMCMapper
from app.ssp_generator import SSPGenerator
from app.deps import get_db_session
from uuid import uuid4

class DocumentProcessor:
    def __init__(self, s3_client: S3Client):
        self.s3 = s3_client
        self.mapper = CMMCMapper()
        self.ssp_gen = SSPGenerator(s3_client=self.s3)
        self._status_queues = {}

    async def enqueue_parse(self, s3_key: str, user, task_id: str = None):
        tid = task_id or str(uuid4())
        # start background task
        asyncio.create_task(self._run_parse(tid, s3_key, user))
        return tid

    async def _run_parse(self, task_id, s3_key, user):
        q = asyncio.Queue()
        self._status_queues[task_id] = q
        await q.put({"status":"started"})
        # download
        tmp = tempfile.NamedTemporaryFile(delete=False)
        self.s3.download_to_file(s3_key, tmp.name)
        await q.put({"status":"downloaded"})
        # parse textual content (pdf/docx)
        text = await self._extract_text(tmp.name)
        await q.put({"status":"extracted_text","words":len(text.split())})
        # embed & semantic map
        mapping = self.mapper.map_text_to_controls(text)
        await q.put({"status":"mapped","controls_matched":len(mapping)})
        # generate SSP docx/pdf
        ssp_path = await self.ssp_gen.generate_ssp(task_id, mapping, user)
        await q.put({"status":"ssp_generated","ssp_path":ssp_path})
        await q.put({"status":"complete"})
        # persist outputs to S3 (done inside ssp_gen)
        await q.put({"status":"archived"})
        # cleanup
        self._status_queues.pop(task_id, None)

    async def stream_status(self, task_id: str, user) -> AsyncGenerator[dict, None]:
        q = self._status_queues.get(task_id)
        if not q:
            # no live queue — yield a final state if exists in storage
            yield {"status":"not_found"}
            return
        while True:
            item = await q.get()
            yield item
            if item.get("status") == "complete":
                break

    async def _extract_text(self, path: str) -> str:
        # simple heuristic: docx vs pdf
        import pypdf, docx
        if path.lower().endswith(".pdf"):
            reader = pypdf.PdfReader(path)
            text = "\n".join(p.extract_text() or "" for p in reader.pages)
            return text
        else:
            doc = docx.Document(path)
            return "\n".join(p.text for p in doc.paragraphs)
