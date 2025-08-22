from find_link import find_download_link
from ddgs import DDGS
from downloader import download


def ddg_first_result(query: str) -> str | None:
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=1):
            return r["href"]
    return None


def search_and_download(Name_list: list):
    for i, line in enumerate(Name_list):
        try:
            line = line.replace(",", " ")
            line = "دانلود اهنگ "+line
            line = line.replace("\n", "")
            line = f"{line} site:musics-mehr.com OR site:musicrooz.com OR site:beroosic.ir OR site:musicsweb.ir"
            try:
                first_result = ddg_first_result(line)
            except:
                raise Exception("fail to fetch")

            dl = find_download_link(first_result)
            file_name = download(dl, path="downloaded_test")
        except Exception as e:
            file_name = f"ERROR: {e}"

        print(i, file_name)

        clean_line = file_name.replace("\n", "")
        with open("download.log", "a+") as c:
            c.write(f"from {i} in {list_file} >> {clean_line}\n")


if __name__ == '__main__':
    list_file = "playlist.csv"
    with open(list_file, "r", encoding="UTF-8") as c:
        lines = c.readlines()
    lines = lines[1:]  # remove table header
    search_and_download(lines)
