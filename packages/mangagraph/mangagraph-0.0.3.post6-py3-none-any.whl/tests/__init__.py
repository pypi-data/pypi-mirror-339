from mangagraph import Mangagraph, MangagraphError
import asyncio

# === tests ===
# python -m tests.__init__
async def test():
    try:
        parser = Mangagraph()
        toc_url, mirror_toc_url = await parser.process_chapter(
            'https://mangalib.me/ru/manga/7965--chainsaw-man',
            chapter_num=90
        )
        print(f"Table of Contents: {toc_url}")
        print(f"Mirror: {mirror_toc_url}")
    except MangagraphError as e:
        print(f"Parser error: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(test())
    except (KeyboardInterrupt, SystemExit):
        print('Sayonara!')