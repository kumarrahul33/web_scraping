_ESCAPE_DICT = {
    "<":r"%3C",
    ">":r"%3E",
    "#":r"%23",
    "%":r"%25",
    ":":r"%3A",
    "/":r"%2F",
    "+":r"%2B",
    "|":r"%7C",
    "\\":r"%5C",
    "~":r"%7E",
}
_GOOGLE_CACHE_RAW = "http://webcache.googleusercontent.com/search?q=cache%3A{0}"
def generateCacheUrl(url):
    global _ESCAPE_DICT, _GOOGLE_CACHE_RAW
    escaped_query = "" 
    replaceables = _ESCAPE_DICT.keys()
    for i in range(len(url)):
        escaped_query += _ESCAPE_DICT[url[i]] if (url[i] in replaceables) else url[i]

    return _GOOGLE_CACHE_RAW.format(escaped_query)

if __name__ == '__main__':
    website = "https://www.zoominfo.com/c/smile-co/348668444"
    print(f"Test: Generating google cache URL for {website}")
    print(generateCacheUrl(website))