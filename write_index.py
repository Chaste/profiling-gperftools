import pathlib

from datetime import datetime
from html import escape


def get_list_of_log_file_directories() -> list[str]:
    """Return a sorted list of valid log file directory names.

    Returns:
        A list of strings of all valid log file directories (i.e. those that themsevles contain an index.html file).
    """

    base_dir = pathlib.Path('log-files')
    dirs_list = [path.name for path in base_dir.iterdir() if path.is_dir() and (path / 'index.html').is_file()]

    return sorted(dirs_list, reverse=True)


def write_index_file(list_of_logs: list[str]) -> None:
    """Write an index.html file containing hyperlinks to the log file directories contained in this directory.

    Args:
        list_of_logs: A list of strings of log file directories to put in the index file.

    Returns:
        None.
    """

    title = 'Index of gperftools profiling output'

    # Directory names are "<timestamp>-<run id>"; only the leading 19 characters
    # (YYYY-MM-DD_HH-MM-SS) are the timestamp.
    dates = [datetime.strptime(x[:19], '%Y-%m-%d_%H-%M-%S') for x in list_of_logs]

    unique_dates = {datetime(year=date.year, month=date.month, day=1) for date in dates}
    unique_dates = sorted(list(unique_dates), reverse=True)

    sections = []
    for unique_date in unique_dates:
        items = []
        for path, date in zip(list_of_logs, dates):
            if date.year == unique_date.year and date.month == unique_date.month:
                escaped_path = escape(path)
                items.append(f'      <li>\n        <a href="{escaped_path}/index.html">{escaped_path}</a>\n      </li>')

        sections.append(f'    <h2>{escape(unique_date.strftime("%B %Y"))}</h2>\n    <ul>\n' + '\n'.join(items) + '\n    </ul>')

    html = f'''<!DOCTYPE html>
<html>
  <head>
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <div id="title">
      <h1>{escape(title)}</h1>
    </div>
    <div id="list-by-month" class="body">
''' + '\n'.join(sections) + '''
    </div>
  </body>
</html>
'''

    with open('log-files/index.html', 'w') as html_file:
        html_file.write(html)


if __name__ == "__main__":

    list_of_logs = get_list_of_log_file_directories()
    write_index_file(list_of_logs)
