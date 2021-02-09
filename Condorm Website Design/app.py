from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')
 
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/order')
def order():
    return render_template('order.html')
    
@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/information')
def information():
    return render_template('update.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')
    
if __name__ == "__main__":
    app.run(debug=True)