import urllib.request, json
import shutil
import errno
import conf
import os
import re

class static_from_wp:

    wp_url = ""
    wp_port = ""

    def __init__(self):
        
        try:
            if os.environ['WP_PORT']:
                self.wp_port = os.environ['WP_PORT']
        except KeyError as e:
            self.wp_port = conf.wp_port

    
    def __get_posts(self, url):
        with urllib.request.urlopen(url) as url:
            posts = json.loads(url.read().decode("utf8"))

        return posts

    def __copy_files(self):
        wp_dir = "wp/wp_content/uploads"
        static_dir = "static/images"

        try:
            shutil.copytree(wp_dir, static_dir)
        except OSError as e:
            if e.errno == errno.ENOTDIR:
                shutil.copy(wp_dir, static_dir)
            elif e.errno == errno.EEXIST:
                shutil.rmtree(static_dir)
                shutil.copytree(wp_dir, static_dir)
            else:
                print('Directory not copied. Error: %s' % e)

    def __parse_post(self, post):

        content = post.get('content').get('rendered')
        content = content.replace(':' + self.wp_port, '')
        content = content.replace('wp-content/uploads/', 'images/')
        content = content.replace('wp-image', 'images/')
        content = re.sub("(wp-image-{\d1,2})", "", content)
        
        post_output = """
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">""" + post.get('title').get('rendered') + """</h5>
                    <div class="card-text">""" + content + """</div>
                </div>
            </div>
                    """
        return post_output

    def __generate_post_html(self):
        url_posts_api = conf.wp_url + ":" + conf.wp_port + "/wp-json/wp/v2/posts/"
        
        html_output = """
        <div>"""
    
        posts = self.__get_posts(url_posts_api)
        for post in posts:
            html_output += self.__parse_post(post)

            html_output += "</div>"
    
        return html_output

    def __get_header(self):
        return """
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
	    <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
	    <title>""" + conf.site_title + """</title>
        <link href="/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container-fluid">
            <div class="card">
                <h2 class="card-header">""" + conf.header_title + """
                </h2>
                <div class="card-body">""" + conf.header_text + """
                </div>
            </div>
            <br/>
        """

    def __get_footer(self):
        return """
        </div>
        </body>
        </html>"""

    def __generate_html(self):
        header = self.__get_header()   
        footer = self.__get_footer()  
        content = u''.join(self.__generate_post_html())
        output = u''.join(header + content + footer)
        
        return output

    def __write_file(self, content):
        filename = "static/index.html"
        fo = open(filename, "wb+")
        fo.write(content.encode("utf8"))
        fo.close()
    
    def run(self):
        self.__copy_files()
        html_output = self.__generate_html()
        self.__write_file(html_output)
        
        print(" *  *  *  *  *  *  *  *  *  *  *  *  *")
        print ("Static files correctly deployed! :-D")

