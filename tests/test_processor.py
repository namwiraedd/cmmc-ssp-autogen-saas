from app.processor import DocumentProcessor
from app.storage import S3Client
import pytest, asyncio

@pytest.mark.asyncio
async def test_map_simple_text(tmp_path):
    s3 = S3Client()
    proc = DocumentProcessor(s3_client=s3)
    text = "Users must have unique IDs and access constrained to authorized users."
    results = proc.mapper.map_text_to_controls(text)
    assert any(r['control']['id'].startswith("3.1") for r in results)
