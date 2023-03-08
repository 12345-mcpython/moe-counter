from flask import Flask, request, jsonify, Response
import base64

count = {}

app = Flask(__name__)

@app.route("/get/@<string:name>")
def get(name):
    svgs = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="315" height="100" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <title>Moe Count</title>
    <g> 
     {}
    </g>
</svg>
    """
    svg = "<image x=\"{}\" y=\"0\" width=\"45\" height=\"100\" xlink:href=\"{}\" />"
    theme = request.args.get("theme", "asoul")
    try:
        len_number = int(request.args.get("len", 7))
    except ValueError:
        return jsonify({"code": -1, "msg": "Argument error!"})
    if count.get(name):
        local_count = count.get(name)
    else:
        local_count = 0
    local_count += 1
    count[name] = local_count
    view_count = ("{:0>" + str(len_number) + "d}").format(local_count)
    x = [i for i in range(0, len_number * 45 + 1, 45)]
    part = ""
    for i in range(len_number):
        data = "data:image/gif;base64,"
        with open("assets/themes/" + theme +  "/" + view_count[i] + ".gif", "rb") as f:
            data += base64.b64encode(f.read()).decode()
        part += svg.format(x[i], data)
    return Response(svgs.format(part), content_type='image/svg+xml')

app.run()