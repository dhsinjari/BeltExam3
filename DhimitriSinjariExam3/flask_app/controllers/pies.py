from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.pie import Pie
from flask import flash


@app.route('/create/pie', methods = ['POST'])
def create_pie():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Pie.validate_pie(request.form):
        return redirect(request.referrer)
    Pie.create_pie(request.form)
    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'pie_id': id,
        'user_id': session['user_id']
    }
    currentPie = Pie.get_pie_by_id(data)
    if not session['user_id'] == currentPie['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')
    Pie.delete(data)
    return redirect(request.referrer)

@app.route('/edit/<int:id>')
def editPie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
            'pie_id': id,
            'user_id': session['user_id']
        }
    currentPie = Pie.get_pie_by_id(data)

    if not session['user_id'] == currentPie['user_id']:
        flash('You do not have the facilities for that big man.', 'noAccessError')
        return redirect('/dashboard')   
    return render_template('editPie.html', loggedUser= User.get_user_by_id(data), pie = Pie.get_pie_by_id(data))

@app.route('/update/<int:id>', methods = ['POST'])
def updatePie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Pie.validate_pie(request.form):
        return redirect(request.referrer)

    data = {
        'pie_id':id
    }

    data1 = {
        "name" : request.form["name"],
        "filling" : request.form["filling"],
        "crust" : request.form["crust"],
        'user_id': session['user_id'],
        'pie_id':id
    }
    
    currentPie = Pie.get_pie_by_id(data)

    if not session['user_id'] == currentPie['user_id']:
        flash('You do not have the facilities for that big man.', 'noAccessError')
        return redirect('/dashboard')
    
    Pie.update_pie(data1)

    return redirect('/')

@app.route('/show/<int:id>')
def viewPie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'pie_id': id,
        'user_id': session['user_id']
    }
    votes = Pie.getPiesVotes(data)
    return render_template('viewPie.html', loggedUser= User.get_user_by_id(data), pie = Pie.get_pie_by_id(data),votes=votes)



@app.route('/vote/<int:id>')
def Vote(id):
    data = {
        'pie_id': id,
        'user_id': session['user_id']
    }
    Pie.addVote(data)
    return redirect(request.referrer)

@app.route('/unvote/<int:id>')
def Unvote(id):
    data = {
        'pie_id': id,
        'user_id': session['user_id']
    }
    Pie.removeVote(data)
    return redirect(request.referrer)

@app.route('/derby')
def derby():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    allPies = Pie.getAllPies()
    userVotedPies = User.get_logged_user_voted_pies(data)
    return render_template('pypieDerby.html',loggedUser= User.get_user_by_id(data), pies= Pie.getAllPies(),userVotedPies=userVotedPies)