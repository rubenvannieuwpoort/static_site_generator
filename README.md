# static site generator

This is a very simple static site generator, written in Python in a single evening.

## Concepts

The basic ideas are:
- Input files have a JSON front matter with some metadata.
- In the metadata, a *renderer* and a *template* are defined.
- The renderer defines how the contents of the file should be transformed to HTML.
- The template is a simple Jinja template.

The objects that are passed to the Jinja template are of the form
```
{
    "metadata": {
        ...<whatever is in the JSON front matter>...
    },
    "content": {
        ...<the content of the file>...
    },
}
```

### Renderers

Renderers are simple Python files that are loaded dynamically. They should define a `render` method, that takes the contents of a file, and outputs HTML.


## Example

By default, `templates/` is used as the folder to find templates, and `renderers/` is used as the folder to find renderers. If no output file or folder is specified, `output` is used.

`input/example.html`:
```
{
    "title": "My first post",
    "date": "2025-06-24",
    "description": "An example of how a blog post for this static site generator can look like.",
    "template": "post.html",
    "renderer": "markdown.py"
}

# Welcome

This is an example of a simple post, writting in **MarkDown**. MarkDown has many advantages:
- Easy to write
- Well-supported by many tools
- Gets you internet credits
```

`templates/post.html`:
```
<html>
    <head>
        <title>{{metadata.title}}</title>
    </head>
    <body>
{{content}}
    </body>
</html>
```

`renderers/markdown.py`:
```
import markdown

def render(input: str) -> str:
    return markdown.markdown(input)
```

With these files in place (and the Python `markdown` module installed), we can generate the HTML with
```
python main.py input
```

which should generate a file `output/example.html` looking like this:
```
<html>
    <head>
        <title>My first post</title>
    </head>
    <body>
<h1>Welcome</h1>
<p>This is an example of a simple post, writting in **MarkDown**. MarkDown has many advantages:</p>
ol>
<li>Easy to write</li>
<li>Well-supported by many tools</li>
<li>Gets you internet credits</li>
</ol>
    </body>
</html>
```