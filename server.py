from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open("database.txt", mode="a") as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f"\n{email}, {subject}, {message}")


def write_to_csv(data):
    # use newline to create always a new line
    with open("database.csv", mode="a", newline="") as database2:
        # define the data
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        # create the csv writer, with the DB, the dilimiter is the ',' no quotes betweem the chars
        csv_writer = csv.writer(
            database2,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,  # and quote only if special chars
        )
        # we write a row with the data we want
        csv_writer.writerow([email, subject, message])


@app.route("/submit_form", methods=["POST", "GET"])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            # use the function
            write_to_csv(data)
            return redirect("/thankyou.html")
        except:
            return "did not safe to database"
    else:
        return "Something went wrong. Try again!"


if __name__ == "__main__":
    app.run(debug=True)
