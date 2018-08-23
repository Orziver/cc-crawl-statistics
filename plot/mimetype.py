import re
import sys

from plot.table import TabularStats
from crawlstats import CST, MonthlyCrawl


class MimeTypeStats(TabularStats):

    MIN_AVERAGE_COUNT = 500
    MAX_MIME_TYPES = 100

    # see https://en.wikipedia.org/wiki/Media_type#Naming
    mime_pattern_str = \
        '(?:x-)?[a-z]+/[a-z0-9]+' \
        '(?:[.-](?:c\+\+[a-z]*|[a-z0-9]+))*(?:\+[a-z0-9]+)?'
    mime_pattern = re.compile('^'+mime_pattern_str+'$')
    mime_extract_pattern = re.compile('^\s*(?:content\s*=\s*)?["\']?\s*(' +
                                      mime_pattern_str +
                                      ')(?:\s*[;,].*)?\s*["\']?\s*$')

    def __init__(self):
        super().__init__()
        self.MAX_TYPE_VALUES = MimeTypeStats.MAX_MIME_TYPES

    def norm_value(self, mimetype):
        if type(mimetype) is str:
            mimetype = mimetype.lower()
            m = MimeTypeStats.mime_extract_pattern.match(mimetype)
            if m:
                return m.group(1)
            return mimetype.strip('"\', \t')
        return ""

    def add(self, key, val):
        self.add_check_type(key, val, CST.mimetype)


if __name__ == '__main__':
    plot_crawls = sys.argv[1:]
    plot_name = 'mimetypes'
    column_header = 'mimetype'
    if len(plot_crawls) == 0:
        plot_crawls = MonthlyCrawl.get_last(3)
        print(plot_crawls)
    else:
        plot_name += '-' + '-'.join(plot_crawls)
    plot = MimeTypeStats()
    plot.read_data(sys.stdin)
    plot.transform_data(MimeTypeStats.MAX_MIME_TYPES,
                        MimeTypeStats.MIN_AVERAGE_COUNT,
                        MimeTypeStats.mime_pattern)
    plot.save_data(plot_name)
    plot.plot(plot_crawls, plot_name, column_header)
