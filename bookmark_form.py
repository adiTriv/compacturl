
bookmark_form_1 = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Make your URL short</title>
    <style>
        form {
            background-color: #eee;
            padding: 10px 20px
        }
        div {
            padding: 10px 20px;
            margin-bottom: 10px;
        }
        input {
            padding: 5px 10px;
            border-radius: 2px;
        }
        button {
            margin-left: 10px;
        }
    </style>
</head>
<body style="background-color: #eee; padding: 20px">
    <form action="https://compacturl.herokuapp.com/" method="post">
        <div><input type="text" name="url_body" placeholder="Place your URL here"></div>
        <div><input type="text" name="short-name" placeholder="Short name that you want"></div>
        <button type="submit">Submit!</button>
    </form>
</body>
</html>'''