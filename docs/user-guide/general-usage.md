# General Usage {: .doctitle}
Using PyMdown.

---

# Using PyMdown
PyMdown was written to aid in batch processing Markdown files with Python Markdown and Pygments (but a JavaScript highlighter can just as easily be used).  It also adds a number of optional extensions.

PyMdown can also optionally use a template with CSS and JavaScript for styling the Markdown outputs.  Templates, CSS, JavaScript, and extensions are all setup in a configuration file.  If for certain batches specific settings need to be tweaked, PyMdown can accept paths to specific settings file via the CLI.  The settings files can be in either JSON or YAML.  PyMdown also supports input sources with a JSON or YAML frontmatter were settings can be configured along with general meta data.

Though PyMdown could be used to generate a site, it was mainly designed to generate static documents from Markdown for general use or previewing.  If you are looking to generate document sites, there are plenty of good tools that already do this ([mkdocs](http://www.mkdocs.org/) is one suggestion).  But even if you don't directly use PyMdown, you may still find the [PyMdown extensions](pymdown-extensions.md) as useful additions in other Python Markdown related projects as they can be installed and used independently.

# Command Line Interface

## Input Files
In its most basic usage, PyMdown accepts a markdown file:

```
pymdown file.md
```

or a file stream:

```
pymdown < file.md
```

## Specifying Output
PyMdown allows the output to be specified with the `--output` or `-o` option:

```
pymdown -o file.html file.md
```

Alternatively you can redirect the output:

```
pymdown -o file.md > file.html
```

## Batch Processing
PyMdown has a batch processing mode (`--batch` or `-b`). When the batch flag is set, PyMdown will accept multiple paths and wild-card patterns.

```
pymdown -b *.md documents/*md
```

When in batch mode, PyMdown will simply transform the input file name: `file.md` -> `file.html`. It will then save the output file in the same location as the input.

## Previewing Markdown
With the `--preview` or `-p` option, PyMdown will generate a temp HTML file and open it in the default web browser.  Preview mode will work in normal and batch mode.

```
pymdown -p file.md
```

## Basepath
PyMdown in various circumstances (particularly in conjunction with specific PyMdown extensions) will try and resolve image, CSS, and JS asset paths for previews, base64 encoding, and other scenarios.  In order for this to work, a base path may be required and can be specified using the `--basepath` option.  If no base path is given, the base path will be that of the source file or `None` if the source is a file stream.

```
pymdown --basepath ../assets file.md
```

## Relpath
PyMdown in various circumstances (particularly in conjunction with specific PyMdown extensions) will try to create relative paths to assets or sources such as images, CSS, and JS.  In order for this to work, a relative path is needed.  The `--relpath` option is used to set this.  If `--relpath` is not set, it defaults to the output directory.  If the output directory is also not set (when output is dumped to stdout), the relative path will not be set.

```
pymdown --relpath ../somedirectory file.md
```

## Settings
PyMdown will normally look in the location of the [configuration directory](#configuration-file) to find the settings file, but the filename and path can be redirected with the `--settings` or `-s` option.

```
pymdown -s ../my_settings.cfg file.md
```

## Encoding
PyMdown can be configured to read the Markdown file(s) with a different encoding than the default `UTF-8`.  This is done with the `--encoding` or `-e` option.

```
pymdown -e utf-8 file.md
```

By default, the output encoding will be the same as the input, but if greater control is needed, the user can set the output encoding via the `--output_encoding` or `-E` option.

```
pymdown -E utf-8 file.md
```

## Title
PyMdown, by default, will use the source file's name as the title, or if the input is a file stream, it will use **Untitled**.  But this can be set/overridden with the `--title` option.  This probably isn't practical for batch processing.  When batch processing, it may make more sense to utilize the [frontmatter](#frontmatter) to set the title per file.

```
pymdown --title "My Awesome File" file.md
```

## Critic
PyMdown has a couple options from CriticMarkup.  By using the `--accept` or `-a` option, when the Markdown is parsed, the suggested changes will be accepted.

When using the `--reject` or `-r` option when Markdown is parsed, the suggested changes will be rejected and the original content will be used instead.

If both `--accept` and `--reject` are set at the same time, PyMdown will use the view mode and convert the file to HTML and will attempt to highlight the blocks targeted with the CriticMarkup.

Lastly, the `--critic-dump` option, when used with either the `--accept` or `--reject` option, will take the source and output it accepting or rejecting respectively the CriticMarkup edits that were made (essentially removing the CriticMarkup from the file).

## Plain HTML
If a stripped down HTML output is preferred, the `--plain-html` or `-P` option will return a stripped down output with no templates, no HTML comments, and no id, style, class, or on* attributes.

```
pymdown -P file.md
```

## Force No Template
If by default the configuration file has defined a template, but it is desired to do an output without the template, the `--force-no-template` option can be used to disable template use.

```
pymdown --force-no-template file.md
```

## Force Stdout
Sometimes a file may have frontmatter that redirects its output to a file, but it may be desirable to send the output to stdout.  In this case, the `--force-stdout` option can be used to force a redirect to stdout.

```
pymdown --force-stdout file.md
```

## Quiet
In some situations it may be desired to hide error messages and general info from the stdout.  In this case, the `--quiet` or `-q` option may be used.

```
pymdown -q file.md
```

# Configuration File
The configuration file is used to specify general Python Markdown settings, optional template, CSS and JS resources for templates, and extensions that will be used.

PyMdown on the first run will unpack user files to `~\.PyMdown` on Windows, `~/.PyMdown` on OSX and `~/.config/PyMdown` on Linux.  The global configuration file can found here at the root of the folder along with default CSS, JavaScript, and other resources which would be under another sub-folder called `default`.  Files under `default` will be auto-upgraded when necessary by newer versions of PyMdown and should be left unaltered.  Default files can be copied and altered outside of the `default` location for personal tweaking and usage.

## Python Markdown Settings
Python Markdown has a number of settings that can be configured:

```yaml
# Length of tabs in source files
tab_length: 4

# Ignore number of first item in ordered list.
# Setting this to false will force the list to start with the
# first specified number in the list.
lazy_ol: true

# Python Markdown by default enables smart logic for _connected_words_
# but only on italic with the underscore character.  I find this behavior odd
# and disable it by default for a more traditional markdown feel by default.
# Extensions can override this.
smart_emphasis: false

# Enable/disable attributes
enable_attributes: true

# Output format (html|html5|html5|xhtml|xhtml1|xhtml5)
# It is recommend to use more specific versions such as: html5 or xhtml1 than
# general html or xhtml
output_format: 'xhtml1'
```

Safe mode setting is omitted as it is pending deprecation in Python Markdown.

## Pygment Settings
The following setting s used when it is not desired to have PyMdown inject the Pygments CSS style into the template:

```yaml
# Include the pygments css when using codehilite extension
use_pygments_css: true,
```

If Pygments is disabled, but the CodeHilite extension is being used, code blocks are converted to a form so that a JavaScript library like [highlight.js](https://highlightjs.org/) can process them.

## Template
PyMdown allows for specifying a simple HTML template that can be used for the output.  Template files can be specified in the settings file via the `template` keyword.

```yaml
# Your HTML template
# PyMdown will look relative to the binary if it can't find the file.
template: default/template.html
```

In the template file, you can add special markup to insert certain items:

| Markup | Description |
|--------|-------------|
| \{\{&nbsp;meta&nbsp;}} |This is where meta data will be inserted.  Mainly the character encoding, and general user defined meta data from the frontmatter. |
| \{\{&nbsp;css&nbsp;}} | Where user defined stylesheets are inserted. |
| \{\{&nbsp;js&nbsp;}} | Where user defined JavaScript is inserted. |
| \{\{&nbsp;title&nbsp;}} | The page title will be inserted here. |
| \{\{&nbsp;content&nbsp;}} | The parsed markdown content gets inserted here. |
| \{\{&nbsp;getPath(myfile/path/img.png)&nbsp;}} | Get file paths, if local, under go conversions internally to make the paths relative or absolute as needed.  If in your template you need to point to a reference a file and want the file path to be converted to an absolute path or a relative path, you can use this to convert it in the template; the file can be preceded by a `!` to prevent path conversion to an absolute or relative path; this is mainly useful if you are just looking to escape the path. |
| \{\{&nbsp;getQuotedPath(myfile/path/img.png)&nbsp;}} | This is the same as `getPath` above except the output is surrounded in double quotes. |

Template files in the settings or frontmatter can be followed by `;encoding` to cause the file to be opened and read with the specified encoding.

## Javascript and CSS
Javascript and CSS can be included in the template by adding them to the following arrays:

```yaml
# Select your CSS for you output html
# or you can have it all contained in your HTML template
#
# Is an array of stylesheets (path or link).
# If it points to a physical file, it will be included.
# PyMdown will look relative to the binary if it can't find the file.
#
# This can be overridden in a file's frontmatter via the 'settings' key word:
#
# ---
# settings:
#     css:
#     -   somefile.css
# ---
#
# but if you want to append to the list, you can use the 'include.css' keyword in the
# frontmatter:
#
# ---
# include.css:
# - somefile.css
# ---
#
css:
-   ^default/markdown.css

# Load up js scripts (in head)
#
# Is an array of scripts (path or link).
# If it points to a physical file, it will be included.
# PyMdown will look relative to the binary if it can't find the file.
#
# This can be overridden in a file's frontmatter via the 'settings' key word:
#
# ---
# settings:
#     js:
#     -   somefile.js
# ---
#
# but if you want to append to the list, you can use the 'include.js' keyword in the
# frontmatter:
#
# ---
# include.js:
# - somefile.js
# ---
#
js: []
```

CSS files and JavaScript files can be URLs or file paths.  When specifying a file path, a `!` can be used to precede the path so that PyMdown will just link the file and skip converting the file to an absolute or relative path.  If the file path is preceded by a `^`, the file content will be embedded in the HTML under a style or script tag depending on the source type.

CSS and JavaScript files can also be followed by `;encoding` to read in the file with the specified encoding.

## JavaScript and CSS Quickload Aliases
Sometimes you may have files you occasionally want to include on the fly.  PyMdown allows for defining aliases that can be referenced in a file's frontmatter to include multiple JavaScript and/or CSS files.  CSS and JavaScript included in the the quick-load aliases follow the same rules as the normal [CSS and JavaScript](#javascript-and-css) includes.

```yaml
# Quick load aliases
#
# This is a quick way to optionally load multiple CSS and JS files when converting a specific file.
# It done using the file's frontmatter:
#
# ---
# include:
# - mathjax
# - flow
# ---
#
# You can create any key you want, but it needs to begin with '@'.  Then just use the include keyword
# in your frontmatter, and provide a list of aliases you wish to load.  Each alias can have a 'css' and/or 'js' keyword.
"@flow":
    js:
        -   "https://cdnjs.cloudflare.com/ajax/libs/raphael/2.1.2/raphael-min.js"
        -   flowchart-min.js
        -   default/uml-converter.js
        -   default/flow-loader.js

"@sequence":
    js:
        -   "https://cdnjs.cloudflare.com/ajax/libs/raphael/2.1.2/raphael-min.js"
        -   "https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.7.0/underscore-min.js"
        -   "https://cdnjs.cloudflare.com/ajax/libs/js-sequence-diagrams/1.0.4/sequence-diagram-min.js"
        -   default/uml-converter.js
        -   default/sequence-loader.js

"@mathjax":
   js:
        -   default/mathjax-config.js
        -   'https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'
```

## Path Conversions
By default, PyMdown converts paths to be relative to the output location.  If desired, this can be changed to an absolute path:

```yaml
# By default resource paths are converted to relative file paths when possible;
# this disables conversion.
path_conversion_absolute: false
```

If path conversion is not wanted, and disabling the conversion inline with the `!` token is not acceptable, path conversion can be completely disabled with the following setting:

```yaml
# By default resource paths are converted to relative file paths when possible;
# this disables conversion.  Previews will still convert paths to render preview proper.
disable_path_conversion: false
```

!!! caution "Note"
    PyMdown utilizes the [pathconverter](../extensions/pathconverter.md) extension to convert links and references in the actual markdown content.  If `pathconverter` is manually configured instead of letting PyMdown handle it, these settings will have no effect.

    The other exception is with previews.  In order for links and references to work in previews, they must be paths that are relative to the preview's temp directory or they must be absolute paths.  For this reason, PyMdown will always enable path conversions for previews.  If you have manually set up the `pathconverter` extension, preview's will overwrite the `relative_path` argument to ensure it is set to `${OUTPUT}` which will allow the preview to display content properly by making asset paths relative to the previews location.  By default, the `relative_path` is set to `${REL_PATH}` which is the output path by default, but can be altered via the command line option `--relpath` or the `relpath` frontmatter option.

## Python Markdown Extensions
Extensions to be used are defined under the **extensions** keyword.  **extensions** is an ordered key/value pair. An extension has a name followed by `:` in yaml format.  If you want to include settings parameters, you can include those as the extension value.  All parameters should be done as key/value pairs as shown below.

```yaml
extensions:
    markdown.extensions.extra:
    markdown.extensions.toc:
        title: Table of Contents
        slugify: ${SLUGIFY}
    markdown.extensions.codehilite:
        guess_lang: false
    markdown.extensions.smarty:
    markdown.extensions.wikilinks:
    markdown.extensions.admonition:
    markdown.extensions.nl2br:
    pymdown.pymdown:
    pymdown.b64:
        base_path: ${BASE_PATH}
    pymdown.critic:
```

There are a couple of special variables you can use in extension settings:

| Name | Description |
|------|-------------|
| $\{BASE_PATH} | Insert the base path from command line or frontmatter. |
| $\{REL_PATH} | Insert the relative path from command line or frontmatter. |
| $\{OUTPUT} | Insert the output path (or destination) from command line or frontmatter. |
| $\{SLUGIFY} | Use PyMdown's internal slugify method which provides a more unique header id for headers that have Unicode characters.  Python Markdown's internal slugify just strips them out, while PyMdown will give a percent encoding of the Unicode characters. |

# Frontmatter
Frontmatter can be used at the very beginning of a Markdown file.  Frontmatter blocks begin with `---` and end with `---`.  Frontmatter must be the very beginning of the file and start on the very first line.

PyMdown front matter content can be either YAML or JSON (JSON is modified to allow JavaScript comments).  The frontmatter is a dictionary of key value pairs which are translated into meta data for all keys except for a few **special** keywords.  For meta data, the key will become the content of the `meta` tag's `name` attribute, and the value will become the data for the `content` attribute.  If an array is specified as the value, each member of the array will be converted to a string and all of them will be strung together and separated by commas.  In all other cases, the value will just be converted to a string.

PyMdown has a few keywords that can be defined to alter the output.

| Keyword | Description |
|---------|-------------|
| title | This item is used in the HTML's title tag. |
| destination | This keyword is the location and file name were the output should be placed. |
| references | This can specify a separate Markdown file containing footnotes, attributes, etc. This feature could be abused to just insert normal Markdown files into other Markdown files; PyMdown currently does nothing to prevent this, but this is not really advised. References can be followed by `;encoding` to specify the read encoding. By default, the encoding from the command line will be used, but this can override it. |
| basepath | This is used to specify the path that PyMdown should use to look for reference material like CSS or JS files and even `references` defined in the frontmatter. It is also used in plugins such as `pathconverter` and `b64`.  This can override the `basepath` fed in at the command line. |
| relpath | This is used to specify the path that images and paths are relative to. It is used in plugins such as `pathconverter`.  This can override the `relpath` fed in at the command line. |
| include | This keyword's value is an array of strings and accepts [quickload aliases](#javascript-and-css-quckload-aliases) (the `@` symbol is omitted from the name). So if a quickload alias named `@alias` is desired, `alias` would be defined under the `include` keyword. |
| include.css | This keyword's value is an array of strings denoting additional single CSS files to include.  They follow the same convention as CSS defined in the settings file: `;encoding` at tail will define the encoding used to access the file, paths starting with `!` will not have their path converted to absolute or relative paths, and `^` will directly embed the content in the HTML file. |
| include.js | This keyword's value is an array of strings denoting additional single JavaScript files to include.  They follow the same convention as JavaScript defined in the settings file: `;encoding` at tail will define the encoding used to access the file, paths starting with `!` will not have their path converted to absolute or relative paths, and `^` will directly embed the content in the HTML file. |
| settings | This is a dictionary and allows the overriding of any of the settings found in the original configuration file. |