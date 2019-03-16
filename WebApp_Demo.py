
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import json
import os
import datetime

# App config.
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '4df31f27d441f27567d441334432f2b6176a'


class ReusableForm(Form):
    PotatoType = TextField('PotatoType:', validators=[validators.required()])
    Quantity = TextField('Quantity:', validators=[validators.required()])
    Price = TextField('Price:', validators=[validators.required()])
    CompanyName = TextField('CompanyName:', validators=[validators.required()])
    Source = TextField('Source:', validators=[validators.required()])
    AgentName = TextField('AgentName:', validators=[validators.required()])
    ContactInfo = TextField('ContactInfo:', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def capturePotatoPrice():
    form = ReusableForm(request.form)

    sources = ['Bloomberg','Email', 'Telephone', 'In-Person']
    print (form.errors)
    if request.method == 'POST':

        ## reading the data
        ptype = request.form['PotatoType']
        qty = request.form['Quantity']
        price = request.form['Price']
        cName = request.form['CompanyName']
        source = request.form.get('Sources')
        agentName = request.form['AgentName']
        agentContactInfo = request.form['ContactInfo']

        ## creating an empty json file if it does not exist.
        fileName = 'pricingData.json'
        if (not os.path.isfile(fileName)):
            open(fileName,'w').close()

        # capturing the input data from the webapp and appending it to the json file.
        with open(fileName, 'a+') as dataFile:
            json.dump({
                    'Time' : str(datetime.datetime.now()),
                   'PotatoType' :ptype,
                   'Quantity' : qty,
                   'Price' : price,
                   'CompanyName':cName,
                   'InfoSource':source,
                   'AgentName': agentName,
                   'ContactInfo': agentContactInfo}, dataFile )
            dataFile.write('\n')

    return render_template('appTemplate.html', form=form, sources= sources)


if __name__ == "__main__":
    app.run()

