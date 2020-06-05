from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import sqlite3

global db_i
app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            db_i = sqlite3.connect("review_db.db")
            searchString = request.form['content'].replace(" ","")
            reviews=[]
            cursorObj = db_i.cursor()
            fetch_list=cursorObj.execute('SELECT name from sqlite_master WHERE type = "table"')
            list_db = [res[0] for res in fetch_list]
            if searchString in list_db:
                res_query = "select * from " + searchString
                records =db_i.execute(res_query)
                db_i.commit()
                list_records = []
                for rec in records:
                    list_records.append(rec)
                for rec in list_records:
                    mydict = {"Product": searchString, "Name": rec[0], "Rating": rec[1], "CommentHead": rec[2],
                              "Comment": rec[3]}
                    reviews.append(mydict)
                return render_template('results.html',reviews=reviews[0:len(reviews)-1])

            c_query = "create table " + searchString + "(name text,rating text,comment_head text,comment text)"
            db_i.execute(c_query)
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "bhgxx2 col-12-12"})
            del bigboxes[0:2]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})
            for commentbox in commentboxes:
                try:
                    #name.encode(encoding='utf-8')
                    n = commentbox.div.div.find_all('p', {'class': '_3LYOAd _3sxSiS'})[0].text

                except:
                    n = 'No Name'

                try:
                    #rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text


                except:
                    rating = 'No Rating'

                try:
                    #commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    #custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": searchString, "Name": n, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
                print(reviews)
                i_query = "insert into " + searchString + "(name,rating,comment_head,comment) values(?,?,?,?)"
                db_i.execute(i_query, (mydict['Name'],mydict['Rating'],mydict['CommentHead'],mydict['Comment']))
                db_i.commit()
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')
if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)