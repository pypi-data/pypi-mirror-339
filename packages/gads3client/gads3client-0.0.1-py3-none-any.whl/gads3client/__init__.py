from contextlib import asynccontextmanager
from enum import Enum
from typing import Optional

import aioboto3
import aiofiles


class Mimetype(str, Enum):
    png = "image/png"
    jpeg = "image/jpeg"
    jpg = "image/jpeg"
    gif = "image/gif"
    bmp = "image/bmp"
    webp = "image/webp"
    svg = "image/svg+xml"
    tiff = "image/tiff"

    mp4 = "video/mp4"
    webm = "video/webm"
    avi = "video/x-msvideo"
    mov = "video/quicktime"
    mpeg = "video/mpeg"
    mkv = "video/x-matroska"

    mp3 = "audio/mpeg"
    wav = "audio/wav"
    ogg = "audio/ogg"
    flac = "audio/flac"
    aac = "audio/aac"

    txt = "text/plain"
    csv = "text/csv"
    html = "text/html"
    css = "text/css"
    js = "application/javascript"
    json = "application/json"
    xml = "application/xml"

    pdf = "application/pdf"
    doc = "application/msword"
    docx = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    xls = "application/vnd.ms-excel"
    xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ppt = "application/vnd.ms-powerpoint"
    pptx = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

    @property
    def format(self) -> str:
        mapping = {
            self.png: ".png",
            self.jpeg: ".jpeg",
            self.jpg: ".jpg",
            self.gif: ".gif",
            self.bmp: ".bmp",
            self.webp: ".webp",
            self.svg: ".svg",
            self.tiff: ".tiff",
            self.mp4: ".mp4",
            self.webm: ".webm",
            self.avi: ".avi",
            self.mov: ".mov",
            self.mpeg: ".mpeg",
            self.mkv: ".mkv",
            self.mp3: ".mp3",
            self.wav: ".wav",
            self.ogg: ".ogg",
            self.flac: ".flac",
            self.aac: ".aac",
            self.txt: ".txt",
            self.csv: ".csv",
            self.html: ".html",
            self.css: ".css",
            self.js: ".js",
            self.json: ".json",
            self.xml: ".xml",
            self.pdf: ".pdf",
            self.doc: ".doc",
            self.docx: ".docx",
            self.xls: ".xls",
            self.xlsx: ".xlsx",
            self.ppt: ".ppt",
            self.pptx: ".pptx",
        }
        return mapping[self]


class S3:
    bucket: str = None
    endpoint_url: str = None
    aws_access_key_id: str = None
    aws_secret_access_key: str = None

    def __init__(self, bucket: str, endpoint_url: str, aws_access_key_id: str, aws_secret_access_key: str) -> None:
        self.bucket = bucket
        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    @asynccontextmanager
    async def client(self):
        async with aioboto3.Session().client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ) as _client:
            yield _client

    def url(self, filename: str, mimetype: Mimetype, storage: str, host: Optional[str] = None) -> str:
        return f"{host if host else self.endpoint_url}/{self.bucket}/{self.path(filename, mimetype, storage)}"

    @classmethod
    def path(cls, filename: str, mimetype: Mimetype, storage: str) -> str:
        return f"{storage}/{cls.name(filename, mimetype)}"

    @classmethod
    def name(cls, filename: str, mimetype: Mimetype) -> str:
        return f"{filename}{mimetype.format}"

    async def upload(self, file: bytes, filename: str, mimetype: Mimetype, storage: str) -> None:
        async with aiofiles.tempfile.NamedTemporaryFile("wb", suffix=mimetype.format) as tmp:
            await tmp.write(file)
            async with self.client() as client:
                await client.upload_file(
                    Filename=tmp.name,
                    Bucket=self.bucket,
                    Key=self.path(filename=filename, mimetype=mimetype, storage=storage),
                )

    async def download(self, filename: str, mimetype: Mimetype, storage: str) -> bytes:
        async with aiofiles.tempfile.NamedTemporaryFile() as tmp:
            async with self.client() as client:
                await client.download_file(
                    Filename=tmp.name,
                    Bucket=self.bucket,
                    Key=self.path(filename=filename, mimetype=mimetype, storage=storage),
                )
                await tmp.seek(0)
                file = await tmp.read()
        return file

    async def delete(self, filename: str, mimetype: Mimetype, storage: str) -> None:
        async with self.client() as client:
            await client.delete_object(
                Bucket=self.bucket,
                Key=self.path(filename=filename, mimetype=mimetype, storage=storage),
            )


__all__ = ["S3", "Mimetype"]
