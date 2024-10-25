
def gen_html(title="title", headers=[], data=[]):
    table = ""
    table += "<table class='table'>"
    table += "<thead><tr>"
    for h in headers:
        table += "<th>" + h + "</th>"
    table += "</tr></thead>"
    table += "<tbody>"
    for row in data:
        table += "<tr>"
        for item in row:
            item = "" if item is None else str(item)
            table += "<td>" + item + "</td>"
        table += "</tr>"
    table += "</tbody>"
    table += "</table>"
    html = f"""
<!DOCTYPE HTML>
<html>
    <head>
        <title>{title}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    </head>
    <body>
        {table}
    </body>
</html>
"""
    return html

if __name__== "__main__":
    headers = ['type', 'noise', 'food']
    data = [
        ['dog', 'bark', 'kibble'],
        ['cat', 'meow', 'fish']
    ]
    print(gen_html(title='animals', headers=headers, data=data))