from flask import Flask, url_for, redirect, render_template, request
from post_data import posts
last_id = posts[-1]['id']
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about_me')
def about_me():
    return "This is the about me page"

@app.route('/create', methods=['POST','GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        subtitle = request.form['subtitle']
        content = request.form['content']
        global last_id

        last_id += 1
        new_post = {
            "id" : last_id,
            "title" : title,
            "subtitle" : subtitle,
            "content" : content
        }
        posts.append(new_post)

        with open('post_data.py', 'w') as f:
            f.write(f"posts = {posts}\n")
        f.close()
        return redirect("/")

    return render_template("create.html")

@app.route('/post/read/<int:id>')
def read(id):
    title = ''
    subtitle = ''
    content = ''
    for p in posts:
        if(p['id'] == id):
            title = p['title']
            subtitle = p['subtitle']
            content = p['content']
    return f'제목 : {title}<br/>부제목 : {subtitle}<br/>내용 : {content}<br>'    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)